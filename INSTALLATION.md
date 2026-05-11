# 安装指南

## 前置条件

- Git 已安装（`git --version` 检查）
- Claude Code 已安装
- GitHub 账户（可选，如果要 clone）

## 三种安装方式

### 方式 1：完全安装（推荐 - 用于全新设置）

```bash
# 1. 克隆仓库
git clone https://github.com/YOUR_USERNAME/claude-configs-skills.git ~/claude-configs-skills
cd ~/claude-configs-skills

# 2. 备份现有配置（重要！）
cp ~/.claude/settings.json ~/.claude/settings.json.backup.$(date +%s)

# 3. 复制所有 skills
cp -r skills/* ~/.claude/skills/

# 4. 复制配置文件
cp configurations/settings/settings.json ~/.claude/settings.json

# 5. （可选）启用 mem 和 agent 策略
# 详见下方 "按需安装"
```

### 方式 2：选择性安装（推荐 - 用于现有配置）

只复制你需要的 skills：

```bash
git clone https://github.com/YOUR_USERNAME/claude-configs-skills.git ~/claude-configs-skills
cd ~/claude-configs-skills

# 复制特定 skill
cp -r skills/gaoyan-daily-report.md ~/.claude/skills/
cp -r skills/gaoyan-ingest/ ~/.claude/skills/
cp -r skills/frontend-design/ ~/.claude/skills/
cp -r skills/lovart-image-gen/ ~/.claude/skills/

# 只复制配置的某些部分
# 不覆盖 settings.json，而是手动合并需要的部分
```

### 方式 3：手动安装（用于没有 Git 的环境）

1. 在 GitHub 页面点击 **Code** → **Download ZIP**
2. 解压文件
3. 手动复制所需的文件到 `~/.claude/skills/` 和 `~/.claude/`

---

## 按需安装

### 只安装 Skills（不修改配置）

```bash
cp -r skills/* ~/.claude/skills/
```

✅ **优点**：不影响现有配置  
⚠️ **注意**：某些 skills 可能依赖特定的 hooks 配置

### 安装配置文件（settings.json）

```bash
# 方式 A：完全覆盖（有风险）
cp configurations/settings/settings.json ~/.claude/settings.json

# 方式 B：手动合并（推荐）
# 用编辑器打开并对比两个文件，选择性地复制需要的部分
# 特别是 "env", "hooks", "permissions" 部分
```

### 启用 Mem（记忆功能）

Mem 是一个强大的记忆插件，需要额外配置：

```bash
# 详见 configurations/mem/memory-setup.md
# 简单版：需要在 settings.json 的 hooks 中添加相关命令
```

### 启用 Agent 策略

```bash
# 详见 configurations/agents/agent-strategy.md
# Agent 策略主要通过 settings.json 中的 hooks 实现
```

### 启用 Dreaming（梦境）

Dreaming 是一个创意生成模块：

```bash
# 需要 LovArt API 配置
# 详见各个创意类 skill 的说明（baoyu-*, lovart-*）
```

---

## 🔑 配置 API 密钥

大部分 skills 需要 API 密钥。编辑 `~/.claude/settings.json`：

```json
{
  "env": {
    "ANTHROPIC_API_KEY": "sk-ant-...",           // Anthropic API
    "OPENROUTER_API_KEY": "sk-or-v1-...",       // OpenRouter (可选)
    "LOVART_API_KEY": "your-lovart-key",        // LovArt (图像生成)
    "ANTHROPIC_BASE_URL": "http://127.0.0.1:4000"  // LiteLLM 代理地址
  }
}
```

### 获取 API 密钥

| API | 获取方式 | 用途 |
|-----|--------|------|
| **Anthropic** | https://console.anthropic.com | Claude 模型调用 |
| **OpenRouter** | https://openrouter.ai | 第三方模型聚合 |
| **LovArt** | 联系方获取 | AI 图像生成 |
| **其他** | 各官网注册 | 特定功能 |

---

## 验证安装

### 检查 Skills 是否正确安装

```bash
ls -la ~/.claude/skills/ | grep gaoyan
# 应该看到：gaoyan-daily-report.md, gaoyan-ingest/ 等
```

### 检查配置文件

```bash
cat ~/.claude/settings.json | head -20
# 应该看到 "theme", "effortLevel", "env" 等字段
```

### 在 Claude Code 中验证

在 Claude Code 中执行：
```
/config
```

应该看到你的配置信息。

### 运行测试 Skill

试试调用一个 skill：
```
/skill gaoyan-daily-report
```

---

## 📦 更新和维护

### 更新到最新配置

```bash
cd ~/claude-configs-skills
git pull origin main

# 然后根据变更日志，选择性地更新文件
cp -r skills/* ~/.claude/skills/      # 更新 skills
# ... 其他文件更新
```

### 贡献你的改进

当你改进了某个 skill 时，可以推送回仓库：

```bash
cd ~/claude-configs-skills

# 同步最新的 skills
cp -r ~/.claude/skills/my-skill-name.md ./skills/

# 提交
git add .
git commit -m "Improve my-skill-name: add new features"
git push origin main
```

---

## ⚠️ 故障排除

### 问题 1：权限不足

```bash
# 如果看到 "Permission denied" 错误
chmod +x ~/.claude/skills/*
```

### 问题 2：Skills 在 Claude Code 中不显示

- 重启 Claude Code
- 检查 skill 文件名是否正确
- 确认 `.gitignore` 没有排除该文件

### 问题 3：API 密钥错误

```bash
# 检查 settings.json 中的 env 部分
cat ~/.claude/settings.json | grep -A 10 '"env"'
```

### 问题 4：无法克隆仓库

```bash
# 检查网络连接
ping github.com

# 或使用 HTTPS 而不是 SSH
git clone https://github.com/YOUR_USERNAME/claude-configs-skills.git
```

---

## 📚 后续学习

- [README.md](./README.md) - 项目概述
- [SKILLS_GUIDE.md](./SKILLS_GUIDE.md) - Skills 详细用法
- [configurations/settings/README.md](./configurations/settings/README.md) - 设置深入讲解

---

**需要帮助？** 提交 Issue 或查看各 skill 的内部文档。
