// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract VerifiableCredentialIssuer {
    struct VerifiableCredential {
        address holder;
        string credential;
        bytes32 signature;
    }

    mapping(address => VerifiableCredential) public credentials;

    event CredentialIssued(address indexed holder, string credential, bytes32 signature);

    function issueCredential(address holder, string memory credential, bytes32 signature) external {
        require(credentials[holder].holder == address(0), "Credential already issued");

        VerifiableCredential memory newCredential = VerifiableCredential({
            holder: holder,
            credential: credential,
            signature: signature
        });

        credentials[holder] = newCredential;
        emit CredentialIssued(holder, credential, signature);
    }

    function getIssuedCredential(address holder) external view returns (string memory, bytes32) {
        return (credentials[holder].credential, credentials[holder].signature);
    }
}
