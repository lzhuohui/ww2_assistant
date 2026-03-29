# -*- coding: utf-8 -*-
"""
模块名称：卡片容器验证

设计思路及联动逻辑:
    验证卡片容器模块的合规性和基本功能，不运行UI界面。
    1. 导入卡片容器模块
    2. 验证模块结构合规性
    3. 测试create方法的基本功能
    4. 验证异常处理机制

模块隔离原则:
    1. 不直接创建被调用模块的内容
    2. 不覆盖被调用模块的计算结果
    3. 通过公开接口访问模块
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
# （用户未指定变量）
# *********************************


def 验证模块结构():
    """验证模块结构合规性"""
    print("=== 验证模块结构 ===")
    try:
        from 前端.用户设置界面.单元模块.卡片容器 import 卡片容器
        print("✅ 模块导入成功")
        
        # 验证create方法存在
        if hasattr(卡片容器, 'create'):
            print("✅ create方法存在")
        else:
            print("❌ create方法不存在")
        
        return True
    except Exception as e:
        print(f"❌ 模块结构验证失败: {e}")
        return False


def 验证基本功能():
    """验证基本功能"""
    print("\n=== 验证基本功能 ===")
    try:
        from 前端.用户设置界面.单元模块.卡片容器 import 卡片容器
        
        # 测试默认参数
        容器1 = 卡片容器.create()
        print("✅ 默认参数创建成功")
        
        # 测试自定义参数
        容器2 = 卡片容器.create(
            width=300,
            height=200,
            title="测试标题",
            subtitle="测试副标题",
            icon="HOME"
        )
        print("✅ 自定义参数创建成功")
        
        # 测试点击事件
        def on_click():
            pass
        
        容器3 = 卡片容器.create(
            title="带点击事件",
            on_click=on_click
        )
        print("✅ 点击事件创建成功")
        
        # 测试禁用状态
        容器4 = 卡片容器.create(
            title="禁用状态",
            enabled=False
        )
        print("✅ 禁用状态创建成功")
        
        return True
    except Exception as e:
        print(f"❌ 基本功能验证失败: {e}")
        return False


def 验证异常处理():
    """验证异常处理机制"""
    print("\n=== 验证异常处理 ===")
    try:
        from 前端.用户设置界面.单元模块.卡片容器 import 卡片容器
        
        # 测试无效参数
        容器 = 卡片容器.create(
            width="无效值",  # 应该是数值
            height=200
        )
        print("✅ 无效参数处理成功")
        
        return True
    except Exception as e:
        print(f"❌ 异常处理验证失败: {e}")
        return False


def 验证规则合规性():
    """验证规则合规性"""
    print("\n=== 验证规则合规性 ===")
    try:
        # 运行规则检查工具
        import subprocess
        result = subprocess.run([
            sys.executable,
            str(Path(__file__).parent.parent / ".trae" / "tools" / "rule_checker.py"),
            str(Path(__file__).parent.parent / "前端" / "用户设置界面" / "单元模块" / "卡片容器.py")
        ], capture_output=True, text=True)
        
        print("规则检查结果:")
        print(result.stdout)
        if result.stderr:
            print("错误:")
            print(result.stderr)
        
        return "所有检查通过" in result.stdout
    except Exception as e:
        print(f"❌ 规则合规性验证失败: {e}")
        return False


def 主验证():
    """主验证函数"""
    print("开始验证卡片容器模块...\n")
    
    验证结果 = []
    验证结果.append(验证模块结构())
    验证结果.append(验证基本功能())
    验证结果.append(验证异常处理())
    验证结果.append(验证规则合规性())
    
    print("\n=== 验证总结 ===")
    成功数 = sum(验证结果)
    总验证数 = len(验证结果)
    成功率 = (成功数 / 总验证数) * 100
    
    print(f"验证项目: {总验证数}")
    print(f"成功项目: {成功数}")
    print(f"成功率: {成功率:.1f}%")
    
    if 成功率 == 100:
        print("🎉 所有验证通过！卡片容器模块完全符合规则要求。")
    else:
        print("⚠️  部分验证失败，需要进一步优化。")
    
    return 成功率 == 100


# *** 调试逻辑 ***
if __name__ == "__main__":
    主验证()