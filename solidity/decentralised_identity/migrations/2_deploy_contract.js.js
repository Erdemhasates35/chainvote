// migrations/2_deploy_contract.js

const Identity = artifacts.require("DecentralizedIdentity");
const CredentialsIssuer = artifacts.require("VerifiableCredentialIssuer");
const CredentialRequest = artifacts.require("VerifiableCredentialRequest");


module.exports = function(deployer) {
  // deployer.deploy(Identity);
  // deployer.deploy(CredentialsIssuer);
  deployer.deploy(CredentialRequest, "0x33970254CC70BA399830f45fC9f0E3EA55C77572");

};
