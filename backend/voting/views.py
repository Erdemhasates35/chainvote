from django.shortcuts import render
from web3 import Web3
import json
import os

# Create your views here.
web3 = Web3(Web3.HTTPProvider('http://localhost:7545'))

contract_file = os.path.join(os.getcwd(), "voting_identity/build/contracts/DecentralizedVoting.json")
with open(contract_file, 'r') as file:
    data = json.load(file)

voting_abi = data['abi']
contract_address = '0xC24724d9c0F0f3C1B9945003F528204de539A5B4'



# Create a contract instance
contract = web3.eth.contract(address=contract_address, abi=voting_abi)

def get_candidate_count():
    return contract.functions.candidateCount().call()

def get_candidate_info(candidate_id):
    return contract.functions.candidates(candidate_id).call()

def get_voter_status(address):
    return contract.functions.voters(address).call()

def vote(candidate_id, sender_address, private_key):
    function = contract.functions.Vote(candidate_id)

    # Build transaction parameters
    nonce = web3.eth.getTransactionCount(sender_address)
    gas_price = web3.eth.gas_price
    gas_limit = 100000  # Adjust gas limit based on your contract's complexity

    transaction = function.buildTransaction({
        'gas': gas_limit,
        'gasPrice': gas_price,
        'nonce': nonce,
        'from': sender_address,
    })

    # Sign the transaction
    signed_transaction = web3.eth.account.sign_transaction(transaction, private_key)

    # Send the transaction
    transaction_hash = web3.eth.sendRawTransaction(signed_transaction.rawTransaction)

    return transaction_hash

def get_votes_for_candidate(candidate_id):
    return contract.functions.getVotesForCandidate(candidate_id).call()

def add_candidate(candidate_name, sender_address, private_key):
    function = contract.functions.addCandidate(candidate_name)

    # Build transaction parameters
    nonce = web3.eth.getTransactionCount(sender_address)
    gas_price = web3.eth.gas_price
    gas_limit = 300000  # Adjust gas limit based on your contract's complexity

    transaction = function.buildTransaction({
        'gas': gas_limit,
        'gasPrice': gas_price,
        'nonce': nonce,
        'from': sender_address,
    })

    # Sign the transaction
    signed_transaction = web3.eth.account.sign_transaction(transaction, private_key)

    # Send the transaction
    transaction_hash = web3.eth.sendRawTransaction(signed_transaction.rawTransaction)

    return transaction_hash