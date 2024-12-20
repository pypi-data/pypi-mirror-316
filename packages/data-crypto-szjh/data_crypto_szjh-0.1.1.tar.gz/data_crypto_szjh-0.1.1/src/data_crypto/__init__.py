import os
from pathlib import Path
from dotenv import load_dotenv
from .encryptor import DataEncryptor
from .decryptor import DataDecryptor

def init_env():
    # 尝试多个可能的.env文件位置
    possible_env_paths = [
        Path.cwd() / '.env',  # 当前工作目录
        Path(__file__).parent.parent.parent / '.env',  # 包的根目录
        Path.home() / '.env'  # 用户主目录
    ]
    
    for env_path in possible_env_paths:
        if env_path.exists():
            load_dotenv(env_path)
            break

# 在包导入时自动初始化环境变量
init_env()

__version__ = "0.1.0" 