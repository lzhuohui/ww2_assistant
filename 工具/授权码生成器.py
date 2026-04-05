# -*- coding: utf-8 -*-

"""
模块名称：授权码生成器.py
模块功能：生成授权码的工具

职责：
- 生成基础授权码（单账号+天数）
- 生成天次数包授权码
- 批量生成
- 导出授权码列表

使用方法：
    # 基础授权（必须指定设备码）
    python 授权码生成器.py --type basic --days 30 --device ABC123DEF456
    
    # 天次数包（无需设备码）
    python 授权码生成器.py --type times --count 30
    
    # 批量生成天次数包
    python 授权码生成器.py --type times --count 30 --batch 5
"""

import argparse
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from 前端.V3.层级0_数据管理.授权管理.加密工具 import CryptoUtils


BASIC_PACKAGES = {
    "日卡": {"days": 1, "price": 3},
    "周卡": {"days": 7, "price": 18},
    "月卡": {"days": 30, "price": 50},
    "季卡": {"days": 90, "price": 120},
    "年卡": {"days": 365, "price": 300},
}

TIMES_PACKAGES = {
    "体验包": {"times": 15, "price": 25},
    "标准包": {"times": 30, "price": 45},
    "超值包": {"times": 60, "price": 80},
    "大户包": {"times": 150, "price": 180},
}


class LicenseGenerator:
    """
    授权码生成器
    
    职责：
    - 生成基础授权码
    - 生成天次数包授权码
    - 批量生成
    - 导出授权码列表
    """
    
    @staticmethod
    def generate_basic(days: int, device_id: str) -> str:
        """
        生成基础授权码（单账号+天数+设备绑定）
        
        参数:
            days: 授权天数
            device_id: 绑定设备码
        
        返回:
            授权码
        """
        license_data = {
            "type": "basic",
            "days": days,
            "device_id": device_id,
            "created_time": datetime.now().isoformat(),
        }
        
        signature = CryptoUtils.sign(json.dumps(license_data, sort_keys=True))
        license_data["signature"] = signature
        
        data = json.dumps(license_data)
        encrypted = CryptoUtils.encrypt(data)
        
        formatted = LicenseGenerator._format_code(encrypted)
        
        return formatted
    
    @staticmethod
    def generate_times(times: int) -> str:
        """
        生成天次数包授权码
        
        参数:
            times: 天次数
        
        返回:
            授权码
        """
        license_data = {
            "type": "times",
            "times": times,
            "created_time": datetime.now().isoformat(),
        }
        
        signature = CryptoUtils.sign(json.dumps(license_data, sort_keys=True))
        license_data["signature"] = signature
        
        data = json.dumps(license_data)
        encrypted = CryptoUtils.encrypt(data)
        
        formatted = LicenseGenerator._format_code(encrypted)
        
        return formatted
    
    @staticmethod
    def _format_code(encrypted: str) -> str:
        """
        格式化授权码（XXXX-XXXX-XXXX-XXXX）
        
        参数:
            encrypted: 加密后的字符串
        
        返回:
            格式化后的授权码
        """
        clean = encrypted.replace("=", "").replace("+", "-").replace("/", "_")
        
        if len(clean) < 16:
            clean = clean.ljust(16, "0")
        
        parts = []
        for i in range(4):
            start = i * 4
            end = start + 4
            part = clean[start:end].upper()
            parts.append(part)
        
        return "-".join(parts)
    
    @staticmethod
    def batch_generate_times(times: int, batch_count: int) -> list:
        """
        批量生成天次数包授权码
        
        参数:
            times: 天次数
            batch_count: 生成数量
        
        返回:
            授权码列表
        """
        licenses = []
        for _ in range(batch_count):
            code = LicenseGenerator.generate_times(times)
            licenses.append(code)
        return licenses
    
    @staticmethod
    def export_to_file(licenses: list, filename: str, license_type: str, value: int):
        """
        导出授权码到文件
        
        参数:
            licenses: 授权码列表
            filename: 文件名
            license_type: 授权类型
            value: 天数或次数
        """
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# 授权码列表\n")
            f.write(f"# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# 授权类型: {license_type}\n")
            if license_type == "basic":
                f.write(f"# 授权天数: {value}\n")
            else:
                f.write(f"# 天次数: {value}\n")
            f.write(f"# 数量: {len(licenses)}\n\n")
            for i, code in enumerate(licenses, 1):
                f.write(f"{i}. {code}\n")
        
        print(f"已导出 {len(licenses)} 个授权码到 {filename}")


