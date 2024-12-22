from myhdl import (block, Signal, intbv, always_comb)


@block
def constants(v, u, x, y, z, a):

    b = Signal(bool(0))
    c = Signal(bool(1))
    d = Signal(intbv(5)[8:])
    e = Signal(intbv(4, min=-3, max=9))

    @always_comb
    def comb():
        u.next = d
        v.next = e
        x.next = b
        y.next = c
        z.next = a

    return comb


x, y, z, a = [Signal(bool(0)) for i in range(4)]
u = Signal(intbv(0)[8:])
v = Signal(intbv(0, min=-3, max=9))


def test_constants():
    assert constants(v, u, x, y, z, a).analyze_convert() == 0
