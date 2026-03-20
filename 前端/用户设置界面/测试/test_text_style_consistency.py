# -*- coding: utf-8 -*-
"""
文字样式一致性测试脚本

功能：
    1. 测试主题提供者的文本样式管理功能
    2. 测试文本标签组件的样式一致性
    3. 验证Win11风格文本样式的正确性
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.用户设置界面.单元模块.文本标签 import LabelText
from 前端.用户设置界面.配置.界面配置 import 界面配置


def test_text_style_consistency():
    """测试文本样式一致性"""
    print("=" * 60)
    print("开始测试文本样式一致性")
    print("=" * 60)
    
    # 初始化主题提供者
    配置 = 界面配置()
    ThemeProvider.initialize(配置)
    
    # 测试1：测试默认文本样式
    print("\n测试1：测试默认文本样式")
    default_style = ThemeProvider.get_default_text_style()
    print(f"默认文本样式: {default_style}")
    assert default_style["font_family"] == "Segoe UI Variable, Segoe UI, sans-serif", "默认字体不正确"
    assert default_style["size"] == 14, "默认字体大小不正确"
    assert default_style["weight"] == ft.FontWeight.W_400, "默认字重不正确"
    print("✓ 默认文本样式测试通过")
    
    # 测试2：测试Win11风格文本样式
    print("\n测试2：测试Win11风格文本样式")
    roles = ["h1", "h2", "h3", "body", "caption", "small"]
    for role in roles:
        style = ThemeProvider.get_win11_text_style(role)
        print(f"{role}: size={style['size']}, weight={style['weight']}, color={style['color']}")
        
        # 验证样式一致性
        assert style["font_family"] == "Segoe UI Variable, Segoe UI, sans-serif", f"{role} 字体不正确"
        assert "size" in style, f"{role} 缺少size属性"
        assert "weight" in style, f"{role} 缺少weight属性"
        assert "color" in style, f"{role} 缺少color属性"
    
    print("✓ Win11风格文本样式测试通过")
    
    # 测试3：测试样式合并功能
    print("\n测试3：测试样式合并功能")
    custom_style = {
        "size": 18,
        "weight": ft.FontWeight.W_600,
    }
    merged_style = ThemeProvider.merge_text_style(custom_style)
    print(f"合并后的样式: {merged_style}")
    assert merged_style["size"] == 18, "合并后的字体大小不正确"
    assert merged_style["weight"] == ft.FontWeight.W_600, "合并后的字重不正确"
    assert merged_style["font_family"] == "Segoe UI Variable, Segoe UI, sans-serif", "合并后的字体不正确"
    print("✓ 样式合并功能测试通过")
    
    # 测试4：测试文本标签组件
    print("\n测试4：测试文本标签组件")
    text = LabelText.create(
        text="测试文本",
        role="body",
        win11_style=True
    )
    print(f"文本标签: value={text.value}, size={text.size}, weight={text.weight}, color={text.color}")
    assert text.value == "测试文本", "文本内容不正确"
    assert text.size == 14, "文本大小不正确"
    assert text.weight == ft.FontWeight.W_400, "文本字重不正确"
    assert text.font_family == "Segoe UI Variable, Segoe UI, sans-serif", "文本字体不正确"
    print("✓ 文本标签组件测试通过")
    
    # 测试5：测试不同角色的文本标签
    print("\n测试5：测试不同角色的文本标签")
    roles = ["h1", "h2", "h3", "body", "caption", "small"]
    for role in roles:
        text = LabelText.create(
            text=f"这是{role}角色的文本",
            role=role,
            win11_style=True
        )
        style = ThemeProvider.get_win11_text_style(role)
        
        # 验证样式一致性
        assert text.size == style["size"], f"{role} size mismatch"
        assert text.weight == style["weight"], f"{role} weight mismatch"
        assert text.color == style["color"], f"{role} color mismatch"
        assert text.font_family == style["font_family"], f"{role} font_family mismatch"
        print(f"✓ {role}角色文本标签测试通过")
    
    print("\n" + "=" * 60)
    print("所有文本样式一致性测试通过！")
    print("=" * 60)


if __name__ == "__main__":
    test_text_style_consistency()