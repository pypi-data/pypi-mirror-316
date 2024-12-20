import pytest
from mathalgo.Math.Vector_space import Vector_space

def test_vector_initialization():
    """測試向量初始化"""
    # 正常初始化
    v = Vector_space([1, 2, 3])
    assert v.vector == [1, 2, 3]
    assert v.dimension == 3

    # 空向量初始化
    v = Vector_space()
    assert v.vector == []
    assert v.dimension == 0

    # 錯誤的輸入類型
    with pytest.raises(ValueError):
        Vector_space("not a list")

def test_dot_product():
    """測試內積運算"""
    v1 = Vector_space([1, 2, 3])
    v2 = Vector_space([4, 5, 6])
    
    # 正常計算
    assert v1.dot_product(v2) == 32

    # 維度不匹配
    v3 = Vector_space([1, 2])
    with pytest.raises(ValueError):
        v1.dot_product(v3)

def test_cross_product():
    """測試外積運算"""
    v1 = Vector_space([1, 0, 0])
    v2 = Vector_space([0, 1, 0])
    
    # 正常計算
    result = v1.cross_product(v2)
    assert result.vector == [0, 0, 1]

    # 非三維向量
    v3 = Vector_space([1, 2])
    with pytest.raises(ValueError):
        v1.cross_product(v3) 