import pytest
from mathalgo.Algorithm.DFS import DFS

def test_dfs_initialization():
    """測試深度優先搜尋初始化"""
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }
    dfs = DFS(graph)
    assert dfs.graph == graph

def test_dfs_search():
    """測試深度優先搜尋"""
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D'],
        'C': ['A'],
        'D': ['B']
    }
    dfs = DFS(graph)
    path = dfs.search('A', 'D')
    assert path == ['A', 'B', 'D'] 