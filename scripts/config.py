"""
配置加载模块
"""
import os
import yaml
from typing import Dict

def load_config(config_path: str = "config/config.yaml") -> Dict:
    """加载配置文件"""
    if not os.path.exists(config_path):
        # 尝试找示例配置
        example_path = "config/config.example.yaml"
        if os.path.exists(example_path):
            raise Exception(f"请先复制 {example_path} 为 {config_path} 并填入您的API密钥")
        else:
            raise Exception(f"配置文件 {config_path} 不存在")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    if not config.get("api_key"):
        raise Exception("请在配置文件中填写您的火山方舟API_KEY")
    
    return config
