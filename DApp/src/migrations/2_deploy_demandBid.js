var DemandBid = artifacts.require("DemandBid");

module.exports = function(deployer) {
  deployer.deploy(DemandBid, 9999);
};
