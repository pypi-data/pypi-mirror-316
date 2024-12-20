from typing import List, Union, Tuple
from mathalgo.Utilities.logger import setup_logger, logging
import numpy as np

logger = setup_logger("LinearAlgebra_mode", "mathalgo/__log__/linear_algebra.log", level=logging.INFO)

class Vector_space:
    """
    # 向量空間類別
    
    提供向量空間運算的核心類別。
    """

    def __init__(self, vector: List[float] = None):
        """
        # 初始化向量
        
        ## 參數
        - `vector`: 以一維列表表示的向量
        """
        if vector is not None and not isinstance(vector, list):
            logger.error("向量初始化失敗: 資料類型錯誤")
            raise ValueError("向量必須是一維列表。")
        self.vector = vector if vector else []
        self.dimension = len(self.vector)
        logger.info("向量初始化成功")

    def dot_product(self, other: 'Vector_space') -> float:
        """
        # 計算內積
        
        ## 參數
        - `other`: 另一個向量物件
        
        ## 回傳
        - 內積計算結果
        """
        if self.dimension != other.dimension:
            logger.error("內積計算失敗: 向量維度不一致")
            raise ValueError("向量維度必須相同。")
        
        result = sum(a * b for a, b in zip(self.vector, other.vector))
        logger.info(f"內積計算成功: {result}")
        return result

    def cross_product(self, other: 'Vector_space') -> 'Vector_space':
        """
        # 計算外積
        
        ## 參數
        - `other`: 另一個向量物件
        
        ## 回傳
        - 外積計算結果的向量物件
        
        ## 說明
        - 僅適用於三維向量
        """
        if self.dimension != 3 or other.dimension != 3:
            logger.error("外積計算失敗: 向量維度必須為3")
            raise ValueError("外積只能在三維向量間計算。")

        result = [
            self.vector[1] * other.vector[2] - self.vector[2] * other.vector[1],
            self.vector[2] * other.vector[0] - self.vector[0] * other.vector[2],
            self.vector[0] * other.vector[1] - self.vector[1] * other.vector[0]
        ]
        logger.info("外積計算成功")
        return Vector_space(result)

    def norm(self) -> float:
        """
        計算向量的範數（長度）
        :return: 向量範數
        """
        result = np.sqrt(sum(x * x for x in self.vector))
        logger.info(f"範數計算成功: {result}")
        return result

    def normalize(self) -> 'Vector_space':
        """
        向量正規化
        :return: 正規化後的向量
        """
        norm = self.norm()
        if norm == 0:
            logger.error("正規化失敗: 零向量")
            raise ValueError("零向量無法正規化。")
        
        result = [x / norm for x in self.vector]
        logger.info("向量正規化成功")
        return Vector_space(result)

    def angle_between(self, other: 'Vector_space') -> float:
        """
        計算兩個向量之間的夾角（以弧度為單位）
        :param other: 另一個向量
        :return: 夾角（弧度）
        """
        dot_prod = self.dot_product(other)
        norms = self.norm() * other.norm()
        
        if norms == 0:
            logger.error("夾角計算失敗: 存在零向量")
            raise ValueError("零向量無法計算夾角。")
        
        cos_theta = dot_prod / norms
        # 處理數值誤差
        cos_theta = min(1.0, max(-1.0, cos_theta))
        angle = np.arccos(cos_theta)
        logger.info(f"夾角計算成功: {angle} 弧度")
        return angle

    def projection(self, other: 'Vector_space') -> 'Vector_space':
        """
        計算此向量在另一個向量上的投影
        :param other: 投影基底向量
        :return: 投影向量
        """
        if other.norm() == 0:
            logger.error("投影計算失敗: 基底為零向量")
            raise ValueError("無法投影到零向量上。")
        
        scalar = self.dot_product(other) / (other.norm() ** 2)
        result = [scalar * x for x in other.vector]
        logger.info("投影計算成功")
        return Vector_space(result)

    def is_orthogonal(self, other: 'Vector_space') -> bool:
        """
        檢查兩個向量是否正交
        :param other: 另一個向量
        :return: 是否正交
        """
        return abs(self.dot_product(other)) < 1e-10