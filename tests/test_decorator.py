import random
import pytest

from tryit.core import tryit 
from tryit.core import ExceptionTarget


@tryit()
def fun():
    raise ValueError()

@tryit(default_callback=lambda err: err)
def fun3():
    raise ImportError()

def division_callback(err: Exception) -> float:
    return float("nan")


@tryit(exceptions=[ExceptionTarget(ZeroDivisionError, division_callback)])
def fun2(a: int, b: int):
    return a / b
  
@tryit(exceptions=[
    ExceptionTarget(ValueError, lambda err: "OK"),
    ExceptionTarget(AttributeError, lambda err: "OK"),
    ExceptionTarget(ImportError, lambda err: "OK"),
    ExceptionTarget(RuntimeError, lambda err: "OK"),
    ExceptionTarget(SyntaxError, lambda err: "OK")
    ]
)

def random_exception():
    exceptions = [
        ValueError,
        AttributeError,
        ImportError,
        RuntimeError,
        SyntaxError
    ]        

    cls = random.choice(exceptions)
    raise cls()


def test_raise_something():
    with pytest.raises(ValueError):
        fun()

def test_division_by_zero_must_return_nan():
    ret = fun2(10, 0)
    assert isinstance(ret, float)

def test_good_division():
    ret = fun2(10, 2)
    assert ret == 5

def test_default_callback():
    ret = fun3()
    assert isinstance(ret, ImportError)

def test_random_exception():
    ret = random_exception()
    assert ret == "OK"
    
