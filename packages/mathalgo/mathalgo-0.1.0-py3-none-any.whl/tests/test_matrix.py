import pytest
from mathalgo.Math.Matrix import Matrix

def test_matrix_initialization():
    """測試矩陣初始化"""
    # 正常初始化
    m = Matrix([[1, 2], [3, 4]])
    assert m.rows == 2
    assert m.cols == 2

    # 不規則矩陣
    with pytest.raises(ValueError):
        Matrix([[1, 2], [3]])

def test_matrix_addition():
    """測試矩陣加法"""
    m1 = Matrix([[1, 2], [3, 4]])
    m2 = Matrix([[5, 6], [7, 8]])
    
    result = m1.add(m2)
    assert result.data == [[6, 8], [10, 12]]

def test_matrix_multiplication():
    """測試矩陣乘法"""
    m1 = Matrix([[1, 2], [3, 4]])
    m2 = Matrix([[5, 6], [7, 8]])
    
    result = m1.multiply(m2)
    assert result.data == [[19, 22], [43, 50]]
