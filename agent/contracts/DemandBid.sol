pragma solidity ^0.5.11;

contract DemandBid {

    // address of the owner of this contract
    address owner;

    // length of round (24 hours, 00:00 - 23:59:59:99)
    uint public auctionLength;

    // uint256 is the date
    mapping (address => mapping (uint => Bet_Info)) agent_details;
    mapping (uint => Round) round_info;

    // initialises day = 0
    uint currentDay = 0;

    // seconds when initialise the contract
    uint secondInit;

    constructor(uint _auctionLength) public {
        secondInit = now;
        auctionLength = _auctionLength;

        // set owner of this contract ot be whi initialises this contract
        owner = msg.sender;
    }

    struct Round {
        uint date;
        uint number_of_players;
        uint total_pot;             // today's total pot rrelative
        uint total_pot_constant;    // today's total pot which will never get deducted
        uint settlement_value;
        uint higherInterval;
        uint lowerInterval;
        uint number_agent_inside_interval;
        uint sum_relativeness;
        bool settlement_is_set;
    }

    struct Bet_Info {
        uint betAmount;
        uint prediction;
        bytes32 hash_prediction;
        uint reward;
        bool claimed;
        bool bet_hashes_correct;
        bool insideInterval;
        uint relativeness;
        bool revealBet_hasSet;
    }

    // Log the event about a bet submission being made by an address and its prediction
    event BetSubmission(address indexed accountAddress, uint prediction, uint dayNumber);
    // Calculate the shares that agent won
    event AuctionEnded(uint day_number, uint amount);
    // Log when the hashes match and the prediction value
    event predictionMatchesHash(uint prediction_value);
    // Log when keccak256 is hashed
    event keccak256Hash(bytes32 hashes);
    // Log when prediction hash is hashed
    event HashPrediction(bytes32 hash_prediction);
    // Log when prediction is get from the hash
    event GetPrediction(uint prediction);
    // Log when prediction_in_bytes32
    event PredictionInBytes32(bytes32 prediction);
    // Log when address has nothing to withdraw (prediction not inside interval)
    event PredictionNotInsideInterval(string str);
    // Log for printing when debugging
    event PrintString(string _string);
    // Log for printing uint
    event PrintUint(uint _uint);

    event PrintBoolean(bool _bool);
    bytes32 hashNow = 0;
    function getHash() public view returns (bytes32) {
        return hashNow;
    }

    function getCurrentDay() public view returns (uint) {
        return currentDay;
    }

    // https://emn178.github.io/online-tools/keccak_256.html
    // Agent needs to go to this website to hash the bet first
    // Bet can only be submitted from 00.00-23.00 of day0
    function submitBet(bytes32 _blindedBid) public payable {

        require (msg.value > 0, "The bet amount needs to be greater than 0");

        // check if currentDay is today
        if (((now - secondInit) / auctionLength) != currentDay) {

              currentDay = (now - secondInit) / auctionLength;
              // calculate rewards for previous day
        }

        // take modulus to find the seconds left in today
        uint today_current_second = (now - secondInit) % auctionLength;
        require (today_current_second <= 23 * auctionLength / 24, "Only accept bet before 23.00.00");

        /*bytes memory stringAndPassword_bytes = abi.encodePacked(_blindedBid);

        bytes32 hash = keccak256(stringAndPassword_bytes);
        emit keccak256Hash(hash);*/

        agent_details[msg.sender][currentDay].betAmount = msg.value;

        //set hash_prediction = _blindedBid (arguments when this function is called)
        agent_details[msg.sender][currentDay].hash_prediction = _blindedBid;
        hashNow = agent_details[msg.sender][currentDay].hash_prediction;

        // PS needs to initialise the reward = 0 after getting commit reveal scheme to work
        agent_details[msg.sender][currentDay].reward = msg.value;

        agent_details[msg.sender][currentDay].claimed = false;

        // increment total_pot with the bet amount
        round_info[currentDay].total_pot += msg.value;
        // increment ttotal_pot_constant with the bet amount
        round_info[currentDay].total_pot_constant += msg.value;
        round_info[currentDay].number_of_players += 1;
        emit BetSubmission(msg.sender, msg.value, currentDay);
    }

    function getTodayHash() private returns (bytes32) {
        currentDay = (now - secondInit) / auctionLength;
        return agent_details[msg.sender][currentDay].hash_prediction;
    }

    function getYesterdayHash() private returns (bytes32) {
        currentDay = (now - secondInit) / auctionLength;
        return agent_details[msg.sender][currentDay--].hash_prediction;
    }

    function getNow() private view returns (uint) {
        uint x = now;
        // return how many seconds have past
        return x - secondInit;
    }

    function getTodayCurrentSeconds() public view returns (uint) {
        // take modulus to find the seconds left in today
        uint today_current_second = (now - secondInit) % auctionLength;
        return today_current_second;
    }

    // withdraw function can only be called after 3a.m. on day2
    // can only call withdraw after
    function withdraw() public {
        currentDay = (now - secondInit) / auctionLength;
        require(currentDay > 1, "No available withdraws yet");
        //require(, "Can only claimed rewards for today");

        // Check whether it has past 3am
        uint today_current_second = (now - secondInit) % auctionLength;
        require(today_current_second >= 3 * auctionLength / 24 && today_current_second <= auctionLength, "Can only called withdraw after 3a.m.");

        if (agent_details[msg.sender][currentDay-2].insideInterval) {

            if (!agent_details[msg.sender][currentDay-2].claimed) {

                // call getReward() to calculate what reward this address can claimed
                // can only be called after all agents called calculateReward()
                // only needs to call getReward() if it is inside interval
                getReward();

                //get reward of the reward that can be withdraw
                uint twoDaysAgoReward = agent_details[msg.sender][currentDay-2].reward;

                emit PrintString("Reward not cliamed yet");
                emit PrintUint(twoDaysAgoReward);

                // only needs to transfer the funds if reward > 0
                if (twoDaysAgoReward > 0) {

                // REMARK: Maybe need to diveide by 100000000 to send in ether
                // REMARK: Also maybe need to have if statement that the reward is not greater than the total pot

                // transfer rewards to the agent
                (msg.sender).transfer((twoDaysAgoReward));

                // deduct the withdraw amount from today's total_pot
                round_info[currentDay-2].total_pot -= twoDaysAgoReward;
                }
            }
        }  else {
            //
            emit PredictionNotInsideInterval("Your prediction are not close to the settlement value so you do not win any prize.");
        }

    }

    // call this function if there is leftover total_pot from yesterday's
    // can call this function first after settlement_value for today is called
    // owner should be the one to call it
    function updateTotalPotFor2DaysAgoRound() public {
        require (msg.sender == owner, "Only owener of the contract should cal this function!");
        currentDay = (now - secondInit) / auctionLength;
        require(currentDay > 2, "Can only update after day2");

        // only needs to update the pot if there is leftover
        if (round_info[currentDay-3].total_pot > 0) {


            // update total_pot with leftover
            round_info[currentDay-2].total_pot_constant += round_info[currentDay-3].total_pot;
            round_info[currentDay-2].total_pot += round_info[currentDay-3].total_pot;

            round_info[currentDay-3].total_pot = 0;
        }
    }

    function getTotalPot(uint day) public view returns (uint) {
      require (day >= 0);
      return round_info[day].total_pot;
    }

    function getTotalPotConstant(uint day) public view returns (uint) {
      require (day >= 0);
      return round_info[day].total_pot_constant;
    }

    // return the rewardAmount of the msg.sender on the day specify
    // only call this function after calculate reward is already called
    function getRewardAmount(uint day) public view returns (uint) {
        require (day >= 0, "Day < 0 does not exist");
        return agent_details[msg.sender][day].reward;
    }

    // return the day that the auction is in right now
    function getDayCount() public view returns (uint) {
      return (now - secondInit) / auctionLength;
    }

    // using 5% interval
    // find the higher interval
    function findHighestInterval() private returns (uint) {
        currentDay = (now - secondInit) / auctionLength;
        require (currentDay > 1, "Can only find highest interval on day2");
        uint highestInterval = round_info[currentDay-2].settlement_value + round_info[currentDay-2].settlement_value / 20;
        emit PrintUint(highestInterval);
        return highestInterval;

    }

    //
    function findLowestInterval() private returns (uint) {
        currentDay = (now - secondInit) / auctionLength;
        require (currentDay > 1, "Can only find lowest interval on day2");
        uint lowestInterval = round_info[currentDay-2].settlement_value - round_info[currentDay-2].settlement_value / 20;
        emit PrintUint(lowestInterval);
        return lowestInterval;
    }

  // get settlementValue from energy supplier and set the settlement Value
  // also calculate the highest and lowest interval
  // starting from day0, settlement_value is set on day2
  // owner of the contract can should call this at midnight of day1
  function setSettlementValue(uint value) public {

     require (msg.sender == owner, "Only owner of the contract can call this function");

     // settlementValue = get_settlement_from_energy_supplier();
    currentDay = (now - secondInit) / auctionLength;

    require(currentDay > 1, "Cannot set settlement value yet");

    // this function needs to be called by owner every midnight

    round_info[(currentDay-2)].settlement_value = value;
    round_info[(currentDay-2)].higherInterval = findHighestInterval();
    round_info[(currentDay-2)].lowerInterval = findLowestInterval();
    round_info[(currentDay-2)].settlement_is_set = true;
  }

    function returnABIEncodePacked(uint prediction, string memory password) private pure returns (bytes memory) {
      return abi.encodePacked(prediction, password);
    }

    function returnKeccak256(bytes memory hash) private pure returns (bytes32) {
      return keccak256(hash);
    }

    // Python can call this function to find the hash of the encode of prediction and password
    function returnKeccak256OfEncoded(uint prediction, string memory password) public pure returns (bytes32) {
        return keccak256(returnABIEncodePacked(prediction, password));
    }
    bool revealDone = false;

    function getRevealedBet() public view returns (bool) {
        return revealDone;
    }


    // Place a blinded bid with `_blindedBid` =
    // keccak256(abi.encodePacked(prediction, password)).
    function revealBet(uint prediction, string memory password) public returns (bool) {
      currentDay = (now - secondInit) / auctionLength;

      uint today_current_second = (now - secondInit) % auctionLength;
      //require (today_current_second >= 23 * auctionLength / 24 && today_current_second <= auctionLength, "Can only reveal bet from 11pm-12pm");

      bytes32 hash = keccak256(abi.encodePacked(prediction, password));
      //emit keccak256Hash(hash);
      hashNow = agent_details[msg.sender][currentDay].hash_prediction;


      if (hash == agent_details[msg.sender][currentDay].hash_prediction) {

            //set the real prediction value
            agent_details[msg.sender][currentDay].prediction = prediction;

            emit predictionMatchesHash(prediction);

            //set bet_hashes_correct = true;
            agent_details[msg.sender][currentDay].bet_hashes_correct = true;
            emit PrintBoolean(true);
            revealDone = true;
            return true;

        } else {
            agent_details[msg.sender][currentDay].bet_hashes_correct = false;
            emit PrintBoolean(false);
            revealDone = false;
            return false;
        }

  }

  // check whether the prediction is inside today's interval
  function checkIfInsideInterval() private returns (bool) {
      currentDay = (now - secondInit) / auctionLength;
      require (currentDay > 1);

      if (agent_details[msg.sender][currentDay-2].prediction <= round_info[currentDay-2].higherInterval &&
      agent_details[msg.sender][currentDay-2].prediction >= round_info[currentDay-2].lowerInterval) {
          agent_details[msg.sender][currentDay-2].insideInterval = true;
          round_info[currentDay-2].number_agent_inside_interval += 1;
          return true;
      }
      return false;

  }

  function getSenderPrediction() public view returns (uint) {
      return agent_details[msg.sender][currentDay-2].prediction;
  }

  // calculate the relativeness value and set the relativeness in the struct at the end
  // calculate by the inverse of the differences between the settlement_value and the guess
  // then multiply it with the betAmount
  function calculateRelativeBetAndCloseness() private {
      currentDay = (now - secondInit) / auctionLength;
      require (currentDay > 1);

      uint difference_from_settlement_value = differenceFromSettlementValue();

      //calculate relativeness using formula 1/diff * betAmount
      uint _relativeness = agent_details[msg.sender][currentDay-2].betAmount / difference_from_settlement_value;
      emit PrintString("calculateRelativeBetAndCloseness");
      //it prints uint: 5000000000000000000
      emit PrintString("Relativeness for this account: ");
      emit PrintUint(_relativeness);

      //maybe needs to have a parameter name relative

      // set relativeness value
      agent_details[msg.sender][currentDay-2].relativeness = _relativeness;

      // add relativeness to today's total relativeness
      round_info[currentDay-2].sum_relativeness += _relativeness;
      emit PrintString("Sum Relativeness for today: ");
      emit PrintUint(round_info[currentDay-2].sum_relativeness);

  }


    // find the difference between prediction and the actual settlement value
    // needs to check for 0 (exact number for guess and settlement_value)
    // if exactly then make equal to 1
    function differenceFromSettlementValue() private returns (uint) {

        currentDay = (now - secondInit) / auctionLength;

        require (currentDay > 1);

        uint difference_from_settlement_value;

        // check if they are equal, if yes then return 1
        if (round_info[currentDay-2].settlement_value - agent_details[msg.sender][currentDay-2].prediction == 0 ) {
            difference_from_settlement_value = 1;
        } else if (agent_details[msg.sender][currentDay-2].prediction - round_info[currentDay-2].settlement_value == 0) {
            difference_from_settlement_value = 1;
        } else if (round_info[currentDay-2].settlement_value > agent_details[msg.sender][currentDay-2].prediction) {
            difference_from_settlement_value = round_info[currentDay-2].settlement_value - agent_details[msg.sender][currentDay-2].prediction;
        } else {
            difference_from_settlement_value = agent_details[msg.sender][currentDay-2].prediction - round_info[currentDay-2].settlement_value;
        }

        emit PrintString("Inside differenceFromSettlementValue");
        emit PrintUint(difference_from_settlement_value);
        return difference_from_settlement_value;
    }

    // Can only calculate the reward on the day you withdraw
    // call in withdraw
    // only allow to withdraw after 3a.m. on day2
    function getReward() private {
      currentDay = (now - secondInit) / auctionLength;

        // calculate the reward using formula (relativeness / sum_relativeness) * total_pot
        uint _reward = agent_details[msg.sender][currentDay-2].relativeness  * round_info[currentDay-2].total_pot_constant / round_info[currentDay-2].sum_relativeness;
        emit PrintString("Reward for this account: ");
        emit PrintUint(_reward);
        // update reward to the address
        agent_details[msg.sender][currentDay-2].reward = _reward;
    }
    bool result = false;
    function getResult() public view returns (bool) {
        return result;
    }

    // calculate rewards should be called after settlement_value is set after midnight
    // this should be called asap
    // only allow to calculate reward  from midnight to 3a.m. on day2
    function calculateReward() public {
        currentDay = (now - secondInit) / auctionLength;

        // take modulus to find the seconds left in today
        uint today_current_second = (now - secondInit) % auctionLength;
        //require (today_current_second >= 0 && today_current_second <= 3 * auctionLength / 24, "Can only calculate rewards from midnight to 3a.m.");

        // checkIfInsideInterval
        if (checkIfInsideInterval()) {
            //calculate parameter for relativeness and sum_relativeness

            emit PrintString("reach inside interval");
            calculateRelativeBetAndCloseness();
            result = true;

        } else {
            emit PrintString("reach not inside interval");
            //if not inside the interval then agent do not get a reward
            agent_details[msg.sender][currentDay-2].reward = 0;
            result = false;

      }
  }

  // return settlement_value of day that make prediction
  function getSettlementValue(uint dayNumber) public view returns (uint) {
      return round_info[dayNumber].settlement_value;
  }



}
