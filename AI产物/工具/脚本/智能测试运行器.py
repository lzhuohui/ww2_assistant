#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能测试运行器

功能：
1. 监听文件变化自动运行测试
2. 智能识别修改的模块
3. 增量测试执行
4. 实时结果反馈

创建日期: 2026-03-08
作者: AI
版本: v1.0.0
"""

import os
import sys
import time
import subprocess
import argparse
from pathlib import Path
from typing import Set, List
from datetime import datetime


class SmartTestRunner:
    """智能测试运行器"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.test_dir = self.project_root / "测试"
        self.last_run_time = 0
        self.cooldown = 2  # 冷却时间（秒）
    
    def get_modified_files(self, since: float = None) -> Set[Path]:
        """获取修改的文件"""
        if since is None:
            since = self.last_run_time
        
        modified = set()
        
        # 扫描项目文件
        for py_file in self.project_root.rglob("*.py"):
            # 排除测试报告和缓存
            if any(exclude in str(py_file) for exclude in [
                "__pycache__", ".pytest_cache", "htmlcov", 
                "venv", ".git"
            ]):
                continue
            
            try:
                mtime = py_file.stat().st_mtime
                if mtime > since:
                    modified.add(py_file)
            except Exception:
                continue
        
        return modified
    
    def find_affected_tests(self, modified_files: Set[Path]) -> Set[Path]:
        """查找受影响的测试"""
        affected_tests = set()
        
        for file in modified_files:
            # 如果是测试文件，直接添加
            if file.name.startswith("test_"):
                affected_tests.add(file)
                continue
            
            # 查找对应的测试文件
            module_name = file.stem
            
            # 单元测试
            unit_test = self.test_dir / "单元测试" / f"test_{module_name}.py"
            if unit_test.exists():
                affected_tests.add(unit_test)
            
            # 集成测试
            integration_test = self.test_dir / "集成测试" / f"test_{module_name}.py"
            if integration_test.exists():
                affected_tests.add(integration_test)
        
        return affected_tests
    
    def run_tests(self, test_files: List[Path], verbose: bool = True) -> bool:
        """运行测试"""
        if not test_files:
            print("⚠️ 没有找到需要运行的测试")
            return True
        
        # 构建命令
        cmd = [
            sys.executable,
            "-m",
            "pytest"
        ]
        
        cmd.extend([str(f) for f in test_files])
        cmd.extend([
            "-v",
            "--tb=short",
            "--color=yes"
        ])
        
        print(f"\n{'='*60}")
        print(f"🧪 运行 {len(test_files)} 个测试文件")
        print(f"{'='*60}")
        for f in test_files:
            print(f"   📄 {f.name}")
        print(f"{'='*60}\n")
        
        # 执行测试
        try:
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=False,
                text=True,
                encoding='utf-8'
            )
            
            return result.returncode == 0
            
        except Exception as e:
            print(f"❌ 测试执行失败: {e}")
            return False
    
    def watch_and_run(self, interval: float = 1.0):
        """监听文件变化并运行测试"""
        print("👀 开始监听文件变化...")
        print(f"   项目目录: {self.project_root}")
        print(f"   检查间隔: {interval}秒")
        print(f"   按 Ctrl+C 停止\n")
        
        self.last_run_time = time.time()
        
        try:
            while True:
                time.sleep(interval)
                
                # 检查冷却时间
                current_time = time.time()
                if current_time - self.last_run_time < self.cooldown:
                    continue
                
                # 获取修改的文件
                modified = self.get_modified_files()
                
                if modified:
                    print(f"\n📝 检测到 {len(modified)} 个文件修改:")
                    for f in list(modified)[:5]:  # 最多显示5个
                        print(f"   - {f.relative_to(self.project_root)}")
                    if len(modified) > 5:
                        print(f"   ... 还有 {len(modified) - 5} 个文件")
                    
                    # 查找受影响的测试
                    affected_tests = self.find_affected_tests(modified)
                    
                    if affected_tests:
                        # 运行测试
                        success = self.run_tests(list(affected_tests))
                        
                        if success:
                            print("\n✅ 测试通过！")
                        else:
                            print("\n❌ 测试失败！")
                    else:
                        print("\n⚠️ 没有找到相关的测试文件")
                    
                    self.last_run_time = time.time()
                    
        except KeyboardInterrupt:
            print("\n\n👋 停止监听")
    
    def run_single_file(self, file_path: str):
        """运行单个文件的测试"""
        file = Path(file_path)
        
        if not file.exists():
            print(f"❌ 文件不存在: {file_path}")
            return False
        
        # 如果是普通Python文件，查找对应的测试
        if not file.name.startswith("test_"):
            affected = self.find_affected_tests({file})
            if affected:
                return self.run_tests(list(affected))
            else:
                print(f"⚠️ 未找到 {file.name} 的测试文件")
                return False
        else:
            # 直接运行测试文件
            return self.run_tests([file])


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="智能测试运行器")
    parser.add_argument("--watch", "-w", action="store_true", help="监听模式")
    parser.add_argument("--file", "-f", help="运行指定文件的测试")
    parser.add_argument("--interval", "-i", type=float, default=1.0, help="监听间隔（秒）")
    
    args = parser.parse_args()
    
    # 获取项目根目录
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent.parent
    
    # 创建运行器
    runner = SmartTestRunner(str(project_root))
    
    if args.watch:
        # 监听模式
        runner.watch_and_run(interval=args.interval)
    elif args.file:
        # 运行单个文件
        success = runner.run_single_file(args.file)
        sys.exit(0 if success else 1)
    else:
        print("用法:")
        print("  监听模式: python 智能测试运行器.py --watch")
        print("  运行文件: python 智能测试运行器.py --file <文件路径>")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
