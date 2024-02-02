from rest_framework.decorators import api_view
from rest_framework.response import Response
from web3 import Web3
import json
import os

w3 = Web3(Web3.HTTPProvider('http://localhost:7545'))

contract_file = os.path.join(os.getcwd(), "../voting_identity/build/contracts/DecentralizedVoting.json")
with open(contract_file, 'r') as file:
    data = json.load(file)

voting_abi = data['abi']
contract_address = '0xfd1a9d2759fE9E4b641194408Eb1C8fa4624B8Cd'

# Create a contract instance
contract = w3.eth.contract(address=contract_address, abi=voting_abi)

@api_view(['GET'])
def get_candidate_count(request):
    candidate_count = contract.functions.candidateCount().call()
    return Response({'candidate_count': candidate_count})

@api_view(['GET'])
def get_candidate_info(request, candidate_id):
    candidate_info = contract.functions.candidates(candidate_id).call()
    return Response({'candidate_info': candidate_info})

@api_view(['GET'])
def get_voter_status(request, address):
    voter_status = contract.functions.voters(address).call()
    return Response({'voter_status': voter_status})

@api_view(['POST'])
def vote(request):
    candidate_id = request.data.get('candidate_id')
    sender_address = request.data.get('sender_address')
    private_key = request.data.get('private_key')

    function = contract.functions.Vote(candidate_id)

    # Build transaction parameters
    nonce = w3.eth.getTransactionCount(sender_address)
    gas_price = w3.eth.gas_price
    gas_limit = 100000  # Adjust gas limit based on your contract's complexity

    transaction = function.buildTransaction({
        'gas': gas_limit,
        'gasPrice': gas_price,
        'nonce': nonce,
        'from': sender_address,
    })

    # Sign the transaction
    signed_transaction = w3.eth.account.sign_transaction(transaction, private_key)

    # Send the transaction
    transaction_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)

    return Response({'transaction_hash': transaction_hash})

@api_view(['GET'])
def get_votes_for_candidate(request, candidate_id):
    votes_for_candidate = contract.functions.getVotesForCandidate(candidate_id).call()
    return Response({'votes_for_candidate': votes_for_candidate})

@api_view(['POST'])
def add_candidate(request):
    candidate_name = request.data.get('candidate_name')
    sender_address = request.data.get('sender_address')
    private_key = request.data.get('private_key')

    function = contract.functions.addCandidate(candidate_name)

    # Build transaction parameters
    nonce = w3.eth.getTransactionCount(sender_address)
    gas_price = w3.eth.gas_price
    gas_limit = 100000  # Adjust gas limit based on your contract's complexity

    transaction = function.buildTransaction({
        'gas': gas_limit,
        'gasPrice': gas_price,
        'nonce': nonce,
        'from': sender_address,
    })

    # Sign the transaction
    signed_transaction = w3.eth.account.sign_transaction(transaction, private_key)

    # Send the transaction
    transaction_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)

    return Response({'transaction_hash': transaction_hash})
