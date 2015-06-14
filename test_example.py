import pytest
from ethereum import tester
from ethertdd import FileContractStore

fs = FileContractStore()

def test_fee():
    contract = fs.contracts.example.create(2000)
    assert contract.fee() == 2000;

def test_is_owner():
    contract = fs.contracts.example.create()
    assert contract.isOwner()

def test_set_owner():
    contract = fs.contracts.example.create()
    assert contract.setOwner(tester.a1)
    assert contract.owner() == tester.a1.encode('hex')

def test_constructor_argument():
    contract = fs.contracts.example.create(2000, tester.a1)
    assert contract.owner() == tester.a1.encode('hex')

if __name__ == '__main__':
    pytest.main()
