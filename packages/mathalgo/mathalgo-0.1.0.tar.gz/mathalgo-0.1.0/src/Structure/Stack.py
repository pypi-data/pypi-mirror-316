class Stack:
    """
    # 堆疊類別
    
    實現後進先出(LIFO)的資料結構。
    """
    
    def __init__(self, max_size: int = None):
        """
        # 初始化空堆疊
        
        ## 參數
        * `max_size`: 堆疊最大容量，None 表示無限制
        """
        self.items = []
        self.max_size = max_size
    
    def __len__(self):
        """返回堆疊大小"""
        return len(self.items)
    
    def __iter__(self):
        """實現迭代器，從堆頂到堆底"""
        return iter(reversed(self.items))
    
    def __str__(self):
        """返回堆疊的字串表示"""
        return f"Stack({self.items})"
    
    def is_empty(self):
        """檢查堆疊是否為空"""
        return len(self.items) == 0
    
    def is_full(self):
        """檢查堆疊是否已滿"""
        return self.max_size is not None and len(self.items) >= self.max_size
    
    def push(self, item):
        """
        # 推入元素
        
        ## 參數
        * `item`: 要推入的元素
        
        ## 異常
        * OverflowError: 當堆疊已滿時
        """
        if self.is_full():
            raise OverflowError("Stack is full")
        self.items.append(item)
    
    def pop(self):
        """
        # 彈出元素
        
        ## 返回
        * 堆頂元素
        
        ## 異常
        * IndexError: 當堆疊為空時
        """
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.items.pop()
    
    def peek(self):
        """
        # 查看堆頂元素
        
        ## 返回
        * 堆頂元素（不移除）
        
        ## 異常
        * IndexError: 當堆疊為空時
        """
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.items[-1]
    
    def clear(self):
        """清空堆疊"""
        self.items.clear()
    
    def swap_top(self):
        """
        # 交換頂部兩個元素
        
        ## 異常
        * IndexError: 當堆疊元素少於2個時
        """
        if len(self.items) < 2:
            raise IndexError("Stack needs at least 2 elements to swap")
        self.items[-1], self.items[-2] = self.items[-2], self.items[-1]
    
    def rotate(self, n: int = 1):
        """
        # 旋轉堆疊元素
        
        ## 參數
        * `n`: 旋轉的元素數量
            * 正數：將頂部 n 個元素循環移動
            * 負數：將底部 n 個元素循環移動
        
        ## 異常
        * ValueError: 當n大於堆疊大小時
        
        ## 實現說明
        ### 向上旋轉 (n > 0)
        1. 取出頂部 n 個元素存入臨時列表
        2. 將剩餘元素轉為列表
        3. 清空當前堆疊
        4. 將臨時列表中的元素依序加入剩餘元素後
        5. 更新堆疊內容
        
        ### 向下旋轉 (n < 0)
        1. 獲取當前迭代順序（從頂到底）
        2. 取出最後 |n| 個元素存入臨時列表
        3. 清空當前堆疊
        4. 將臨時列表中的元素插入到迭代序列前端
        5. 反轉序列以保持正確的堆疊順序
        6. 依序將元素推入堆疊
        
        ## 範例
        ```python
        stack = Stack()
        # 向上旋轉
        [1,2,3,4] 旋轉 2 位
        1. temp = [4,3]
        2. remaining = [1,2]
        3. 結果 = [1,2,4,3]
        
        # 向下旋轉
        [1,2,3,4] 旋轉 -1 位
        1. re = [4,3,2,1]
        2. temp = [1]
        3. re = [1,4,3,2]
        4. 反轉後 = [2,3,4,1]
        ```
        """
        if abs(n) > len(self.items):
            raise ValueError("Rotation amount exceeds stack size")
            
        if n > 0:
            # 向上旋轉
            temp = []
            # 1. 取出頂部 n 個元素
            for _ in range(n):
                temp.append(self.items.pop())
            
            # 2. 將剩餘元素轉為列表
            remaining = list(self.items)
            
            # 3. 清空當前堆疊
            self.items = []
            
            # 4. 將臨時列表中的元素依序加入
            for item in temp:
                remaining.append(item)
            
            # 5. 更新堆疊內容
            self.items = remaining
        else:
            # 向下旋轉
            # 1. 獲取當前迭代順序（從頂到底）
            re = list(self)
            temp = []
            
            # 2. 取出最後 |n| 個元素
            for i in range(-n):
                temp.append(re.pop())
            
            # 3. 清空當前堆疊
            self.clear()

            # 4. 將臨時列表中的元素插入到前端
            for i in temp:
                re.insert(0, i)
                
            # 5. 反轉序列以保持正確的堆疊順序
            re.reverse()
            
            # 6. 依序將元素推入堆疊
            for i in re:
                self.push(i)
