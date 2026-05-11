# Claude Code Settings 配置说明

## settings.json 详解

这是 Claude Code 的核心配置文件，位于 `~/.claude/settings.json`

### 主要配置项

#### 1. 主题和界面 (Theme & UI)

```json
{
  "theme": "light",           // "light" 或 "dark"
  "effortLevel": "xhigh"      // 工作强度：low, medium, high, xhigh
}
```

- **theme**: 界面主题
- **effortLevel**: 控制 Claude 的处理深度
  - `low`: 快速、简洁的响应
  - `medium`: 平衡
  - `high`: 详细、深思熟虑
  - `xhigh`: 最大努力（推荐用于复杂任务）

#### 2. 模型配置 (Models)

```json
{
  "model": "haiku",                              // 默认模型
  "env": {
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "claude-opus-4.7",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "claude-sonnet-4.6",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "claude-haiku-4.5",
    "ANTHROPIC_CUSTOM_MODEL_OPTION": "kimi-k2.6"
  }
}
```

**模型选择指南**：

| 模型 | 速度 | 智能 | 成本 | 用途 |
|-----|-----|-----|-----|------|
| Haiku | ⚡⚡⚡ | ⭐⭐⭐ | 💰 | 快速任务、编码 |
| Sonnet | ⚡⚡ | ⭐⭐⭐⭐ | 💰💰 | 平衡任务（推荐） |
| Opus | ⚡ | ⭐⭐⭐⭐⭐ | 💰💰💰 | 复杂分析、创意工作 |
| Kimi | ⚡⚡ | ⭐⭐⭐⭐ | 💰💰 | 多语言处理 |

#### 3. API 配置 (Environment)

```json
{
  "env": {
    "ANTHROPIC_API_KEY": "sk-ant-...",           // 你的 Anthropic API 密钥
    "ANTHROPIC_BASE_URL": "http://127.0.0.1:4000",  // LiteLLM 代理地址
    "OPENROUTER_API_KEY": "sk-or-v1-...",        // OpenRouter（可选）
    "ANTHROPIC_AUTH_TOKEN": "dummy"              // 用于本地代理
  }
}
```

**重要**：
- 不要将真实的 API 密钥提交到 GitHub
- 在 `.gitignore` 中已排除敏感文件
- 个人使用时才在 `settings.json` 中设置密钥

#### 4. 权限配置 (Permissions)

```json
{
  "permissions": {
    "allow": [
      "Read", "Write", "Edit", "Glob", "Grep",
      "Bash(git *)",
      "Bash(python*)",
      "Bash(npm*)",
      ...
    ],
    "deny": [
      "Bash(rm -rf*)",
      "Bash(sudo*)",
      "Bash(git push*)",  // 危险操作需要手动确认
      ...
    ],
    "defaultMode": "acceptEdits"
  }
}
```

**权限策略**：
- ✅ **allow**: 自动批准的操作（文件读写、git 基础操作）
- ❌ **deny**: 自动拒绝（危险操作）
- ❓ **其他**: 需要用户确认

**常用权限白名单**：

```json
"allow": [
  // 文件操作
  "Read", "Write", "Edit", "MultiEdit", "Glob", "Grep",
  
  // Git 操作
  "Bash(git status)",
  "Bash(git diff*)",
  "Bash(git add*)",
  "Bash(git commit*)",
  "Bash(git branch*)",
  "Bash(git pull*)",
  "Bash(git clone*)",
  
  // 包管理
  "Bash(npm*)",
  "Bash(pip*)",
  "Bash(python*)",
  
  // 数据处理
  "Bash(jq*)",
  "Bash(pandoc*)",
  "Bash(curl*)",
  "Bash(grep*)",
  "Bash(find*)"
]
```

#### 5. 钩子配置 (Hooks)

钩子是在特定事件发生时执行的命令（如启动、工具使用后、结束等）

```json
{
  "hooks": {
    "SessionStart": [          // 会话启动时
      { "type": "command", "command": "启动 mem...", ... }
    ],
    "PreToolUse": [            // 工具使用前
      { "matcher": "Read", ... }
    ],
    "PostToolUse": [           // 工具使用后
      { "matcher": "*", ... }
    ],
    "Stop": [                  // 停止时
      { "type": "command", ... }
    ]
  }
}
```

**关键钩子说明**：

| 钩子 | 触发时机 | 用途 |
|-----|--------|------|
| `SessionStart` | 会话开始 | 初始化 mem、启动 LiteLLM 等 |
| `PostToolUse` | 工具使用后 | 记录观察、更新记忆 |
| `PreToolUse` | 工具使用前 | 加载上下文 |
| `Stop` | 会话结束 | 保存记忆、总结 |

---

## 🔧 常见修改

### 修改默认模型

```json
// 改为 Opus（最强）
"model": "opus"

// 改为 Sonnet（均衡）
"model": "sonnet"

// 改为 Haiku（最快）
"model": "haiku"
```

### 调整工作强度

```json
"effortLevel": "high"  // 更深思熟虑，但更慢
```

### 自定义 API 端点

```json
"env": {
  "ANTHROPIC_BASE_URL": "http://localhost:4000",  // 自己的代理
  "ANTHROPIC_API_KEY": "sk-ant-..."
}
```

### 添加新的权限

```json
"allow": [
  ...,
  "Bash(docker*)",      // 允许 docker 命令
  "Bash(kubectl*)"      // 允许 kubernetes 命令
]
```

---

## 🔐 安全建议

1. **不要提交 API 密钥到 GitHub**
   - 使用 `.gitignore` 排除敏感文件
   - 或使用环境变量

2. **权限最小化原则**
   - 只添加必要的权限
   - 危险操作保持在 "deny" 列表

3. **定期更新**
   - 保持 Claude 模型版本最新
   - 检查是否有新的安全建议

---

## 📚 相关文件

- `~/.claude/settings.json` - 实际配置文件
- `~/.claude/plugins/cache/thedotmack/claude-mem/` - mem 插件
- `.claude/litellm/config.yaml` - LiteLLM 配置

---

## 🆘 常见问题

**Q: 如何重置为默认配置？**
```bash
# 备份当前配置
cp ~/.claude/settings.json ~/.claude/settings.json.backup

# 删除配置文件，重启 Claude Code 时会创建默认配置
rm ~/.claude/settings.json
```

**Q: 如何在不同项目使用不同配置？**
```bash
# 创建项目级配置
touch .claude/settings.json  # 项目根目录下
# Claude Code 会优先使用项目级配置
```

**Q: 如何快速查看当前配置？**
```bash
cat ~/.claude/settings.json | jq .
```

---

**最后更新**: 2026-05-11
