from ethereum import tester

class EvmContract(object):
    # Most of the code in this class was pulled from the _abi_contract class
    # defined in state.abi_contract in https://github.com/ethereum/pyethereum/blob
    # /a4d642e3fd100cf8db44b8e7932fba9027c23f3e/ethereum/tester.py
    # I just modified it to take precompiled code instead of uncompiled code.

    def __init__(self, compiled_abi, compiled_code, sender=tester.k0,
                 endowment=0, gas=None, state=None):
        if not state:
            state = tester.state()

        self.state = state
        self.address = self.state.evm(compiled_code, sender, endowment, gas)
        assert len(self.state.block.get_code(self.address)), \
            "Contract code empty"
        self._translator = tester.abi.ContractTranslator(compiled_abi)

        def kall_factory(f):

            def kall(*args, **kwargs):
                self.state.block.log_listeners.append(
                    lambda log: self._translator.listen(log))
                o = self.state._send(kwargs.get('sender', tester.k0),
                                 self.address,
                                 kwargs.get('value', 0),
                                 self._translator.encode(f, args),
                                 **tester.dict_without(kwargs, 'sender',
                                                'value', 'output'))
                self.state.block.log_listeners.pop()
                # Compute output data
                if kwargs.get('output', '') == 'raw':
                    outdata = o['output']
                elif not o['output']:
                    outdata = None
                else:
                    outdata = self._translator.decode(f, o['output'])
                    outdata = outdata[0] if len(outdata) == 1 \
                        else outdata
                # Format output
                if kwargs.get('profiling', ''):
                    return dict_with(o, output=outdata)
                else:
                    return outdata
            return kall

        for f in self._translator.function_data:
            vars(self)[f] = kall_factory(f)


class FileContractStore(object):
    def __init__(self, name='', path='.', parent=None):
        self._name = name
        self._path = path
        self._parent = parent
        self._stores = {}
        self._contents = None

    def __call__(self, **kwargs):
        if self._name == 'create':
            return EvmContract(self._parent.abi(), self._parent.binary(), **kwargs)

        if self._contents is None and self._name in ['abi', 'binary']:
            with open('%s.%s' % (self._path[0:-1], self._name), 'r') as f:
                self._contents = f.read()

            if self._name == 'binary':
                self._contents = self._contents.decode('hex')

        return self._contents

    def __getattr__(self, attr):
        if attr not in self._stores:
            self._stores[attr] = FileContractStore(
                name=attr, path='%s%s/' % (self._path, self._name), parent=self
            )
        return self._stores[attr]

