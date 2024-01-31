// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Identity {
    struct IdentityData {
        string name;
        string ipfshash;
    }

    mapping(address => IdentityData) public identities;

    function createIdentity(string memory _name, uint256 _age, string memory _dob, string memory _occupation, string memory _address) public {
        require(bytes(identities[msg.sender].name).length == 0, "Identity already exists");
        identities[msg.sender] = IdentityData(_name, _age, _dob, _occupation, _address);
    }

    function getIdentity(address _user) public view returns (string memory, uint256, string memory, string memory, string memory) {
        IdentityData memory data = identities[_user];
        return (data.name, data.age, data.dob, data.occupation, data.address);
    }
}
