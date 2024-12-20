from typing import List
from mathalgo.Utilities.logger import setup_logger, logging

logger = setup_logger("Matrix_mode", "mathalgo/__log__/matrix.log", level=logging.INFO)

class Matrix:
    """
    矩陣相關功能的核心類
    """

    def __init__(self, data: List[List[float]]):
        """
        初始化矩陣
        :param data: 二維列表表示的矩陣
        """
        if not data or not all(len(row) == len(data[0]) for row in data):
            logger.error("矩陣初始化失敗: 資料無效")
            raise ValueError("所有列必須具有相同的長度且資料不可為空。")
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0])
        logger.info("矩陣初始化成功")
    
    def _check_dimensions(self, other: 'Matrix', operation: str):
        if self.rows != other.rows or self.cols != other.cols:
            logger.error(f"矩陣{operation}失敗: 維度不一致")
            raise ValueError(f"矩陣的維度必須相同才能進行{operation}運算。")

    def __repr__(self) -> str:
        """
        矩陣的字串表示
        """
        return "\n".join([str(row) for row in self.data])

    def add(self, other: 'Matrix') -> 'Matrix':
        """
        矩陣加法
        :param other: 另一個矩陣
        :return: 相加後的矩陣
        """
        self._check_dimensions(other, "加法")
        result = [
            [self.data[i][j] + other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]
        logger.info("矩陣加法成功")
        return Matrix(result)

    def subtract(self, other: 'Matrix') -> 'Matrix':
        """
        矩陣減法
        :param other: 另一個矩陣
        :return: 相減後的矩陣
        """
        self._check_dimensions(other, "減法")
        result = [
            [self.data[i][j] - other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]
        logger.info("矩陣減法成功")
        return Matrix(result)

    def multiply(self, other: 'Matrix') -> 'Matrix':
        """
        矩陣乘法
        :param other: 另一個矩陣
        :return: 相乘後的矩陣
        """
        self._check_dimensions(other, "乘法")
        result = [
            [
                sum(self.data[i][k] * other.data[k][j] for k in range(self.cols))
                for j in range(other.cols)
            ]
            for i in range(self.rows)
        ]
        logger.info("矩陣乘法成功 : {result}")
        return Matrix(result)

    def transpose(self) -> 'Matrix':
        """
        矩陣轉置
        :return: 轉置後的矩陣
        """
        result = [[self.data[j][i] for j in range(self.rows)] for i in range(self.cols)]
        logger.info("矩陣轉置成功")
        return Matrix(result)

    def determinant(self) -> float:
        """
        計算方陣的行列式
        :return: 行列式的值
        """
        if not self.is_square():
            logger.error("行列式計算失敗: 非方陣")
            raise ValueError("只有方陣才能計算行列式。")

        def _det_recursive(matrix: List[List[float]]) -> float:
            if len(matrix) == 1:
                return matrix[0][0]
            if len(matrix) == 2:
                return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
            det = 0
            for col in range(len(matrix)):
                minor = [row[:col] + row[col + 1:] for row in matrix[1:]]
                det += ((-1) ** col) * matrix[0][col] * _det_recursive(minor)
            return det

        determinant_value = _det_recursive(self.data)
        logger.info(f"行列式計算成功: {determinant_value}")
        return determinant_value

    def inverse(self) -> 'Matrix':
        """
        計算方陣的逆矩陣
        :return: 逆矩陣
        """
        if not self.is_square():
            logger.error("逆矩陣計算失敗: 非方陣")
            raise ValueError("只有方陣才能計算逆矩陣。")
        if self.determinant() == 0:
            logger.error("逆矩陣計算失敗: 奇異矩陣")
            raise ValueError("此矩陣是奇異矩陣，無法求逆。")
        
        # 計算逆矩陣（省略詳盡實現）
        # ...

    def is_square(self) -> bool:
        """
        檢查矩陣是否為方陣
        :return: 是否為方陣
        """
        return self.rows == self.cols