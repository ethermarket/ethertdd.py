import pytest
from ethertdd import EvmContract, FileContractStore
from ethereum import tester, utils, abi

fs = FileContractStore()

def test_fee():
    contract = fs.contracts.example.create()
    assert contract.fee() == 10000;

def test_is_owner():
    contract = fs.contracts.example.create()
    assert contract.isOwner() == 1

def test_set_owner():
    contract = fs.contracts.example.create()
    assert contract.setOwner(tester.a1) == 1
    assert contract.owner() == tester.a1.encode('hex')

if __name__ == '__main__':
    pytest.main()
