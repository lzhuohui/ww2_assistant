# -*- coding: utf-8 -*-
"""
模块名称：ExportService
设计思路: 提供数据转换和导出的业务逻辑
模块隔离: 服务层依赖数据层和核心层，不依赖表示层
"""

import json
from typing import Dict, Any, List
from datetime import datetime
from 前端.新界面_v2.核心.配置.配置映射 import ConfigMapping


class ExportService:
    """导出服务 - 数据转换和导出的业务逻辑"""
    
    def generate_game_config(self, user_config: Dict[str, Any]) -> Dict[str, Any]:
        """生成按键精灵格式的游戏控制配置"""
        result = {}
        
        for i in range(1, 22):
            result[f"控制{i}"] = ""
        
        result.update(self._convert_system_config(user_config))
        result.update(self._convert_strategy_config(user_config))
        result.update(self._convert_task_config(user_config))
        result.update(self._convert_funding_config(user_config))
        result.update(self._convert_cleaning_config(user_config))
        result.update(self._convert_hunting_config(user_config))
        result.update(self._convert_building_config(user_config))
        result.update(self._convert_accounts(user_config))
        
        result["挂机统帅信息"] = self._generate_commander_info(user_config)
        
        return result
    
    def _convert_system_config(self, user_config: Dict[str, Any]) -> Dict[str, Any]:
        """转换系统配置"""
        result = {}
        
        mode = user_config.get("hangup_mode.挂机模式", "全自动")
        mode_index = "0" if mode == "全自动" else "1"
        result["控制1"] = mode_index
        result["挂机模式"] = "自动挂机" if mode == "全自动" else "手动控制"
        
        speed = user_config.get("command_speed.指令速度", "100")
        result["控制3"] = "0"
        result["挂机速度"] = speed
        
        retry = user_config.get("retry_count.尝试次数", "15")
        retry_index = str(int(retry) // 5 - 2) if retry.isdigit() else "2"
        result["控制4"] = retry_index
        result["尝试次数"] = retry
        
        cache = user_config.get("cache_limit.清缓限量", "1.0")
        cache_value = int(float(cache) * 1000)
        result["控制5"] = "0"
        result["缓存限制"] = str(cache_value)
        
        return result
    
    def _convert_strategy_config(self, user_config: Dict[str, Any]) -> Dict[str, Any]:
        """转换策略配置"""
        result = {}
        
        build_level = user_config.get("quick_build.速建限级", "08")
        result["控制6"] = str(int(build_level) - 5)
        result["速建限级"] = build_level
        
        build_type = user_config.get("quick_build.速建类型", "城资建筑")
        type_index = {"城市建筑": "0", "资源建筑": "1", "城资建筑": "2"}.get(build_type, "2")
        result["控制7"] = type_index
        result["速建类别"] = {"城市建筑": "城市", "资源建筑": "资源", "城资建筑": "城资"}.get(build_type, "城资")
        
        prod_level = user_config.get("quick_produce.速产限级", "07")
        result["控制8"] = str(int(prod_level) - 5)
        result["速产限级"] = prod_level
        
        prod_type = user_config.get("quick_produce.速产类型", "平衡资源")
        strategy_index = {"平衡资源": "0", "战时经济": "1", "钢铁熔炉": "2", "橡胶采集": "3", "石油开采": "4"}.get(prod_type, "0")
        result["控制9"] = strategy_index
        result["速产策略"] = prod_type
        
        points = user_config.get("point_reserve.保留点数", "60")
        points_index = str(int(points) // 30 - 1)
        result["控制10"] = points_index
        result["保留策点"] = points
        
        return result
    
    def _convert_task_config(self, user_config: Dict[str, Any]) -> Dict[str, Any]:
        """转换任务配置"""
        result = {}
        
        side_level = user_config.get("main_task.支线限级", "10")
        result["控制11"] = str(int(side_level) - 5)
        result["支线限级"] = side_level
        
        side_enabled = user_config.get("main_task.enabled", False)
        result["控制12"] = "True" if side_enabled else "False"
        result["支线状态"] = "开启" if side_enabled else "关闭"
        
        return result
    
    def _convert_funding_config(self, user_config: Dict[str, Any]) -> Dict[str, Any]:
        """转换集资配置"""
        result = {}
        
        result["控制17"] = "0"
        result["集资限级"] = "10"
        
        result["控制18"] = "0"
        result["集资限量"] = "20000"
        
        result["控制19"] = "False"
        result["主帅集资"] = "关闭"
        
        result["控制20"] = "False"
        result["附城集资"] = "关闭"
        
        result["控制21"] = ""
        result["集资统帅"] = ""
        
        return result
    
    def _convert_cleaning_config(self, user_config: Dict[str, Any]) -> Dict[str, Any]:
        """转换打扫配置"""
        result = {}
        
        clean_type = user_config.get("cleaning.打扫类型", "城区战场")
        type_index = {"城区战场": "0", "城政战场": "1"}.get(clean_type, "0")
        result["控制13"] = type_index
        result["打扫战场类型"] = clean_type
        
        return result
    
    def _convert_hunting_config(self, user_config: Dict[str, Any]) -> Dict[str, Any]:
        """转换打野配置"""
        result = {}
        
        hunting_enabled = user_config.get("auto_hunting.enabled", False)
        result["控制14"] = "True" if hunting_enabled else "False"
        result["自动打野模式"] = "自动攻占" if hunting_enabled else "停止攻占"
        
        result["控制15"] = "0"
        result["打野战场限级"] = "10"
        
        result["控制16"] = "2"
        result["打野叛军限级"] = "3"
        
        return result
    
    def _convert_building_config(self, user_config: Dict[str, Any]) -> Dict[str, Any]:
        """转换建筑配置"""
        result = {}
        
        for i in range(1, 47):
            result[f"建筑{i}"] = ""
        
        result["建筑1"] = "26"
        result["建筑2"] = "25"
        result["建筑3"] = "25"
        result["建筑4"] = "8"
        result["建筑5"] = "5"
        result["建筑6"] = "5"
        result["建筑7"] = "5"
        result["建筑8"] = "5"
        result["建筑9"] = "5"
        result["建筑10"] = "3"
        result["建筑11"] = "3"
        result["建筑12"] = "5"
        
        result["主帅主城城市建筑设置"] = "|城市/26|兵工厂/25|陆军基地/25|空军基地/8|商业区/5|补给品厂/5|高产农场/6|高产铁矿/6|高产橡胶厂/6|高产油井/6|岸防炮/5|炮塔/5"
        result["主帅主城村庄建筑设置"] = "|农场/6|村庄/5|狙击塔/5"
        result["主帅主城资源区建筑设置"] = "|铁矿/6|橡胶厂/6|油井/6|资源区/5|狙击塔/5"
        result["主帅主城军事区建筑设置"] = "|军事区/3|岸防炮/5|炮塔/5"
        result["主帅主城海港建筑设置"] = "|海军基地/15|海港/3|岸防炮/5|炮塔/5"
        
        return result
    
    def _convert_accounts(self, user_config: Dict[str, Any]) -> Dict[str, Any]:
        """转换账号配置"""
        result = {}
        
        for i in range(1, 16):
            account_num = f"{i:02d}"
            base_index = (i - 1) * 4 + 1
            
            account_type = user_config.get(f"account_{account_num}.类型", "副帅")
            type_index = "0" if account_type == "主帅" else "1"
            result[f"统帅{base_index}"] = type_index
            
            name = user_config.get(f"account_{account_num}.名称", "")
            account = user_config.get(f"account_{account_num}.账号", "")
            password = user_config.get(f"account_{account_num}.密码", "")
            result[f"统帅{base_index + 1}"] = f"{name}/{account}/{password}" if name else ""
            
            platform = user_config.get(f"account_{account_num}.平台", "Tap")
            platform_index = {"Tap": "0", "九游": "1", "Fan": "2", "小7": "3", "Vivo": "4", "Opop": "5"}.get(platform, "0")
            result[f"统帅{base_index + 2}"] = platform_index
            
            enabled = user_config.get(f"account_{account_num}.开关", False)
            result[f"统帅{base_index + 3}"] = "True" if enabled else "False"
        
        return result
    
    def _generate_commander_info(self, user_config: Dict[str, Any]) -> str:
        """生成挂机统帅信息"""
        info_list = []
        
        for i in range(1, 16):
            account_num = f"{i:02d}"
            
            enabled = user_config.get(f"account_{account_num}.开关", False)
            if not enabled:
                continue
            
            name = user_config.get(f"account_{account_num}.名称", "")
            if not name:
                continue
            
            account_type = user_config.get(f"account_{account_num}.类型", "副帅")
            account = user_config.get(f"account_{account_num}.账号", "")
            password = user_config.get(f"account_{account_num}.密码", "")
            platform = user_config.get(f"account_{account_num}.平台", "Tap")
            
            info_list.append(f"{account_type}/{name}/{account}/{password}/{platform}")
        
        return "/".join(info_list)