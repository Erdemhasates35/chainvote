import json
import os

import ipfshttpclient
from web3 import Web3

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


web3 = Web3(Web3.HTTPProvider('http://localhost:7545'))
client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')
contract_file = os.path.join(os.getcwd(), "../voting_identity/build/contracts/DecentralizedIdentity.json")
with open(contract_file, 'r') as file:
    data = json.load(file)

contract_abi = data['abi']
contract_address = '0xf9eec06980Ef79Df610f7Df49fc31342d4B0D383' 

class CreateIdentity(APIView):
    """View to create an identity"""

    def post(self, request):
        # get the details of the identity
        data = request.data['data']

        # hash the details and save in ipfs
        ipfshash = client.add_json(data)
        # call smart contract and save ipfs hash
        contract = web3.eth.contract(address=contract_address, abi=contract_abi)
        tx_hash = contract.functions.createIdentity(ipfshash).transact({'from': f'{owner}'})
        tx_data = web3.eth.wait_for_transaction_receipt(tx_hash)
        resp = {
            "txn":f"{tx_data}"
        }
        return Response(resp, status=status.HTTP_201_CREATED)

class UserDataList(APIView):
    """Get a list of the user data.
    Receives the eth address of the user and returns the list of the users data
    """

    def get(self, request, address):
        # call smart conrarct to get list of identiy of a user
        contract = web3.eth.contract(address=contract_address, abi=contract_abi)
        user_data = contract.functions.getAllIdentities(address).call()
        print(user_data)

        resp_data = []
        for data in user_data:
            actual_data = client.cat(data[0])
            resp_data.append({"ipfshash":data, "data": actual_data})

        resp = {
            "userData":resp_data
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
        owner = request.data.get('address')
        ipfshash = request.data.get('ipfshash')

        contract = web3.eth.contract(address=contract_address, abi=contract_abi)
        request_tx_hash = contract.functions.createCredentialRequest(ipfshash).transact({'from': f'{owner}'})
        tx_data = web3.eth.wait_for_transaction_receipt(request_tx_hash)