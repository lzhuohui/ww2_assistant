---
name: 04-Flet前端规范-基础
description: Flet框架基础规范
globs: ["gui/**/*.py", "ui/**/*.py", "**/*view*.py", "**/*page*.py"]
---

# Flet前端开发规范（基础）

## 技术栈
- 前端框架：Flet（基于Flutter的Python框架）
- 布局使用Column、Row、Container等控件
- 样式通过控件的属性直接设置，或定义主题

## 目录结构
```
gui/
├── main.py                 # 应用入口
├── pages/                  # 页面模块
│   ├── home_page.py       # 主页
│   ├── settings_page.py   # 设置页
│   └── monitor_page.py    # 监控页
├── components/             # 可复用组件
│   ├── game_status_card.py # 游戏状态卡片
│   └── log_viewer.py      # 日志查看器
└── theme.py                # 主题配置（颜色、字体）
```

## 命名规范
- 页面类：`HomePage`（继承`ft.View`或`ft.Column`）
- 组件类：`GameStatusCard`（继承`ft.UserControl`或`ft.Container`）
- 控件变量：描述性名称 + 类型（如`start_button`, `status_text`）

## 界面要求
- **监控页**：必须包含游戏状态显示、运行日志、截图预览（可选）
- **设置页**：配置项分组（游戏连接、脚本参数、热键），提供"保存"和"重置"
- 配置文件使用JSON/YAML，保存在`config/`目录
- 使用`ft.Page`的`update()`方法刷新UI，避免在非主线程直接操作
