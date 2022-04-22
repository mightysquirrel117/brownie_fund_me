from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helper import get_account, deploy_mock_aggregator
from scripts.helper import deploy_fund_me as helper_deploy
from web3 import Web3


def deploy_fund_me():
    account = get_account()
    fund_me = helper_deploy(account)


def main():
    deploy_fund_me()
