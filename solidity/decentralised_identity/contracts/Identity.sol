// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DecentralizedIdentity {
    struct Identity {
        // IPFS hash holding some user's data
        string Identityipfs;
    }
    
    mapping(address => Identity) public identities;
    // mapping(address => UserData[]) public userIdentities;

    event IdentityRegistered(address indexed user, string identity);
    event RequestCreated(address indexed user);

    // Creating and retrieving user data
    function createIdentity(string memory _Identityipfs) external {
        require(bytes(identities[msg.sender].Identityipfs).length == 0, "Identity already registered");
        require(bytes(_Identityipfs).length > 0, "Identity cannot be empty");

        identities[msg.sender] = Identity(_Identityipfs);
        emit IdentityRegistered(msg.sender, _Identityipfs);
    }

    function getIdentity() external view returns (string memory) {
        return identities[msg.sender].Identityipfs;
    }
}
