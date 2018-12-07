from vector import Vector

class R1CSCircuit:

    def __init__(self, symbols, L, R, O):
        self.symbols = symbols
        self.L, self.R, self.O = L, R, O

    def verify(self, solution):
        sol = [0] * len(self.symbols)
        for k, v in solution.items():
            sol[self.symbols[k]] = v
        sol = Vector(sol)
        L = Vector((v.dot(sol) for v in self.L))
        R = Vector((v.dot(sol) for v in self.R))
        O = Vector((v.dot(sol) for v in self.O))
        result = L * R - O
        return result.dot(result) == 0

class CircuitGenerator:

    def __init__(self):
        self.gates = []
        self.vars = set()

    def _new_var(self, var):
        if var in self.vars:
            raise Exception("'{}' is already set!".format(var))
        self.vars.add(var)

    def mov(self, result, a):
        l = {'1': a} if type(a) is int else {a: 1}
        r = {'1': 1}
        o = {result: 1}
        self._new_var(result)
        self.gates.append((l, r, o))

    def mul(self, result, a, b):
        l = {'1': a} if type(a) is int else {a: 1}
        r = {'1': b} if type(b) is int else {b: 1}
        o = {result: 1}
        self._new_var(result)
        self.gates.append((l, r, o))

    def inv(self, result, a):
        l = {result: 1}
        r = {'1': a} if type(a) is int else {a: 1}
        o = {'1': 1}
        self._new_var(result)
        self.gates.append((l, r, o))

    def neg(self, result, a):
        self.mul(result, '-1', a)

    def add(self, result, a, b):
        if type(a) is int and type(b) is int:
            self.mov(result, a + b)
            return
        if a == b:
            self.mul(result, a, 2)
            return
        l = {'1': a} if type(a) is int else {a: 1}
        l.update({'1': b} if type(b) is int else {b: 1})
        r = {'1': 1}
        o = {result: 1}
        self._new_var(result)
        self.gates.append((l,r,o))

    def compile(self):
        syms = set()
        for gate in self.gates:
            for part in gate:
                syms.update(part.keys())
        syms = {sym: i for i,sym in enumerate(list(syms))}
        LRO = [[[0] * len(syms) for i in range(len(self.gates))] for i in range(3)]
        for i, gate in enumerate(self.gates):
            for j in range(3):
                for k,v in gate[j].items():
                    LRO[j][i][syms[k]] = v
                LRO[j][i] = Vector(LRO[j][i])
        return R1CSCircuit(syms, LRO[0], LRO[1], LRO[2])


if __name__ == '__main__':
    g = CircuitGenerator()

    g.mul('x^2', 'x', 'x')
    g.mul('x^3', 'x^2', 'x')
    g.add('x^3+x', 'x^3', 'x')
    g.add('x^3+x+5', 'x^3+x', 5)
    g.inv('1/5', 5)
    g.neg('-x', 'x')
    g.mul('(x^3+x+5)/5', 'x^3+x+5', '1/5')
    g.add('((x^3+x+5)/5)-x', '(x^3+x+5)/5', '-x')

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

    circuit = g.compile()
    print(circuit.verify(solution))
