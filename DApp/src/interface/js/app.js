
var settlementValues = [101643, 99419, 100924, 92123, 98228, 96530, 97947, 96135, 94158, 97995];
var totalPots = [25,25,25,25,25,25,25,25,25,25];
var predictions = [101929, 95802, 95327, 95296, 95295, 95295, 95295, 95295, 95295, 95295];
// var r = getPearsonCorrelation(settlementValues, totalPots);

App = {
  web3Provider: null,
  contracts: {},
  account: 0x10,

  init: async function() {
     return await App.initWeb3();
  },

  initWeb3: async function() {

     // Modern dapp browsers...
    if (window.ethereum) {
      App.web3Provider = window.ethereum;
      try {
        // Request account access
        await window.ethereum.enable();
      } catch (error) {
        // User denied account access...
        console.error("User denied account access")
      }
    }
    // Legacy dapp browsers...
    else if (window.web3) {
      App.web3Provider = window.web3.currentProvider;
    }
    // If no injected web3 instance is detected, fall back to Ganache
    else {
      App.web3Provider = new Web3.providers.HttpProvider('http://localhost:8545');
    }
    web3 = new Web3(App.web3Provider);

    return App.initContract();
  },

  initContract: function() {

     $.getJSON('DemandBid.json', function(data) {
      // Get the necessary contract artifact file and instantiate it with truffle-contract
      App.contracts.DemandBid = TruffleContract(data);

      // Set the provider for our contract
      App.contracts.DemandBid.setProvider(App.web3Provider);

      // Use our contract to retrieve information
      return App.render();
    });

    //return App.bindEvents();
  },

//   bindEvents: function() {
//     $(document).on('click', '.btn-adopt', App.handleAdopt);
//   },

   render: function() {
     var predictionInstance;
     var results = $("#pastdata");

     // Load account data
    web3.eth.getCoinbase(function(err, account) {
      if (err === null) {
        App.account = account;
        $("#accountAddress").html("Your Account: " + account);
      }
    });

      // Load contract data
      App.contracts.DemandBid.deployed().then(function(instance) {
        predictionInstance = instance;

        return predictionInstance.getCurrentDay();
      }).then(function(currentDay) {
          results.empty();
          var index = 0;

          for (var i = 0; i < currentDay; i++) {
            var settlement;
            var total_pot;

          predictionInstance.round_info(i).then(function(r) {
          //settlement = r[0];
          //total_pot = r[3];

          // Render the Result
           var template = "<tr><th>" + (index+1) + "</th><td>" + totalPots[index] + "</td><td>" + settlementValues[index] +   "</td><<td>" + predictions[index] +   "</td>/tr>";
           results.append(template);
           index++;
        });
      }
          // var prediction;
          // var betAmount;
          //
          // predictionInstance.agent_detail[App.account](1).then(function(betInfo) {
          // prediction = betInfo[1];
          // betAmount = betInfo[0];
          // var template1 = "<tr><th>" + index + "</th><td>" + prediction + "</td><td>" + betAmount +   "</td></tr>";
          // results.append(template1);

      }).catch(function(error) {
        console.warn(error);
      });
      }
};



$(function() {
  $(window).load(function() {
    App.init();
  });

  Highcharts.chart('myChart', {

    chart: {
      backgroundColor:"#1e2844",
      scrollablePlotArea: {
        minWidth: 300
      }
    },
    colors : ['#78DF97', '#F34D41', '#FFEBCD', '#FFEBCD', '#FFEBCD',
        '#FFEBCD', '#FFEBCD', '#FFEBCD', '#FFEBCD', '#FFEBCD'],

    title: {
      text: 'Daily Energy usage',
      style :{
        color :"#FFEBCD"
      }
    },
    subtitle: {
      text: 'Source: SoftEng27 Analytics',
      style :{
        color :"#FFEBCD"
      }
    },
    xAxis: {

      type:'datetime',
      dateTimeLabelFormats:{
        day:'%e of %b'
      },

      title:{
        text:'date',
        style :{
          color :"#FFEBCD"
        }
      },

      labels: {
        style :{
          color :"#FFEBCD"
        },
        step : 1
      }
    },

    yAxis: [{ // left y axis
      title: {
        text: 'energy usage',
        style :{
          color :"#FFEBCD"
        }
      },
      labels: {
        style :{
          color :"#FFEBCD"
        }
      }
    }],

    legend: {
      layout: 'vertical',
        align: 'right',
        verticalAlign: 'middle'
    },

    series: [{
      name: 'Settlement Values',
      data:  [101643, 99419, 100924, 92123, 98228, 96530, 97947, 96135, 94158, 97995],
      pointStart: Date.UTC(2020, 0, 1),
      pointInterval: 24 * 3600 * 1000 // one day
    }, {
      name: 'Your Predictions',
      data: [101929, 95802, 95327, 95296, 95295, 95295, 95295, 95295, 95295, 95295],
      pointStart: Date.UTC(2020, 0, 1),
      pointInterval: 24 * 3600 * 1000 // one day
    }],
    responsive: {
      rules: [{
          condition: {
              maxWidth: 600
          },
          chartOptions: {
              legend: {
                  layout: 'horizontal',
                  align: 'center',
                  verticalAlign: 'bottom',
              }
          }
      }]
  }
  });
});

// getPearsonCorrelation: function(x, y) {
//     var shortestArrayLength = 0;
//
//     if(x.length == y.length) {
//         shortestArrayLength = x.length;
//     } else if(x.length > y.length) {
//         shortestArrayLength = y.length;
//         console.error('x has more items in it, the last ' + (x.length - shortestArrayLength) + ' item(s) will be ignored');
//     } else {
//         shortestArrayLength = x.length;
//         console.error('y has more items in it, the last ' + (y.length - shortestArrayLength) + ' item(s) will be ignored');
//     }
//
//     var xy = [];
//     var x2 = [];
//     var y2 = [];
//
//     for(var i=0; i<shortestArrayLength; i++) {
//         xy.push(x[i] * y[i]);
//         x2.push(x[i] * x[i]);
//         y2.push(y[i] * y[i]);
//     }
//
//     var sum_x = 0;
//     var sum_y = 0;
//     var sum_xy = 0;
//     var sum_x2 = 0;
//     var sum_y2 = 0;
//
//     for(var i=0; i< shortestArrayLength; i++) {
//         sum_x += x[i];
//         sum_y += y[i];
//         sum_xy += xy[i];
//         sum_x2 += x2[i];
//         sum_y2 += y2[i];
//     }
//
//     var step1 = (shortestArrayLength * sum_xy) - (sum_x * sum_y);
//     var step2 = (shortestArrayLength * sum_x2) - (sum_x * sum_x);
//     var step3 = (shortestArrayLength * sum_y2) - (sum_y * sum_y);
//     var step4 = Math.sqrt(step2 * step3);
//     var answer = step1 / step4;
//
//     return answer;
