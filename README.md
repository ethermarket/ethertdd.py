# EtherTDD.py 
EtherTDD is a collection of testing tools for Ethereum contracts.

EtherTDD.py is designed for use with third-party testing frameworks. It does not itself provide a testing framework, but simply provides tools to make it easier to write tests for smart contracts. The [example test](https://raw.githubusercontent.com/ethermarket/ethertdd.py/master/test_example.py) included here uses [Pytest](http://pytest.org), but you could just as easily use any other framework, such as [Nose](https://nose.readthedocs.org) or Python's built-in [unittest](https://docs.python.org/2/library/unittest.html) module.

EtherTDD.py is best-suited for testing discrete units of functionality on contracts. EtherTDD.py tests run in PyEthereum's EVM and at no time touch the blockchain. This means tests run as fast as possible at the expense of having no way to actually connect to contracts controlled by third parties on the blockchain. To test functionality that requires integrating with contracts controlled by third parties, use [EtherTDD.js](https://github.com/ethermarket/ethertdd.js). Ideally you'd write your integration tests with EtherTDD.js and write your unit tests with EtherTDD.py.

EtherTDD.py executes compiled EVM code and is thus language-independent.

# Requirements

You must have [PyEthereum](https://github.com/ethereum/pyethereum/tree/develop) installed.

# Installation

    git clone https://github.com/ethermarket/ethertdd.py.git
    cd ethertdd.py
    python setup.py install

Depending on your system, you might need to use `sudo` to run `python setup.py install`.

# Usage

EtherTDD.py provides an EvmContract class that takes a contract's compiled JSON ABI and its compiled binary. You may also optionally supply a sender's private key (`sender`), an initial endowment (`endowment`), a gas price (`gas`), a PyEthereum tester.state instance (`state`), and a custom event log listener function (`log_listener`) via keyword arguments to the constructor.

Here is a simple demonstration of the EvmContract class:

    >>> from ethertdd import EvmContract
    >>> with open('contracts/example.abi', 'r') as f:
    ...    example_abi = f.read()
    ...
    >>> with open('contracts/example.binary', 'r') as f:
    ...    example_binary = f.read().decode('hex')
    ...
    >>> echo = lambda x: print x
    >>> contract = EvmContract(example_abi, example_binary, log_listener=echo)
    ('starting', 1000000, 1000000)
    >>> contract.fee()
    10000
    >>> contract.owner()
    '82a978b3f5962a5b0957d9ee9eef472ee55b42f1'
    >>> contract.setFee(20000)
    True
    >>> contract.fee()
    20000

In a normal testing situation, manually opening contract files and reading them in before passing them on to the EvmContract class would be needlessly repetitive. EtherTDD.py also supplies a FileContractStore class that allows for automatically finding, opening, and instantiating contracts. The above example could be simplified using this class like so:

    >>> from ethertdd import FileContractStore
    >>> fs = FileContractStore()
    >>> contract = fs.contracts.example.create()
    ('starting', 1000000, 1000000)
    >>> contract.fee()
    10000
    >>> contract.owner()
    '82a978b3f5962a5b0957d9ee9eef472ee55b42f1'
    >>> contract.setFee(20000)
    True
    >>> contract.fee()
    20000

FileContractStore optionally takes a `path` keyword argument which defaults to '.' when omitted. The `create` function also optionally takes the same keyword arguments as the EvmContract's constructor does. Aside from the `create` function, FileContractStore also supplies `abi` and `binary` functions that return the contract's ABI string and its compiled binary, respectively.

FileContractStore also allows contract paths to be addressed using `dict` notation:

    >>> from ethertdd import FileContractStore
    >>> fs = FileContractStore()
    >>> contract = fs['contracts']['example'].create()
    ('starting', 1000000, 1000000)

This can be useful if the path to your contracts contains a character that would cause Python to throw a syntax error.
