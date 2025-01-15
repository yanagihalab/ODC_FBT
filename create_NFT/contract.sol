// SPDX-License-Identifier: MIT
// Compatible with OpenZeppelin Contracts ^5.0.0
pragma solidity ^0.8.22;

import {ERC721} from "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract FerryTK is ERC721 {
    constructor() ERC721("FerryTK", "FTK") {}

    function _baseURI() internal pure override returns (string memory) {
        return "https://ipfs.yamada.jo.sus.ac.jp/ipfs/QmU2gFym7mVEPrxTm3rY1BYsoaEJRajTJiqu4EXreCvHFC";
    }
}
