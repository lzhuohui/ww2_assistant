# -*- coding: utf-8 -*-
"""
模块名称：导出仓库
设计思路: 提供配置导出的文件操作
模块隔离: 数据层只依赖核心层，不依赖其他层
"""

import os
import json
import time
from typing import Dict, Any
from 前端.新界面_v2.核心.配置.全局配置 import 全局配置


# *** 用户指定变量 - AI不得修改 ***
# （用户未指定变量）
# *********************************


class 导出仓库:
    """导出仓库 - 配置导出的文件操作"""
    
    def __init__(self):
        self._导出目录 = os.path.join(os.path.dirname(__file__), "..", "..", "..", "导出")
        self._确保导出目录存在()
    
    def _确保导出目录存在(self) -> None:
        """确保导出目录存在"""
        if not os.path.exists(self._导出目录):
            os.makedirs(self._导出目录, exist_ok=True)
    
    def 导出配置(self, 配置数据: Dict[str, Any]) -> str:
        """导出配置到文件"""
        try:
            文件名 = f"游戏配置_{int(time.time())}.json"
            导出路径 = os.path.join(self._导出目录, 文件名)
            
            with open(导出路径, 'w', encoding='utf-8') as f:
                json.dump(配置数据, f, ensure_ascii=False, indent=2)
            
            return f"配置导出成功: {导出路径}"
        except Exception as e:
            return f"配置导出失败: {e}"
    
    def 读取导出(self) -> Dict[str, Any]:
        """读取导出的配置"""
        try:
            # 获取最新的导出文件
            导出文件 = sorted(
                [f for f in os.listdir(self._导出目录) if f.endswith('.json')],
                key=lambda x: os.path.getmtime(os.path.join(self._导出目录, x)),
                reverse=True
            )
            
            if 导出文件:
                最新文件 = os.path.join(self._导出目录, 导出文件[0])
                with open(最新文件, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {}
        except Exception as e:
            print(f"读取导出失败: {e}")
            return {}
    
    def 清理导出(self, 保留天数: int = 7) -> str:
        """清理过期的导出文件"""
        try:
            现在 = os.time()
            过期时间 = 保留天数 * 24 * 60 * 60
            
            清理数量 = 0
            for 文件 in os.listdir(self._导出目录):
                文件路径 = os.path.join(self._导出目录, 文件)
                if os.path.isfile(文件路径) and 文件.endswith('.json'):
                    if os.time() - os.path.getmtime(文件路径) > 过期时间:
                        os.remove(文件路径)
                        清理数量 += 1
            
            return f"清理完成，删除了 {清理数量} 个过期文件"
        except Exception as e:
            return f"清理失败: {e}"
