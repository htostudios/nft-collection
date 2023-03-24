from brownie import accounts,config,network,interface,Contract,LinkToken,VRFCoordinatorMock
from web3 import Web3

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork","mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development","ganache-local"]
DECIMALS = 8
OPENSEA_URL = "https://testnets.opensea.io/assets/goerli/{}/{}"
STARTING_PRICE = 200000000000
OPENSEA_URL = "https://testnets.opensea.io/assets/goerli/{}/{}"

def get_account(index=None,id=None):
    if index:
        return accounts[index]

    if id:
        return accounts.load(id)

    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIRONMENTS:
        return accounts[0]
        
    return accounts.add(config["wallets"]["from_key"])

contract_to_mock = {
    "vrf_coordinator":VRFCoordinatorMock,
    "link_token":LinkToken
}

def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(contract_type._name, contract_address, contract_type.abi)
    return contract

def deploy_mocks(decimals=DECIMALS,initial_value=STARTING_PRICE):
    print("Deploying Mocks!")
    account = get_account()
    link_token = LinkToken.deploy({"from":account})
    VRFCoordinatorMock.deploy(link_token.address,{"from":account})
    print("Mocks Deployed!")

def fund_with_link(contract_address,account=None,link_token=None,amount=Web3.toWei(1,"ether")):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    link_token_contract = interface.LinkTokenInterface(link_token.address)
    tx = link_token_contract.transfer(contract_address,amount,{"from":account})
    tx.wait(1)
    print("Funded contract with Link!")
    return tx