# -*- coding: utf-8 -*-
"""
组件基类 - 核心接口

设计思路:
    定义组件的基础接口，规定所有组件应该实现的方法和属性。

功能:
    1. 基础接口：定义组件的通用接口
    2. 状态管理：提供状态管理的通用方法
    3. 事件处理：提供事件处理的通用方法
    4. 生命周期：提供组件生命周期的通用方法

数据来源:
    无特定数据来源，主要定义接口规范。

使用场景:
    被组件继承，作为所有组件的基础。

可独立运行调试: python 组件基类.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from abc import ABC, abstractmethod
from typing import Any, Dict, Callable, Optional

import flet as ft


class ComponentBase(ABC):
    """组件基类"""
    
    def __init__(self):
        """
        初始化组件
        """
        self._state: Dict[str, Any] = {}
        self._event_handlers: Dict[str, Callable] = {}
        self._control: Optional[ft.Control] = None
    
    @abstractmethod
    def build(self) -> ft.Control:
        """
        构建控件
        
        返回:
            ft.Control: 构建的Flet控件
        """
        pass
    
    def get_control(self) -> Optional[ft.Control]:
        """
        获取构建的控件
        
        返回:
            Optional[ft.Control]: 构建的Flet控件
        """
        if not self._control:
            self._control = self.build()
        return self._control
    
    def set_state(self, key: str, value: Any):
        """
        设置状态
        
        参数:
            key: 状态键
            value: 状态值
        """
        self._state[key] = value
        self.update()
    
    def get_state(self, key: str, default: Any = None) -> Any:
        """
        获取状态
        
        参数:
            key: 状态键
            default: 默认值
        
        返回:
            Any: 状态值
        """
        return self._state.get(key, default)
    
    def get_all_state(self) -> Dict[str, Any]:
        """
        获取所有状态
        
        返回:
            Dict[str, Any]: 所有状态
        """
        return self._state.copy()
    
    def clear_state(self):
        """
        清空状态
        """
        self._state.clear()
        self.update()
    
    def register_event_handler(self, event_name: str, handler: Callable):
        """
        注册事件处理器
        
        参数:
            event_name: 事件名称
            handler: 事件处理器
        """
        self._event_handlers[event_name] = handler
    
    def unregister_event_handler(self, event_name: str):
        """
        取消注册事件处理器
        
        参数:
            event_name: 事件名称
        """
        if event_name in self._event_handlers:
            del self._event_handlers[event_name]
    
    def trigger_event(self, event_name: str, *args, **kwargs):
        """
        触发事件
        
        参数:
            event_name: 事件名称
            *args: 位置参数
            **kwargs: 关键字参数
        """
        if event_name in self._event_handlers:
            self._event_handlers[event_name](*args, **kwargs)
    
    def update(self):
        """
        更新控件
        """
        control = self.get_control()
        if control and hasattr(control, "update"):
            try:
                # 尝试更新控件，只有当控件已添加到页面时才会成功
                control.update()
            except RuntimeError:
                # 控件未添加到页面，跳过更新
                pass
    
    def dispose(self):
        """
        销毁组件
        """
        self._state.clear()
        self._event_handlers.clear()
        self._control = None
    
    def init(self):
        """
        初始化组件
        """
        pass
    
    def on_mount(self):
        """
        组件挂载时调用
        """
        pass
    
    def on_unmount(self):
        """
        组件卸载时调用
        """
        pass


class InteractiveComponent(ComponentBase):
    """交互式组件基类"""
    
    def __init__(self):
        """
        初始化交互式组件
        """
        super().__init__()
        self._is_enabled = True
        self._is_focused = False
    
    def set_enabled(self, enabled: bool):
        """
        设置是否启用
        
        参数:
            enabled: 是否启用
        """
        self._is_enabled = enabled
        self.update()
    
    def get_enabled(self) -> bool:
        """
        获取是否启用
        
        返回:
            bool: 是否启用
        """
        return self._is_enabled
    
    def set_focused(self, focused: bool):
        """
        设置是否聚焦
        
        参数:
            focused: 是否聚焦
        """
        self._is_focused = focused
        self.update()
    
    def get_focused(self) -> bool:
        """
        获取是否聚焦
        
        返回:
            bool: 是否聚焦
        """
        return self._is_focused
    
    def focus(self):
        """
        聚焦控件
        """
        control = self.get_control()
        if control and hasattr(control, "focus"):
            control.focus()
    
    def unfocus(self):
        """
        取消聚焦控件
        """
        control = self.get_control()
        if control and hasattr(control, "unfocus"):
            control.unfocus()


class VisualComponent(ComponentBase):
    """视觉组件基类"""
    
    def __init__(self):
        """
        初始化视觉组件
        """
        super().__init__()
        self._visibility = True
        self._opacity = 1.0
    
    def set_visibility(self, visible: bool):
        """
        设置可见性
        
        参数:
            visible: 是否可见
        """
        self._visibility = visible
        self.update()
    
    def get_visibility(self) -> bool:
        """
        获取可见性
        
        返回:
            bool: 是否可见
        """
        return self._visibility
    
    def set_opacity(self, opacity: float):
        """
        设置透明度
        
        参数:
            opacity: 透明度 (0.0-1.0)
        """
        self._opacity = max(0.0, min(1.0, opacity))
        self.update()
    
    def get_opacity(self) -> float:
        """
        获取透明度
        
        返回:
            float: 透明度
        """
        return self._opacity


# ==================== 示例实现 ====================
class ExampleButton(InteractiveComponent):
    """示例按钮实现"""
    
    def __init__(self, text: str = "Button"):
        """
        初始化示例按钮
        
        参数:
            text: 按钮文本
        """
        super().__init__()
        self._text = text
    
    def build(self) -> ft.Button:
        """
        构建按钮控件
        """
        def on_click(e):
            self.trigger_event("click", e)
        
        return ft.Button(
            content=ft.Text(self._text),
            on_click=on_click,
            disabled=not self._is_enabled
        )
    
    def set_text(self, text: str):
        """
        设置按钮文本
        
        参数:
            text: 按钮文本
        """
        self._text = text
        self._control = None  # 强制重新构建
        self.update()
    
    def get_text(self) -> str:
        """
        获取按钮文本
        
        返回:
            str: 按钮文本
        """
        return self._text


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    # 1. 测试示例组件
    print("=== 测试示例组件 ===")
    button = ExampleButton("测试按钮")
    
    # 2. 获取控件
    control = button.get_control()
    print(f"创建的按钮控件: {control}")
    
    # 3. 测试状态管理
    print("\n=== 测试状态管理 ===")
    button.set_state("count", 0)
    print(f"初始状态: {button.get_state('count')}")
    
    # 4. 测试事件处理
    print("\n=== 测试事件处理 ===")
    def on_button_click(e):
        count = button.get_state("count", 0)
        button.set_state("count", count + 1)
        print(f"按钮被点击，计数: {button.get_state('count')}")
    
    button.register_event_handler("click", on_button_click)
    
    # 5. 模拟点击事件
    print("模拟点击事件...")
    # 创建一个模拟的事件对象
    class MockEvent:
        pass
    e = MockEvent()
    button.trigger_event("click", e)
    button.trigger_event("click", e)
    
    # 6. 测试启用/禁用
    print("\n=== 测试启用/禁用 ===")
    print(f"初始启用状态: {button.get_enabled()}")
    button.set_enabled(False)
    print(f"禁用后状态: {button.get_enabled()}")
    button.set_enabled(True)
    print(f"重新启用后状态: {button.get_enabled()}")
    
    # 7. 测试文本设置
    print("\n=== 测试文本设置 ===")
    print(f"初始文本: {button.get_text()}")
    button.set_text("新按钮文本")
    print(f"新文本: {button.get_text()}")
    
    # 8. 测试获取状态
    print("\n=== 测试获取状态 ===")
    print(f"最终计数状态: {button.get_state('count')}")
    print(f"所有状态: {button.get_all_state()}")
    
    # 9. 测试销毁
    print("\n=== 测试销毁 ===")
    button.dispose()
    print("按钮已销毁")