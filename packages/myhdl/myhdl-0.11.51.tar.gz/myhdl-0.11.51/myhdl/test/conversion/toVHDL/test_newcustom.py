import os
path = os.path

import random
from random import randrange
random.seed(2)

from myhdl import (block, Signal, intbv, delay, instance,
                   always, always_comb, StopSimulation)

from myhdl import ConversionError

ACTIVE_LOW, INACTIVE_HIGH = 0, 1


@block
def incRef(count, enable, clock, reset, n):
    """ Incrementer with enable.
    
    count -- output
    enable -- control input, increment when 1
    clock -- clock input
    reset -- asynchronous reset input
    n -- counter max value
    """

    @instance
    def comb():
        while 1:
            yield clock.posedge, reset.negedge
            if reset == ACTIVE_LOW:
                count.next = 0
            else:
                if enable:
                    count.next = (count + 1) % n

    return comb


@block
def incGen(count, enable, clock, reset, n):
    """ Generator with __vhdl__ is not permitted """

    @instance
    def comb():
        incGen.vhdl_code = "Template string"
        while 1:
            yield clock.posedge, reset.negedge
            if reset == ACTIVE_LOW:
                count.next = 0
            else:
                if enable:
                    count.next = (count + 1) % n

    return comb


@block
def inc(count, enable, clock, reset, n):
    """ Incrementer with enable.
    
    count -- output
    enable -- control input, increment when 1
    clock -- clock input
    reset -- asynchronous reset input
    n -- counter max value
    """

    @always(clock.posedge, reset.negedge)
    def incProcess():
        # make it fail in conversion
        import types
        if reset == ACTIVE_LOW:
            count.next = 0
        else:
            if enable:
                count.next = (count + 1) % n

    count.driven = "reg"

    inc.vhdl_code = \
"""
process ($clock, $reset) begin
    if ($reset = '0') then
        $count <= (others => '0');
    elsif rising_edge($clock) then
        if ($enable = '1') then
            $count <= ($count + 1) mod $n;
        end if;
    end if;
end process;
"""

    return incProcess


@block
def incErr(count, enable, clock, reset, n):

    @always(clock.posedge, reset.negedge)
    def incProcess():
        # make it fail in conversion
        import types
        if reset == ACTIVE_LOW:
            count.next = 0
        else:
            if enable:
                count.next = (count + 1) % n

    count.driven = "reg"

    incErr.vhdl_code = \
"""
always @(posedge $clock, negedge $reset) begin
    if ($reset == 0) begin
        $count <= 0;
    end
    else begin
        if ($enable) begin
            $count <= ($countq + 1) %% $n;
        end
    end
end
"""

    return incProcess


@block
def inc_comb(nextCount, count, n):

    @always_comb
    def comb():
        # make if fail in conversion
        import types
        nextCount.next = (count + 1) % n

    nextCount.driven = "wire"

    inc_comb.vhdl_code = \
"""
$nextCount <= ($count + 1) mod $n;
"""

    return comb


@block
def inc_seq(count, nextCount, enable, clock, reset):

    @always(clock.posedge, reset.negedge)
    def comb():
        if reset == ACTIVE_LOW:
            count.next = 0
        else:
            if (enable):
                count.next = nextCount

    count.driven = True

    inc_seq.vhdl_code = \
"""
process ($clock, $reset) begin
    if ($reset = '0') then
        $count <= (others => '0');
    elsif rising_edge($clock) then
        if ($enable = '1') then
            $count <= $nextCount;
        end if;
    end if;
end process;
"""

    return comb


@block
def inc2(count, enable, clock, reset, n):

    nextCount = Signal(intbv(0, min=0, max=n))

    comb = inc_comb(nextCount, count, n)
    seq = inc_seq(count, nextCount, enable, clock, reset)

    return comb, seq


@block
def inc3(count, enable, clock, reset, n):
    inc2_inst = inc2(count, enable, clock, reset, n)
    return inc2_inst


@block
def clockGen(clock):

    @instance
    def comb():
        clock.next = 1
        while 1:
            yield delay(10)
            clock.next = not clock

    return comb


NRTESTS = 1000

ENABLES = tuple([min(1, randrange(5)) for i in range(NRTESTS)])


@block
def stimulus(enable, clock, reset):

    @instance
    def comb():
        reset.next = INACTIVE_HIGH
        yield clock.negedge
        reset.next = ACTIVE_LOW
        yield clock.negedge
        reset.next = INACTIVE_HIGH
        for i in range(NRTESTS):
            enable.next = 1
            yield clock.negedge
        for i in range(NRTESTS):
            enable.next = ENABLES[i]
            yield clock.negedge
        raise StopSimulation

    return comb


@block
def check(count, enable, clock, reset, n):

    @instance
    def comb():
        expect = 0
        yield reset.posedge
        # assert count == expect
        print(count)
        while 1:
            yield clock.posedge
            if enable:
                expect = (expect + 1) % n
            yield delay(1)
            # print "%d count %s expect %s count_v %s" % (now(), count, expect, count_v)
            # assert count == expect
            print(count)

    return comb


@block
def customBench(inc):

    m = 8
    n = 2 ** m

    count = Signal(intbv(0)[m:])
    enable = Signal(bool(0))
    clock, reset = [Signal(bool(1)) for i in range(2)]

    inc_inst = inc(count, enable, clock, reset, n=n)
    clk_1 = clockGen(clock)
    st_1 = stimulus(enable, clock, reset)
    ch_1 = check(count, enable, clock, reset, n=n)

    return inc_inst, clk_1, st_1, ch_1


def testIncRef():
    assert customBench(incRef).verify_convert() == 0


def testInc():
    assert customBench(inc).verify_convert() == 0


def testInc2():
    assert customBench(inc2).verify_convert() == 0


def testInc3():
    assert customBench(inc3).verify_convert() == 0


def testIncGen():
    try:
        assert customBench(incGen).verify_convert() == 0
    except ConversionError:
        pass
    else:
        assert False


def testIncErr():
    try:
        assert customBench(incErr).verify_convert() == 0
    except ConversionError:
        pass
    else:
        assert False

