import pytest
from mathalgo.Math.Calculus import Calculus

def test_calculus_initialization():
    """測試函數初始化"""
    # 字符串形式初始化
    f = Calculus("x**2")
    assert str(f) == "f(x) = x**2"

    # 無效表達式
    with pytest.raises(ValueError):
        Calculus("invalid expression")

def test_derivative():
    """測試導數計算"""
    f = Calculus("x**2")
    
    # 一階導數
    f_prime = f.derivative()
    assert str(f_prime) == "f(x) = 2*x"
    
    # 二階導數
    f_double_prime = f.derivative(2)
    assert str(f_double_prime) == "f(x) = 2"

def test_definite_integral():
    """測試定積分計算"""
    f = Calculus("x**2")
    
    # 計算定積分
    result = f.definite_integral(0, 1)
    assert abs(result - 1/3) < 1e-10
