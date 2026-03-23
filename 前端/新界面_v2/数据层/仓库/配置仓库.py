# -*- coding: utf-8 -*-
"""
模块名称：配置仓库
设计思路: 提供配置文件的读写操作
模块隔离: 数据层只依赖核心层，不依赖其他层
"""

import os
import json
from typing import Dict, Any
from 前端.新界面_v2.核心.配置.全局配置 import 全局配置


# *** 用户指定变量 - AI不得修改 ***
# （用户未指定变量）
# *********************************


class 配置仓库:
    """配置仓库 - 配置文件的读写操作"""
    
    def __init__(self):
        self._配置文件路径 = os.path.join(os.path.dirname(__file__), "..", "..", "..", "配置", "用户配置.json")
        self._确保配置目录存在()
    
    def _确保配置目录存在(self) -> None:
        """确保配置目录存在"""
        目录 = os.path.dirname(self._配置文件路径)
        if not os.path.exists(目录):
            os.makedirs(目录, exist_ok=True)
    
    def 读取配置(self) -> Dict[str, Any]:
        """读取配置文件"""
        try:
            if os.path.exists(self._配置文件路径):
                with open(self._配置文件路径, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return self._获取默认配置()
        except Exception as e:
            print(f"读取配置失败: {e}")
            return self._获取默认配置()
    
    def 保存配置(self, 配置数据: Dict[str, Any]) -> str:
        """保存配置文件"""
        try:
            with open(self._配置文件路径, 'w', encoding='utf-8') as f:
                json.dump(配置数据, f, ensure_ascii=False, indent=2)
            return f"配置保存成功: {self._配置文件路径}"
        except Exception as e:
            return f"配置保存失败: {e}"
    
    def _获取默认配置(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "系统配置": {
                "自动启动": False,
                "最小化到托盘": True,
                "开机自启": False
            },
            "游戏配置": {
                "游戏路径": "",
                "游戏窗口标题": "二战风云",
                "自动登录": False
            },
            "界面配置": {
                "主题": "light",
                "字体大小": 12,
                "语言": "zh-CN"
            }
        }
