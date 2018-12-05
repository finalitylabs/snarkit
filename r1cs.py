class R1CSCircuit:

    def __init__(self):
        self.symbols = {'~one': 0, '~out': 1}
        self.gates = []

    def add_symbol(self, name):
        if name in self.symbols:
            raise Exception("Symbol already exists!")
        self.symbols[name] = len(self.symbols)

    def add_mult(self, result, a, b):
        l, r, o = {},{},{}
        if type(a) is int:
            l[self.symbols['~one']] = a
        else:
            l[self.symbols[a]] = 1
        if type(b) is int:
            r[self.symbols['~one']] = b
        else:
            r[self.symbols[b]] = 1
        o[self.symbols[result]] = 1
        self.gates.append((l,r,o))

    def add_inv(self, result, a):
        l, r, o = {},{},{}
        l[self.symbols[result]] = 1
        o[self.symbols['~one']] = 1
        if type(a) is int:
            r[self.symbols['~one']] = a
        else:
            r[self.symbols[a]] = 1
        self.gates.append((l,r,o))

    def add_sum(self, result, a, b):
        l, r, o = {},{},{}
        if type(a) is int and type(b) is int:
            raise Exception("Operands cannot be both int!")
        if type(a) is int:
            l[self.symbols['~one']] = a
        else:
            l[self.symbols[a]] = 1
        if type(b) is int:
            l[self.symbols['~one']] = b
        else:
            l[self.symbols[b]] = 1
        r[self.symbols['~one']] = 1
        o[self.symbols[result]] = 1
        self.gates.append((l,r,o))

    def check_solution(self, syms):
        def mul(sol, gate):
            vec = [0] * len(self.symbols)
            sm = 0
            for k,v in gate.items():
                sm += v * sol[k]
            return sm
        sol = [0] * len(self.symbols)
        for k, v in syms.items():
            sol[self.symbols[k]] = v
        for l, r, o in self.gates:
            L,R,O = mul(sol, l), mul(sol, r), mul(sol, o)
            if L * R - O != 0:
                return False
        return True


if __name__ == '__main__':
    circuit = R1CSCircuit()

    circuit.add_symbol('x')

    circuit.add_symbol('sym_1')
    circuit.add_mult('sym_1', 'x', 'x')

    circuit.add_symbol('y')
    circuit.add_mult('y', 'sym_1', 'x')

    circuit.add_symbol('sym_2')
    circuit.add_sum('sym_2', 'y', 'x')

    circuit.add_symbol('sym_3')
    circuit.add_sum('sym_3', 'sym_2', 5)

    circuit.add_symbol('sym_4')
    circuit.add_inv('sym_4', 5)

    circuit.add_mult('~out', 'sym_3', 'sym_4')

    solution = {'~one':1,
                'x':3,
                'sym_1':9,
                'y':27,
                'sym_2':30,
                'sym_3':35,
                'sym_4':0.2,
                '~out': 7}

    print(circuit.check_solution(solution))
