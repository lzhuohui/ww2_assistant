# 前端数据输出API文档

## 概述

本文档描述前端用户设置数据的输出接口，供游戏控制模块调用。

---

## 一、数据输出服务 (DataOutputService)

### 1.1 位置
```
前端/新界面/服务/数据输出服务.py
```

### 1.2 核心方法

| 方法 | 说明 | 输入 | 输出 |
|------|------|------|------|
| `generate_game_config(user_config)` | 生成游戏配置 | 用户设置字典 | 游戏配置字典 |
| `save_game_config(game_config, filename)` | 保存配置到文件 | 配置数据, 文件名 | 文件路径 |
| `export_config(user_config)` | 导出配置（主入口） | 用户设置字典 | 文件路径 |

### 1.3 使用示例

```python
from 前端.新界面.服务.数据输出服务 import DataOutputService

service = DataOutputService()

user_config = {
    "挂机模式.挂机模式": "自动",
    "指令速度.指令速度": "100毫秒",
    "尝试次数.尝试次数": "10次",
    # ... 更多配置
}

game_config = service.generate_game_config(user_config)
file_path = service.save_game_config(game_config)
```

---

## 二、配置收集器 (ConfigCollector)

### 2.1 位置
```
前端/新界面/服务/配置收集器.py
```

### 2.2 核心方法

| 方法 | 说明 | 参数 |
|------|------|------|
| `set_value(interface_id, card_id, config_key, value)` | 设置单个配置值 | 界面ID, 卡片ID, 配置键, 值 |
| `set_account(account_id, account_data)` | 设置账号配置 | 账号ID, 账号数据字典 |
| `get_all_config()` | 获取所有配置 | 无 |
| `export_for_game()` | 导出游戏配置 | 无 |
| `save_config(file_path)` | 保存配置到文件 | 文件路径(可选) |
| `load_config(file_path)` | 从文件加载配置 | 文件路径(可选) |

### 2.3 使用示例

```python
from 前端.新界面.服务.配置收集器 import ConfigCollector

collector = ConfigCollector()

collector.set_value("系统", "挂机模式", "挂机模式", "自动")
collector.set_value("系统", "指令速度", "指令速度", "100毫秒")

collector.set_account("01账号", {
    "开关": True,
    "统帅种类": "主帅",
    "名称": "测试统帅",
    "账号": "test@example.com",
    "密码": "password123",
    "平台": "Tap",
})

game_config = collector.export_for_game()
```

---

## 三、主界面接口

### 3.1 静态方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `主界面.get_game_config()` | 获取游戏控制配置 | Dict[str, Any] |
| `主界面.save_game_config()` | 保存游戏控制配置 | str (文件路径) |

### 3.2 使用示例

```python
from 前端.新界面.主界面 import 主界面

# 获取当前配置
game_config = 主界面.get_game_config()

# 保存配置到文件
file_path = 主界面.save_game_config()
```

---

## 四、输出数据格式

### 4.1 完整配置结构

```json
{
  "__version__": "1.0.0",
  "__timestamp__": "2026-03-22T15:10:20.752162",
  
  "系统设置": {
    "挂机模式": "自动挂机",
    "挂机速度": 100,
    "尝试次数": 10,
    "缓存限制": 1048576.0
  },
  
  "策略设置": {
    "速建限级": 8,
    "速建类别": "城资",
    "速建开关": true,
    "速产限级": 7,
    "速产策略": "自动平衡",
    "速产开关": true,
    "保留策点": 60,
    "保留开关": true
  },
  
  "任务设置": {
    "主线限级": 12,
    "支线限级": 15,
    "支线状态": "开启"
  },
  
  "集资设置": {
    "集资限级": 5,
    "集资限量": 20000,
    "主帅集资": "开启",
    "附城集资": "关闭",
    "集资统帅": "默认主帅"
  },
  
  "账号设置": [
    {
      "序号": 1,
      "帅类": "主帅",
      "名称": "测试统帅",
      "账号": "test@example.com",
      "密码": "password123",
      "平台": "Tap",
      "挂机": true
    }
  ],
  
  "打扫设置": {
    "打扫战场类型": "城政战场",
    "打扫城区": "开启",
    "打扫政区": "开启"
  },
  
  "打野设置": {
    "自动打野模式": "自动攻占",
    "打野战场限级": 10,
    "打野叛军限级": 1
  },
  
  "建筑设置": {
    "主帅主城": {
      "城市": 17,
      "兵工厂": 17,
      "陆军基地": 14,
      "空军基地": 3,
      "商业区": 4,
      "补给品厂": 3
    },
    "付帅主城": {...},
    "附城": {...}
  },
  
  "挂机统帅信息": "主帅/测试统帅/Tap"
}
```

### 4.2 字段说明

#### 系统设置
| 字段 | 类型 | 说明 |
|------|------|------|
| 挂机模式 | string | "自动挂机" / "手动控制" |
| 挂机速度 | int | 指令间隔(毫秒) |
| 尝试次数 | int | 失败重试次数 |
| 缓存限制 | float | 缓存阈值(字节) |

#### 策略设置
| 字段 | 类型 | 说明 |
|------|------|------|
| 速建限级 | int | 建筑加速等级限制 |
| 速建类别 | string | "城市" / "资源" / "城资" |
| 速建开关 | bool | 是否启用速建 |
| 速产限级 | int | 资源加速等级限制 |
| 速产策略 | string | 资源生产策略 |
| 保留策点 | int | 保留的策略点数 |

#### 账号设置
| 字段 | 类型 | 说明 |
|------|------|------|
| 序号 | int | 账号序号(1-15) |
| 帅类 | string | "主帅" / "副帅" |
| 名称 | string | 统帅名称 |
| 账号 | string | 登录账号 |
| 密码 | string | 登录密码 |
| 平台 | string | "Tap" / "九游" / ... |
| 挂机 | bool | 是否参与挂机 |

---

## 五、游戏控制模块调用方式

### 5.1 直接调用

```python
from 前端.新界面.主界面 import 主界面

class GameController:
    def __init__(self):
        self.config = 主界面.get_game_config()
    
    def get_system_config(self):
        return self.config.get("系统设置", {})
    
    def get_accounts(self):
        return self.config.get("账号设置", [])
    
    def get_active_accounts(self):
        accounts = self.get_accounts()
        return [acc for acc in accounts if acc.get("挂机")]
```

### 5.2 文件读取

```python
import json
from pathlib import Path

class GameController:
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = Path(__file__).parent.parent / "output" / "game_config.json"
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
```

---

## 六、配置文件位置

| 文件 | 路径 | 说明 |
|------|------|------|
| 用户配置 | `前端/新界面/配置/user_config.json` | 用户设置原始数据 |
| 游戏配置 | `output/game_config.json` | 转换后的游戏控制配置 |

---

**文档版本**: v1.0.0  
**更新日期**: 2026-03-22
