import logging
import os

def setup_logger(name, log_file=None, level=logging.INFO):
    """
    設置並返回一個日誌記錄器。
    
    Args:
        name (str): 日誌記錄器名稱。
        log_file (str, optional): 日誌輸出檔案，若為 None，則僅輸出到控制台。
        level (int): 日誌等級，例如 logging.DEBUG、logging.INFO。
    
    Returns:
        logging.Logger: 配置完成的日誌記錄器。
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # 防止重複添加處理器
    if not logger.handlers:
        # 格式化
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # 控制台處理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # 檔案處理器（可選）
        if log_file:
            file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    return logger
