# -*- coding: utf-8 -*-
"""
模块名称：ExportRepository
设计思路: 提供配置导出的文件操作
模块隔离: 数据层只依赖核心层，不依赖其他层
"""

import os
import json
import time
from typing import Dict, Any


class ExportRepository:
    """导出仓库 - 配置导出的文件操作"""
    
    def __init__(self):
        self._export_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "导出")
        self._ensure_export_dir_exists()
    
    def _ensure_export_dir_exists(self) -> None:
        """确保导出目录存在"""
        if not os.path.exists(self._export_dir):
            os.makedirs(self._export_dir, exist_ok=True)
    
    def export_config(self, config_data: Dict[str, Any]) -> str:
        """导出配置到文件"""
        try:
            filename = "游戏配置.json"
            export_path = os.path.join(self._export_dir, filename)
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, ensure_ascii=False, indent=2)
            
            return f"配置导出成功: {export_path}"
        except Exception as e:
            return f"配置导出失败: {e}"
    
    def read_export(self) -> Dict[str, Any]:
        """读取导出的配置"""
        try:
            export_path = os.path.join(self._export_dir, "游戏配置.json")
            if os.path.exists(export_path):
                with open(export_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {}
        except Exception as e:
            print(f"读取导出失败: {e}")
            return {}
    
    def cleanup_exports(self, retention_days: int = 7) -> str:
        """清理过期的导出文件"""
        try:
            now = time.time()
            expiration_time = retention_days * 24 * 60 * 60
            
            cleaned_count = 0
            for file in os.listdir(self._export_dir):
                file_path = os.path.join(self._export_dir, file)
                if os.path.isfile(file_path) and file.endswith('.json'):
                    if now - os.path.getmtime(file_path) > expiration_time:
                        os.remove(file_path)
                        cleaned_count += 1
            
            return f"清理完成，删除了 {cleaned_count} 个过期文件"
        except Exception as e:
            return f"清理失败: {e}"