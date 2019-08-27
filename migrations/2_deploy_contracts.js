var GuessingGame = artifacts.require("GuessingGame");

module.exports = function(deployer, network, accounts) {
  deployer.deploy(GuessingGame, {from: accounts[0]} );
};