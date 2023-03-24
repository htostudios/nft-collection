from scripts.helpful_scripts import get_account,get_contract
from brownie import NFTCollection,config,network

def deploy():
    account = get_account()
    nft_collection = NFTCollection.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["keyhash"],
        config["networks"][network.show_active()]["fee"],
        {
            "from":account
        },
    )
    print("NFTCollection contract has been deployed")
    return nft_collection

def main():
    deploy()
