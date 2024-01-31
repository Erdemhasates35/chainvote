from django.shortcuts import render

# Create your views here.

def create_did():
    """View for creating a decentralized identity on the blockchain
    it should accept the basic identity for a user. Attributes to accept include
    name, age, dob, address, occupation. The data shou;ld be in json format
      Each of this data should be stored in ipfs and the hash should be stored """