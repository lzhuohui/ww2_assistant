# Windows 11 设置界面设计规范

## 一、布局结构

### 1.1 整体布局

| 区域 | 宽度 | 说明 |
|------|------|------|
| 左侧导航栏 | 280-320px | 固定宽度 |
| 右侧内容区 | 自适应 | 填充剩余空间 |
| 分割线 | 1px | 导航与内容分隔 |

### 1.2 导航栏结构

```
导航栏布局：
├── 用户信息卡片 (80px高度)
├── 间距 (10px)
├── 导航按钮列表 (自适应)
│   └── 每个按钮 (40-48px高度)
└── 功能按钮列表
```

### 1.3 间距规范

| 类型 | 值 | 用途 |
|------|-----|------|
| xs | 4px | 紧凑间距 |
| sm | 8px | 小间距 |
| md | 12px | 中等间距 |
| lg | 16px | 大间距 |

---

## 二、色彩系统

### 2.1 深色主题

| 名称 | 色值 | 用途 |
|------|------|------|
| bg_primary | #202020 | 主背景 |
| bg_secondary | #252525 | 次级背景 |
| bg_card | #2D2D2D | 卡片背景 |
| bg_selected | #4D4D4D | 选中背景 |
| bg_hover | #3D3D3D | 悬停背景 |
| text_primary | #FFFFFF | 主文字 |
| text_secondary | #C5C5C5 | 次级文字 |
| accent | #0078D4 | 强调色 |

### 2.2 浅色主题

| 名称 | 色值 | 用途 |
|------|------|------|
| bg_primary | #F3F3F3 | 主背景 |
| bg_secondary | #FFFFFF | 次级背景 |
| bg_card | #FFFFFF | 卡片背景 |
| bg_selected | #0078D4 | 选中背景 |
| bg_hover | #E5E5E5 | 悬停背景 |
| text_primary | #1A1A1A | 主文字 |
| text_secondary | #666666 | 次级文字 |
| accent | #0078D4 | 强调色 |

---

## 三、字体样式

### 3.1 字体家族

```
Segoe UI Variable, Segoe UI, system-ui, sans-serif
```

### 3.2 字号层级

| 层级 | 字号 | 用途 |
|------|------|------|
| 标题 | 16-20px | 页面标题 |
| 正文 | 14px | 主要内容 |
| 小字 | 12-13px | 辅助信息 |
| 微型 | 10-11px | 标签、提示 |

---

## 四、圆角设计

| 类型 | 值 | 用途 |
|------|-----|------|
| radius_sm | 4px | 小控件、标签 |
| radius_md | 8px | 按钮、输入框、卡片 |
| radius_lg | 12px | 大容器、面板 |

---

## 五、动画效果

### 5.1 时长规范

| 类型 | 值 | 用途 |
|------|-----|------|
| fast | 167ms | 快速反馈（悬停、选中） |
| normal | 250ms | 常规过渡（展开、收起） |
| slow | 350ms | 复杂动画（页面切换） |

### 5.2 缓动函数

```python
ft.AnimationCurve.EASE_OUT  # 默认缓动
ft.AnimationCurve.EASE_IN_OUT  # 平滑过渡
```

---

## 六、阴影效果

### 6.1 卡片阴影

```python
ft.BoxShadow(
    spread_radius=0,
    blur_radius=4,
    color="rgba(0, 0, 0, 0.25)",
    offset=ft.Offset(0, 2),
)
```

### 6.2 悬浮阴影

```python
ft.BoxShadow(
    spread_radius=0,
    blur_radius=8,
    color="rgba(0, 0, 0, 0.3)",
    offset=ft.Offset(0, 4),
)
```

---

## 七、控件状态

### 7.1 按钮状态

| 状态 | 背景 | 边框 | 文字 |
|------|------|------|------|
| 默认 | bg_secondary | 无 | text_primary |
| 悬停 | bg_hover | 无 | text_primary |
| 选中 | accent | 无 | #FFFFFF |
| 禁用 | bg_card | 无 | text_hint |

### 7.2 输入框状态

| 状态 | 背景 | 边框 |
|------|------|------|
| 默认 | bg_input | border |
| 聚焦 | bg_input | accent |
| 禁用 | bg_card | 无 |

---

## 八、导航按钮设计

### 8.1 选中效果

Win11风格：背景块从左向右展开

```python
背景块 = ft.Container(
    bgcolor=accent if 选中 else "transparent",
    border_radius=6,
    animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
    width=float("inf") if 选中 else 0,
)
```

### 8.2 悬停效果

未选中时显示半透明背景块

---

## 九、卡片设计

### 9.1 基础卡片

```python
卡片 = ft.Container(
    bgcolor=bg_card,
    border_radius=8,
    padding=16,
    shadow=ft.BoxShadow(...),
)
```

### 9.2 折叠卡片

- 左侧：图标 + 标题 + 分割线
- 右侧：副标题 ↔ 控件切换
- 高度：固定 80px

---

## 十、主题切换

### 10.1 支持主题

- 深色主题（默认）
- 浅色主题

### 10.2 切换逻辑

```python
def 切换主题(主题名称: str):
    配置.切换主题(主题名称)
    # 刷新界面
    页面.update()
```
