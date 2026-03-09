import flet as ft
import sys
from pathlib import Path

# 添加正确的路径
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "windows11_v2"))

from 原子层.界面配置 import 界面配置
from 组件层.下拉框设置卡片 import 下拉框设置卡片

def main(page: ft.Page):
    page.title = "测试下拉框设置卡片"
    page.padding = 20
    page.bgcolor = "#1C1C1C"
    
    配置 = 界面配置()
    
    # 测试下拉框设置卡片
    卡片1 = 下拉框设置卡片.创建(
        配置=配置,
        标题="测试卡片1",
        描述="这是一个测试卡片",
        icon="POWER_BUTTON",
        options=["选项1", "选项2", "选项3"],
        value="选项1"
    )
    
    卡片2 = 下拉框设置卡片.创建(
        配置=配置,
        标题="测试卡片2",
        描述="这是另一个测试卡片",
        icon="SPEED_HIGH",
        options=["A", "B", "C"],