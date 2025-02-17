import pycalc

def test_add():
    assert pycalc.add(5,5) == 10.0
    assert pycalc.add(10,10) == 20.0

def test_subtract():
    assert pycalc.subtract(5,1) == 4.0
    assert pycalc.subtract(100,50) == 50.0

def test_mult():
    assert pycalc.multiply(5,5) == 25.0
    assert pycalc.multiply(100, 0) == 0

def test_divide():
    assert pycalc.divide(5,5) == 1.0
    assert pycalc.divide(5,0) == "Cannot divide by zero!"


