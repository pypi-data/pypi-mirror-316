from typing import Optional, List, Any
from mathalgo.Utilities.logger import setup_logger, logging

logger = setup_logger("Tree_mode", "mathalgo/__log__/tree.log", level=logging.INFO)

class TreeNode:
    """樹節點類別"""
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class Tree:
    """
    # 二元樹類別
    
    實現基本的二元樹操作。
    """
    
    def __init__(self):
        """初始化空樹"""
        self.root = None
        logger.info("樹結構初始化成功")
    
    def insert(self, value):
        """
        # 插入節點
        
        ## 參數
        * `value`: 要插入的值
        """
        if not self.root:
            self.root = TreeNode(value)
            logger.info(f"插入根節點: {value}")
            return
            
        def _insert_recursive(node, value):
            if value < node.value:
                if node.left is None:
                    node.left = TreeNode(value)
                    logger.info(f"插入左子節點: {value}")
                else:
                    _insert_recursive(node.left, value)
            else:
                if node.right is None:
                    node.right = TreeNode(value)
                    logger.info(f"插入右子節點: {value}")
                else:
                    _insert_recursive(node.right, value)
                    
        _insert_recursive(self.root, value)
    
    def search(self, value) -> Optional[TreeNode]:
        """
        # 搜尋節點
        
        ## 參數
        * `value`: 要搜尋的值
        
        ## 返回
        * TreeNode: 找到的節點
        * None: 如果沒找到
        """
        def _search_recursive(node, value):
            if node is None or node.value == value:
                return node
            
            if value < node.value:
                return _search_recursive(node.left, value)
            return _search_recursive(node.right, value)
            
        result = _search_recursive(self.root, value)
        if result:
            logger.info(f"找到節點: {value}")
        else:
            logger.info(f"未找到節點: {value}")
        return result
    
    def delete(self, value):
        """
        # 刪除節點
        
        ## 參數
        * `value`: 要刪除的值
        """
        def _find_min(node):
            current = node
            while current.left:
                current = current.left
            return current
            
        def _delete_recursive(node, value):
            if node is None:
                return None
                
            if value < node.value:
                node.left = _delete_recursive(node.left, value)
            elif value > node.value:
                node.right = _delete_recursive(node.right, value)
            else:
                # 節點有一個或沒有子節點
                if node.left is None:
                    return node.right
                elif node.right is None:
                    return node.left
                    
                # 節點有兩個子節點
                temp = _find_min(node.right)
                node.value = temp.value
                node.right = _delete_recursive(node.right, temp.value)
                
            return node
            
        self.root = _delete_recursive(self.root, value)
        logger.info(f"刪除節點: {value}")
    
    def inorder_traversal(self) -> List[Any]:
        """
        # 中序遍歷
        
        ## 返回
        * 遍歷結果列表
        """
        result = []
        
        def _inorder(node):
            if node:
                _inorder(node.left)
                result.append(node.value)
                _inorder(node.right)
                
        _inorder(self.root)
        logger.info(f"中序遍歷結果: {result}")
        return result
    
    def preorder_traversal(self) -> List[Any]:
        """
        # 前序遍歷
        
        ## 返回
        * 遍歷結果列表
        """
        result = []
        
        def _preorder(node):
            if node:
                result.append(node.value)
                _preorder(node.left)
                _preorder(node.right)
                
        _preorder(self.root)
        logger.info(f"前序遍歷結果: {result}")
        return result
    
    def postorder_traversal(self) -> List[Any]:
        """
        # 後序遍歷
        
        ## 返回
        * 遍歷結果列表
        """
        result = []
        
        def _postorder(node):
            if node:
                _postorder(node.left)
                _postorder(node.right)
                result.append(node.value)
                
        _postorder(self.root)
        logger.info(f"後序遍歷結果: {result}")
        return result
    
    def is_balanced(self) -> bool:
        """
        # 檢查樹是否平衡
        
        ## 返回
        * bool: 是否平衡
        """
        def _height(node):
            if not node:
                return 0
            return 1 + max(_height(node.left), _height(node.right))
            
        def _is_balanced_recursive(node):
            if not node:
                return True
                
            left_height = _height(node.left)
            right_height = _height(node.right)
            
            if abs(left_height - right_height) > 1:
                return False
                
            return _is_balanced_recursive(node.left) and _is_balanced_recursive(node.right)
            
        result = _is_balanced_recursive(self.root)
        logger.info(f"樹平衡檢查結果: {'平衡' if result else '不平衡'}")
        return result
    
    def level_order_traversal(self) -> List[List[Any]]:
        """
        # 層序遍歷
        
        ## 返回
        * 按層組織的節點值列表
        """
        if not self.root:
            return []
            
        result = []
        queue = [self.root]
        
        while queue:
            level = []
            level_size = len(queue)
            
            for _ in range(level_size):
                node = queue.pop(0)
                level.append(node.value)
                
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
                    
            result.append(level)
            
        logger.info(f"層序遍歷結果: {result}")
        return result
    
    def serialize(self) -> str:
        """
        # 序列化樹結構
        
        ## 返回
        * 樹的字符串表示
        """
        if not self.root:
            return "[]"
            
        result = []
        queue = [self.root]
        
        while queue:
            node = queue.pop(0)
            if node:
                result.append(str(node.value))
                queue.append(node.left)
                queue.append(node.right)
            else:
                result.append("null")
                
        # 移除尾部的 null
        while result[-1] == "null":
            result.pop()
            
        return "[" + ",".join(result) + "]"
    
    @classmethod
    def deserialize(cls, data: str) -> 'Tree':
        """
        # 從字符串創建樹
        
        ## 參數
        * `data`: 樹的字符串表示
        
        ## 返回
        * 新的樹實例
        """
        if data == "[]":
            return cls()
            
        values = data[1:-1].split(",")
        tree = cls()
        tree.root = TreeNode(int(values[0]))
        queue = [tree.root]
        i = 1
        
        while queue and i < len(values):
            node = queue.pop(0)
            
            # 左子節點
            if i < len(values) and values[i] != "null":
                node.left = TreeNode(int(values[i]))
                queue.append(node.left)
            i += 1
            
            # 右子節點
            if i < len(values) and values[i] != "null":
                node.right = TreeNode(int(values[i]))
                queue.append(node.right)
            i += 1
            
        return tree