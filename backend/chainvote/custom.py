import ipfshttpclient
import os
import json


from web3 import Web3
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:

    web3 = Web3(Web3.HTTPProvider('http://localhost:7545'))
    web3.eth.default_account = web3.eth.account.from_key(os.getenv('PRIVATE_KEY'))

    print(web3.eth.default_account)

    client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')
    identity_contract_file = os.path.join(os.getcwd(), "../voting_identity/build/contracts/DecentralizedIdentity.json")
    request_contract_file = os.path.join(os.getcwd(), "../voting_identity/build/contracts/VerifiableCredentialIssuer.json")
    credential_contract_file= os.path.join(os.getcwd(), "../voting_identity/build/contracts/VerifiableCredentialRequest.json")

    def __init__(self):
        with open(Config.identity_contract_file, 'r') as file:
            self.identity_data = json.load(file)
        with open(Config.request_contract_file, 'r') as file:
            self.request_data = json.load(file)
        with open(Config.credential_contract_file, 'r') as file:
            self.credential_data = json.load(file)

        self.IDENTITY_CONTRACT_ABI = self.identity_data['abi']
        self.IDENTITY_CONTRACT_ADDRESS = '0x96263426fcd503465150B74f1e0D867cE332D6Fe'

        self.REQUEST_CONTRACT_ABI = self.request_data['abi']
        self.REQUEST_CONTRACT_ADDRESS = '0x3fa6186B6DAb430F53d9ED22196c40fA8bc82e17'

        self.CREDENTIAL_CONTRACT_ABI = self.credential_data['abi']
        self.CREDENTIAL_CONTRACT_ADDRESS = '0x23c5B395615255b94Fe277e13aEfCAF6CCbCCCD2'

        self.request_contract = Config.web3.eth.contract(address=self.REQUEST_CONTRACT_ADDRESS, abi=self.REQUEST_CONTRACT_ABI)
        self.credential_contract = Config.web3.eth.contract(address=self.CREDENTIAL_CONTRACT_ADDRESS, abi=self.CREDENTIAL_CONTRACT_ABI)
        self.identity_contract = Config.web3.eth.contract(address=self.IDENTITY_CONTRACT_ADDRESS, abi=self.IDENTITY_CONTRACT_ABI)


settings = Config()