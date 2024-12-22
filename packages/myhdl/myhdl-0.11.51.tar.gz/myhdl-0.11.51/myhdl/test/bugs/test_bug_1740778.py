import os
path = os.path
import random
random.seed(2)

from myhdl import (block, Signal, intbv, instance, delay)

ACTIVE_LOW, INACTIVE_HIGH = bool(0), bool(1)


@block
def bug_1740778 ():
    """ Conversion of min and max attribute.

    """
    s = Signal(intbv(0, min=-13, max=46))

    @instance
    def comb():
        v = intbv(0, min=-15, max=45)
        yield delay(10)
        print(v.min)
        print(v.max)
        print(s.val)
        print(s.min)
        print(s.max)

    return comb


def test_bug_1740778 ():
    assert bug_1740778().verify_convert() == 0

