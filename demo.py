from fractions import Fraction

class Vector(dict):
    def __init__(self):
        super().__init__(self)

    def eli(self, v, vec):
        if v in self:
            c = self[v]
            for _ in vec: self[_] = self.get(_, 0) + c * vec[_]
            self.pop(v)

    def sol(self, v):
        c = - self.pop(v)
        for _ in self: self[_] /= c

    def val(self, vu):
        res = 0
        for _ in self: res += self[_] * vu[_]
        return res

class Graph:
    def __init__(self):
        self.v = {}
        self.e = {}

    def addV(self, v):
        self.v[v] = set()

    def addE(self, v1, v2, e, w = 1):
        if v1 not in self.v: self.addV(v1)
        if v2 not in self.v: self.addV(v2)
        self.e[e] = (v1, v2, w)
        self.v[v1].add(e)
        self.v[v2].add(e)

    def _link(self, v, e):
        vs = self.e[e]
        return vs[1] if v == vs[0] else vs[0]

    def delV(self, v):
        for e in self.v[v]:
            self.v[self._link(v, e)].remove(v)
            self.e.pop(e)
        self.v.pop(v)
            
    def delE(self, e):
        vs = self.e[e]
        self.v[vs[0]].remove(e)
        self.v[vs[1]].remove(e)
        self.e.pop(e)

    def __str__(self):
        res = 'v: (e:w)v\n'
        for v in self.v:
            res += '%s: ' % v
            for e in self.v[v]:
                res += '(%s:%s)%s ' % (e, self.e[e][2], self._link(v, e))
            res += '\n'
        return res
    __repr__ = __str__


class Solver:
    def __init__(self, graph, vu):
        self.g = graph
        self.vu = vu
        self._U = self._solU()

    def _khVec(self, v):
        vec = Vector()
        for e in self.g.v[v]:
            vec[self.g._link(v, e)] = Fraction(1, self.g.e[e][2])
        vec[v] = - sum(vec.values())
        return vec
        
    def _solU(self):
        res = {}
        for v in self.g.v:
            if v in self.vu: continue
            vec = self._khVec(v)
            for _ in res: vec.eli(_, res[_])
            vec.sol(v)
            for _ in res: res[_].eli(v, vec)
            res[v] = vec
        return {v: self.vu[v] if v in self.vu else res[v].val(self.vu) for v in self.g.v}

    @property
    def U(self):
        return self._U

    @property
    def I(self):
        return {v: self._khVec(v).val(self._U) if v in self.vu else 0 for v in self.g.v}

    @property
    def R(self):
        vu1, vu2 = self.vu.items()
        return abs((vu2[1] - vu1[1]) / self._khVec(vu1[0]).val(self._U))

        
if __name__ == '__main__':
    from itertools import count
    g = Graph()
    edge = count()
    g.addE(1, 2, next(edge))
    g.addE(1, 4, next(edge))
    g.addE(1, 5, next(edge))
    g.addE(2, 3, next(edge))
    g.addE(2, 6, next(edge))
    g.addE(4, 3, next(edge))
    g.addE(4, 8, next(edge))
    g.addE(5, 6, next(edge))
    g.addE(5, 8, next(edge))
    g.addE(7, 3, next(edge))
    g.addE(7, 6, next(edge))
    g.addE(7, 8, next(edge))
    print(g)
    print('R12 = ', Solver(g, {1: 1, 2: 0}).R)
    print('R13 = ', Solver(g, {1: 1, 3: 0}).R)
    print('R17 = ', Solver(g, {1: 1, 7: 0}).R)
