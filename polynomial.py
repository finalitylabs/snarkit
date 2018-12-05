class Polynomial:

    def __init__(self, coefs):
        self.coefs = coefs if coefs else [0]

    def __add__(self, p):
        cnt = max(len(self.coefs), len(p.coefs))
        coefs = [0] * cnt
        for i in range(cnt):
            coefs[i] += self.coefs[i] if len(self.coefs) > i else 0
            coefs[i] += p.coefs[i] if len(p.coefs) > i else 0
        return Polynomial(coefs)

    def __neg__(self):
        return Polynomial([-c for c in self.coefs])

    def __sub__(self, p):
        return self + (-p)

    def __mul__(self, p):
        cnt = len(self.coefs) + len(p.coefs) - 1
        coefs = [0] * cnt
        for i, coef1 in enumerate(self.coefs):
            for j, coef2 in enumerate(p.coefs):
                coefs[i + j] += coef1 * coef2
        return Polynomial(coefs)

    def __mod__(self, p):
        num = self.normalized().coefs
        den = p.normalized().coefs
        if len(num) >= len(den):
            shiftlen = len(num) - len(den)
            den = [0] * shiftlen + den
        else:
            return Polynomial(num).normalized()
        quot = []
        divisor = float(den[-1])
        for i in range(shiftlen + 1):
            mult = num[-1] / divisor
            quot = [mult] + quot
            if mult != 0:
                d = [mult * u for u in den]
                num = [u - v for u, v in zip(num, d)]
            num.pop()
            den.pop(0)
        return Polynomial(num).normalized()

    def normalized(self):
        coefs = list(self.coefs)
        while coefs and coefs[-1] == 0:
            coefs.pop()
        return Polynomial(coefs)

    def __str__(self):
        return ' + '.join(["{}x^{}".format(coef, deg) for deg,coef in enumerate(self.coefs)])
