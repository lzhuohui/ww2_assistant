import flet as ft
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "windows11_v2"))

from 原子层.界面配置 import 界面配置
from 组件层.下拉框设置卡片 import 下拉框设置卡片

def main(page: ft.Page):
    配置 = 界面配置()
    page.title = "测试卡片颜色"
    page.padding = 20
    page.bgcolor = 配置.获取颜色("bg_primary")
    
    print(f"页面背景色: {page.bgcolor}")
    print(f"卡片背景色: {配置.获取颜色('bg_card')}")
    
    卡片 = 下拉框设置卡片.创建(
        配置=配置, 
        标题="测试卡片", 
        描述="测试描述",
        图标="POWER_BUTTON",
        options=["选项1", "选项2", "选项3"],
        value="选项1"
    )
    
    print(f"卡片bgcolor: {卡片.bgcolor}")
    
    page.add(
        ft.Column([
            ft.Text("测试卡片颜色", size=20, color="white"),
            ft.Divider(height=20, color="transparent"),
            卡片,
        ])
    )

if __name__ == "__main__":
    ft.run(main)