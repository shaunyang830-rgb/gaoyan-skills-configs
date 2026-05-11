# Claude Code 配置与 Skills 打包

这是我的 Claude Code 个性化配置和 skills 的完整打包，包括：
- ✅ 98+ 个自定义 skills
- ✅ Claude Code 核心配置（settings.json）
- ✅ Agent 策略和执行规则
- ✅ 记忆（mem/memory）配置
- ✅ 梦境（dreaming）模块配置

## 📁 目录结构

```
claude-configs-skills/
├── skills/                      # 所有自定义 skills
│   ├── article-writing/
│   ├── gaoyan-daily-report.md   # 高岩科技餐饮日报生成
│   ├── gaoyan-ingest/           # 知识库入库处理
│   ├── frontend-design/         # 前端设计 skill
│   └── ... (90+ 个 skills)
│
├── configurations/              # 配置文件
│   ├── settings/
│   │   ├── settings.json        # Claude Code 主配置
│   │   └── README.md            # 配置说明
│   ├── agents/                  # Agent 策略
│   │   └── agent-strategy.md
│   └── mem/                     # 记忆配置
│       └── memory-setup.md
│
├── INSTALLATION.md              # 安装指南
├── SKILLS_GUIDE.md              # Skills 使用指南
├── .gitignore                   # Git 忽略规则
└── README.md                    # 本文件
```

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/YOUR_USERNAME/claude-configs-skills.git
cd claude-configs-skills
```

### 2. 安装 Skills

**方式 A：复制所有 skills**
```bash
cp -r skills/* ~/.claude/skills/
```

**方式 B：复制特定 skill**
```bash
# 只复制你需要的 skill
cp -r skills/gaoyan-daily-report.md ~/.claude/skills/
cp -r skills/gaoyan-ingest/ ~/.claude/skills/
```

### 3. 导入配置

**设置 Claude Code 核心配置：**
```bash
# 备份你的旧配置
cp ~/.claude/settings.json ~/.claude/settings.json.backup

# 复制新配置
cp configurations/settings/settings.json ~/.claude/settings.json
```

> ⚠️ **重要**：这会覆盖你的 Claude Code 配置。建议先备份！

### 4. 配置 mem（记忆）

如果你想启用 claude-mem 插件的记忆功能，参考 `configurations/mem/memory-setup.md`

## 📋 Skills 清单

### 高岩科技相关 (8 个)
- `gaoyan-daily-report.md` - 餐饮日报生成（双轨采集）
- `gaoyan-weekly-review.md` - 周报汇总
- `gaoyan-ingest/` - 知识库入库处理
- `gaoyan-ingest-full-version/` - 完整版入库
- `gaoyan-market-analysis/` - 市场分析
- `gaoyan-ppt-design/` - PPT 设计
- `gaoyan-diner-crosstab-codex/` - 餐饮交叉表
- `gaoyan-financial-report-insight/` - 财报洞察

### 创意生成类 (15+ 个)
- `baoyu-image-gen.md` - AI 图像生成
- `baoyu-imagine.md` - 想象力助手
- `baoyu-slide-deck.md` - 幻灯片生成
- `baoyu-comic.md` - 漫画生成
- `baoyu-post-to-wechat.md` - 微信发布
- `lovart-image-gen/` - LovArt 图像生成
- `frontend-design/` - 前端设计

### 工具与集成 (30+ 个)
- `web-access/` - 网络访问
- `remembering-conversations/` - 对话记忆
- `research-ops/` - 研究操作
- `skill-creator.md` - Skill 创建工具
- ...等等

[完整清单见 SKILLS_GUIDE.md]

## ⚙️ 配置说明

### settings.json 包含的配置

```json
{
  "theme": "light",
  "effortLevel": "xhigh",
  "model": "haiku",
  "env": {
    "ANTHROPIC_BASE_URL": "http://127.0.0.1:4000",
    "ANTHROPIC_API_KEY": "你的API密钥",
    ...
  },
  "permissions": { ... },      // 权限白名单
  "hooks": { ... }             // SessionStart / PostToolUse 等钩子
}
```

### 支持的模型

- `claude-opus-4.7` - 最强模型（用于复杂任务）
- `claude-sonnet-4.6` - 均衡模型（默认）
- `claude-haiku-4.5` - 快速模型（默认）
- `kimi-k2.6` - Moonshot Kimi（通过 LiteLLM）

### 权限配置

已预配置的权限包括：
- ✅ 文件读写 (Read, Write, Edit, Glob, Grep)
- ✅ Git 操作（status, diff, add, commit, push 等）
- ✅ 包管理 (npm, pip, uv, yarn 等)
- ✅ 数据处理 (jq, pandoc, markitdown)
- ❌ 危险操作 (rm -rf, sudo, 强制推送 等)

## 🔐 安全性注意

⚠️ **此仓库包含你的个人配置。分享前：**

1. **移除敏感信息**：
   - API 密钥已在 `.gitignore` 中排除
   - 但仍需检查 `settings.json` 中的自定义模型配置

2. **验证权限**：
   - 检查 `settings.json` 中允许的 Bash 命令
   - 确保没有暴露内部系统路径

3. **隐私设置**：
   - 如果包含公司相关 skills（如高岩科技），考虑设为 Private
   - 或者创建 Public 和 Private 两个分支

## 📖 深入文档

- [INSTALLATION.md](./INSTALLATION.md) - 详细安装指南
- [SKILLS_GUIDE.md](./SKILLS_GUIDE.md) - 所有 skills 的使用说明
- [configurations/settings/README.md](./configurations/settings/README.md) - 设置详解
- [configurations/agents/agent-strategy.md](./configurations/agents/agent-strategy.md) - Agent 策略说明
- [configurations/mem/memory-setup.md](./configurations/mem/memory-setup.md) - 记忆功能配置

## 🔄 保持更新

当你在 Claude Code 中修改或创建了新的 skills 后，可以同步回来：

```bash
# 复制最新的 skills 到本仓库
cp -r ~/.claude/skills/* ./skills/

# 提交更改
git add .
git commit -m "Update skills and configurations"
git push origin main
```

## 🤝 贡献

如果你想改进这些 skills，欢迎：
- Fork 此仓库
- 创建 feature 分支
- 提交 PR

## 📝 许可证

MIT License - 自由使用和修改

---

**最后更新**：2026-05-11  
**Claude 版本**：Claude Code (Opus/Sonnet/Haiku)  
**Skills 数量**：98+
