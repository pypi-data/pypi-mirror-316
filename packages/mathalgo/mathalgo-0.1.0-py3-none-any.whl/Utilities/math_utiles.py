from mymod.algorithm.Structure.Stack import Stack


def is_almost_equal(a, b, tolerance=1e-9):
    """ # FUN 檢查兩個浮點數是否幾乎相等。"""
    return abs(a - b) < tolerance

"""
    > 1. 所有數字直接輸出
    > 2. 運算子優先級高於 棧 內的 ( 或棧空 ) 要入棧
    > 3. 所有 ' ( ' 皆入棧
    > 4. 若 棧 內有 ' ( ' 則運算子皆入棧
    > 5. 若是 ' ) ' ，棧內的不斷出棧，直至遇見 ' ( '
    > 6. 最後棧內所有運算子出棧

"""
    
"""
    > 再次入棧，所有數字依序入棧
    > 遇見運算子則出棧兩次，用運算子計算並入棧

"""

# FUN 後綴表達式計算
def evaluate_postfix( expression ):
    """
    計算 後綴表達式 的值。

    : 參數型態 : list, 後綴表達式 的元素列表 ( 如: ["2", "3", "+", "4", "*"] )
    : return : 計算後的結果 ( float )
    """
    stack = Stack()

    # 定義可支持的運算符對應的計算邏輯
    operators = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: a / b if b != 0 else float('inf')  # 避免除以零
    }

    for token in expression:
        if token.isdigit() or (token.lstrip('-').isdigit()):  # 處理數字 (包括負數)
            stack.push(float(token))
        elif token in operators:
            if stack.size() < 2:
                raise ValueError("表達式不合法，操作數不足")
            # 從堆疊中彈出兩個數進行運算
            b = stack.pop()
            a = stack.pop()
            result = operators[token](a, b)
            stack.push(result)
        else:
            raise ValueError(f"不支援的符號: {token}")

    if stack.size() != 1:
        raise ValueError("表達式不合法，結果堆疊有多於一個值")

    return stack.items

# FUN 後綴表達式轉換
def postfix_expression(mula) :
    """ 
        將 中綴表達式 轉換成 後綴表達式
        : 參數型態 : string
        : 回傳型態 : list
    
    """
    
    def precedence(op):
        """ 返回运算符的优先级 """
        if op == '+' or op == '-':
            return 1
        if op == '*' or op == '/':
            return 2
        if op == '^':
            return 3
        return 0

    out = Stack()
    stack = Stack()
    
    for ch in mula :
        if ch.isalnum() :
            out.push(ch)
        elif ch == "(" :
            stack.push(ch)
        elif ch == ")" :
            while stack.peek() != "(" :
                out.push(stack.pop())
            stack.pop()  # 弹出 '('
        else :
            while ( not stack.is_empty and precedence(stack.peek()) >= precedence(ch)) :
                out.push(stack.pop())
            stack.push(ch)
    while not stack.is_empty():
        out.push(stack.pop())

    return out.items


# def Marix_expression(m) :
    