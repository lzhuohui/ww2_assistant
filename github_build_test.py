#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Actions构建测试脚本
用于模拟GitHub Actions环境中的构建过程
"""

import os
import sys
import subprocess
import json

def run_command(cmd, cwd=None):
    """运行命令并返回结果"""
    print(f"执行命令: {cmd}")
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            cwd=cwd,
            capture_output=True, 
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        print(f"返回码: {result.returncode}")
        if result.stdout:
            print(f"标准输出:\n{result.stdout}")
        if result.stderr:
            print(f"标准错误:\n{result.stderr}")
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        print(f"执行命令出错: {e}")
        return -1, "", str(e)

def test_build_environment():
    """测试构建环境"""
    print("=" * 60)
    print("测试构建环境...")
    print("=" * 60)
    
    # 检查Python版本
    print("\n1. 检查Python环境:")
    run_command("python --version")
    run_command("python -m pip --version")
    
    # 检查Flutter
    print("\n2. 检查Flutter环境:")
    run_command("flutter --version")
    
    # 检查Flet
    print("\n3. 检查Flet安装:")
    run_command("python -c \"import flet; print(f'Flet版本: {flet.__version__}')\"")
    
    # 检查项目结构
    print("\n4. 检查项目结构:")
    run_command("dir" if sys.platform == "win32" else "ls -la")
    
    return True

def validate_pubspec_yaml():
    """验证pubspec.yaml文件"""
    print("\n" + "=" * 60)
    print("验证pubspec.yaml文件...")
    print("=" * 60)
    
    pubspec_path = os.path.join("build", "flutter", "pubspec.yaml")
    if os.path.exists(pubspec_path):
        print(f"找到pubspec.yaml文件: {pubspec_path}")
        # 检查文件内容
        with open(pubspec_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"文件大小: {len(content)} 字符")
            
            # 检查关键字段
            required_fields = ['name:', 'version:', 'dependencies:']
            missing_fields = []
            for field in required_fields:
                if field not in content:
                    missing_fields.append(field)
            
            if missing_fields:
                print(f"警告: 缺少以下字段: {missing_fields}")
            else:
                print("pubspec.yaml基本结构正常")
                
            # 检查name字段位置
            lines = content.split('\n')
            for i, line in enumerate(lines[:10]):  # 只检查前10行
                if line.strip().startswith('name:'):
                    print(f"name字段在第 {i+1} 行: {line.strip()}")
                    break
            else:
                print("警告: 在前10行未找到name字段")
    else:
        print(f"警告: 未找到pubspec.yaml文件: {pubspec_path}")
        print("这可能在构建过程中生成")
    
    return True

def test_apk_build():
    """测试APK构建"""
    print("\n" + "=" * 60)
    print("测试APK构建...")
    print("=" * 60)
    
    # 设置环境变量
    env = os.environ.copy()
    env['FLET_CLI_NO_RICH_OUTPUT'] = '1'
    env['PYTHONIOENCODING'] = 'utf-8'
    
    # 清理之前的构建
    print("清理之前的构建...")
    if os.path.exists("build"):
        run_command("rmdir /s /q build" if sys.platform == "win32" else "rm -rf build")
    
    # 尝试构建
    print("\n尝试构建APK...")
    build_cmd = "python -m flet.cli build apk --verbose"
    returncode, stdout, stderr = run_command(build_cmd)
    
    if returncode == 0:
        print("\n构建成功！")
        # 检查生成的APK
        apk_dir = os.path.join("build", "apk")
        if os.path.exists(apk_dir):
            print(f"APK目录内容:")
            run_command("dir" if sys.platform == "win32" else f"ls -la {apk_dir}")
        else:
            print("警告: build/apk目录不存在")
    else:
        print("\n构建失败！")
        print("可能的问题:")
        print("1. Flutter环境未正确配置")
        print("2. Android SDK未安装")
        print("3. pubspec.yaml格式错误")
        print("4. 依赖项问题")
    
    return returncode == 0

def main():
    """主函数"""
    print("GitHub Actions APK构建测试脚本")
    print("=" * 60)
    
    # 切换到项目目录
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    print(f"工作目录: {project_dir}")
    
    # 测试环境
    test_build_environment()
    
    # 验证pubspec.yaml
    validate_pubspec_yaml()
    
    # 测试构建
    success = test_apk_build()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ 测试完成 - APK构建应该可以在GitHub Actions中正常工作")
    else:
        print("❌ 测试失败 - 需要修复问题才能在GitHub Actions中构建")
        print("\n建议:")
        print("1. 检查Flutter和Android SDK配置")
        print("2. 确保pubspec.yaml格式正确")
        print("3. 检查所有依赖项是否正确安装")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())