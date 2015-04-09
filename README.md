# EtherTDD.py 
EtherTDD is a collection of testing tools for Ethereum contracts.

EtherTDD.py is best-suited for testing discrete units of functionality on contracts. EtherTDD.py tests run in PyEthereum's EVM and at no time touch the blockchain. This means tests run as fast as possible at the expense of having no way to actually connect to contracts controlled by third parties on the blockchain. To test functionality that requires integrating with contracts controlled by third parties, use [EtherTDD.js](https://github.com/ethermarket/ethertdd.js). Ideally you'd write your integration tests with EtherTDD.js and write your unit tests with EtherTDD.py.

EtherTDD.py executes compiled EVM code and is thus language-independent.

**Caveat:** It appears that Solidity's compiled code is not yet entirely supported by PyEthereum's EVM: during testing, it was discovered that any Solidity functions that return `bool` types will always return `None` in their Python tests. The workaround at the moment is to return `uint8` types instead, with `1` standing for `true` and `0` standing for `false`. This will allow you to write your tests as if your contracts were returning boolean values, making the transition to proper booleans easier once PyEthereum's EVM introduces suppoort for boolean return values.
