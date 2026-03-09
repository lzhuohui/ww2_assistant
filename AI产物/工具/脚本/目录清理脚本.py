#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
目录清理脚本
用于定期清理AI产物目录中的过期文件
"""

import os
import shutil
import json
from datetime import datetime, timedelta
from pathlib import Path


class 目录清理器:
    """目录清理器类"""
    
    # 清理配置
    清理配置 = {
        "临时/缓存/": {"保留天数": 7, "自动清理": True},
        "临时/草稿/": {"保留天数": 30, "自动清理": True},
        "日志/操作/": {"保留天数": 30, "自动清理": True},
        "日志/错误/": {"保留天数": 90, "自动清理": True},
        "日志/审计/": {"保留天数": 365, "自动清理": False},
        "数据/原始/": {"保留天数": 90, "自动清理": False},
        "数据/处理/": {"保留天数": 30, "自动清理": True},
        "文档/临时/": {"保留天数": 7, "自动清理": True},
    }
    
    def __init__(self, 基础路径: str = "AI产物"):
        """初始化"""
        self.基础路径 = Path(基础路径)
        self.清理记录 = []
    
    def 扫描过期文件(self, 目录路径: str, 保留天数: int) -> list:
        """
        扫描指定目录中的过期文件
        
        参数:
            目录路径: 要扫描的目录
            保留天数: 文件保留天数
        
        返回:
            过期文件列表
        """
        过期文件 = []
        截止日期 = datetime.now() - timedelta(days=保留天数)
        
        目标目录 = self.基础路径 / 目录路径
        if not 目标目录.exists():
            return 过期文件
        
        for 文件 in 目标目录.iterdir():
            if 文件.is_file():
                修改时间 = datetime.fromtimestamp(文件.stat().st_mtime)
                if 修改时间 < 截止日期:
                    过期文件.append({
                        "路径": str(文件),
                        "名称": 文件.name,
                        "修改时间": 修改时间.strftime("%Y-%m-%d %H:%M:%S"),
                        "大小": 文件.stat().st_size
                    })
        
        return 过期文件
    
    def 归档文件(self, 文件路径: str) -> bool:
        """
        将文件归档到归档目录
        
        参数:
            文件路径: 要归档的文件路径
        
        返回:
            是否归档成功
        """
        try:
            源文件 = Path(文件路径)
            if not 源文件.exists():
                return False
            
            # 构建归档路径
            归档目录 = self.基础路径 / "归档" / "历史" / datetime.now().strftime("%Y%m")
            归档目录.mkdir(parents=True, exist_ok=True)
            
            # 归档文件名
            归档文件名 = f"{源文件.stem}_归档_{datetime.now().strftime('%Y%m%d')}{源文件.suffix}"
            归档路径 = 归档目录 / 归档文件名
            
            # 移动文件
            shutil.move(str(源文件), str(归档路径))
            
            return True
            
        except Exception as e:
            print(f"归档失败 {文件路径}: {e}")
            return False
    
    def 删除文件(self, 文件路径: str) -> bool:
        """
        删除指定文件
        
        参数:
            文件路径: 要删除的文件路径
        
        返回:
            是否删除成功
        """
        try:
            文件 = Path(文件路径)
            if 文件.exists():
                文件.unlink()
                return True
            return False
        except Exception as e:
            print(f"删除失败 {文件路径}: {e}")
            return False
    
    def 执行清理(self, 模拟运行: bool = False) -> dict:
        """
        执行清理操作
        
        参数:
            模拟运行: 如果为True，只显示将要清理的文件，不实际删除
        
        返回:
            清理结果统计
        """
        结果 = {
            "扫描目录": 0,
            "发现过期文件": 0,
            "归档文件": 0,
            "删除文件": 0,
            "失败": 0,
            "详情": []
        }
        
        print(f"{'='*60}")
        print(f"开始清理任务 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        
        for 目录路径, 配置 in self.清理配置.items():
            结果["扫描目录"] += 1
            
            print(f"\n扫描目录: {目录路径}")
            print(f"保留天数: {配置['保留天数']}天")
            print(f"自动清理: {'是' if 配置['自动清理'] else '否'}")
            
            # 扫描过期文件
            过期文件 = self.扫描过期文件(目录路径, 配置["保留天数"])
            结果["发现过期文件"] += len(过期文件)
            
            if not 过期文件:
                print("  未发现过期文件")
                continue
            
            print(f"  发现 {len(过期文件)} 个过期文件")
            
            if 模拟运行:
                for 文件信息 in 过期文件:
                    print(f"    [模拟] 将清理: {文件信息['名称']}")
                continue
            
            # 执行清理
            for 文件信息 in 过期文件:
                文件路径 = 文件信息["路径"]
                
                if 配置["自动清理"]:
                    # 直接删除
                    if self.删除文件(文件路径):
                        结果["删除文件"] += 1
                        结果["详情"].append({
                            "操作": "删除",
                            "文件": 文件信息["名称"],
                            "路径": 文件路径
                        })
                        print(f"    已删除: {文件信息['名称']}")
                    else:
                        结果["失败"] += 1
                else:
                    # 归档
                    if self.归档文件(文件路径):
                        结果["归档文件"] += 1
                        结果["详情"].append({
                            "操作": "归档",
                            "文件": 文件信息["名称"],
                            "路径": 文件路径
                        })
                        print(f"    已归档: {文件信息['名称']}")
                    else:
                        结果["失败"] += 1
        
        # 保存清理记录
        self._保存清理记录(结果)
        
        print(f"\n{'='*60}")
        print("清理任务完成")
        print(f"扫描目录: {结果['扫描目录']}")
        print(f"发现过期文件: {结果['发现过期文件']}")
        print(f"归档文件: {结果['归档文件']}")
        print(f"删除文件: {结果['删除文件']}")
        print(f"失败: {结果['失败']}")
        print(f"{'='*60}")
        
        return 结果
    
    def _保存清理记录(self, 结果: dict):
        """保存清理记录"""
        记录文件 = self.基础路径 / "日志" / "操作" / "清理记录.json"
        记录文件.parent.mkdir(parents=True, exist_ok=True)
        
        记录 = {
            "时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "结果": 结果
        }
        
        # 读取现有记录
        现有记录 = []
        if 记录文件.exists():
            with open(记录文件, 'r', encoding='utf-8') as f:
                现有记录 = json.load(f)
        
        # 添加新记录
        现有记录.append(记录)
        
        # 保存记录
        with open(记录文件, 'w', encoding='utf-8') as f:
            json.dump(现有记录, f, ensure_ascii=False, indent=2)
    
    def 获取存储统计(self) -> dict:
        """获取存储统计信息"""
        统计 = {
            "总文件数": 0,
            "总大小": 0,
            "目录统计": {}
        }
        
        if not self.基础路径.exists():
            return 统计
        
        for 文件 in self.基础路径.rglob('*'):
            if 文件.is_file():
                统计["总文件数"] += 1
                统计["总大小"] += 文件.stat().st_size
                
                # 目录统计
                父目录 = str(文件.parent.relative_to(self.基础路径))
                if 父目录 not in 统计["目录统计"]:
                    统计["目录统计"][父目录] = {"文件数": 0, "大小": 0}
                
                统计["目录统计"][父目录]["文件数"] += 1
                统计["目录统计"][父目录]["大小"] += 文件.stat().st_size
        
        return 统计


# 使用示例
if __name__ == "__main__":
    import argparse
    
    解析器 = argparse.ArgumentParser(description="AI产物目录清理工具")
    解析器.add_argument("--dry-run", action="store_true", help="模拟运行，不实际删除文件")
    解析器.add_argument("--stats", action="store_true", help="显示存储统计信息")
    
    参数 = 解析器.parse_args()
    
    清理器 = 目录清理器()
    
    if 参数.stats:
        统计 = 清理器.获取存储统计()
        print("存储统计信息:")
        print(f"总文件数: {统计['总文件数']}")
        print(f"总大小: {统计['总大小'] / 1024 / 1024:.2f} MB")
        print("\n目录统计:")
        for 目录, 信息 in 统计["目录统计"].items():
            print(f"  {目录}: {信息['文件数']} 个文件, {信息['大小'] / 1024:.2f} KB")
    else:
        清理器.执行清理(模拟运行=参数.dry_run)
