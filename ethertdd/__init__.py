from ethereum import abi, tester
from ethereum.utils import is_string

def set_gas_limit(new_limit):
    tester.gas_limit = new_limit

class EvmContract(object):
    # Most of the code in this class was pulled from the _abi_contract class
    # defined in state.abi_contract in https://github.com/ethereum/pyethereum/blob
    # /a4d642e3fd100cf8db44b8e7932fba9027c23f3e/ethereum/tester.py
    # I just modified it to take precompiled code instead of uncompiled code.

    def __init__(self, compiled_abi, compiled_code, name,
                 constructor_args=[], sender=tester.k0, endowment=0,
                 gas=None, state=None, log_listener=None):
        if not state:
            state = tester.state()

        self.state = state

        if is_string(compiled_abi):
            compiled_abi = abi.json_decode(compiled_abi)

        for item in compiled_abi:
            if item['type'] == 'constructor':
                item['type'] = 'function'
                item['name'] = name
                item['outputs'] = []
                break

        self._translator = tester.abi.ContractTranslator(compiled_abi)

        if log_listener:
            self.state.block.log_listeners.append(
                lambda x: log_listener(self._translator.listen(x, noprint=True)))

        if len(constructor_args) > 0:
            compiled_code += self._translator.encode(name, constructor_args)[4:]

        self.address = self.state.evm(compiled_code, sender, endowment, gas)

        assert len(self.state.block.get_code(self.address)), \
            "Contract code empty"

        def kall_factory(f):

            def kall(*args, **kwargs):
                o = self.state._send(kwargs.get('sender', tester.k0),
                                 self.address,
                                 kwargs.get('value', 0),
                                 self._translator.encode(f, args),
                                 **tester.dict_without(kwargs, 'sender',
                                                'value', 'output'))
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
    def __init__(self, name='', path='.', caching=True, parent=None):
        self._name = name
        self._path = path
        self._parent = parent
        self._stores = {}
        self._contents = None
        self._caching = caching

    def __call__(self, *args, **kwargs):
        if self._name == 'create':
            return EvmContract(self._parent.abi(), self._parent.binary(),
                               self._parent._name, args, **kwargs)

        if self._contents is not None:
            return self._contents

        if self._name in ['binary', 'bin']:
            try:
                with open('%s.bin' % self._path[0:-1], 'r') as f:
                    self._contents = f.read()
            except IOError:
                with open('%s.binary' % self._path[0:-1], 'r') as f:
                    self._contents = f.read()

            self._contents = self._contents.decode('hex')

        else:
            with open('%s.%s' % (self._path[0:-1], self._name), 'r') as f:
                self._contents = f.read()

        return self._contents

    def __getattr__(self, attr):
        if not self._caching or attr not in self._stores:
            self._stores[attr] = FileContractStore(
                name=attr, path='%s%s/' % (self._path, self._name), parent=self
            )
        return self._stores[attr]

    def __getitem__(self, item):
        return self.__getattr__(item)
