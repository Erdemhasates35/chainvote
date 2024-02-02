import json
import os

from pyld import jsonld

import ipfshttpclient
from web3 import Web3
from web3.exceptions import ContractLogicError

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from datetime import datetime

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


import uuid
from chainvote.custom import settings


class SetAccountByPrivateKey(APIView):
    """Change the address of the account with your private key"""

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'private-key': openapi.Schema(type=openapi.TYPE_STRING, description='Private key of the account'),
            },
            required=['private-key'],
        ),
        responses={
            201: openapi.Response(description='Account set successfully', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING, description='Message indicating success'),
                    'address': openapi.Schema(type=openapi.TYPE_STRING, description='Public key (address) of the account'),
                }
            )),
            400: openapi.Response(description='Bad Request'),
            500: openapi.Response(description='Internal Server Error'),
        },
        operation_description="Set the account for the ChainVote application using the provided private key. All transactions henceforth will be made with this account.",
        tags=['Account'],
    )
    def post(self, request):
        """Set the account for the chainvote application. Receive the private key and returns the public key.
        All transactions henceforth will be made with this account
        """
        private_key = request.data['private-key']
        address = settings.set_account(private_key)
        resp = {"message":"OK",
                "address":f"{address}"}
        return Response(resp, status=status.HTTP_201_CREATED)
    
class CreateIdentity(APIView):
    """View to create an identity. Receives the address of the user creating the identity
    and the attributes of the identity in json
    """

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'data': openapi.Schema(type=openapi.TYPE_OBJECT, description='Attributes(data) of the identity in JSON format'),
            },
            required=['data'],
        ),
        responses={
            201: openapi.Response(description='Identity created successfully'),
            400: openapi.Response(description='Bad Request'),
            500: openapi.Response(description='Internal Server Error'),
        },
        operation_description="Create an identity and a verifiable credential for an individual.\
        Returns the ipfs hash of the verifiable credential and the transaction hash where the ipfs hash is stored.""",
        tags=['Identity'],
    )
    def post(self, request):
        # get the details of the identity
        data = request.data
        # eth_address = settings.web3.eth.default_account.address
        did = f"did:chainvote:{uuid.uuid4()}"

        context = {
            "@context": {
                # common properties to be determined later(or leave it empty)
            }
        }

        compact_data = jsonld.compact(data, context)

        vc = {
            "@context": ["https://www.w3.org/2018/credentials/v1"],
            "type": ["VerifiableCredential"],
            "issuer": settings.inec_did,
            "holder": f"{did}",
            "credentialSubject": compact_data
        }

        vc_json = json.dumps(vc, separators=(',', ':'), sort_keys=True)

        # generating RSA key pair
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()

        # sign the Credential
        signature = private_key.sign(
            vc_json.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        # Construct the Proof Field
        proof = {
            "type": "RsaSignature2018",
            "created": datetime.utcnow().isoformat(),
            "proofPurpose": "assertionMethod",
            "verificationMethod": "did:example:123#key-1",
            "signatureValue": signature.hex()
        }

        # Add the Proof Field to the Credential
        vc["proof"] = proof

        

        # hash the vc and save in ipfs
        ipfshash = settings.client.add_json(vc)
        # call smart contract and save ipfs hash
        try:
            tx_hash = settings.identity_contract.functions.createIdentity(ipfshash).transact({"from": settings.web3.eth.default_account.address})
            tx_data = settings.web3.eth.wait_for_transaction_receipt(tx_hash)
            resp = {
            "vc_ipfs_hash": ipfshash,
            "txn_hash":f"{tx_data['transactionHash']}"
        }
        except ContractLogicError as e:
            resp = {
            "message":f"Error in creating identity: {e}"
            }
        except Exception as e:
            resp = {
            "message":f"Internal Error: {e}"
            }
        
        return Response(resp, status=status.HTTP_201_CREATED)

class getIdentity(APIView):
    """Get a list of the user data.
    Receives the eth address of the user and returns the list of the users data
    """

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Success', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'ipfshash': openapi.Schema(type=openapi.TYPE_STRING, description='IPFS hash of the identity'),
                    'identity': openapi.Schema(type=openapi.TYPE_STRING, description='Identity data retrieved from IPFS'),
                }
            )),
            500: openapi.Response(description='Internal Server Error'),
        },
        operation_description="Retrieve a list of the user's data by calling a smart contract to get the identity and fetching data from IPFS.",
        tags=['Identity'],
    )
    def get(self, request):
        # call smart conrarct to get list of identiy of a user
        identity = settings.identity_contract.functions.getIdentity().call({"from": settings.web3.eth.default_account.address})
        actual_data = settings.client.cat(identity)
        resp = {
            "ipfshash":identity,
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

        request_tx_hash = settings.credential_contract.functions.createRequest(identity).transact({"from": settings.web3.eth.default_account.address})
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
