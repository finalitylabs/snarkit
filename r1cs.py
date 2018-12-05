class R1CSCircuit:

    def __init__(self):
        self.symbols = {'1': 0, '-1': 1}
        self.gates = []

    def add_symbol(self, name):
        if name in self.symbols:
            raise Exception("Symbol already exists!")
        self.symbols[name] = len(self.symbols)

    def add_mult(self, result, a, b):
        l, r, o = {},{},{}
        if type(a) is int:
            l[self.symbols['1']] = a
        else:
            l[self.symbols[a]] = 1
        if type(b) is int:
            r[self.symbols['1']] = b
        else:
            r[self.symbols[b]] = 1
        o[self.symbols[result]] = 1
        self.gates.append((l,r,o))

    def add_inv(self, result, a):
        l, r, o = {},{},{}
        l[self.symbols[result]] = 1
        o[self.symbols['1']] = 1
        if type(a) is int:
            r[self.symbols['1']] = a
        else:
            r[self.symbols[a]] = 1
        self.gates.append((l,r,o))

    def add_neg(self, result, a):
        l, r, o = {},{},{}
        l[self.symbols['-1']] = 1
        r[self.symbols[result]] = 1
        if type(a) is int:
            o[self.symbols['1']] = a
        else:
            o[self.symbols[a]] = 1
        self.gates.append((l,r,o))

    def add_sum(self, result, a, b):
        l, r, o = {},{},{}
        if type(a) is int and type(b) is int:
            raise Exception("Operands cannot be both int!")
        if type(a) is int:
            l[self.symbols['1']] = a
        else:
            l[self.symbols[a]] = 1
        if type(b) is int:
            l[self.symbols['1']] = b
        else:
            l[self.symbols[b]] = 1
        r[self.symbols['1']] = 1
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
    circuit.add_symbol('((x^3+x+5)/5)-x')

    circuit.add_symbol('x^2')
    circuit.add_mult('x^2', 'x', 'x')

    circuit.add_symbol('x^3')
    circuit.add_mult('x^3', 'x^2', 'x')

    circuit.add_symbol('x^3+x')
    circuit.add_sum('x^3+x', 'x^3', 'x')

    circuit.add_symbol('x^3+x+5')
    circuit.add_sum('x^3+x+5', 'x^3+x', 5)

    circuit.add_symbol('1/5')
    circuit.add_inv('1/5', 5)

    circuit.add_symbol('-x')
    circuit.add_neg('-x', 'x')

    circuit.add_symbol('(x^3+x+5)/5')
    circuit.add_mult('(x^3+x+5)/5', 'x^3+x+5', '1/5')

    circuit.add_sum('((x^3+x+5)/5)-x', '(x^3+x+5)/5', '-x')

    solution = {'1':1,
                '-1':-1,
                'x':3,
                'x^2':9,
                'x^3':27,
                'x^3+x':30,
                'x^3+x+5':35,
                '1/5':0.2,
                '-x': -3,
                '(x^3+x+5)/5': 7,
                '((x^3+x+5)/5)-x': 4}

    print(circuit.check_solution(solution))
