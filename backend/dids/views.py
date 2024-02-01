import json
import os

import ipfshttpclient
from web3 import Web3

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


web3 = Web3(Web3.HTTPProvider('http://localhost:7545'))
contract_file = os.path.join(os.getcwd(), "../solidity/decentralised_identity/build/contracts/DecentralizedIdentity.json")
with open(contract_file, 'r') as file:
    data = json.load(file)

contract_abi = data['abi']
contract_address = '0xf9eec06980Ef79Df610f7Df49fc31342d4B0D383'

class CreateIdentity(APIView):
    """View to create an identity"""

    def post(self, request):
        # get the details of the identity
        details = request.data

        # hash the details and save in ipfs
        client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')
        ipfshash = client.add_json(details)
        # call smart contract and save ipfs hash
        contract = web3.eth.contract(address=contract_address, abi=contract_abi)
        tx_hash = contract.functions.createIdentity(ipfshash).transact({'from': '0x9dF6993313a6b59663cf54b2D86A16fD7545A320'})
        tx_data = web3.eth.wait_for_transaction_receipt(tx_hash)
        resp = {
            "txn":f"{tx_data}"
        }
        return Response(resp, status=status.HTTP_201_CREATED)