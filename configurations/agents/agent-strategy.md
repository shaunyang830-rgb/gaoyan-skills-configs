# Agent 策略和执行规则

## 什么是 Claude Code Agent？

Agent 是一种**自主执行复杂任务的 AI 代理**，具有：
- 🎯 **目标设定** - 明确的任务目标
- 🔄 **迭代执行** - 循环执行和优化
- 🧠 **推理能力** - 分析当前状态并制定计划
- 🛠️ **工具使用** - 调用各种工具完成任务

## 你的 Agent 执行环境

### 当前配置

在 `settings.json` 的 `hooks` 中，已配置了 agent 相关的钩子：

| 钩子点 | 功能 | 触发时机 |
|-------|------|--------|
| `SessionStart` | 初始化 agent 策略 | 会话开始 |
| `PostToolUse` | 记录 agent 执行步骤 | 工具使用后 |
| `Stop` | 总结 agent 完成情况 | 会话结束 |

### 支持的 Agent 类型

1. **通用 Agent** - 处理任意任务
2. **子 Agent（Subagents）** - 并行或串行执行任务
3. **后台 Agent** - 长时间运行任务
4. **搜索 Agent** - 探索型 agent（如 Explore agent）
5. **计划 Agent** - 架构和设计 agent

## 如何使用 Agent

### 1. 通用 Agent（推荐入门）

```
Claude, analyze this codebase and create a plan to refactor it.
```

Claude 会自动：
- 探索文件结构
- 理解代码逻辑
- 制定重构计划
- 执行修改

### 2. 调用特定 Agent 类型

#### 搜索 Agent（快速查找信息）

```
@explore 查找所有使用 React hooks 的文件
```

或用工具调用：
```python
Agent(
  subagent_type="explore",
  description="在代码库中查找特定模式",
  prompt="搜索所有调用 useEffect 的组件"
)
```

#### 计划 Agent（架构设计）

```
@plan 为新的用户认证系统设计实现策略
```

或：
```python
Agent(
  subagent_type="plan",
  description="设计系统架构",
  prompt="规划如何实现 OAuth 2.0 集成"
)
```

#### 通用 Agent（复杂任务）

```
Claude, 帮我重构这个函数并添加单元测试
```

或显式调用：
```python
Agent(
  subagent_type="general-purpose",
  prompt="重构并测试这个模块",
  description="复杂重构任务"
)
```

### 3. 后台执行 Agent

用于长时间运行的任务：

```python
Agent(
  prompt="生成今天的餐饮日报，耗时可能较长",
  description="后台生成日报",
  run_in_background=True  # ← 后台运行
)
```

## Agent 执行策略

### 🎯 策略 1：同步执行（默认）

```python
Agent(
  prompt="完成任务",
  run_in_background=False  # 同步等待结果
)
```

**优点**：可以立即获得结果  
**缺点**：阻塞其他操作  
**适用**：快速、简单的任务

### 🎯 策略 2：后台执行

```python
Agent(
  prompt="长时间任务",
  run_in_background=True  # 后台运行
)
# 继续其他工作，稍后用 TaskOutput 获取结果
```

**优点**：不阻塞主流程  
**缺点**：需要手动获取结果  
**适用**：耗时的任务（>5分钟）

### 🎯 策略 3：并行 Agent

同时运行多个 agent：

```python
# 同时执行三个任务
Agent(prompt="任务A", run_in_background=False)
Agent(prompt="任务B", run_in_background=False)
Agent(prompt="任务C", run_in_background=False)
```

**优点**：并行加速  
**缺点**：需要协调结果  
**适用**：独立的并行任务

### 🎯 策略 4：串行 Agent

前一个 agent 的输出作为下一个的输入：

```python
result1 = Agent(prompt="步骤1", run_in_background=False)
result2 = Agent(prompt=f"步骤2，基于: {result1}", run_in_background=False)
```

**优点**：任务有依赖关系  
**缺点**：必须等待前一个完成  
**适用**：步骤化任务

## 你的项目中的 Agent 使用

### Gaoyan 餐饮日报生成

这是你最常用的 agent 用法：

```python
Agent(
  subagent_type="general-purpose",
  prompt="使用双轨采集生成今天的餐饮日报...",
  description="生成餐饮日报",
  run_in_background=True  # 后台运行，因为很耗时
)
```

**执行流程**：
1. 启动双轨 agent（一个搜索新闻，一个访问 CDP）
2. 并行采集数据
3. 合并整理
4. 生成 Markdown
5. 保存到 Obsidian Vault

