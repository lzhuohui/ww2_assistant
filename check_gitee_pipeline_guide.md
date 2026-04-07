# Gitee流水线功能开启检查指南

## 🔍 如何确认"流水线"功能已开启

### 步骤1: 登录Gitee并访问仓库设置

1. **打开浏览器**，访问：**https://gitee.com/lzhuohui/ww2_assistant**
2. **登录你的账号**（如果尚未登录）
3. **点击右上角的"管理"**（仓库设置）

![Gitee管理按钮位置](https://gitee.com/help/_images/project-settings.png)

### 步骤2: 进入功能设置

1. 在左侧菜单中找到 **"功能设置"**
2. 点击进入功能设置页面

![功能设置位置](https://gitee.com/help/_images/feature-settings.png)

### 步骤3: 检查流水线功能

在功能设置页面中，找到 **"流水线"** 选项：

#### ✅ 如果已开启，你会看到：
```
☑ 流水线
   开启后可以在代码仓库进行持续集成/持续部署
```

#### ❌ 如果未开启，你会看到：
```
□ 流水线
   开启后可以在代码仓库进行持续集成/持续部署
```

### 步骤4: 开启流水线功能（如果未开启）

1. **勾选"流水线"复选框**
2. **点击页面底部的"保存"按钮**
3. **等待设置生效**（通常几秒钟）

### 步骤5: 验证流水线功能

开启后，按以下步骤验证：

1. **返回仓库主页**：**https://gitee.com/lzhuohui/ww2_assistant**
2. **检查顶部菜单栏**，应该能看到 **"流水线"** 标签
3. **点击"流水线"标签**，应该能看到构建历史

![流水线菜单位置](https://gitee.com/help/_images/pipeline-tab.png)

## 🎯 快速检查清单

### 检查点1: 菜单栏
- [ ] 顶部菜单是否有"流水线"标签？
- [ ] 点击"流水线"是否能进入页面？

### 检查点2: 流水线页面
- [ ] 是否显示"Build APK for Gitee"工作流？
- [ ] 是否显示构建历史（包括失败的任务）？

### 检查点3: 运行按钮
- [ ] 是否有"运行流水线"按钮？
- [ ] 是否可以手动触发构建？

### 检查点4: 构建状态
- [ ] 是否能查看构建 #7 的详细日志？
- [ ] 是否能查看之前的构建记录？

## 🚨 常见问题及解决方法

### 问题1: 看不到"流水线"菜单
**可能原因**：流水线功能未开启或仓库类型不支持
**解决方法**：
1. 确认仓库是公开仓库（私有仓库可能需要企业版）
2. 确认已登录正确的账号
3. 确认有仓库的管理权限

### 问题2: 点击"流水线"显示404
**可能原因**：功能未正确开启
**解决方法**：
1. 刷新页面
2. 重新开启流水线功能
3. 清除浏览器缓存

### 问题3: 无法保存设置
**可能原因**：权限不足或网络问题
**解决方法**：
1. 确认你是仓库所有者或管理员
2. 检查网络连接
3. 换个浏览器试试

## 📱 截图参考

### 正确的流水线开启状态：
```
仓库设置 → 功能设置
↓
[☑] 流水线
    开启后可以在代码仓库进行持续集成/持续部署
↓
[保存] 按钮
```

### 仓库页面的流水线标签：
```
代码 | 议题 | 合并请求 | 流水线 | Wiki | 设置
```

### 流水线页面内容：
```
运行流水线 [按钮]

工作流列表：
- Build APK for Gitee
- Simple APK Build
- debug-build

构建历史：
#7 失败 修复Gitee工作流的APK文件检查逻辑
#6 失败 修复构建失败问题并添加Gitee专用工作流
...
```

## 🔧 手动检查脚本

运行以下Python脚本来检查本地配置：

```python
# 检查本地工作流文件
import os

def check_workflow_files():
    workflow_dir = ".github/workflows"
    if os.path.exists(workflow_dir):
        print("✅ .github/workflows 目录存在")
        files = os.listdir(workflow_dir)
        for file in files:
            print(f"  📄 {file}")
    else:
        print("❌ .github/workflows 目录不存在")
    
    # 检查具体文件
    required_files = [
        "build-apk-gitee.yml",
        "debug-build.yml",
        "build-apk-simple.yml"
    ]
    
    for file in required_files:
        path = os.path.join(workflow_dir, file)
        if os.path.exists(path):
            print(f"✅ {file} 存在")
        else:
            print(f"❌ {file} 不存在")

check_workflow_files()
```

## 📞 如果仍然有问题

### 情况A: 完全看不到"流水线"选项
1. **确认仓库类型**：必须是公开仓库或企业版私有仓库
2. **联系Gitee客服**：可能有平台限制
3. **使用GitHub Actions替代**：改回GitHub构建

### 情况B: 能看到但无法使用
1. **提供截图**：给我看你的页面截图
2. **检查控制台错误**：按F12查看浏览器控制台
3. **尝试不同浏览器**：Chrome/Firefox/Edge

### 情况C: 已开启但仍失败
1. **查看构建 #7 的详细错误**
2. **运行调试工作流**：Simple APK Build
3. **提供错误日志**：我可以分析具体问题

## 🎯 立即操作

1. **立即访问**：**https://gitee.com/lzhuohui/ww2_assistant/settings**
2. **检查并开启**流水线功能
3. **告诉我结果**：
   - 是否已开启？
   - 能看到"流水线"菜单吗？
   - 能查看构建 #7 的日志吗？

## 💡 备用方案

如果Gitee流水线确实无法使用，我们可以：

### 方案1: 使用GitHub Actions
```bash
# 改回GitHub远程
git remote set-url origin https://github.com/lzhuohui/ww2_assistant.git
git push origin master
```

### 方案2: 本地构建
```bash
# 本地生成APK
python local_build_alternative.py
```

### 方案3: 其他CI/CD平台
- Travis CI
- GitLab CI
- Jenkins

**请先检查Gitee流水线设置，然后告诉我你看到的情况！**