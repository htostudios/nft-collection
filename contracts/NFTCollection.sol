// SPDX-License-Identifier: MIT

pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract NFTCollection is ERC721, VRFConsumerBase {
    
    uint256 public tokenCounter;
    bytes32 public keyHash;
    uint256 public fee;

    mapping(bytes32 => address) public requestIdToSender;

    event requestedCollectible(bytes32 indexed requestId, address requester);

    constructor (address _vrfCoodinator, address _linkToken, bytes32 _keyHash, uint256 _fee) public
        VRFConsumerBase(_vrfCoodinator,_linkToken)
        ERC721("2048 Shots", "2048") {
            tokenCounter = 0;
            keyHash = _keyHash;
            fee = _fee;
    }

    function createCollectible() public returns(bytes32) {
        bytes32 requestId = requestRandomness(keyHash,fee);
        requestIdToSender[requestId] = msg.sender;
        emit requestedCollectible(requestId,msg.sender);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber) internal override {
        uint256 newTokenId = tokenCounter;
        address nft_owner = requestIdToSender[requestId];
        _safeMint(nft_owner,newTokenId);
        tokenCounter = tokenCounter + 1;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        require(_isApprovedOrOwner(_msgSender(),tokenId),"ERC721 caller is not owner nor approved");
        _setTokenURI(tokenId, _tokenURI);
    }
}