import pytest
from mathalgo.Structure.Stack import Stack

def test_stack_initialization():
    """測試堆疊初始化"""
    stack = Stack()
    assert len(stack) == 0
    assert stack.is_empty()

def test_stack_push():
    """測試推入元素"""
    stack = Stack()
    stack.push(1)
    assert len(stack) == 1
    assert not stack.is_empty()
    assert stack.peek() == 1

def test_stack_pop():
    """測試彈出元素"""
    stack = Stack()
    stack.push(1)
    stack.push(2)
    
    assert stack.pop() == 2
    assert len(stack) == 1
    assert stack.pop() == 1
    assert stack.is_empty()
    
    with pytest.raises(IndexError):
        stack.pop()

def test_stack_peek():
    """測試查看堆頂元素"""
    stack = Stack()
    stack.push(1)
    assert stack.peek() == 1
    assert len(stack) == 1  # peek 不應該移除元素
    
    with pytest.raises(IndexError):
        Stack().peek()

def test_stack_clear():
    """測試清空堆疊"""
    stack = Stack()
    stack.push(1)
    stack.push(2)
    stack.clear()
    assert stack.is_empty()

def test_stack_iteration():
    """測試堆疊迭代"""
    stack = Stack()
    items = [1, 2, 3]
    for item in items:
        stack.push(item)
    
    # 驗證迭代順序是從堆頂到堆底（後進先出）
    assert list(stack) == [3, 2, 1]  # 最後 push 的元素應該最先出現

def test_stack_max_size():
    """測試堆疊容量限制"""
    stack = Stack(max_size=2)
    stack.push(1)
    stack.push(2)
    with pytest.raises(OverflowError):
        stack.push(3)

def test_stack_swap_top():
    """測試交換頂部元素"""
    stack = Stack()
    stack.push(1)
    stack.push(2)
    stack.swap_top()
    assert stack.pop() == 1
    assert stack.pop() == 2

def test_stack_rotate_upward():
    """測試堆疊向上旋轉操作
    
    向上旋轉時，頂部的元素會被移動到較低的位置
    例如：[1,2,3,4] 向上旋轉 2 位後變成 [3,4,2,1]（從底部看）
    """
    stack = Stack()
    for item in [1, 2, 3, 4]:
        stack.push(item)
    
    stack.rotate(2)
    assert list(stack) == [3, 4, 2, 1]
    
    # 測試錯誤情況
    stack_error = Stack()
    stack_error.push(1)
    with pytest.raises(ValueError):
        stack_error.rotate(2)  # 嘗試旋轉超過堆疊大小
        
def test_stack_rotate_downward():
    """測試堆疊向下旋轉操作
    
    向下旋轉時，從底部抽出元素放到頂部
    例如：[1,2,3,4] 向下旋轉 1 位
    1. 內部存儲: [1,2,3,4]
    2. 取出最後一個元素: [2,3,4,1]
    3. 迭代時會得到: [1,4,3,2]
    """
    stack = Stack()
    for item in [1, 2, 3, 4]:  # 內部順序: [1, 2, 3, 4]
        stack.push(item)

    stack.rotate(-1)
    assert list(stack) == [1, 4, 3, 2]  # 從頂到底的順序