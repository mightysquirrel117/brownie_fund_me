from brownie import network, accounts, config
from brownie import MockV3Aggregator, FundMe
from web3 import Web3

LOCAL_FORKED_EVNS = ["mainnet-fork"]
LOCAL_CHAIN_EVNS = ["development", "ganache-local"]

DECIMALS = 8
START_PRICE = 2000 * 10**8


def get_account():
    if network.show_active() in LOCAL_CHAIN_EVNS + LOCAL_FORKED_EVNS:
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


def deploy_mock_aggregator(account):
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(DECIMALS, START_PRICE, {"from": account})


def deploy_fund_me(account):

    if network.show_active() not in LOCAL_CHAIN_EVNS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed_address"
        ]
    else:
        deploy_mock_aggregator(account)
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )

    return fund_me
