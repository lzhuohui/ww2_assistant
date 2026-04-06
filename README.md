# 二战风云 - Flet应用

## 项目简介

这是一个基于Flet框架开发的二战风云游戏辅助工具设置界面。

## 功能特性

- ✅ 多账号管理
- ✅ 自动打野
- ✅ 建筑升级
- ✅ 任务执行
- ✅ 策略加速
- ✅ 个性化主题

## 本地运行

```bash
# 安装依赖
pip install flet

# 运行应用
python main.py
```

## 打包APK

### 方法1：GitHub Actions自动打包（推荐）

**步骤：**

1. **推送代码到GitHub**
   ```bash
   git add .
   git commit -m "准备打包APK"
   git push
   ```

2. **触发自动打包**
   - 方式1：推送到main/master分支自动触发
   - 方式2：在GitHub仓库页面 → Actions → Build APK → Run workflow

3. **下载APK文件**
   - 在GitHub仓库页面 → Actions
   - 点击最新的workflow运行记录
   - 在Artifacts部分下载`app-release`
   - 解压后得到`app-release.apk`文件

**优点：**
- ✅ 完全免费
- ✅ 无需本地环境配置
- ✅ 自动化流程
- ✅ 可反复打包

### 方法2：本地打包

**前提条件：**
- 安装Android Studio
- 配置Android SDK
- 安装Flutter SDK

**步骤：**
```bash
flet build apk
```

APK文件位置：`build/apk/release/app-release.apk`

## 项目结构

```
二战风云/
├── main.py                    # 应用入口
├── 设置界面/
│   ├── 层级0_数据管理/         # 数据管理层
│   ├── 层级1_主入口/           # 主入口
│   ├── 层级2_功能界面/         # 功能界面层
│   ├── 层级3_功能卡片/         # 功能卡片层
│   ├── 层级4_复合模块/         # 复合模块层
│   └── 层级5_基础模块/         # 基础模块层
└── .github/
    └── workflows/
        └── build-apk.yml      # GitHub Actions配置
```

## 技术栈

- **前端框架**: Flet (基于Flutter)
- **编程语言**: Python 3.11+
- **UI组件**: Material Design
- **数据存储**: YAML配置文件

## 开发指南

### 代码规范

- 遵循PEP 8编码规范
- 使用类型注解
- 添加详细的文档字符串

### 模块化设计

项目采用5层架构设计：
- 层级0：数据管理
- 层级1：主入口
- 层级2：功能界面
- 层级3：功能卡片
- 层级4：复合模块
- 层级5：基础模块

## 许可证

本项目仅供学习和研究使用。

## 联系方式

如有问题或建议，请提交Issue。
