# nft-collection
## How to create and deploy NFTs on Ethereum and OpenSea using python and solidity

## Prerequisites

Please install or have installed the following:

- [nodejs and npm](https://nodejs.org/en/download/)
- [python](https://www.python.org/downloads/)
## Installation

1. [Install Brownie](https://eth-brownie.readthedocs.io/en/stable/install.html), if you haven't already. Here is a simple way to install brownie.

```bash
pip install eth-brownie
```
Or, if that doesn't work, via pipx
```bash
pip install --user pipx
pipx ensurepath
# restart your terminal
pipx install eth-brownie
```
Remember it is best practise to configure the project inside a virtual environment with all its dependencies.

2. [Install ganache-cli](https://www.npmjs.com/package/ganache-cli)

```bash
npm install -g ganache-cli
```

## Quickstart


1. Clone this repo

```bash
git clone https://github.com/htostudios/nft-collection.git
```

2. Run a script

To deploy the Contract
```
brownie run scripts/deploy.py --network <network name>
```
To Create the collection

```
brownie run scripts/create_collection.py --network <network name>
```