def print_packages():
    """打印套餐列表"""
    print("\n" + "=" * 50)
    print("基础授权套餐（单账号+设备绑定）")
    print("=" * 50)
    for name, info in BASIC_PACKAGES.items():
        daily = round(info["price"] / info["days"], 2)
        print(f"  {name}: {info['days']}天 / {info['price']}元 (日均{daily}元)")
    
    print("\n" + "=" * 50)
    print("天次数包（多账号使用）")
    print("=" * 50)
    for name, info in TIMES_PACKAGES.items():
        daily = round(info["price"] / info["times"], 2)
        print(f"  {name}: {info['times']}次 / {info['price']}元 (日均{daily}元)")
    print("=" * 50)


def main():
    parser = argparse.ArgumentParser(description="授权码生成器", formatter_class=argparse.RawDescriptionHelpFormatter)
    
    parser.add_argument("--type", "-t", type=str, choices=["basic", "times"], required=True,
                        help="授权类型: basic(基础授权) / times(天次数包)")
    parser.add_argument("--days", "-d", type=int, default=None,
                        help="基础授权天数 (1/7/30/90/365)")
    parser.add_argument("--count", "-c", type=int, default=None,
                        help="天次数包次数 (15/30/60/150)")
    parser.add_argument("--device", type=str, default=None,
                        help="设备码（基础授权必填）")
    parser.add_argument("--batch", "-b", type=int, default=1,
                        help="批量生成数量（默认1）")
    parser.add_argument("--output", "-o", type=str, default=None,
                        help="导出文件名")
    parser.add_argument("--list", "-l", action="store_true",
                        help="显示套餐列表")
    
    args = parser.parse_args()
    
    if args.list:
        print_packages()
        return
    
    print("=" * 50)
    print("授权码生成器")
    print("=" * 50)
    
    if args.type == "basic":
        if not args.days:
            print("错误: 基础授权必须指定 --days 参数")
            print("可用天数: 1/7/30/90/365")
            return
        if not args.device:
            print("错误: 基础授权必须指定 --device 参数（设备码）")
            return
        
        print(f"授权类型: 基础授权")
        print(f"授权天数: {args.days}天")
        print(f"设备码: {args.device}")
        print(f"生成数量: {args.batch}")
        print("=" * 50)
        
        licenses = []
        for _ in range(args.batch):
            code = LicenseGenerator.generate_basic(args.days, args.device)
            licenses.append(code)
        
        print("\n生成的授权码:")
        for i, code in enumerate(licenses, 1):
            print(f"  {i}. {code}")
        
        if args.output:
            LicenseGenerator.export_to_file(licenses, args.output, "basic", args.days)
    
    elif args.type == "times":
        if not args.count:
            print("错误: 天次数包必须指定 --count 参数")
            print("可用次数: 15/30/60/150")
            return
        
        print(f"授权类型: 天次数包")
        print(f"天次数: {args.count}次")
        print(f"生成数量: {args.batch}")
        print("=" * 50)
        
        licenses = LicenseGenerator.batch_generate_times(args.count, args.batch)
        
        print("\n生成的授权码:")
        for i, code in enumerate(licenses, 1):
            print(f"  {i}. {code}")
        
        if args.output:
            LicenseGenerator.export_to_file(licenses, args.output, "times", args.count)
    
    print("\n完成!")


if __name__ == "__main__":
    main()
