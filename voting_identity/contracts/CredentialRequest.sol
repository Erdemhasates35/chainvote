// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// Import the VerifiableCredentialIssuer contract for issuing credentials
import "./Credentials.sol";

contract VerifiableCredentialRequest {
    enum RequestStatus { Pending, Successful, Declined }

    struct CredentialRequest {
        address requester;
        string identity;
        RequestStatus status;
    }

    VerifiableCredentialIssuer public issuerContract;
    mapping(uint256 => CredentialRequest) public requests;
    uint256 public requestCount;

    event RequestCreated(uint256 requestId, address indexed requester, string identity, RequestStatus status);
    event RequestStatusUpdated(uint256 requestId, RequestStatus status);

    constructor(address _issuerContractAddress) {
        issuerContract = VerifiableCredentialIssuer(_issuerContractAddress);
    }

    function createRequest(string memory _identity) external {
        requestCount++;
        requests[requestCount] = CredentialRequest({
            requester: msg.sender,
            identity: _identity,
            status: RequestStatus.Pending
        });
        emit RequestCreated(requestCount, msg.sender, _identity, RequestStatus.Pending);
    }

    function updateRequestStatus(uint256 _requestId, RequestStatus _status) external {
        require(_requestId <= requestCount, "Invalid request ID");
        require(requests[_requestId].requester == msg.sender, "You are not the requester of this credential");

        requests[_requestId].status = _status;
        emit RequestStatusUpdated(_requestId, _status);

        if (_status == RequestStatus.Successful) {
            // Call the function in the VerifiableCredentialIssuer contract to issue a credential
            issuerContract.issueCredential(msg.sender, requests[_requestId].identity, generateSignature(msg.sender, requests[_requestId].identity));
        }
    }

    function generateSignature(address _holder, string memory _identity) private pure returns (bytes32) {
        // Generate a dummy signature for demonstration purposes
        return keccak256(abi.encodePacked(_holder, _identity));
    }
}
