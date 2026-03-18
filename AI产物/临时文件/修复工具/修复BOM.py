#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复BOM字符脚本
用于修复文件开头的U+FEFF字符（BOM）
支持多种编码格式
"""

import os
import sys
from pathlib import Path

def fix_bom_in_file(file_path):
    """修复单个文件的BOM字符"""
    try:
        # 先以二进制模式读取
        with open(file_path, 'rb') as f:
            content = f.read()
        
        original_content = content
        encoding = None
        need_fix = False
        
        # 检查各种BOM
        if content.startswith(b'\xef\xbb\xbf'):
            # UTF-8 BOM
            content = content[3:]
            encoding = 'utf-8'
            need_fix = True
            print(f"发现UTF-8 BOM: {file_path}")
        elif content.startswith(b'\xff\xfe'):
            # UTF-16 LE BOM
            content = content[2:]
            try:
                text = content.decode('utf-16-le')
                encoding = 'utf-16-le'
                need_fix = True
                print(f"发现UTF-16 LE BOM: {file_path}")
            except:
                pass
        elif content.startswith(b'\xfe\xff'):
            # UTF-16 BE BOM
            content = content[2:]
            try:
                text = content.decode('utf-16-be')
                encoding = 'utf-16-be'
                need_fix = True
                print(f"发现UTF-16 BE BOM: {file_path}")
            except:
                pass
        
        if need_fix:
            # 写入修复后的内容
            if encoding and encoding != 'utf-8':
                # 如果是UTF-16编码，需要先解码再以UTF-8编码写入
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(text)
            else:
                # UTF-8 BOM，直接写入移除BOM后的内容
                with open(file_path, 'wb') as f:
                    f.write(content)
            return True
        
        # 检查文件内容是否以UTF-8编码且没有BOM
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            # 检查文本开头是否有U+FEFF字符
            if text.startswith('\ufeff'):
                print(f"发现文本BOM字符: {file_path}")
                text = text[1:]  # 移除BOM字符
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                return True
        except UnicodeDecodeError:
            # 如果UTF-8解码失败，尝试其他编码
            pass
        
        return False
    except Exception as e:
        print(f"错误处理文件 {file_path}: {e}")
        import traceback
        traceback.print_exc()
        return False

def scan_and_fix_bom(directory):
    """扫描目录并修复所有Python文件的BOM字符"""
    fixed_count = 0
    total_count = 0
    fixed_files = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                total_count += 1
                if fix_bom_in_file(file_path):
                    fixed_count += 1
                    fixed_files.append(file_path)
    
    return fixed_count, total_count, fixed_files

def main():
    """主函数"""
    # 扫描用户设置界面目录
    target_dir = os.path.dirname(__file__)
    
    print("=" * 60)
    print("开始扫描并修复BOM字符...")
    print(f"目标目录: {target_dir}")
    print("=" * 60)
    
    fixed, total, fixed_files = scan_and_fix_bom(target_dir)
    
    print("=" * 60)
    print(f"扫描完成!")
    print(f"总文件数: {total}")
    print(f"修复文件数: {fixed}")
    
    if fixed_files:
        print("\n已修复的文件:")
        for f in fixed_files:
            print(f"  ✓ {f}")
    
    # 验证修复结果
    print("\n验证修复结果...")
    still_has_bom = []
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text = f.read()
                    if text.startswith('\ufeff'):
                        still_has_bom.append(file_path)
                except:
                    pass
    
    if still_has_bom:
        print("\n⚠️ 仍有BOM字符的文件:")
        for f in still_has_bom:
            print(f"  ✗ {f}")
    else:
        print("✓ 所有文件BOM字符已清除!")

if __name__ == "__main__":
    main()