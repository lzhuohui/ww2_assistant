# -*- coding: utf-8 -*-

"""
模块名称：注册界面.py
模块功能：注册授权管理界面

职责：
- 注册信息管理（用户名称、设备码、注册状态）
- 套餐选择（基础包、扩展包）
- 价格预估
- 复制注册信息
- 授权码激活

不负责：
- 数据存储
- 界面布局（由界面容器负责）
"""

import flet as ft
from typing import Callable, Dict, Any

from 设置界面.层级0_数据管理.配置管理 import ConfigManager
from 设置界面.层级0_数据管理.授权管理.设备识别 import DeviceIdentifier
from 设置界面.层级0_数据管理.授权管理.加密工具 import CryptoUtils
from 设置界面.层级4_复合模块.信息卡片 import InfoCard
from 设置界面.层级3_功能卡片.界面容器 import InterfaceContainer
from 设置界面.层级5_基础模块.方案选择器 import SchemeSelector


class RegisterInterface:
    """注册界面 - V3版本"""
    
    INTERFACE_NAME = "注册界面"
    INTERFACE_TITLE = "注册管理"
    INTERFACE_HINT = "注册信息、购买授权、联系方式"
    
    def __init__(self, page: ft.Page, config_manager: ConfigManager, on_scheme_change: Callable[[str], None] = None):
        self._page = page
        self._config_manager = config_manager
        self._on_scheme_change = on_scheme_change
        self._info_card = InfoCard(page, config_manager)
        self._interface_container = InterfaceContainer(page, config_manager)
        self._cards: Dict[str, ft.Container] = {}
        self._container: ft.Container = None
        self._username_input: ft.TextField = None
        self._license_input: ft.TextField = None
        self._device_code_text: ft.Text = None
        self._status_text: ft.Text = None
        self._basic_selector: SchemeSelector = None
        self._extension_selector: SchemeSelector = None
        self._basic_value: str = "月卡"
        self._extension_value: str = "无"
        self._basic_prices: Dict[str, int] = {}
        self._extension_prices: Dict[str, int] = {}
        self._price_text: ft.Text = None
        self._row_spacing: int = 2
        self._device_code: str = ""
    
    def build(self) -> ft.Container:
        """构建注册界面"""
        theme_colors = self._config_manager.get_theme_colors()
        
        self._load_layout_config()
        
        card_names = self._config_manager.get_card_names(self.INTERFACE_NAME)
        
        cards = []
        for card_name in card_names:
            card_info = self._config_manager.get_card_info(self.INTERFACE_NAME, card_name)
            controls = self._config_manager.get_controls(self.INTERFACE_NAME, card_name)
            card_info["控件列表"] = controls if controls else []
            
            if card_name == "注册信息":
                card = self._build_register_info_card(card_info, theme_colors)
            elif card_name == "购买授权":
                card = self._build_license_card(card_info, theme_colors)
            else:
                card = self._info_card.create(
                    interface=self.INTERFACE_NAME,
                    card=card_name,
                    card_info=card_info,
                    theme_colors=theme_colors,
                )
            
            cards.append(card)
            self._cards[card_name] = card
        
        self._container = self._interface_container.create(
            title=self.INTERFACE_TITLE,
            hint=self.INTERFACE_HINT,
            cards=cards,
            on_scheme_change=self._on_scheme_change,
        )
        
        return self._container
    
    def _load_layout_config(self):
        """加载界面布局配置"""
        try:
            layout_config = self._config_manager._data.load_interface_config(self.INTERFACE_NAME)
            if layout_config and "界面布局" in layout_config:
                self._row_spacing = layout_config["界面布局"].get("row_spacing", 2)
        except:
            self._row_spacing = 2
    
    def _build_register_info_card(self, card_info: Dict, theme_colors: Dict) -> ft.Container:
        """构建注册信息卡片"""
        accent = theme_colors.get("accent", "#0078D4")
        text_primary = theme_colors.get("text_primary", "#FFFFFF")
        text_secondary = theme_colors.get("text_secondary", "#B0B0B0")
        bg_card = theme_colors.get("bg_card", "#2D2D2D")
        border_color = theme_colors.get("border", "#3D3D3D")
        
        icon_size = self._info_card.get_icon_size()
        title_size = self._info_card.get_title_size()
        info_size = self._info_card.get_info_size()
        left_width = self._info_card.get_left_width()
        padding = self._config_manager.get_ui_config("卡片开关", "内边距") or 16
        card_height = self._config_manager.get_card_height(self.INTERFACE_NAME, "注册信息")
        card_row_spacing = card_info.get("卡片信息", {}).get("row_spacing", self._row_spacing)
        
        prefs = self._config_manager._data.load_user_preference()
        user_info = prefs.get("用户信息", {})
        username = user_info.get("username", "试用用户")
        status = user_info.get("status", "试用期")
        
        self._device_code = user_info.get("device_code", "")
        if not self._device_code:
            device_identifier = DeviceIdentifier()
            raw_device_id = device_identifier.get_device_id()
            encrypted_id = CryptoUtils.encrypt(raw_device_id)
            self._device_code = encrypted_id[:16].upper()
            self._device_code = f"{self._device_code[:4]}-{self._device_code[4:8]}-{self._device_code[8:12]}-{self._device_code[12:16]}"
            if "用户信息" not in prefs:
                prefs["用户信息"] = {}
            prefs["用户信息"]["device_code"] = self._device_code
            prefs["用户信息"]["_device_hash"] = CryptoUtils.sign(raw_device_id)
            self._config_manager._data.save_user_preference(prefs)
        
        icon_control = ft.Icon(ft.Icons.PERSON, size=icon_size, color=accent)
        title_text = ft.Text("注册信息", size=title_size, weight=ft.FontWeight.BOLD, color=text_primary)
        
        self._username_input = ft.TextField(
            value=username,
            text_size=info_size,
            color=text_primary,
            border_color=border_color,
            focused_border_color=accent,
            content_padding=ft.Padding.symmetric(horizontal=8, vertical=4),
            height=30,
            width=200,
            on_change=self._on_username_change,
            disabled=(status != "试用期"),
        )
        
        self._device_code_text = ft.Text(self._device_code, size=info_size, color=text_primary, width=200, no_wrap=True)
        self._status_text = ft.Text(status, size=info_size, color=accent if status == "试用期" else text_primary, width=60)
        
        basic_options = []
        extension_options = []
        self._basic_prices = {}
        self._extension_prices = {}
        
        controls = card_info.get("控件列表", [])
        for ctrl in controls:
            if ctrl.get("id") == "基础包":
                self._basic_value = ctrl.get("value", "月卡")
                for opt in ctrl.get("options", []):
                    if isinstance(opt, dict):
                        text = opt.get("text", "")
                        price = opt.get("price", 0)
                        basic_options.append({"text": text, "value": text})
                        self._basic_prices[text] = price
            elif ctrl.get("id") == "扩展包":
                self._extension_value = ctrl.get("value", "无")
                for opt in ctrl.get("options", []):
                    if isinstance(opt, dict):
                        text = opt.get("text", "")
                        price = opt.get("price", 0)
                        extension_options.append({"text": text, "value": text})
                        self._extension_prices[text] = price
        
        initial_price = self._basic_prices.get(self._basic_value, 0) + self._extension_prices.get(self._extension_value, 0)
        self._price_text = ft.Text(f"{initial_price}元", size=info_size, color=accent, weight=ft.FontWeight.BOLD)
        
        def on_basic_change(value: str):
            self._basic_value = value
            self._update_price()
        
        def on_extension_change(value: str):
            self._extension_value = value
            self._update_price()
        
        self._basic_selector = SchemeSelector(self._page, self._config_manager)
        self._extension_selector = SchemeSelector(self._page, self._config_manager)
        
        basic_container = self._basic_selector.create(
            options=basic_options,
            current_value=self._basic_value,
            on_change=on_basic_change,
            width=200,
            height=30,
        )
        
        extension_container = self._extension_selector.create(
            options=extension_options,
            current_value=self._extension_value,
            on_change=on_extension_change,
            width=200,
            height=30,
        )
        
        hint_text = ft.Text(
            "确认以上信息后，请复制并联系作者获取授权码",
            size=info_size - 2,
            color=text_secondary,
        )
        
        async def on_copy_info(e):
            info_text = f"""【注册信息】
注册名称: {self._username_input.value or "试用用户"}
设备码: {self._device_code}
注册状态: {self._status_text.value}
基础包: {self._basic_value}({self._basic_prices.get(self._basic_value, 0)}元)
扩展包: {self._extension_value}({self._extension_prices.get(self._extension_value, 0)}元)
合计总价: {self._price_text.value}"""
            await ft.Clipboard().set(info_text)
            self._show_snackbar("已复制注册信息")
        
        copy_info_btn = ft.IconButton(
            icon=ft.Icons.CONTENT_COPY,
            icon_size=16,
            icon_color=text_secondary,
            tooltip="复制注册信息",
            on_click=on_copy_info,
            style=ft.ButtonStyle(padding=4),
        )
        
        col1_width = 280
        col2_width = 265
        col3_width = 110
        
        row1 = ft.Row([
            ft.Container(
                content=ft.Row([
                    ft.Text("注册名:", size=info_size, color=text_secondary, width=70),
                    self._username_input,
                ], spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                width=col1_width,
            ),
            ft.Container(
                content=ft.Row([
                    ft.Text("设备码:", size=info_size, color=text_secondary, width=55),
                    self._device_code_text,
                ], spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                width=col2_width,
            ),
            ft.Container(
                content=ft.Row([
                    ft.Text("状态:", size=info_size, color=text_secondary, width=40),
                    self._status_text,
                ], spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                width=col3_width,
            ),
        ], spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        row2 = ft.Row([
            ft.Container(
                content=ft.Row([
                    ft.Text("基础包:", size=info_size, color=text_secondary, width=70),
                    basic_container,
                ], spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                width=col1_width,
            ),
            ft.Container(
                content=ft.Row([
                    ft.Text("扩展包:", size=info_size, color=text_secondary, width=55),
                    extension_container,
                ], spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                width=col2_width,
            ),
            ft.Container(
                content=ft.Row([
                    ft.Text("总价:", size=info_size, color=text_secondary, width=40),
                    self._price_text,
                ], spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                width=col3_width,
            ),
        ], spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        row3 = ft.Row([
            hint_text,
            copy_info_btn,
        ], spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        info_rows = [row1, row2, row3]
        
        left_content = ft.Column([
            icon_control,
            ft.Container(height=4),
            title_text,
        ], spacing=0, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        left_container = ft.Container(
            content=left_content,
            width=left_width - 2,
            padding=ft.Padding(padding, 0, padding, 0),
            alignment=ft.alignment.Alignment(0, 0.5),
        )
        
        divider_height = card_height - padding
        divider_width = self._config_manager.get_ui_config("卡片开关", "分割线宽度") or 2
        
        divider_container = ft.Container(
            content=ft.Container(width=divider_width, height=divider_height, bgcolor=accent),
            height=divider_height,
            alignment=ft.alignment.Alignment(0, 0.5),
        )
        
        right_content = ft.Column(
            info_rows,
            spacing=card_row_spacing,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        
        right_container = ft.Container(
            content=right_content,
            expand=True,
            padding=ft.Padding(8, 0, padding, 0),
            alignment=ft.alignment.Alignment(-1, 0.5),
        )
        
        card_row = ft.Row([
            left_container,
            divider_container,
            right_container,
        ], spacing=0, vertical_alignment=ft.CrossAxisAlignment.CENTER, height=card_height)
        
        return ft.Container(
            content=card_row,
            bgcolor=bg_card,
            border=ft.Border.all(1, border_color),
            border_radius=self._config_manager.get_radius("中") or 8,
        )
    
    def _build_license_card(self, card_info: Dict, theme_colors: Dict) -> ft.Container:
        """构建购买授权卡片"""
        accent = theme_colors.get("accent", "#0078D4")
        text_primary = theme_colors.get("text_primary", "#FFFFFF")
        text_secondary = theme_colors.get("text_secondary", "#B0B0B0")
        bg_card = theme_colors.get("bg_card", "#2D2D2D")
        border_color = theme_colors.get("border", "#3D3D3D")
        
        icon_size = self._info_card.get_icon_size()
        title_size = self._info_card.get_title_size()
        info_size = self._info_card.get_info_size()
        left_width = self._info_card.get_left_width()
        padding = self._config_manager.get_ui_config("卡片开关", "内边距") or 16
        card_height = self._config_manager.get_card_height(self.INTERFACE_NAME, "购买授权")
        card_row_spacing = card_info.get("卡片信息", {}).get("row_spacing", self._row_spacing)
        
        icon_control = ft.Icon(ft.Icons.KEY, size=icon_size, color=accent)
        title_text = ft.Text("购买授权", size=title_size, weight=ft.FontWeight.BOLD, color=text_primary)
        
        self._license_input = ft.TextField(
            value="",
            text_size=info_size,
            color=text_primary,
            border_color=border_color,
            focused_border_color=accent,
            content_padding=ft.Padding.symmetric(horizontal=8, vertical=4),
            height=30,
            width=200,
            hint_text="XXXX-XXXX-XXXX-XXXX",
        )
        
        activate_btn = ft.IconButton(
            icon=ft.Icons.KEY,
            icon_size=20,
            icon_color=text_secondary,
            tooltip="激活授权",
            on_click=self._on_activate,
            style=ft.ButtonStyle(padding=4),
        )
        
        hint_text = ft.Text(
            "提示: 授权码格式为 XXXX-XXXX-XXXX-XXXX",
            size=info_size - 2,
            color=text_secondary,
        )
        
        info_rows = [
            ft.Row([
                ft.Text("授权码:", size=info_size, color=text_secondary, width=70),
                self._license_input,
                activate_btn,
            ], spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Row([
                ft.Container(width=70),
                hint_text,
            ], spacing=0),
        ]
        
        left_content = ft.Column([
            icon_control,
            ft.Container(height=4),
            title_text,
        ], spacing=0, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        left_container = ft.Container(
            content=left_content,
            width=left_width - 2,
            padding=ft.Padding(padding, 0, padding, 0),
            alignment=ft.alignment.Alignment(0, 0.5),
        )
        
        divider_height = card_height - padding
        divider_width = self._config_manager.get_ui_config("卡片开关", "分割线宽度") or 2
        
        divider_container = ft.Container(
            content=ft.Container(width=divider_width, height=divider_height, bgcolor=accent),
            height=divider_height,
            alignment=ft.alignment.Alignment(0, 0.5),
        )
        
        right_content = ft.Column(
            info_rows,
            spacing=card_row_spacing,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        
        right_container = ft.Container(
            content=right_content,
            expand=True,
            padding=ft.Padding(8, 0, padding, 0),
            alignment=ft.alignment.Alignment(-1, 0.5),
        )
        
        card_row = ft.Row([
            left_container,
            divider_container,
            right_container,
        ], spacing=0, vertical_alignment=ft.CrossAxisAlignment.CENTER, height=card_height)
        
        return ft.Container(
            content=card_row,
            bgcolor=bg_card,
            border=ft.Border.all(1, border_color),
            border_radius=self._config_manager.get_radius("中") or 8,
        )
    
    def _on_username_change(self, e):
        """注册名称变更"""
        prefs = self._config_manager._data.load_user_preference()
        if "用户信息" not in prefs:
            prefs["用户信息"] = {}
        prefs["用户信息"]["username"] = e.control.value
        self._config_manager._data.save_user_preference(prefs)
    
    def _update_price(self):
        """更新价格显示"""
        basic_price = self._basic_prices.get(self._basic_value, 0)
        extension_price = self._extension_prices.get(self._extension_value, 0)
        total = basic_price + extension_price
        self._price_text.value = f"{total}元"
        self._price_text.update()
    
    def _on_activate(self, e):
        """激活授权码"""
        license_code = self._license_input.value.strip() if self._license_input.value else ""
        
        if not license_code:
            self._show_snackbar("请输入授权码")
            return
        
        if len(license_code) != 19 or license_code.count("-") != 3:
            self._show_snackbar("授权码格式错误，应为 XXXX-XXXX-XXXX-XXXX")
            return
        
        result = self._verify_license(license_code)
        
        if result.get("valid"):
            self._show_snackbar(f"激活成功！{result.get('message', '')}")
            self._update_status(result)
        else:
            self._show_snackbar(f"激活失败：{result.get('message', '授权码无效')}")
    
    def _verify_license(self, license_code: str) -> Dict:
        """验证授权码"""
        return {
            "valid": False,
            "message": "授权验证功能待实现",
        }
    
    def _update_status(self, result: Dict):
        """更新注册状态显示"""
        prefs = self._config_manager._data.load_user_preference()
        if "用户信息" not in prefs:
            prefs["用户信息"] = {}
        
        license_type = result.get("type", "basic")
        if license_type == "basic":
            prefs["用户信息"]["status"] = "已授权"
            prefs["用户信息"]["remaining_days"] = f"{result.get('days', 0)}天"
        else:
            prefs["用户信息"]["status"] = "已授权"
            prefs["用户信息"]["remaining_days"] = f"{result.get('times', 0)}次"
        
        self._config_manager._data.save_user_preference(prefs)
        
        if self._status_text:
            self._status_text.value = prefs["用户信息"]["status"]
            self._status_text.update()
    
    def _show_snackbar(self, message: str):
        """显示提示消息"""
        self._page.show_dialog(ft.SnackBar(ft.Text(message), duration=2000))
    
    def destroy(self):
        """销毁界面"""
        self._info_card.destroy()
        self._cards.clear()
        self._container = None
        self._username_input = None
        self._license_input = None
        self._device_code_text = None
        self._status_text = None
        self._basic_selector = None
        self._extension_selector = None
        self._price_text = None


if __name__ == "__main__":
    def main(page: ft.Page):
        from 设置界面.层级0_数据管理.配置管理 import ConfigManager
        config_manager = ConfigManager()
        InfoCard.set_config_manager(config_manager)
        
        interface = RegisterInterface(page, config_manager)
        page.add(interface.build())
    
    ft.app(target=main)
