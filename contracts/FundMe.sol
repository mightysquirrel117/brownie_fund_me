// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

contract FundMe {
    AggregatorV3Interface internal priceFeed;

    uint256 public minDepositValueinUSD;
    address public owner;

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the deployer can call this!");
        _;
    }

    constructor(address _priceFeed) public {
        priceFeed = AggregatorV3Interface(_priceFeed);
        minDepositValueinUSD = 50 * 10**18;
        owner = msg.sender;
    }

    mapping(address => uint256) public addressToFunds;

    function fund() public payable returns (bool) {
        require(
            msg.value >= getMinimumValue(),
            "Value needs to be at least 50USD"
        );
        addressToFunds[msg.sender] += msg.value;
        return true;
    }

    function withdraw() public payable onlyOwner {
        payable(owner).transfer(address(this).balance);
    }

    function getPrice() public view returns (uint256) {
        (, int256 price, , , ) = priceFeed.latestRoundData();
        return uint256(price) * 10**10;
    }

    function getMinimumValue() public view returns (uint256) {
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        return (minDepositValueinUSD * precision) / price;
    }

    // function getUsdAmount(uint256 ethAmount) public view returns (uint256) {
    //     uint256 ethInUsd = getPrice(); // (eth/usd * 10^7) / 10^(7+18)
    //     return (ethAmount * ethInUsd) / 10**18; // eth = wei * 10^18
    // }

    function getPFVersion() public view returns (uint256) {
        return priceFeed.version();
    }

    function getPFDecimals() public view returns (uint8) {
        return priceFeed.decimals();
    }

    function getPFDescription() public view returns (string memory) {
        return priceFeed.description();
    }
}
