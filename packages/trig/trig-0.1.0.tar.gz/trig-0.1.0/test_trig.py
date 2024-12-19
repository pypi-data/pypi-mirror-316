import cmath
import random
from math import pi, sqrt

import trig

ALL_FUNCTIONS = [
    trig.sin,
    trig.asin,
    trig.cos,
    trig.acos,
    trig.tan,
    trig.atan,
    trig.sec,
    trig.asec,
    trig.csc,
    trig.acsc,
    trig.cot,
    trig.acot,
    trig.ver,
    trig.aver,
    trig.cvs,
    trig.acvs,
    trig.vcs,
    trig.avcs,
    trig.cvc,
    trig.acvc,
    trig.hvs,
    trig.ahvs,
    trig.hcv,
    trig.ahcv,
    trig.hvc,
    trig.ahvc,
    trig.hcc,
    trig.ahcc,
    trig.exs,
    trig.aexs,
    trig.exc,
    trig.aexc,
    trig.crd,
    trig.acrd,
    trig.sinh,
    trig.asinh,
    trig.cosh,
    trig.acosh,
    trig.tanh,
    trig.atanh,
    trig.sech,
    trig.asech,
    trig.csch,
    trig.acsch,
    trig.coth,
    trig.acoth,
    trig.verh,
    trig.averh,
    trig.cvsh,
    trig.acvsh,
    trig.vcsh,
    trig.avcsh,
    trig.cvch,
    trig.acvch,
    trig.hvsh,
    trig.ahvsh,
    trig.hcvh,
    trig.ahcvh,
    trig.hvch,
    trig.ahvch,
    trig.hcch,
    trig.ahcch,
    trig.exsh,
    trig.aexsh,
    trig.exch,
    trig.aexch,
    trig.crdh,
    trig.acrdh,
]


def random_complex():
    c = []
    for _ in range(2):
        method = random.randrange(4)
        if method == 0:
            x = 0
        elif method == 1:
            x = random.uniform(-0.1, 0.1)
        elif method == 2:
            x = random.uniform(-(10 ** 10), 10 ** 10)
        elif method == 3:
            x = random.uniform(-10, 10)
        c.append(x)
    return complex(*c)


def test_types():
    for _ in range(1000):
        c = random_complex()
        for f in ALL_FUNCTIONS:
            try:
                r = f(c)
                assert type(r) is complex
            except (OverflowError, ZeroDivisionError):
                pass


def test_exact_values():
    table = {
        0: {trig.sin: 0, trig.cos: 1, trig.tan: 0},
        pi / 6: {trig.sin: 0.5, trig.cos: sqrt(3) / 2, trig.tan: sqrt(3) / 3},
        pi / 4: {trig.sin: sqrt(2) / 2, trig.cos: sqrt(2) / 2, trig.tan: 1},
        pi / 3: {trig.sin: sqrt(3) / 2, trig.cos: 1 / 2, trig.tan: sqrt(3)},
        pi / 2: {trig.sin: 1, trig.cos: 0},
    }

    for arg, fs in table.items():
        for function, value in fs.items():
            assert cmath.isclose(function(arg), value, abs_tol=1e-12)


def test_inverses():
    for _ in range(1000):
        c = random_complex()
        for f in ALL_FUNCTIONS:
            if f.__name__.startswith("a"):
                continue
            try:
                r = f(vars(trig)[f"a{f.__name__}"](c))
                print(f, r, c)
                assert cmath.isclose(r, c, rel_tol=1e-5, abs_tol=1e-12)
            except (OverflowError, ZeroDivisionError):
                pass
