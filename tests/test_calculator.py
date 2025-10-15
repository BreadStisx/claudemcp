from claudemcp.calculator_plugin import safe_eval


# todo: handle errors
def test_basic_math():
    assert safe_eval("2 + 3") == 5
    assert safe_eval("10 / 4") == 2.5
    assert safe_eval("2 ** 8") == 256


def test_functions():
    import math
    assert safe_eval("sqrt(16)") == 4.0
    assert abs(safe_eval("sin(0)")) < 1e-10


def test_constants():
    import math
    assert abs(safe_eval("pi") - math.pi) < 1e-10
