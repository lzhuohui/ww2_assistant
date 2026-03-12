# -*- coding: utf-8 -*-
"""
违规检查脚本 - 自动检测模块化设计违规

功能：
    1. 检查是否修改了零件层核心模块
    2. 检查是否重新定义了被调用模块的默认值
    3. 检查是否干预了被调用模块的内部布局
    4. 生成检查报告

使用方法：
    python 违规检查.py
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Tuple


class ViolationChecker:
    """违规检查器"""
    
    # 零件层核心模块（禁止修改）
    FORBIDDEN_MODULES = [
        "自定义下拉框.py",
        "帮助标签.py",
        "分割线.py",
        "卡片容器.py",
    ]
    
    # 组合零件（只调用不覆盖）
    COMBINATION_MODULES = {
        "图标标题.py": ["帮助标签", "分割线"],
        "标签下拉框.py": ["自定义下拉框"],
        "标签输入框.py": [],
    }
    
    # 组件层（只装配不干预）
    ASSEMBLY_MODULES = {
        "通用卡片.py": ["图标标题"],
        "基础设置卡片.py": ["通用卡片"],
        "开关下拉卡片.py": ["通用卡片"],
    }
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.violations: List[Dict] = []
        self.warnings: List[Dict] = []
    
    def check_all(self):
        """执行所有检查"""
        print("=" * 60)
        print("开始执行违规检查...")
        print("=" * 60)
        
        # 检查零件层
        self._check_parts_layer()
        
        # 检查组合零件
        self._check_combination_modules()
        
        # 检查组件层
        self._check_assembly_modules()
        
        # 生成报告
        self._generate_report()
    
    def _check_parts_layer(self):
        """检查零件层核心模块"""
        print("\n【检查1】零件层核心模块修改检查")
        print("-" * 60)
        
        parts_path = self.base_path / "零件层"
        if not parts_path.exists():
            print(f"⚠️  路径不存在: {parts_path}")
            return
        
        for module_name in self.FORBIDDEN_MODULES:
            module_path = parts_path / module_name
            if module_path.exists():
                print(f"✅ 找到模块: {module_name}")
                # 检查是否有修改记录（这里可以扩展为检查git diff等）
            else:
                print(f"⚠️  模块不存在: {module_name}")
    
    def _check_combination_modules(self):
        """检查组合零件"""
        print("\n【检查2】组合零件默认值覆盖检查")
        print("-" * 60)
        
        parts_path = self.base_path / "零件层"
        if not parts_path.exists():
            return
        
        for module_name, dependencies in self.COMBINATION_MODULES.items():
            module_path = parts_path / module_name
            if not module_path.exists():
                continue
            
            print(f"\n检查模块: {module_name}")
            
            with open(module_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否重新定义了被调用模块的默认值（从配置文件获取）
            # 注意：如果模块自己定义默认值（如width=width if width is not None else 120），这是允许的
            patterns = [
                r'ui_config\s*=\s*config\.定义尺寸\.get\(["\']组件["\']',
                r'default_width\s*=\s*ui_config\.get\(',
                r'default_height\s*=\s*ui_config\.get\(',
                r'current_width\s*=\s*width\s*if\s*width\s*is\s*not\s*None\s*else\s*default_width',
                r'current_height\s*=\s*height\s*if\s*height\s*is\s*not\s*None\s*else\s*default_height',
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, content)
                if matches:
                    self.violations.append({
                        'type': '从配置文件重新定义默认值',
                        'module': module_name,
                        'content': matches,
                        'pattern': pattern,
                    })
                    print(f"  ❌ 发现违规: 从配置文件重新定义默认值")
                    print(f"     内容: {matches}")
    
    def _check_assembly_modules(self):
        """检查组件层"""
        print("\n【检查3】组件层布局干预检查")
        print("-" * 60)
        
        assembly_path = self.base_path / "组件层"
        if not assembly_path.exists():
            return
        
        for module_name, dependencies in self.ASSEMBLY_MODULES.items():
            module_path = assembly_path / module_name
            if not module_path.exists():
                continue
            
            print(f"\n检查模块: {module_name}")
            
            with open(module_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否干预了被调用模块的布局
            patterns = [
                r'alignment\s*=\s*ft\.Alignment\(',
                r'top\s*=\s*0,\s*bottom\s*=\s*0',
                r'left_width\s*=\s*.*\.get\(',
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, content)
                if matches:
                    self.warnings.append({
                        'type': '可能干预布局',
                        'module': module_name,
                        'content': matches,
                        'pattern': pattern,
                    })
                    print(f"  ⚠️  发现警告: 可能干预布局")
                    print(f"     内容: {matches}")
    
    def _generate_report(self):
        """生成检查报告"""
        print("\n" + "=" * 60)
        print("检查报告")
        print("=" * 60)
        
        if self.violations:
            print(f"\n❌ 发现 {len(self.violations)} 个违规:")
            for i, v in enumerate(self.violations, 1):
                print(f"\n  违规 {i}:")
                print(f"    类型: {v['type']}")
                print(f"    模块: {v['module']}")
                print(f"    内容: {v['content']}")
        else:
            print("\n✅ 未发现违规")
        
        if self.warnings:
            print(f"\n⚠️  发现 {len(self.warnings)} 个警告:")
            for i, w in enumerate(self.warnings, 1):
                print(f"\n  警告 {i}:")
                print(f"    类型: {w['type']}")
                print(f"    模块: {w['module']}")
                print(f"    内容: {w['content']}")
        else:
            print("\n✅ 未发现警告")
        
        print("\n" + "=" * 60)
        print("检查完成")
        print("=" * 60)


if __name__ == "__main__":
    base_path = Path(__file__).parent
    checker = ViolationChecker(str(base_path))
    checker.check_all()
