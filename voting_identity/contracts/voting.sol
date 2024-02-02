// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0 <0.9.0;

contract DecentralizedVoting {
    struct Candidate {
        uint id;
        string name;
        uint voteCount;
    }

    mapping (address => bool) public voters;
    mapping (uint => Candidate) public candidates;
    uint public candidateCount;


    function addCandidate (string memory _name) public {
        candidateCount ++;
        candidates[candidateCount] = Candidate(candidateCount, _name, 0);
    }

    constructor () public{
        addCandidate("Olusegun Obasanjo");
        addCandidate("Goodluck EBele Jonathan");
        addCandidate("MKO Abiola");
        addCandidate("Atiku Abubakar");
        addCandidate("Bola Ahmed Tinubu");
    }
    function Vote(uint _candidateID) public payable {
        require(!voters[msg.sender]);
        require(_candidateID!=0 && _candidateID<=candidateCount);
        voters[msg.sender]=true;
        candidates[_candidateID].voteCount ++;
    }
    function getVotesForCandidate(uint _candidateID) public view returns (uint) {
        require(_candidateID > 0 && _candidateID <= candidateCount);  // Validate candidate ID
        return candidates[_candidateID].voteCount;
    }

}