# 核心接口目录说明

## 目录结构

```
核心接口/
├── __init__.py
├── 主题提供者.py
├── 配置提供者.py
├── 状态提供者.py
├── 控件构建器.py
├── 组件基类.py
└── README.md
```

## 功能说明

核心接口目录包含了系统的核心服务和接口，为整个前端系统提供基础功能支持。

### 1. 主题提供者.py

**功能**：提供主题相关的统一访问接口，负责颜色和尺寸的管理。

**主要方法**：
- `initialize(config)`: 初始化主题提供者
- `get_color(color_key)`: 获取主题颜色
- `get_size(category, size_key)`: 获取主题尺寸
- `get_theme()`: 获取当前主题配置

**使用场景**：被界面层、组件层、单元层调用，用于获取统一的主题样式。

### 2. 配置提供者.py

**功能**：提供配置管理的统一访问接口，负责配置的加载、获取和设置。

**主要方法**：
- `initialize()`: 初始化配置提供者
- `get_value(card_name, config_key, default)`: 获取配置值
- `set_value(card_name, config_key, value)`: 设置配置值
- `reset_value(card_name, config_key)`: 重置配置值
- `get_all_values(card_name)`: 获取卡片的所有配置值
- `get_card_config(card_name)`: 获取卡片配置
- `get_all_card_configs()`: 获取所有卡片配置

**使用场景**：被界面层、组件层、单元层调用，用于管理和访问配置数据。

### 3. 状态提供者.py

**功能**：提供全局状态管理的统一访问接口，负责状态的存储、获取和更新。

**主要方法**：
- `initialize(initial_state)`: 初始化状态提供者
- `get_state(key, default)`: 获取状态值
- `set_state(key, value)`: 设置状态值
- `remove_state(key)`: 移除状态值
- `clear_state()`: 清空所有状态
- `get_all_state()`: 获取所有状态
- `add_listener(key, listener)`: 添加状态监听器
- `remove_listener(key, listener)`: 移除状态监听器
- `remove_all_listeners(key)`: 移除指定状态的所有监听器

**使用场景**：被界面层、组件层、单元层调用，用于管理全局状态。

### 4. 控件构建器.py

**功能**：提供统一的控件创建接口，负责根据主题和配置创建各种Flet控件。

**主要方法**：
- `create_text(text, size, color, weight)`: 创建文本控件
- `create_button(text, on_click, variant, size)`: 创建按钮控件
- `create_input(label, value, on_change, password)`: 创建输入框控件
- `create_container(content, padding, margin, bgcolor)`: 创建容器控件
- `create_card(content, padding)`: 创建卡片控件
- `create_row(controls, spacing)`: 创建行容器控件
- `create_column(controls, spacing)`: 创建列容器控件
- `create_icon(icon, size, color)`: 创建图标控件

**使用场景**：被界面层、组件层、单元层调用，用于创建统一风格的控件。

### 5. 组件基类.py

**功能**：定义组件的基础接口，规定所有组件应该实现的方法和属性。

**主要类**：
- `ComponentBase`: 组件基类，定义通用接口
- `InteractiveComponent`: 交互式组件基类
- `VisualComponent`: 视觉组件基类

**主要方法**：
- `build()`: 构建控件（抽象方法）
- `get_control()`: 获取构建的控件
- `set_state(key, value)`: 设置状态
- `get_state(key, default)`: 获取状态
- `get_all_state()`: 获取所有状态
- `clear_state()`: 清空状态
- `register_event_handler(event_name, handler)`: 注册事件处理器
- `unregister_event_handler(event_name)`: 取消注册事件处理器
- `trigger_event(event_name, *args, **kwargs)`: 触发事件
- `update()`: 更新控件
- `dispose()`: 销毁组件
- `init()`: 初始化组件
- `on_mount()`: 组件挂载时调用
- `on_unmount()`: 组件卸载时调用

**使用场景**：被组件继承，作为所有组件的基础。

## 使用示例

### 主题提供者使用示例

```python
from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.用户设置界面.配置.界面配置 import 界面配置

# 初始化主题提供者
配置 = 界面配置()
ThemeProvider.initialize(配置)

# 获取颜色
primary_color = ThemeProvider.get_color("primary")

# 获取尺寸
font_size = ThemeProvider.get_size("字体", "font_size_md")
```

### 配置提供者使用示例

```python
from 前端.用户设置界面.核心接口.配置提供者 import ConfigProvider

# 初始化配置提供者
ConfigProvider.initialize()

# 获取配置值
value = ConfigProvider.get_value("测试卡片", "test_key", "默认值")

# 设置配置值
ConfigProvider.set_value("测试卡片", "test_key", "新值")
```

### 状态提供者使用示例

```python
from 前端.用户设置界面.核心接口.状态提供者 import StateProvider

# 初始化状态提供者
StateProvider.initialize({"current_page": "首页"})

# 获取状态
page = StateProvider.get_state("current_page")

# 设置状态
StateProvider.set_state("current_page", "设置页")

# 添加监听器
def page_change_listener(new_value, old_value):
    print(f"页面变化: {old_value} -> {new_value}")

StateProvider.add_listener("current_page", page_change_listener)
```

### 控件构建器使用示例

```python
from 前端.用户设置界面.核心接口.控件构建器 import ControlBuilder

# 创建文本控件
text = ControlBuilder.create_text("测试文本", size="lg", color="text_primary")

# 创建按钮控件
def on_click(e):
    print("按钮被点击")

button = ControlBuilder.create_button("测试按钮", on_click=on_click)

# 创建容器控件
container = ControlBuilder.create_container(
    content=text,
    padding=ft.Padding.all(16)
)
```

### 组件基类使用示例

```python
from 前端.用户设置界面.核心接口.组件基类 import InteractiveComponent
import flet as ft

class MyButton(InteractiveComponent):
    def __init__(self, text):
        super().__init__()
        self._text = text
    
    def build(self):
        def on_click(e):
            self.trigger_event("click", e)
        
        return ft.Button(
            content=ft.Text(self._text),
            on_click=on_click,
            disabled=not self._is_enabled
        )

# 使用自定义组件
button = MyButton("点击我")

# 注册事件处理器
def on_button_click(e):
    print("按钮被点击")

button.register_event_handler("click", on_button_click)

# 获取控件
control = button.get_control()
```

## 开发指南

1. **新增核心接口**：当需要添加新的核心功能时，应该在核心接口目录中创建新的接口文件。

2. **修改现有接口**：修改现有接口时，应确保向后兼容，避免破坏现有代码。

3. **测试**：每个核心接口文件都应该包含调试逻辑，确保功能正常。

4. **文档**：添加新功能时，应更新此README文件，确保文档与代码保持同步。

## 注意事项

1. 核心接口是系统的基础，修改时应谨慎，确保不会影响其他模块。

2. 核心接口应保持简洁，只提供必要的功能，避免过度设计。

3. 核心接口应遵循统一的设计风格和命名规范。

4. 核心接口应提供清晰的文档和使用示例，便于其他开发者使用。