from scripts.helper import (
    get_account,
    LOCAL_CHAIN_EVNS,
    deploy_mock_aggregator,
    deploy_fund_me,
)
import pytest
from brownie import FundMe, Wei, config, network, exceptions, accounts
from web3 import Web3


def test_fund():

    account = get_account()
    fund_me = deploy_fund_me(account)

    print(f"ETH/USD on mainnet fork is {fund_me.getPrice()}")
    print(f"Minimum ETH to fund is {fund_me.getMinimumValue() / 10**18}")

    min_value = fund_me.getMinimumValue()
    start_acc_balance = account.balance()
    tx = fund_me.fund({"from": account, "value": min_value})
    tx.wait(1)

    end_acc_balance = account.balance()

    if network.show_active() in LOCAL_CHAIN_EVNS:
        assert min_value == 0.025 * 10**18

    assert start_acc_balance - end_acc_balance == min_value + tx.gas_price * tx.gas_used


def test_withdraw_bad_actor():
    if network.show_active() not in LOCAL_CHAIN_EVNS:
        pytest.skip("Skipping test for this network")

    fund_me = FundMe[-1]
    bad_actor = accounts[1]

    with pytest.raises(ValueError):
        fund_me.withdraw({"from": bad_actor})


def test_withdraw_deployer():
    fund_me = FundMe[-1]
    account = get_account()

    funds = fund_me.addressToFunds(account.address)

    start_acc_balance = account.balance()
    tx = fund_me.withdraw({"from": account})
    tx.wait(1)
    end_acc_balance = account.balance()

    assert end_acc_balance - start_acc_balance + tx.gas_used * tx.gas_price == funds
