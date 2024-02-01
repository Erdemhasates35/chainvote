import json
import os

import ipfshttpclient
from web3 import Web3

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.conf import settings

# web3.eth.default_account = web3.eth.account.from_key(PRIVATE_KEY)
# client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')
# contract_file = os.path.join(os.getcwd(), "../solidity/decentralised_identity/build/contracts/DecentralizedIdentity.json")
# with open(contract_file, 'r') as file:
#     data = json.load(file)

# contract_abi = data['abi']
# contract_address = '0xf9eec06980Ef79Df610f7Df49fc31342d4B0D383'
# contract = web3.eth.contract(address=contract_address, abi=contract_abi)
# credential_request_contract = object # placeholder

class CreateIdentity(APIView):
    """View to create an identity. Receives the address of the user creating the identity
    and the attributes of the identity in json
    """

    def post(self, request):
        # get the details of the identity
        data = request.data['data']

        # hash the details and save in ipfs
        ipfshash = settings.client.add_json(data)
        # call smart contract and save ipfs hash
        tx_hash = settings.identity_contract.functions.createIdentity(ipfshash).transact()
        tx_data = settings.web3.eth.wait_for_transaction_receipt(tx_hash)
        resp = {
            "txn":f"{tx_data}"
        }
        return Response(resp, status=status.HTTP_201_CREATED)

class getIdentity(APIView):
    """Get a list of the user data.
    Receives the eth address of the user and returns the list of the users data
    """

    def get(self, request, address):
        # call smart conrarct to get list of identiy of a user
        identity = settings.identity_contract.functions.getIdentity().call()

        actual_data = settings.client.cat(identity[0])
        resp = {
            "identity":actual_data
        }
        return Response(resp, status=status.HTTP_200_OK)


class RegisterForCredential(APIView):
    """A view for users to register for a credential to be issued by an entity,
      for example voters card to be issued by INEC. It receives the the user's address and the 
      ipfshash of the users data and returns the transaction details of the request
      """
    
    def post(self, request):
        # get the user making this request and the ipfshash
        # of the data they submit for credential issuance
        # owner = request.data.get('address')
        identity = request.data.get('ipfshash')

        request_tx_hash = settings.credential_contract.functions.createRequest(identity).transact()
        tx_receipt = settings.web3.eth.wait_for_transaction_receipt(request_tx_hash)

        if tx_receipt.status ==1:

            resp = {
                "message": "Request for credential created successfully",
                "request_txn":f"{tx_receipt}"
            }
            return Response(resp, status=status.HTTP_201_CREATED)
        else:
                return Response({"message": "Failed to create request for credential"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# class UserCredentialRequest(APIView):
#     """A view to get all the credentials requested by a user
#     """
#     def get(self, request):
#         # call smart conrarct to get list of identiy of a user
#         credential_requests = contract.functions.getUserCredentialRequests().call()

#         resp = {
#             "userData":credential_requests
#         }
#         return Response(resp, status=status.HTTP_200_OK)address
    
class AllCredentialRequest(APIView):
    """A view to get all the credentials requests by all users
    """
    def get(self, request):
        # call smart conrarct to get list of identiy of users
        # Get the total number of requests
        request_count = settings.credential_contract.functions.requestCount().call()

        # Get all requests and their status
        all_requests = []
        for i in range(1, request_count + 1):
            requester = settings.credential_contract.functions.requests(i).call()[0]
            identity = settings.credential_contract.functions.requests(i).call()[1]
            status_code = settings.credential_contract.functions.requests(i).call()[2]

            if status_code == 0:
                status_str = "Pending"
            elif status_code == 1:
                status_str = "Successful"
            else:
                status_str = "Declined"
            identity = settings.client.cat(identity)
            all_requests.append({"request_id": i, "requester": requester, "identity": identity, "status": status_str})

        return Response(all_requests, status=status.HTTP_200_OK)
    
class IssueCredential(APIView):
    """A view to issue a credential from the request."""
    
    def post(self, request):
        request_id = request.data.get('request_id')
        request_contract = settings.credential_contract.functions.requestCount().call()

        request_status = request_contract.functions.requests(request_id).call()[2]
        if request_status != 0:
            return Response({"message": "Request does not exist or is not pending"}, status=status.HTTP_400_BAD_REQUEST)

        # Update request status to successful
        tx_hash = request_contract.functions.updateRequestStatus(request_id, 1).transact()
        tx_receipt = settings.web3.eth.wait_for_transaction_receipt(tx_hash)

        if tx_receipt.status != 1:
            return Response({"message": "Failed to update request status"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"message": "Request approved and credential issued successfully"}, status=status.HTTP_200_OK)
