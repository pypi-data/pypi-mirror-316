from myhdl import (block, Signal, intbv, always)


@block
def module42_2(sigin, sigout):

    # Using @always(sigin) only warns, but using @always_comb breaks.
    # The reason is that len(sigout) is interpreted as sigout being used as
    # an input.
    @always(sigin)
    def output():
        sigout.next = sigin[len(sigout):]

    return output


sigin = Signal(intbv(0)[2:])
sigout = Signal(intbv(0)[2:])


def test_bug_42_2():
    module42_2(sigin, sigout).convert(hdl='VHDL')


module42_2(sigin, sigout).convert(hdl='VHDL')

