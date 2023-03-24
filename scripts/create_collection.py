
from brownie import NFTCollection, network, config
from scripts.helpful_scripts import fund_with_link, get_account,OPENSEA_URL
import os
import requests
import json
from pathlib import Path
from num2words import num2words

# The Metadata template
from metadata.sample_metadata import metadata_template

# Creating the NFT collection
def create_nft_collection(no_of_tokens):
    account = get_account()
    nft_collection = NFTCollection[-1]

    for collection_index in range(no_of_tokens):
        fund_with_link(nft_collection.address)
        creation_transaction = nft_collection.createCollectible({"from":account,"gas_limit": 30000000000})
        creation_transaction.wait(1)
        print(f"NFT #{collection_index} created successfully")
        print(f"Creating Metadata for NFT #{collection_index}")
        # Getting the TokenId of the recently created NFT
        token_id = nft_collection.tokenCounter()
        image_uri = create_metadata(nft_collection,token_id)
        set_tokenURI(token_id,nft_collection,image_uri)

# Generating Unique Metadata for the NFTs
def create_metadata(nft_contract,token_id):
    number_of_collectibles = nft_contract.tokenCounter() + 1
    print(f"You have created {number_of_collectibles} collectible(s)")

    word = num2words(token_id)
    metadata_file_name =f"./metadata/{network.show_active()}/{word}.json"

    collectible_metadata = metadata_template
    print(metadata_file_name)
    if Path(metadata_file_name).exists():
        print(f"{metadata_file_name} already exists! Please delete it to overwrite")
    else:
        print(f"Creating metadata file: {metadata_file_name}")
        os.makedirs(metadata_file_name)
        # Creating Metadata for the collection from the metadata template
        collectible_metadata["name"] = f"2048 #{token_id}"
        collectible_metadata["description"] = "A cool 2048 snapshot!"
        image_path = f"./img/{token_id}.jpg"
        filename = image_path.split("/")[-1:][0]
        # Uploading Image to IPFS and generating URI from IPFS
        print("Uploading to IPFS to generate ImageURI")
        image_uri = upload_to_ipfs(image_path)
        collectible_metadata["image"] = image_uri
        # Creating the metadata file.
        with open(metadata_file_name ,"w") as file:
            json.dump(collectible_metadata, file)
            print("Metadata created successfully")
        return image_uri

# Uploading the NFT Images to IPFS
def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file":image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        image_uri = f"ipfs://ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri
        
# Set Token URI
def set_tokenURI(token_id,nft_contract,token_uri):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id,token_uri,{"from":account})
    tx.wait(1)
    print(f"Added tokenURI for {token_id}")
    print(f"You can view your NFT at {OPENSEA_URL.format(nft_contract.address,token_id)}")
    print("Please wait up to 20 minutes and hit the refresh metadata button")

def main():
    create_nft_collection(5)

'''
brownie run scripts/deploy.py --network goerli
'''