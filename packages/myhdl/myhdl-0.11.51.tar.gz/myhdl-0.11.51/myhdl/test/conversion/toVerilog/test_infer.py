import os
path = os.path
import unittest

from myhdl import (block, Signal, enum, intbv, delay, instance,
                   StopSimulation, toVerilog)
from myhdl._Simulation import Simulation
from myhdl import ConversionError
from myhdl.conversion._misc import _error

from .util import setupCosimulation

b = c = 2


@block
def UnboundError1(a, out):

    @instance
    def comb():
        while 1:
            yield a
            out.next = a + b
            b = 1

    return comb


@block
def UnboundError2(a, out):

    @instance
    def comb():
        while 1:
            yield a
            if a == 1:
                c = 1
            else:
                out.next = c

    return comb


@block
def UnboundError3(a, out):

    @instance
    def comb():
        while 1:
            yield a
            out.next = a + d  # this is the error we want to test
            d = 1

    return comb


@block
def UnboundError4(a, out):

    @instance
    def comb():
        while 1:
            yield a
            if a == 1:
                e = 1
            else:
                out.next = e

    return comb


@block
def InferError1(a, out):

    @instance
    def comb():
        yield a
        b = 2
        b = intbv(0)[5:]
        b[:] = 4
        out.next = b

    return comb


@block
def InferError2(a, out):

    @instance
    def comb():
        yield a
        c = intbv(0)[5:]
        c[:] = 4
        c = intbv(0)[4:]
        c[:] = 4
        out.next = c

    return comb


enumType = enum("a", "b", "c")


@block
def InferError3(a, out):

    @instance
    def comb():
        yield a
        d = enumType.a
        d = 4
        out.next = b

    return comb


@block
def InferError4(a, out):

    @instance
    def comb():
        h = intbv(0)
        yield a
        out.next = h

    return comb


def InferError5Func(a):
    h = intbv(0)[5:]
    if a:
        return h
    else:
        return 1


@block
def InferError5(a, out):

    @instance
    def comb():
        yield a
        out.next = InferError5Func(a)

    return comb


def InferError6Func(a):
    if a:
        return intbv(0)
    else:
        return intbv(1)


@block
def InferError6(a, out):

    @instance
    def comb():
        yield a
        out.next = InferError6Func(a)

    return comb


def InferError7Func(a):
    if a:
        return intbv(0)[5:]
    else:
        return intbv(0xff)[7:2]


@block
def InferError7(a, out):

    @instance
    def comb():
        yield a
        out.next = InferError7Func(a)

    return comb


class TestErrors(unittest.TestCase):

    def check(self, *args):
        try:
            i = toVerilog(*args)
        except ConversionError as e:
            self.assertEqual(e.kind, _error.NotSupported)
        except:
            self.fail()
        else:
            self.fail()

    def check(self, Infertest, err):
        a = Signal(intbv(-1)[16:])
        out_v = Signal(intbv(0)[16:])
        out = Signal(intbv(0)[16:])
        try:
            infertest_inst = Infertest(a, out).convert(hdl='Verilog')
        except ConversionError as e:
            self.assertEqual(e.kind, err)
        except:
            self.fail()
        else:
            self.fail()

    def nocheck(self, Infertest, err=None):
        a = Signal(intbv(-1)[16:])
        out_v = Signal(intbv(0)[16:])
        out = Signal(intbv(0)[16:])
        infertest_inst = Infertest(a, out).convert(hdl='Verilog')

    def testUnboundError1(self):
        sim = self.check(UnboundError1, _error.UnboundLocal)

    def testUnboundError2(self):
        sim = self.check(UnboundError2, _error.UnboundLocal)

    def testUnboundError3(self):
        sim = self.check(UnboundError3, _error.UnboundLocal)

    def testUnboundError4(self):
        sim = self.check(UnboundError4, _error.UnboundLocal)

    def testInferError1(self):
        sim = self.check(InferError1, _error.TypeMismatch)

    def testInferError2(self):
        sim = self.check(InferError2, _error.NrBitsMismatch)

    def testInferError3(self):
        sim = self.check(InferError3, _error.TypeMismatch)

    def testInferError4(self):
        sim = self.check(InferError4, _error.IntbvBitWidth)

    def testInferError5(self):
        sim = self.check(InferError5, _error.ReturnTypeMismatch)

    def testInferError6(self):
        sim = self.check(InferError6, _error.ReturnIntbvBitWidth)

    def testInferError7(self):
        sim = self.nocheck(InferError7, _error.ReturnIntbvBitWidth)


@block
def Infer1(a, out):

    @instance
    def comb():
        while 1:
            yield a
            c = 5
            c = a < 4
            c = bool(0)
            c = False
            c = not a
            c = True
            out.next = c

    return comb


@block
def Infer2(a, out):

    @instance
    def comb():
        while 1:
            yield a
            c = a < 4
            c = bool(0)
            c = False
            c = not a
            c = True
            c = 5
            out.next = c

    return comb


def Infer3Func(a):
    if True:
        return a > 0
    else:
        return 5


@block
def Infer3(a, out):

    @instance
    def comb():
        while 1:
            yield a
            out.next = Infer3Func(a)

    return comb


def Infer4Func(a):
    while 1:
        if True:
            return 6
        else:
            return a < 3


@block
def Infer4(a, out):

    @instance
    def comb():
        while 1:
            yield a
            out.next = Infer4Func(a)

    return comb


@block
def Infer5(a, out):

    @instance
    def comb():
        while 1:
            yield a
            c = a + 1
            c = a - 1
            c = a * 3
            c = a // 2
            c = a << 2
            c = a >> 2
            c = a % 16
            c = +a
            c = -(-a)
            c = ~(-3)
            c = not a
            c = 5 & 4
            c = 5 | 2
            c = 6 ^ 3
            c = bool(a) and 1
            out.next = c

    return comb


def Infertest_v(name, a, out):
    return setupCosimulation(**locals())


class TestInfer(unittest.TestCase):

    def bench(self, Infertest):

        a = Signal(intbv()[16:])
        out_v = Signal(intbv(0)[16:])
        out = Signal(intbv(0)[16:])

        infertest_inst = Infertest(a, out).convert(hdl='Verilog')
        # infertest_inst = Infertest(hec, header)
        infertest_v_inst = Infertest_v(Infertest.__name__, a, out_v)

        def stimulus():
            a.next = 1
            yield delay(10)
            # print "%s %s" % (out, out_v)
            self.assertEqual(out, out_v)
            raise StopSimulation

        return stimulus(), infertest_inst, infertest_v_inst

    def testInfer1(self):
        sim = self.bench(Infer1)
        Simulation(sim).run()

    def testInfer2(self):
        sim = self.bench(Infer2)
        Simulation(sim).run()

    def testInfer3(self):
        sim = self.bench(Infer3)
        Simulation(sim).run()

    def testInfer4(self):
        sim = self.bench(Infer4)
        Simulation(sim).run()

    def testInfer5(self):
        sim = self.bench(Infer5)
        Simulation(sim).run()


if __name__ == '__main__':
    unittest.main()
