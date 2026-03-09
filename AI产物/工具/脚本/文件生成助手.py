#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件生成助手
用于帮助AI生成符合规范的文件
"""

import os
import re
from datetime import datetime
from pathlib import Path


class 文件生成助手:
    """文件生成助手类"""
    
    # 文件类型映射
    类型映射 = {
        "报告": ("文档/报告/", "md"),
        "方案": ("文档/方案/", "md"),
        "分析": ("文档/分析/", "md"),
        "脚本": ("工具/脚本/", "py"),
        "配置": ("工具/配置/", "json"),
        "数据": ("数据/原始/", "json"),
        "日志": ("日志/操作/", "log"),
        "临时": ("临时/", "tmp"),
    }
    
    # 基础路径
    基础路径 = "AI产物"
    
    def __init__(self):
        """初始化"""
        self.当前日期 = datetime.now().strftime("%Y%m%d")
    
    def 生成文件路径(self, 文件类型: str, 文件描述: str, 扩展名: str = None) -> str:
        """
        生成标准文件路径
        
        参数:
            文件类型: 报告/方案/分析/脚本/配置/数据/日志/临时
            文件描述: 文件内容简述
            扩展名: 文件扩展名（可选，根据类型自动确定）
        
        返回:
            完整的文件路径
        """
        # 获取目标目录和默认扩展名
        if 文件类型 in self.类型映射:
            目标目录, 默认扩展名 = self.类型映射[文件类型]
        else:
            目标目录, 默认扩展名 = "临时/", "txt"
        
        # 使用指定的扩展名或默认扩展名
        扩展名 = 扩展名 or 默认扩展名
        
        # 生成文件名
        版本号 = "v1.0.0"
        文件名 = f"{文件类型}_{self.当前日期}_{文件描述}_{版本号}.{扩展名}"
        
        # 构建完整路径
        完整路径 = os.path.join(self.基础路径, 目标目录, 文件名)
        
        return 完整路径
    
    def 检查路径合法性(self, 目标路径: str) -> tuple:
        """
        检查目标路径是否合法
        
        参数:
            目标路径: 要检查的路径
        
        返回:
            (是否合法, 提示信息)
        """
        # 禁止的根目录
        禁止根目录 = ["./", ".\\", "", "src/", "docs/", ".git/"]
        
        # 检查是否在禁止的根目录
        for 禁止 in 禁止根目录:
            if 目标路径.startswith(禁止) and not 目标路径.startswith("AI产物/"):
                return False, f"禁止在根目录创建文件: {目标路径}"
        
        # 检查是否包含非法字符
        非法字符 = ['<', '>', ':', '"', '|', '?', '*']
        if any(字符 in 目标路径 for 字符 in 非法字符):
            return False, f"路径包含非法字符: {目标路径}"
        
        return True, "路径合法"
    
    def 创建文件(self, 文件路径: str, 内容: str, 元数据: dict = None) -> bool:
        """
        创建文件并记录元数据
        
        参数:
            文件路径: 目标文件路径
            内容: 文件内容
            元数据: 文件元数据（可选）
        
        返回:
            是否创建成功
        """
        try:
            # 检查路径合法性
            合法, 提示 = self.检查路径合法性(文件路径)
            if not 合法:
                print(f"错误: {提示}")
                return False
            
            # 确保目录存在
            目录 = os.path.dirname(文件路径)
            os.makedirs(目录, exist_ok=True)
            
            # 写入文件
            with open(文件路径, 'w', encoding='utf-8') as f:
                # 添加文件头信息
                if 文件路径.endswith('.md'):
                    f.write(self._生成markdown文件头(元数据))
                elif 文件路径.endswith('.py'):
                    f.write(self._生成python文件头(元数据))
                
                f.write(内容)
            
            print(f"文件创建成功: {文件路径}")
            return True
            
        except Exception as e:
            print(f"文件创建失败: {e}")
            return False
    
    def _生成markdown文件头(self, 元数据: dict = None) -> str:
        """生成Markdown文件头"""
        元数据 = 元数据 or {}
        
        文件头 = f"""---
创建日期: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
作者: {元数据.get('作者', 'AI')}
版本: {元数据.get('版本', 'v1.0.0')}
类型: {元数据.get('类型', '文档')}
---

"""
        return 文件头
    
    def _生成python文件头(self, 元数据: dict = None) -> str:
        """生成Python文件头"""
        元数据 = 元数据 or {}
        
        文件头 = f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
{元数据.get('描述', '脚本描述')}

创建日期: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
作者: {元数据.get('作者', 'AI')}
版本: {元数据.get('版本', 'v1.0.0')}
\"\"\"

"""
        return 文件头
    
    def 获取目录统计(self) -> dict:
        """获取AI产物目录统计信息"""
        统计 = {}
        
        基础路径 = Path(self.基础路径)
        if not 基础路径.exists():
            return {"错误": "AI产物目录不存在"}
        
        # 统计各目录文件数量
        for 子目录 in 基础路径.rglob('*'):
            if 子目录.is_file():
                父目录 = str(子目录.parent.relative_to(基础路径))
                统计[父目录] = 统计.get(父目录, 0) + 1
        
        return 统计


# 使用示例
if __name__ == "__main__":
    助手 = 文件生成助手()
    
    # 示例1: 生成报告文件路径
    报告路径 = 助手.生成文件路径("报告", "环境配置")
    print(f"报告路径: {报告路径}")
    
    # 示例2: 生成脚本文件路径
    脚本路径 = 助手.生成文件路径("脚本", "字符统计")
    print(f"脚本路径: {脚本路径}")
    
    # 示例3: 检查路径合法性
    合法, 提示 = 助手.检查路径合法性("AI产物/文档/报告/测试.md")
    print(f"路径检查: {合法}, {提示}")
    
    # 示例4: 获取目录统计
    统计 = 助手.获取目录统计()
    print(f"目录统计: {统计}")
