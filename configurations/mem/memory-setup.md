# Claude Mem - 记忆功能配置

## 什么是 Claude Mem？

Claude Mem 是一个强大的**持久化记忆插件**，让 Claude 能够：
- 📝 **记住你的偏好**（编码风格、说话方式、项目细节）
- 🔄 **跨会话保持上下文**（不需要每次都重新解释）
- 🧠 **学习你的工作流**（自动优化建议）
- 📊 **积累知识**（长期项目的历史信息）

## 当前状态

✅ **已启用** - 你的 settings.json 中已配置 mem 插件

在 SessionStart 钩子中自动启动：
```bash
node ~/.claude/plugins/cache/thedotmack/claude-mem/12.1.0/scripts/worker-service.cjs start
```

## 工作原理

### 1. 记忆存储位置

```
~/.claude/plugins/cache/thedotmack/claude-mem/
├── 12.1.0/                    # 插件版本
│   ├── node_modules/          # 依赖
│   ├── scripts/               # 启动脚本
│   └── ui/                    # 用户界面
```

### 2. 记忆触发时机

根据 settings.json 的钩子配置：

| 事件 | 钩子 | 说明 |
|-----|-----|------|
| **会话开始** | SessionStart | 初始化记忆服务 |
| **工具使用后** | PostToolUse | 记录操作和结果 |
| **文件读取前** | PreToolUse (Read) | 加载文件相关记忆 |
| **会话结束** | SessionEnd | 保存和汇总记忆 |

### 3. 记忆内容

Mem 会自动记录：
- ✅ 你的工作目标和项目信息
- ✅ 你提到的偏好（代码风格、工具选择等）
- ✅ 关键决策和设计理由
- ✅ 常见问题和解决方案
- ✅ 个人背景信息（如果你愿意分享）

## 如何使用

### 查看已记忆的内容

在 Claude Code 中输入：
```
show me my memories
```

或者查看记忆服务状态：
```bash
curl http://localhost:37777/health
```

### 添加新记忆

直接告诉 Claude：
```
remember: I prefer using TypeScript for all projects
remember: My company is Gaoyan Tech, focused on food & beverage industry
remember: I use Obsidian vault at ~/Documents/Obsidian Vault
```

### 编辑或删除记忆

```
update my memory: change "X" to "Y"
remove memory about: "old project name"
```

### 查看记忆摘要

```
summarize what you know about me
what's my work style based on our interactions?
```

## 🔧 配置选项

### 修改记忆服务端口

如果 37777 端口被占用，编辑 settings.json：

```json
{
  "env": {
    "CLAUDE_MEM_PORT": "37778"  // 改为其他端口
  }
}
```

### 禁用记忆功能

如果想暂时禁用 mem，有两种方式：

**方式 1：注释掉 hooks**（暂时）
```json
"SessionStart": [
  // {
  //   "type": "command",
  //   "command": "node ~/.claude/plugins/cache/thedotmack/claude-mem/12.1.0/scripts/worker-service.cjs start"
  // }
]
```

**方式 2：完全卸载**
```bash
rm -rf ~/.claude/plugins/cache/thedotmack/claude-mem
rm -rf ~/.claude/plugins/marketplaces/thedotmack
```

### 导出或备份记忆

```bash
# 导出所有记忆
curl http://localhost:37777/export > my-memories.json

# 或者压缩整个 mem 目录
tar -czf mem-backup.tar.gz ~/.claude/plugins/cache/thedotmack/claude-mem
```

## 💡 使用最佳实践

### 1. 定期更新记忆

每周告诉 Claude 你的新项目和目标：
```
remember: This week I'm working on [project name]
remember: The deadline is [date]
remember: Key stakeholders are [names]
```

### 2. 记录常见问题

```
remember: We always use prettier for code formatting
remember: The codebase uses pnpm, not npm
remember: Our Obsidian vault structure is: [structure]
```

### 3. 个人偏好

```
remember: I prefer detailed explanations with examples
remember: I like to see code before prose
remember: I'm in GMT+8 timezone
```

### 4. 项目背景

```
remember: Gaoyan Tech is a food & beverage data company
remember: We generate daily reports for restaurant industry
remember: Key products: daily reports, market analysis, CRM
```

## 📊 记忆大小和管理

### 查看记忆占用

```bash
curl http://localhost:37777/stats
```

### 清理过期记忆

Mem 会自动清理不再相关的记忆，但你也可以手动：

```
clean up memories older than [date]
forget about: [old project name]
```

## 🔐 隐私和安全

### 记忆存储位置

所有记忆都存储在本地：
```
~/.claude/
└── plugins/
    └── cache/
        └── thedotmack/
            └── claude-mem/
                └── 12.1.0/
                    └── memories/  ← 记忆数据库
```

**不会上传到云端** - 完全本地化

### 不要记录敏感信息

避免记录：
- 🚫 API 密钥、密码
- 🚫 财务数据、员工信息
- 🚫 机密的商业信息
- 🚫 个人身份信息（除非必要）

### 如果想迁移到新设备

```bash
# 在旧设备上导出记忆
curl http://localhost:37777/export > memories-export.json

# 复制到新设备
cp memories-export.json ~/.claude/plugins/cache/thedotmack/claude-mem/12.1.0/

# 导入
curl -X POST http://localhost:37777/import -d @memories-export.json
```

## 🆘 故障排除

### 问题 1：记忆服务无法启动

```bash
# 检查端口是否被占用
lsof -i :37777

# 检查日志
tail -f ~/.claude/litellm/logs/litellm.log
```

### 问题 2：记忆丢失

```bash
# 检查数据文件是否存在
ls -la ~/.claude/plugins/cache/thedotmack/claude-mem/12.1.0/memories/

# 从备份恢复
tar -xzf mem-backup.tar.gz -C ~/.claude/plugins/
```

### 问题 3：记忆变得混乱

```
clear my memories and start fresh
```

然后重新启动 Claude Code。

## 📚 高级用法

### 使用记忆进行智能提示

```
based on my past preferences, what should I do next?
suggest improvements for [project] considering what you know about me
```

### 联动其他工具

记忆可以与以下工具配合：
- 📝 Obsidian Vault - 自动引用你的笔记
- 📊 CRM Skills - 记住客户关系
- 🔄 Agent Strategy - 自动调整执行策略

---

## 📖 更多信息

- **官方文档**：https://github.com/thedotmack/claude-mem
- **插件位置**：`~/.claude/plugins/cache/thedotmack/claude-mem/`
- **相关配置**：`~/.claude/settings.json` 的 hooks 部分

---

**最后更新**：2026-05-11  
**Mem 版本**：12.1.0  
**状态**：✅ 已启用且正常工作