### CRM 和周会数据处理

```python
Agent(
  subagent_type="general-purpose",
  prompt="处理钉钉业财一体数据，生成周会跟进表",
  run_in_background=False  # 同步执行
)
```

## Agent 配置最佳实践

### 1. 任务分解

大任务拆成小任务：
```
❌ 不好: "生成完整的年度报告"
✅ 好:   分三步
  1. Agent("收集数据")
  2. Agent("分析数据")
  3. Agent("生成报告")
```

### 2. 清晰的提示词

```python
Agent(
  prompt="""
  你的目标：生成餐饮日报
  
  输入：
  - WebSearch 新闻关键词：中国餐饮
  - CDP 数据源：垂直媒体列表
  
  输出：
  - Markdown 格式日报
  - 信息图（如果可能）
  - 保存到 Obsidian Vault
  
  要求：
  - 时间戳：今天日期
  - 数据来源标注
  - 3-5 条重点新闻
  """,
  description="餐饮日报生成"
)
```

### 3. 错误处理

```python
try:
  result = Agent(prompt="任务")
except Exception as e:
  print(f"Agent 失败: {e}")
  # 回退策略
  result = fallback_function()
```

### 4. 结果验证

```python
result = Agent(prompt="...", run_in_background=False)

# 检查结果
if result.success:
  print("✅ 任务成功")
else:
  print(f"❌ 失败原因: {result.error}")
  # 重试或调整策略
```

## Agent 与 Skills 的协作

你的许多 skills 都使用 agent：

| Skill | Agent 用法 |
|------|----------|
| `gaoyan-daily-report` | 双轨并行 agent 采集新闻 |
| `gaoyan-ingest` | 后台 agent 处理文件 |
| `gaoyan-weekly-review` | 串行 agent（收集→分析→生成） |
| `research-ops` | 搜索 agent 查找资料 |
| `web-access` | 通用 agent 访问网页 |

## 🔧 调整 Agent 行为

### 修改超时时间

```json
{
  "env": {
    "AGENT_TIMEOUT_MS": 300000  // 5分钟超时
  }
}
```

### 修改并发数

```json
{
  "env": {
    "MAX_PARALLEL_AGENTS": 3  // 同时最多 3 个 agent
  }
}
```

### 启用 Agent 日志

```json
{
  "env": {
    "AGENT_DEBUG": "true",
    "AGENT_LOG_LEVEL": "verbose"
  }
}
```

## 💡 高级 Agent 用法

### 使用 Agent 进行自动化工作流

```python
# 每日自动化流程
Agent(prompt="生成今日餐饮日报", run_in_background=True)
Agent(prompt="更新 CRM 客户状态", run_in_background=True)
Agent(prompt="生成周会跟进表", run_in_background=True)
```

### 链式 Agent 处理

```python
# 步骤 1：收集
data = Agent(prompt="从钉钉导出本周数据")

# 步骤 2：分析
analysis = Agent(prompt=f"分析这些数据: {data}")

# 步骤 3：生成报告
report = Agent(prompt=f"基于分析生成周报: {analysis}")
```

### Agent 与记忆集成

Agent 执行会自动被记录到 mem 中：
```
[Agent 执行记录]
- 2026-05-11 10:30: 生成餐饮日报（成功）
- 2026-05-11 14:45: 更新 CRM（进行中）
- 2026-05-10 16:20: 生成周报（成功）
```

## 🆘 常见问题

**Q: Agent 执行太慢了？**
```
→ 使用更小的模型（Haiku）
→ 拆成更小的子任务
→ 启用后台执行不阻塞
```

**Q: Agent 经常失败？**
```
→ 提供更详细的提示词
→ 添加错误处理
→ 检查权限配置
```

**Q: 如何监控 Agent 执行进度？**
```bash
# 查看最近的 agent 执行
curl http://localhost:37777/agent/history

# 监视正在运行的 agent
watch -n 1 'curl http://localhost:37777/agent/status'
```

---

## 📚 相关资源

- [Agent 官方文档](https://docs.anthropic.com/agents)
- [Settings 配置](./settings/README.md)
- [Mem 记忆配置](../mem/memory-setup.md)
- 你的 Skills：`gaoyan-daily-report`, `gaoyan-ingest` 等

---

**最后更新**：2026-05-11  
**Agent API 版本**：最新  
**支持的 Agent 类型**：explore, plan, general-purpose, 子 agent 等
