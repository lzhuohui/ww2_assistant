#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trae IDE测试联动工具

功能：
1. 自动识别选中文件的测试模块
2. 智能匹配对应的测试用例
3. 执行测试并生成报告
4. 实时展示测试结果

创建日期: 2026-03-08
作者: AI
版本: v1.0.0
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path
from typing import List, Optional, Dict, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TestConfig:
    """测试配置"""
    test_dir: str = "测试"
    unit_test_dir: str = "测试/单元测试"
    integration_test_dir: str = "测试/集成测试"
    report_dir: str = "测试/报告"
    coverage_threshold: float = 60.0


class TestLinker:
    """测试联动器"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.config = TestConfig()
        self.test_mapping = self._build_test_mapping()
    
    def _build_test_mapping(self) -> Dict[str, List[str]]:
        """构建文件到测试的映射关系"""
        mapping = {}
        
        # 扫描单元测试目录
        unit_test_dir = self.project_root / self.config.unit_test_dir
        if unit_test_dir.exists():
            for test_file in unit_test_dir.glob("test_*.py"):
                # 解析测试文件对应的目标模块
                target_module = self._extract_target_module(test_file)
                if target_module:
                    mapping[target_module] = [str(test_file)]
        
        return mapping
    
    def _extract_target_module(self, test_file: Path) -> Optional[str]:
        """从测试文件名提取目标模块"""
        # test_配置服务.py -> 配置服务
        name = test_file.stem.replace("test_", "")
        return name
    
    def find_related_tests(self, file_path: str) -> List[str]:
        """查找与文件相关的测试"""
        file_path = Path(file_path)
        related_tests = []
        
        # 如果是测试文件，直接返回
        if file_path.name.startswith("test_"):
            return [str(file_path)]
        
        # 根据文件名查找对应的测试
        module_name = file_path.stem
        
        # 查找单元测试
        unit_test = self.project_root / self.config.unit_test_dir / f"test_{module_name}.py"
        if unit_test.exists():
            related_tests.append(str(unit_test))
        
        # 查找集成测试
        integration_test = self.project_root / self.config.integration_test_dir / f"test_{module_name}.py"
        if integration_test.exists():
            related_tests.append(str(integration_test))
        
        return related_tests
    
    def run_tests(self, test_files: List[str], verbose: bool = True, coverage: bool = False) -> Tuple[bool, str]:
        """运行测试"""
        if not test_files:
            return False, "未找到相关测试文件"
        
        # 构建pytest命令
        cmd = [
            sys.executable,
            "-m",
            "pytest"
        ]
        
        # 添加测试文件
        cmd.extend(test_files)
        
        # 添加参数
        cmd.extend([
            "-v",
            "--tb=short",
            "--color=yes",
            "--strict-markers"
        ])
        
        # 添加覆盖率
        if coverage:
            cmd.extend([
                "--cov=前端",
                f"--cov-report=html:{self.config.report_dir}/htmlcov",
                "--cov-report=term"
            ])
        
        # 添加HTML报告
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"{self.config.report_dir}/report_{timestamp}.html"
        cmd.extend([f"--html={report_file}"])
        
        # 执行测试
        try:
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace'
            )
            
            success = result.returncode == 0
            stdout = result.stdout if result.stdout else ""
            stderr = result.stderr if result.stderr else ""
            output = stdout + "\n" + stderr
            
            return success, output
            
        except Exception as e:
            return False, f"测试执行失败: {str(e)}"
    
    def run_all_tests(self, coverage: bool = True) -> Tuple[bool, str]:
        """运行全部测试"""
        cmd = [
            sys.executable,
            "-m",
            "pytest",
            self.config.test_dir,
            "-v",
            "--tb=short",
            "--color=yes"
        ]
        
        if coverage:
            cmd.extend([
                "--cov=前端",
                f"--cov-report=html:{self.config.report_dir}/htmlcov",
                "--cov-report=xml:{self.config.report_dir}/coverage.xml",
                "--cov-report=term"
            ])
        
        # 添加HTML报告
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"{self.config.report_dir}/report_{timestamp}.html"
        cmd.extend([f"--html={report_file}"])
        
        try:
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace'
            )
            
            success = result.returncode == 0
            stdout = result.stdout if result.stdout else ""
            stderr = result.stderr if result.stderr else ""
            output = stdout + "\n" + stderr
            
            return success, output
            
        except Exception as e:
            return False, f"测试执行失败: {str(e)}"
    
    def get_test_summary(self) -> Dict:
        """获取测试摘要"""
        summary = {
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "coverage": 0.0
        }
        
        # 这里可以解析测试结果文件获取详细统计
        
        return summary


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Trae IDE测试联动工具")
    parser.add_argument("--file", "-f", help="选中的文件路径")
    parser.add_argument("--all", "-a", action="store_true", help="运行全部测试")
    parser.add_argument("--coverage", "-c", action="store_true", help="生成覆盖率报告")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    
    args = parser.parse_args()
    
    # 获取项目根目录
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent.parent
    
    # 创建测试联动器
    linker = TestLinker(str(project_root))
    
    if args.all:
        # 运行全部测试
        print("🧪 运行全部测试...")
        success, output = linker.run_all_tests(coverage=args.coverage)
    elif args.file:
        # 查找相关测试
        print(f"🔍 查找与 {args.file} 相关的测试...")
        related_tests = linker.find_related_tests(args.file)
        
        if related_tests:
            print(f"✅ 找到 {len(related_tests)} 个相关测试文件:")
            for test in related_tests:
                print(f"   - {test}")
            
            print("\n🧪 运行测试...")
            success, output = linker.run_tests(related_tests, verbose=args.verbose, coverage=args.coverage)
        else:
            print(f"⚠️ 未找到与 {args.file} 相关的测试文件")
            print("📝 尝试运行全部测试...")
            success, output = linker.run_all_tests(coverage=args.coverage)
    else:
        print("❌ 请指定文件路径 (--file) 或使用 --all 运行全部测试")
        return 1
    
    # 输出结果
    print("\n" + "="*60)
    print("测试结果")
    print("="*60)
    print(output)
    print("="*60)
    
    if success:
        print("✅ 测试通过！")
        return 0
    else:
        print("❌ 测试失败！")
        return 1


if __name__ == "__main__":
    sys.exit(main())
