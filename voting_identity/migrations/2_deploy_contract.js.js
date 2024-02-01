// migrations/2_deploy_contract.js

const MyContract = artifacts.require("DecentralizedIdentity");
const VotingContract = artifacts.require("DecentralizedVoting")

module.exports = function(deployer) {
  deployer.deploy(MyContract);
  deployer.deploy(VotingContract)
};
