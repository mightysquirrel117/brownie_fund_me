from brownie import FundMe, web3
from scripts.helper import get_account
from web3 import Web3


def fund_me():
    fund_me = FundMe[-1]
    account = get_account()

    min_eth = fund_me.getMinimumValue()
    print(min_eth / 10**18)

    tx = fund_me.fund({"from": account, "value": Web3.toWei(0.025, "ether")})
    print(tx.return_value)


def check_fund_amount():
    fund_me = FundMe[-1]
    account = get_account()

    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

    print(len(fund_me.address))
    # w3.eth.contract(fund_me.abi[0], fund_me.address)


def main():
    # fund_me()
    check_fund_amount()
