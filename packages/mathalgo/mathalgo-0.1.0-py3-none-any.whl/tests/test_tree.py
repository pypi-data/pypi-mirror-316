import pytest
from mathalgo.Structure.Tree import Tree

def test_tree_initialization():
    """測試樹的初始化"""
    tree = Tree()
    assert tree.root is None

def test_tree_insert():
    """測試插入節點"""
    tree = Tree()
    tree.insert(5)
    assert tree.root.value == 5
    
    tree.insert(3)
    tree.insert(7)
    assert tree.root.left.value == 3
    assert tree.root.right.value == 7

def test_tree_search():
    """測試搜尋節點"""
    tree = Tree()
    tree.insert(5)
    tree.insert(3)
    tree.insert(7)
    
    assert tree.search(5).value == 5
    assert tree.search(3).value == 3
    assert tree.search(7).value == 7
    assert tree.search(10) is None

def test_tree_delete():
    """測試刪除節點"""
    tree = Tree()
    tree.insert(5)
    tree.insert(3)
    tree.insert(7)
    
    tree.delete(3)
    assert tree.search(3) is None
    assert tree.search(5) is not None
    assert tree.search(7) is not None

def test_tree_traversal():
    """測試樹的遍歷"""
    tree = Tree()
    tree.insert(5)
    tree.insert(3)
    tree.insert(7)
    
    assert tree.inorder_traversal() == [3, 5, 7]
    assert tree.preorder_traversal() == [5, 3, 7]
    assert tree.postorder_traversal() == [3, 7, 5]

def test_tree_balance():
    """測試樹的平衡性"""
    tree = Tree()
    # 建立一個平衡的樹
    tree.insert(5)
    tree.insert(3)
    tree.insert(7)
    assert tree.is_balanced()
    
    # 建立一個不平衡的樹
    tree = Tree()
    tree.insert(5)
    tree.insert(4)
    tree.insert(3)
    assert not tree.is_balanced()

def test_level_order_traversal():
    """測試層序遍歷"""
    tree = Tree()
    tree.insert(5)
    tree.insert(3)
    tree.insert(7)
    tree.insert(2)
    tree.insert(4)
    
    levels = tree.level_order_traversal()
    assert levels == [[5], [3, 7], [2, 4]]

def test_serialization():
    """測試序列化和反序列化"""
    # 創建原始樹
    tree = Tree()
    tree.insert(5)
    tree.insert(3)
    tree.insert(7)
    
    # 序列化
    serialized = tree.serialize()
    assert serialized == "[5,3,7]"
    
    # 反序列化
    new_tree = Tree.deserialize(serialized)
    assert new_tree.inorder_traversal() == [3, 5, 7]