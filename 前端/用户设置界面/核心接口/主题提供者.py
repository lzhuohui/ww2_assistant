# -*- coding: utf-8 -*-
"""
主题提供者 - 核心接口

设计思路:
    提供主题相关的统一访问接口，负责颜色和尺寸的管理。

功能:
    1. 颜色管理：获取主题颜色
    2. 尺寸管理：获取主题尺寸
    3. 主题初始化：加载主题配置

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    被界面层、组件层、单元层调用。

可独立运行调试: python 主题提供者.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from 前端.配置.界面配置 import 界面配置


class ThemeProvider:
    """主题提供者 - 核心接口"""
    
    _instance = None
    _config = None
    
    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super(ThemeProvider, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def initialize(cls, config: 界面配置):
        """
        初始化主题提供者
        
        参数:
            config: 界面配置对象
        """
        cls._config = config
    
    @classmethod
    def get_color(cls, color_key: str) -> str:
        """
        获取主题颜色
        
        参数:
            color_key: 颜色键名
        
        返回:
            str: 颜色值
        """
        if not cls._config:
            cls._config = 界面配置()
        
        theme_colors = cls._config.当前主题颜色
        return theme_colors.get(color_key, "#000000")
    
    @classmethod
    def get_size(cls, category: str, size_key: str) -> int:
        """
        获取主题尺寸
        
        参数:
            category: 尺寸类别
            size_key: 尺寸键名
        
        返回:
            int: 尺寸值
        """
        if not cls._config:
            cls._config = 界面配置()
        
        sizes = cls._config.定义尺寸.get(category, {})
        return sizes.get(size_key, 0)
    
    @classmethod
    def get_theme(cls) -> dict:
        """
        获取当前主题配置
        
        返回:
            dict: 主题配置
        """
        if not cls._config:
            cls._config = 界面配置()
        
        return {
            "colors": cls._config.当前主题颜色,
            "sizes": cls._config.定义尺寸,
        }


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    # 1. 界面配置初始化
    配置 = 界面配置()
    
    # 2. 初始化主题提供者
    ThemeProvider.initialize(配置)
    
    # 3. 测试获取颜色
    print("=== 测试获取颜色 ===")
    print(f"获取颜色 'text_primary': {ThemeProvider.get_color('text_primary')}")
    print(f"获取颜色 'bg_primary': {ThemeProvider.get_color('bg_primary')}")
    print(f"获取颜色 'accent': {ThemeProvider.get_color('accent')}")
    
    # 4. 测试获取尺寸
    print("\n=== 测试获取尺寸 ===")
    print(f"获取尺寸 '字体.font_size_md': {ThemeProvider.get_size('字体', 'font_size_md')}")
    print(f"获取尺寸 '间距.spacing_md': {ThemeProvider.get_size('间距', 'spacing_md')}")
    print(f"获取尺寸 '圆角.radius_md': {ThemeProvider.get_size('圆角', 'radius_md')}")
    
    # 5. 测试获取主题
    print("\n=== 测试获取主题 ===")
    theme = ThemeProvider.get_theme()
    print(f"主题颜色数量: {len(theme['colors'])}")
    print(f"主题尺寸类别: {list(theme['sizes'].keys())}")
