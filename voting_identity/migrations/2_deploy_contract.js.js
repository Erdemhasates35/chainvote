// migrations/2_deploy_contract.js

const Identity = artifacts.require("DecentralizedIdentity");
const CredentialsIssuer = artifacts.require("VerifiableCredentialIssuer");
const CredentialRequest = artifacts.require("VerifiableCredentialRequest");
const VotingContract = artifacts.require("DecentralizedVoting")


module.exports = function(deployer) {
  // deployer.deploy(Identity);
  deployer.deploy(CredentialsIssuer);
  // deployer.deploy(CredentialRequest, "0x96263426fcd503465150B74f1e0D867cE332D6Fe");
  deployer.deploy(VotingContract)
};
