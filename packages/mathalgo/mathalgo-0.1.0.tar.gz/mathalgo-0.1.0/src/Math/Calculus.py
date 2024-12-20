from typing import Union, Optional, List, Tuple
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from mathalgo.Utilities.logger import setup_logger, logging

logger = setup_logger("Calculus_mode", "mathalgo/__log__/calculus.log", level=logging.INFO)

# 定義符號變量
x = sp.Symbol("x")

class Calculus:
    """
    # 微積分類別
    
    提供各種微積分相關運算的核心類別。
    
    ## 功能
    - 符號微分和數值微分
    - 不定積分和定積分
    - 極限計算
    - 函數繪圖
    - 泰勒級數展開
    """

    def __init__(self, func_expr: Union[str, sp.Expr]):
        """
        # 初始化函數表達式
        
        ## 參數
        - `func_expr`: 字串或 sympy 表達式形式的函數
        """
        try:
            self.func_expr = sp.sympify(func_expr) if isinstance(func_expr, str) else func_expr
            logger.info(f"函數表達式 f(x) = {self.func_expr} 初始化成功")
        except Exception as e:
            logger.error(f"函數表達式初始化失敗: {str(e)}")
            raise ValueError("無效的函數表達式")

    def __repr__(self) -> str:
        """函數表達式的字串表示"""
        return f"f(x) = {str(self.func_expr)}"

    def derivative(self, order: int = 1) -> 'Calculus':
        """
        # 計算函數導數
        
        ## 參數
        - `order`: 導數階數
        
        ## 回傳
        - 導數結果的 Calculus 物件
        """
        try:
            result = sp.diff(self.func_expr, x, order)
            logger.info(f"{order} 階導數計算成功: {result}")
            return Calculus(result)
        except Exception as e:
            logger.error(f"導數計算失敗: {str(e)}")
            raise ValueError("導數計算錯誤")

    def evaluate(self, x_value: float) -> float:
        """
        # 計算函數在特定點的值
        
        ## 參數
        * `x_value`: x 的值
        
        ## 返回
        * 函數值
        """
        try:
            result = float(self.func_expr.subs(x, x_value))
            logger.info(f"函數在 x = {x_value} 處的值為 {result}")
            return result
        except Exception as e:
            logger.error(f"函數值計算失敗: {str(e)}")
            raise ValueError("函數值計算錯誤")

    def indefinite_integral(self) -> 'Calculus':
        """
        # 計算不定積分
        
        ## 返回
        * 不定積分結果
        """
        try:
            result = sp.integrate(self.func_expr, x)
            logger.info(f"不定積分計算成功: {result}")
            return Calculus(result)
        except Exception as e:
            logger.error(f"不定積分計算失敗: {str(e)}")
            raise ValueError("不定積分計算錯誤")

    def definite_integral(self, lower: float, upper: float) -> float:
        """
        # 計算定積分
        
        ## 參數
        * `lower`: 積分下限
        * `upper`: 積分上限
        
        ## 返回
        * 定積分值
        """
        try:
            result = float(sp.integrate(self.func_expr, (x, lower, upper)))
            logger.info(f"定積分從 {lower} 到 {upper} 的值為 {result}")
            return result
        except Exception as e:
            logger.error(f"定積分計算失敗: {str(e)}")
            raise ValueError("定積分計算錯誤")

    def limit(self, point: float, direction: Optional[str] = None) -> float:
        """
        # 計算極限
        
        ## 參數
        * `point`: 趨近點
        * `direction`: 趨近方向 ('left', 'right', None)
        
        ## 返回
        * 極限值
        """
        try:
            if direction == 'left':
                result = float(sp.limit(self.func_expr, x, point, dir='-'))
            elif direction == 'right':
                result = float(sp.limit(self.func_expr, x, point, dir='+'))
            else:
                result = float(sp.limit(self.func_expr, x, point))
            logger.info(f"極限計算在 x -> {point} ({direction if direction else 'both'}) 的值為 {result}")
            return result
        except Exception as e:
            logger.error(f"極限計算失敗: {str(e)}")
            raise ValueError("極限計算錯誤")

    def taylor_series(self, point: float, order: int) -> 'Calculus':
        """
        # 計算泰勒級數展開
        
        ## 參數
        * `point`: 展開點
        * `order`: 展開階數
        
        ## 返回
        * 泰勒級數
        """
        try:
            result = sp.series(self.func_expr, x, point, order).removeO()
            logger.info(f"在 x = {point} 處的 {order} 階泰勒展開成功")
            return Calculus(result)
        except Exception as e:
            logger.error(f"泰勒展開失敗: {str(e)}")
            raise ValueError("泰勒展開錯誤")

    def plot(self, start: float = -10, end: float = 10, points: int = 1000) -> None:
        """
        # 繪製函數圖形
        
        ## 參數
        * `start`: x 軸起始值
        * `end`: x 軸結束值
        * `points`: 採樣點數
        """
        try:
            x_vals = np.linspace(start, end, points)
            y_vals = [self.evaluate(float(x_val)) for x_val in x_vals]
            
            plt.figure(figsize=(10, 6))
            plt.plot(x_vals, y_vals, label=f'f(x) = {self.func_expr}')
            plt.grid(True)
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title('Function Plot')
            plt.legend()
            plt.show()
            
            logger.info("函數圖形繪製成功")
        except Exception as e:
            logger.error(f"函數圖形繪製失敗: {str(e)}")
            raise ValueError("函數圖形繪製錯誤")

    def find_critical_points(self) -> List[float]:
        """
        # 尋找函數的臨界點
        
        ## 返回
        * 臨界點列表
        """
        try:
            derivative = self.derivative()
            critical_points = sp.solve(derivative.func_expr, x)
            critical_points = [float(point.evalf()) for point in critical_points if point.is_real]
            logger.info(f"找到的臨界點: {critical_points}")
            return critical_points
        except Exception as e:
            logger.error(f"臨界點計算失敗: {str(e)}")
            raise ValueError("臨界點計算錯誤")