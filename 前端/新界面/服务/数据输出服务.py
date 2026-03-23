# -*- coding: utf-8 -*-
"""
模块名称：数据输出服务
设计思路: 将用户设置数据转换为游戏控制模块可用的标准格式
模块隔离: 只负责数据转换和输出，不包含游戏控制逻辑
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime


# *** 用户指定变量 - AI不得修改 ***
USER_OUTPUT_DIR = "output"
USER_CONFIG_FILE = "game_config.json"
# *********************************


class DataOutputService:
    """数据输出服务 - 用户设置数据转换输出"""
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, output_dir: str = None):
        if hasattr(self, '_initialized') and self._initialized:
            return
        
        self.output_dir = Path(output_dir) if output_dir else Path(__file__).parent.parent.parent / USER_OUTPUT_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self._initialized = True
    
    def convert_system_config(self, user_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        转换系统配置
        
        输入格式: {"挂机模式.挂机模式": "自动", "指令速度.指令速度": "100毫秒", ...}
        输出格式: {"挂机模式": "自动", "挂机速度": 100, ...}
        """
        result = {}
        
        mode_map = {"自动": "自动挂机", "手动": "手动控制"}
        if user_config.get("挂机模式.挂机模式"):
            result["挂机模式"] = mode_map.get(user_config["挂机模式.挂机模式"], user_config["挂机模式.挂机模式"])
        
        speed_str = user_config.get("指令速度.指令速度", "100毫秒")
        result["挂机速度"] = int(speed_str.replace("毫秒", "")) if "毫秒" in speed_str else 100
        
        retry_str = user_config.get("尝试次数.尝试次数", "10次")
        result["尝试次数"] = int(retry_str.replace("次", "")) if "次" in retry_str else 10
        
        cache_str = user_config.get("清缓限量.清缓限量", "1.0M")
        result["缓存限制"] = float(cache_str.replace("M", "")) * 1024 * 1024 if "M" in cache_str else 1.0 * 1024 * 1024
        
        return result
    
    def convert_strategy_config(self, user_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        转换策略配置
        
        输入格式: {"建筑速建.速建限级": "08", "建筑速建.速建类型": "城市建筑", ...}
        输出格式: {"速建限级": 8, "速建类别": "城市", ...}
        """
        result = {}
        
        level_str = user_config.get("建筑速建.速建限级", "08")
        result["速建限级"] = int(level_str.replace("级", "")) if "级" in level_str else int(level_str)
        
        type_map = {"城市建筑": "城市", "资源建筑": "资源", "城资建筑": "城资"}
        type_str = user_config.get("建筑速建.速建类型", "城资建筑")
        result["速建类别"] = type_map.get(type_str, type_str)
        
        result["速建开关"] = user_config.get("建筑速建.速建开关", True)
        
        prod_level = user_config.get("资源速产.速产限级", "07")
        result["速产限级"] = int(prod_level.replace("级", "")) if "级" in prod_level else int(prod_level)
        
        prod_type_map = {"平衡资源": "自动平衡", "战时经济": "战时经济", "钢铁熔炉": "钢铁熔炉", "橡胶采集": "橡胶采集", "油井开采": "油井开采"}
        prod_type = user_config.get("资源速产.速产类型", "平衡资源")
        result["速产策略"] = prod_type_map.get(prod_type, prod_type)
        
        result["速产开关"] = user_config.get("资源速产.速产开关", True)
        
        points_str = user_config.get("策点保留.保留点数", "60")
        result["保留策点"] = int(points_str)
        
        result["保留开关"] = user_config.get("策点保留.保留开关", True)
        
        return result
    
    def convert_task_config(self, user_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        转换任务配置
        
        输入格式: {"主线任务.主线限级": "12", "支线任务.支线限级": "15"}
        输出格式: {"主线限级": 12, "支线限级": 15, "支线状态": "开启"}
        """
        result = {}
        
        main_level = user_config.get("主线任务.主线限级", "05")
        result["主线限级"] = int(main_level.replace("级", "")) if "级" in main_level else int(main_level)
        
        side_level = user_config.get("支线任务.支线限级", "10")
        result["支线限级"] = int(side_level.replace("级", "")) if "级" in side_level else int(side_level)
        
        result["支线状态"] = "开启"
        
        return result
    
    def convert_fundraising_config(self, user_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        转换集资配置
        
        输入格式: {"小号上贡.小号上贡_上贡限级": "05", "小号上贡.小号上贡_上贡限量": "2", ...}
        输出格式: {"集资限级": 5, "集资限量": 20000, ...}
        """
        result = {}
        
        level_str = user_config.get("小号上贡.小号上贡_上贡限级", "05")
        result["集资限级"] = int(level_str.replace("级", "")) if "级" in level_str else int(level_str)
        
        limit_str = user_config.get("小号上贡.小号上贡_上贡限量", "2")
        result["集资限量"] = int(limit_str) * 10000
        
        result["主帅集资"] = "开启"
        result["附城集资"] = "关闭"
        
        result["集资统帅"] = user_config.get("小号上贡.主要统帅", "默认主帅")
        
        return result
    
    def convert_account_config(self, user_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        转换账号配置
        
        输入格式: {"01账号.开关": true, "01账号.统帅种类": "主帅", "01账号.名称": "xxx", ...}
        输出格式: [{"帅类": "主帅", "名称": "xxx", "账号": "xxx", ...}, ...]
        """
        accounts = []
        
        for i in range(1, 16):
            account_id = f"{i:02d}账号"
            
            if not user_config.get(f"{account_id}.开关", False):
                continue
            
            account = {
                "序号": i,
                "帅类": user_config.get(f"{account_id}.统帅种类", "副帅"),
                "名称": user_config.get(f"{account_id}.名称", ""),
                "账号": user_config.get(f"{account_id}.账号", ""),
                "密码": user_config.get(f"{account_id}.密码", ""),
                "平台": user_config.get(f"{account_id}.平台", "Tap"),
                "挂机": user_config.get(f"{account_id}.开关", False),
            }
            
            accounts.append(account)
        
        return accounts
    
    def convert_cleaning_config(self, user_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        转换打扫配置
        
        输入格式: {"打扫城区.开关": true, "打扫政区.开关": true}
        输出格式: {"打扫战场类型": "城区战场", "打扫城区": "开启", "打扫政区": "开启"}
        """
        result = {}
        
        clean_district = user_config.get("打扫城区.开关", False)
        clean_political = user_config.get("打扫政区.开关", False)
        
        if clean_district and clean_political:
            result["打扫战场类型"] = "城政战场"
        elif clean_district:
            result["打扫战场类型"] = "城区战场"
        elif clean_political:
            result["打扫战场类型"] = "政区战场"
        else:
            result["打扫战场类型"] = "关闭"
        
        result["打扫城区"] = "开启" if clean_district else "关闭"
        result["打扫政区"] = "开启" if clean_political else "关闭"
        
        return result
    
    def convert_wild_config(self, user_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        转换打野配置
        
        输入格式: {"自动打野.开关": true}
        输出格式: {"自动打野模式": "自动攻占", "打野战场限级": 10, ...}
        """
        result = {}
        
        wild_enabled = user_config.get("自动打野.开关", False)
        result["自动打野模式"] = "自动攻占" if wild_enabled else "停止攻占"
        
        result["打野战场限级"] = 10
        result["打野叛军限级"] = 1
        
        return result
    
    def convert_building_config(self, user_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        转换建筑配置
        
        输入格式: 从用户配置中提取建筑相关设置
        输出格式: 标准化的建筑配置
        """
        result = {}
        
        result["主帅主城"] = {
            "城市": 17,
            "兵工厂": 17,
            "陆军基地": 14,
            "空军基地": 3,
            "商业区": 4,
            "补给品厂": 3,
        }
        
        result["付帅主城"] = {
            "城市": 15,
            "兵工厂": 10,
            "陆军基地": 10,
            "空军基地": 3,
            "商业区": 4,
            "补给品厂": 3,
        }
        
        result["附城"] = {
            "城市": 15,
            "兵工厂": 10,
            "陆军基地": 10,
            "空军基地": 3,
            "商业区": 4,
            "补给品厂": 3,
        }
        
        return result
    
    def generate_game_config(self, user_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成完整的游戏控制配置
        
        参数:
            user_config: 用户设置数据（扁平化格式）
        
        返回:
            游戏控制配置（结构化格式）
        """
        game_config = {
            "__version__": "1.0.0",
            "__timestamp__": datetime.now().isoformat(),
            "系统设置": self.convert_system_config(user_config),
            "策略设置": self.convert_strategy_config(user_config),
            "任务设置": self.convert_task_config(user_config),
            "集资设置": self.convert_fundraising_config(user_config),
            "账号设置": self.convert_account_config(user_config),
            "打扫设置": self.convert_cleaning_config(user_config),
            "打野设置": self.convert_wild_config(user_config),
            "建筑设置": self.convert_building_config(user_config),
        }
        
        accounts = game_config["账号设置"]
        if accounts:
            account_info = "/".join([
                f"{acc['帅类']}/{acc['名称']}/{acc['平台']}"
                for acc in accounts if acc.get("挂机") and acc.get("名称")
            ])
            game_config["挂机统帅信息"] = account_info
        
        return game_config
    
    def save_game_config(self, game_config: Dict[str, Any], filename: str = None) -> Path:
        """
        保存游戏配置到文件
        
        参数:
            game_config: 游戏配置数据
            filename: 文件名（可选）
        
        返回:
            保存的文件路径
        """
        filename = filename or USER_CONFIG_FILE
        file_path = self.output_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(game_config, f, ensure_ascii=False, indent=2)
        
        return file_path
    
    def export_config(self, user_config: Dict[str, Any]) -> Path:
        """
        导出配置（主入口）
        
        参数:
            user_config: 用户设置数据
        
        返回:
            导出的文件路径
        """
        game_config = self.generate_game_config(user_config)
        file_path = self.save_game_config(game_config)
        return file_path
    
    def get_config_summary(self, game_config: Dict[str, Any]) -> str:
        """
        获取配置摘要
        
        参数:
            game_config: 游戏配置数据
        
        返回:
            配置摘要文本
        """
        lines = [
            f"配置版本: {game_config.get('__version__', 'N/A')}",
            f"生成时间: {game_config.get('__timestamp__', 'N/A')}",
            "",
            f"挂机模式: {game_config['系统设置'].get('挂机模式', 'N/A')}",
            f"挂机速度: {game_config['系统设置'].get('挂机速度', 'N/A')}ms",
            f"尝试次数: {game_config['系统设置'].get('尝试次数', 'N/A')}次",
            "",
            f"账号数量: {len(game_config['账号设置'])}个",
        ]
        
        for acc in game_config['账号设置']:
            lines.append(f"  - {acc['帅类']}: {acc['名称']} ({acc['平台']})")
        
        return "\n".join(lines)


if __name__ == "__main__":
    service = DataOutputService()
    
    test_config = {
        "挂机模式.挂机模式": "自动",
        "指令速度.指令速度": "100毫秒",
        "尝试次数.尝试次数": "10次",
        "清缓限量.清缓限量": "1.0M",
        "建筑速建.速建限级": "08",
        "建筑速建.速建类型": "城资建筑",
        "建筑速建.速建开关": True,
        "主线任务.主线限级": "12",
        "支线任务.支线限级": "15",
        "01账号.开关": True,
        "01账号.统帅种类": "主帅",
        "01账号.名称": "测试统帅",
        "01账号.账号": "test@example.com",
        "01账号.密码": "password123",
        "01账号.平台": "Tap",
        "打扫城区.开关": True,
        "打扫政区.开关": True,
        "自动打野.开关": True,
    }
    
    game_config = service.generate_game_config(test_config)
    print(json.dumps(game_config, ensure_ascii=False, indent=2))
    
    file_path = service.export_config(test_config)
    print(f"\n配置已导出到: {file_path}")
    
    print("\n" + service.get_config_summary(game_config))
