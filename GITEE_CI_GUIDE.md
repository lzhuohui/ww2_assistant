# Gitee CI/CD 配置指南

## 方案1：使用Gitee Go（推荐）

Gitee Go是Gitee官方的CI/CD服务，支持类似GitHub Actions的语法。

### 步骤：

1. **启用Gitee Go**：
   - 访问：https://gitee.com/lzhuohui/ww2_assistant
   - 点击"管理" → "流水线" → "启用Gitee Go"
   - 或直接访问：https://gitee.com/lzhuohui/ww2_assistant/gitee_go

2. **配置文件已创建**：
   - 文件位置：`.gitee-ci.yml`
   - 配置内容：构建APK的完整流程

3. **触发构建**：
   - 推送代码到master分支自动触发
   - 或在Gitee Go页面手动触发

## 方案2：使用Gitee Pages + 手动构建

如果Gitee Go不可用，可以：

1. 在本地构建APK
2. 将APK上传到Gitee Release
3. 用户从Release下载

## 方案3：使用第三方CI/CD服务

可以使用以下服务：
- Jenkins
- Drone CI
- Travis CI
- CircleCI

## 当前配置

已创建 `.gitee-ci.yml` 文件，包含：
- Python 3.11环境
- Flet依赖安装
- APK构建
- 构建产物上传

## 下一步

1. 访问Gitee仓库的Gitee Go页面
2. 启用Gitee Go服务
3. 推送代码触发构建
4. 下载构建好的APK

## 注意事项

- Gitee Go可能需要付费或申请试用
- 免费用户可能有构建时长限制
- 建议同时保留GitHub Actions作为备用
