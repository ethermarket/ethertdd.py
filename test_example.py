import pytest
from __init__ import EvmContract
from ethereum import tester, utils, abi

with open('contracts/example.abi', 'r') as f:
    example_abi = f.read()

with open('contracts/example.binary', 'r') as f:
    example_binary = f.read().decode('hex')

def test_fee():
    contract = EvmContract(example_abi, example_binary)
    assert contract.fee() == 10000;

def test_is_owner():
    contract = EvmContract(example_abi, example_binary)
    assert contract.isOwner() == 1

def test_set_owner():
    contract = EvmContract(example_abi, example_binary)
    assert contract.setOwner(tester.a1) == 1
    assert contract.owner() == tester.a1.encode('hex')

if __name__ == '__main__':
    pytest.main()
