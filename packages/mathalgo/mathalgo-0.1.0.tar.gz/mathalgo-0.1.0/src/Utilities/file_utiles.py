import os

def read_file(file_path):
    """讀取檔案內容，返回為字串。"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"檔案未找到: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_file(file_path, content):
    """將內容寫入檔案。"""
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
