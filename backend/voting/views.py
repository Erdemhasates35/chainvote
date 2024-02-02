from django.shortcuts import render
from web3 import Web3
import json

# Create your views here.
web3 = Web3(Web3.HTTPProvider('http://localhost:7545'))

contract_file = os.path.join(os.getcwd(), "../voting_identity/build/contracts/DecentralizedVoting.json")
with open(contract_file, 'r') as file:
    data = json.load(file)

voting_abi = data['abi']
contract_address = '0xC24724d9c0F0f3C1B9945003F528204de539A5B4'

