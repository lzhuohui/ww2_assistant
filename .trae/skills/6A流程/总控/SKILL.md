---
name: 6a-orchestrator
description: 6A开发流程总控，引导用户按六个阶段逐步推进项目
---

# 6A智能开发总控

## 描述
本技能负责启动6A开发流程，按顺序引导用户完成Align→Architect→Atomize→Approve→Automate→Assess六个阶段，并在每个阶段调用对应的专业技能。

## 使用场景
- 用户输入"@6A 新任务"或"开始6A流程"
- 需要规范化开发的新功能

## 指令
1. **初始化**：创建任务目录 `docs/任务名/`，记录任务名称和简要描述。
2. **阶段1（Align）**：调用 `6a-align` 技能完成需求对齐。
3. **阶段2（Architect）**：待Align文档确认后，调用 `6a-architect` 技能进行架构设计。
4. **阶段3（Atomize）**：基于架构设计，调用 `6a-atomize` 技能拆分原子任务。
5. **阶段4（Approve）**：调用 `6a-approve` 技能执行风险审批。
6. **阶段5（Automate）**：审批通过后，调用 `6a-automate` 技能指导编码实施。
7. **阶段6（Assess）**：实施完成后，调用 `6a-assess` 技能进行交付评估。
8. **进度反馈**：每完成一个阶段，更新状态并向用户报告。
