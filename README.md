# **Crowd-sourcing agent-based machine learning algorithms using prediction marketplaces implemented on a blockchain**

Over the coming decade there will be an explosion in the number and computational power of
Internet of Things (IoT) devices that are deployed across the world. The transient data that is
observed by IoT sensors is usually of too low a value to justify keeping it in a centralized server.
In most cases, this leads to the data being deleted shortly after collection and all of its potential
value being lost. The goal of this project is to develop an integrated system that monetizes data
that is collected from IoT devices. The IoT devices are deployed with an agent that has access
to streams of sensor data and a machine learning framework for training prediction algorithms.
The monetization of the algorithms occurs via a prediction marketplace that is implemented in a
smart contract and deployed on a blockchain.


## <a name="general-info"></a>General info
Our project offers institutional groups, who have access to large amounts of 
generally low-value individual data offered by Internet of Things (IoT) devices 
deployed across the globe, the opportunity to monetise this information. 
Specifically, we've create a marketplace for the oracle (which represents the 
wholesale energy supplier) where agent's representing different households 
attempt to make predictive bets on what they believe the next day's energy 
aggregate demand will be for their area. In return, agent's are rewarded for and
incentivised to make accurate predictions. These can then be used at the 
discretion by the as a prediction of the next day's energy demand which can then
be used to budget and account for, allowing companies to greatly improve their 
operational costs and efficiency.

## Build with
Project is created with:
* Python version: 3.7
* Solidity version: 0.5.11
* Javascript 
* HTML5

## Technologies
* [Brownie](https://github.com/iamdefinitelyahuman/brownie)
* [Ganache](https://www.trufflesuite.com/ganache)
* [Metamask](https://metamask.io)
* [npm](https://www.npmjs.com)
* [Truffle](https://www.trufflesuite.com)
* [Web3.js](https://web3js.readthedocs.io/en/v1.2.4/#)
* [Bootstrap](https://getbootstrap.com)

## Getting Started

### Prerequistes
Install Dependencies
```
$ npm install
```

### Training dataset
You can use your own training dataset and put it inside

```
src/model/dataset
```
or you can use the dataset we use

### Setting up EC2
1. Getting into the EC2 instance
```
$ ssh -i model-app.pem ec2-user@<ec2-public-dns>
```
2. Starting the Docker image
```
$ sudo service docker start
$ sudo usermod -a -G docker ec2-user
$ docker build -t model-app .
$ docker run -p 80:80 -v ~/softeng27/dataset:/deploy/dataset model-app .
```
3. Making request to train the model on the EC2 instance (run from your own machine)
```
$ curl -X POST <ec2-public-dns>:80/train -H 'Content-Type:application/json' -d {"dataset_size": "x", "individual_data": "y"}
```
4. Making request to predict the model on the EC2 instance (run from your own machine)
```
$ curl -X POST <ec2-public-dns>:80/predict -H 'Content-Type:application/json' -d {"prediction_size": "z"}
```

### Deploying Contracts with Brownie
```
$ brownie run <script> [function]
```

### Running the Decentralized App

#### Step 1. Clone the project

```
$ git clone https://gitlab.doc.ic.ac.uk/g1936227/softeng27.git
```

#### Step 2. Start Ganache
Open the Ganache GUI client that you downloaded and installed. This will start
your local blockchain instance. 

#### Step 3. Compile and Deploy Smart Contract
```
$ cd src/
$ truffle migrate --reset
```
You must migrate the smart contract each time you restart Ganache.

#### Step 4. Configure Metamask
- Unlock Metamask
- Connect Metamask to your local Ethereum blockchain provided by Ganache
- Import an account provided by Ganache

#### Step 5. Run the Front End Application
```
$ npm run dev
```

Visit this URL in your browser: http://localhost:3000

### Locations

#### Machine Learning Model
```
src/model/gp_model/
```
#### Smart Contract
```
src/contracts/DemandBid.sol
```
#### Test Case
```
tests/test_multiple_days.py
```

#### DApp
```
src/interface/js/app.js
```

## Authors
* Prem Chowdhry
* Salman Hussain
* Suphanat Sangwongwanich
* Theerathat Pornprinya
* Vitaliy Trofymuk
* Nanfeng Liu
* Under the supervision of Dominik Harz

## In collaboration Fetch.AI
* [Fetch](https://fetch.ai)
 

