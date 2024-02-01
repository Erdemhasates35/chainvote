// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DecentralizedIdentity {
    struct UserData {
        // IPFS hash holding some user's data
        string ipfshash;
        }
    
    struct CredentialRequests {
        string ipfshash;
    }


    mapping(address => UserData[]) public userIdentities;



    function createIdentity(string memory _ipfshash) public {
        userIdentities[msg.sender].push(UserData(_ipfshash));
    }

    function getAllIdentities(address _user) public view returns (UserData[] memory) {
        return userIdentities[_user];
    }

    function getIdentity(address _user, uint256 _index) public view returns (string memory) {
        require(_index < userIdentities[_user].length, "Identity index out of bounds");
        UserData memory identity = userIdentities[_user][_index];
        return (identity.ipfshash);
    }
}
