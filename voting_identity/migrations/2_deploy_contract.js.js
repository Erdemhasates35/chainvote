// migrations/2_deploy_contract.js

const MyContract = artifacts.require("DecentralizedIdentity");

module.exports = function(deployer) {
  deployer.deploy(MyContract);
};
