# Skills 完整使用指南

这是你所有 98+ 个 Claude Code Skills 的详细分类和使用说明。

## 📊 Skills 分类统计

| 类别 | 数量 | 主要用途 |
|-----|-----|--------|
| **高岩科技** | 8 | 餐饮行业数据分析、日报、报告 |
| **创意生成** | 15+ | AI 图像、文案、设计 |
| **工具与集成** | 30+ | 网络访问、数据处理、自动化 |
| **文档处理** | 10+ | PDF、PPTX、XLSX、Markdown |
| **其他工具** | 35+ | 各类实用工具 |
| **总计** | **98+** | 覆盖各类工作场景 |

---

## 🏢 高岩科技 Skills（8 个）

这些是你定制的高岩科技专用 skills，用于餐饮行业数据分析。

### 1. **gaoyan-daily-report** ⭐⭐⭐
**生成餐饮行业日报**

```
触发: /skill gaoyan-daily-report
或: 生成今天的餐饮日报
```

**功能**：
- 双轨采集（WebSearch 全网 + CDP 垂类媒体）
- 自动汇总重要新闻
- 生成 Markdown 格式日报
- 保存到 Obsidian Vault
- 生成信息图（可选）

**输入**：
- 日期（默认今天）
- 关键词（可选）

**输出**：
- `YYYY-MM-DD-餐饮日报.md`

**文件位置**：`Gaoyan Projects/餐饮日报/`

### 2. **gaoyan-weekly-review**
**生成周报汇总**

```
触发: /skill gaoyan-weekly-review
```

**功能**：
- 汇总本周所有日报的要点
- 生成周报 Markdown
- 创建信息图（用 Puppeteer 截图）
- 标注重点项目和客户

**输出**：
- `YYYY-WW-周报.md`
- `YYYY-WW-周报.png`（信息图）

### 3. **gaoyan-ingest** ⭐
**知识库入库处理**

```
触发: /skill gaoyan-ingest
或: 帮我入库这个文件
```

**支持的文件类型**：
- PDF、PPTX、DOCX、XLSX
- HTML/网页内容
- Markdown
- DingTalk 录音转录

**功能**：
- 自动提取文本内容（MarkItDown）
- 生成标准 Markdown 笔记
- 添加 YAML frontmatter
- 创建内部双链
- 关联高岩业务洞察

**使用示例**：
```
处理这个 PDF 报告，帮我入库
把这个 Excel 数据整理成 Markdown
把这个网页内容保存到 Obsidian Vault
```

### 4. **gaoyan-ingest-full-version**
**完整版入库（用于厚报告）**

```
触发: /skill gaoyan-ingest-full-version
```

**适用场景**：
- 蓝皮书
- 厚重的研究报告
- 需要**逐页内容 + 摘要 + 原文**三件套的文档

**优点**：比标准入库保留更多细节

### 5. **gaoyan-market-analysis**
**市场分析报告**

```
触发: /skill gaoyan-market-analysis
```

**功能**：
- 分析餐饮市场趋势
- 竞争对手研究
- 消费者洞察
- 生成分析报告

### 6. **gaoyan-ppt-design**
**PPT 设计生成**

```
触发: /skill gaoyan-ppt-design
```

**功能**：
- 从数据生成专业 PPT
- 高岩品牌主题应用
- 图表和可视化
- 支持模板自定义

**使用**：
```
基于这些数据生成一份高岩风格的 PPT
```

### 7. **gaoyan-diner-crosstab-codex**
**餐饮交叉表分析**

```
触发: /skill gaoyan-diner-crosstab-codex
```

**功能**：
- 交叉数据透视表分析
- 餐饮细分市场数据
- 多维度对比分析

### 8. **gaoyan-financial-report-insight**
**财报洞察分析**

```
触发: /skill gaoyan-financial-report-insight
```

**功能**：
- 上市公司财报分析
- 同行业对标分析
- 财务指标解读
- 生成深度洞察报告

---

## 🎨 创意生成 Skills（15+ 个）

用于 AI 图像、文案、设计等创意工作。

### Baoyu 系列（11 个）

| Skill | 功能 |
|-------|------|
| **baoyu-image-gen** | AI 图像生成（Stable Diffusion） |
| **baoyu-imagine** | 想象力助手（创意头脑风暴） |
| **baoyu-comic** | 漫画生成（故事转漫画） |
| **baoyu-slide-deck** | 幻灯片生成（从大纲生成 PPT） |
| **baoyu-post-to-wechat** | 微信公众号发布助手 |
| **baoyu-post-to-weibo** | 微博发布助手 |
| **baoyu-post-to-x** | Twitter/X 发布助手 |
| **baoyu-cover-image** | 封面图生成 |
| **baoyu-infographic** | 信息图生成 |
| **baoyu-translate** | 多语言翻译 |
| **baoyu-youtube-transcript** | YouTube 视频转录 |

### LovArt 系列（2 个）

| Skill | 功能 |
|-------|------|
| **lovart-image-gen** | 专业 AI 图像生成（高质量） |
| **lovart-api** | LovArt API 集成 |

### Frontend 设计（1 个）

| Skill | 功能 |
|-------|------|
| **frontend-design** | 前端 UI/UX 设计生成 |

---

## 🛠️ 工具与集成 Skills（30+ 个）

系统级和集成类工具。

### 网络与访问

| Skill | 功能 |
|-------|------|
| **web-access** | 网络访问、网页抓取、登录后操作 |
| **research-ops** | 研究操作、资料收集 |
| **baoyu-danger-x-to-markdown** | Twitter 转 Markdown |
| **baoyu-danger-gemini-web** | Gemini 网络搜索集成 |

### 文档处理

| Skill | 功能 |
|-------|------|
| **pdf** | PDF 读写处理 |
| **pptx** | PowerPoint 处理 |
| **docx** | Word 文档处理 |
| **xlsx** | Excel 表格处理 |
| **markdown-to-html** | Markdown 转 HTML |
| **doc-coauthoring** | 多人文档协作 |

### 任务与工作流

| Skill | 功能 |
|-------|------|
| **background-agent-management** | 后台 Agent 管理 |
| **skill-creator** | 创建和优化新 skills |
| **remembering-conversations** | 对话记忆搜索 |
| **streamlit-dashboard** | 数据仪表板生成 |
| **web-artifacts-builder** | Web 交互式工件生成 |

### 其他工具

| Skill | 功能 |
|-------|------|
| **content-engine** | 内容生成引擎 |
| **humanizer-zh** | 中文内容人性化处理 |
| **model-switcher** | 模型快速切换 |
| **tag-linker** | Obsidian 标签链接 |
| **vault-lint** | Obsidian Vault 检查 |

---

## 📁 文档处理 Skills（10+ 个）

专门处理各类文件格式。

```
pdf.md          - PDF 处理
pptx.md         - PowerPoint
docx.md         - Word 文档
xlsx.md         - Excel
```

**典型流程**：
```
1. 读取文件 (pdf.md, pptx.md 等)
2. 提取内容
3. 转换格式（通常转 Markdown）
4. 保存到 Obsidian Vault
```

---

## 🎯 使用场景速查

### 📰 日常工作

```
"生成今天的餐饮日报"
→ gaoyan-daily-report

"帮我汇总本周的数据"
→ gaoyan-weekly-review

"我有个 PDF 报告，帮我入库"
→ gaoyan-ingest
```

### 🎨 创意工作

```
"给我生成一个关于 AI 的图片"
→ baoyu-image-gen 或 lovart-image-gen

"帮我生成一份演讲 PPT"
→ baoyu-slide-deck

"把这个故事转成漫画"
→ baoyu-comic
```

### 📊 数据分析

```
"分析最近的市场趋势"
→ gaoyan-market-analysis

"帮我看看这份财报"
→ gaoyan-financial-report-insight

"生成餐饮市场的交叉分析"
→ gaoyan-diner-crosstab-codex
```

### 🌐 网络操作

```
"搜索关于 XXX 的最新新闻"
→ web-access

"帮我抓取这个网页"
→ web-access

"登录这个网站并导出数据"
→ web-access
```

### 📝 文件处理

```
"把这个 Excel 数据转成 Markdown"
→ xlsx.md

"读取这个 PDF 并提取表格"
→ pdf.md

"帮我生成一份 PowerPoint"
→ pptx.md 或 baoyu-slide-deck
```

---

## 🔗 Skills 依赖关系

```
gaoyan-daily-report
├─ web-access (搜索新闻)
├─ web-artifacts-builder (生成信息图)
└─ 输出到 Obsidian Vault

gaoyan-ingest
├─ pdf.md / pptx.md / xlsx.md (提取内容)
├─ markdown-to-html (格式转换)
└─ 输出到 Obsidian Vault

baoyu-image-gen
├─ lovart-api (图像生成)
└─ web-artifacts-builder (预览)
```

---

## 💡 高级用法

### 1. 链式 Skills

```
"处理这个 PDF，然后生成一份分析报告"

步骤：
1. gaoyan-ingest (处理 PDF)
2. gaoyan-market-analysis (分析内容)
3. gaoyan-ppt-design (生成 PPT)
```

### 2. 并行执行

```
Agent(
  prompt="同时生成日报和周报",
  run_in_background=True
)
```

### 3. 与 Mem 集成

当你使用 skills 时，所有操作会被 mem 记录：
```
[Mem 自动记录]
- 2026-05-11: 生成了餐饮日报
- 使用的关键词：中国餐饮、新店开业
- 输出文件：2026-05-11-餐饮日报.md
```

下次执行时，Claude 会参考这个历史。

---

## 📚 找 Skill 源文件

所有 skills 的源文件位置：

```
~/.claude/skills/

├── gaoyan-daily-report.md           # 单文件 skill
├── gaoyan-daily-report/             # 多文件 skill
│   ├── SKILL.md                    # 主 skill 定义
│   └── ... (辅助文件)
├── lovart-image-gen/                # 带脚本的 skill
│   ├── SKILL.md
│   └── scripts/
│       └── generate.py
└── ... (其他 skills)
```

**编辑 skill**：
```bash
# 用编辑器打开某个 skill
code ~/.claude/skills/gaoyan-daily-report.md

# 或在 Claude Code 中直接编辑
# 用 Edit 工具修改 skill 文件
```

---

## 🚀 创建新 Skill

使用 `skill-creator` skill：

```
请帮我创建一个新 skill，名字是 "my-awesome-skill"，功能是 XXX
```

或参考已有 skill 的结构：
```
~/.claude/skills/template-skill.md
```

---

## 🔄 保持更新

### 同步最新 Skills

```bash
# 从 GitHub 更新
cd ~/claude-configs-skills
git pull origin main
cp -r skills/* ~/.claude/skills/
```

### 提交你的改进

```bash
# 修改后同步回仓库
cp -r ~/.claude/skills/my-skill.md ~/claude-configs-skills/skills/
cd ~/claude-configs-skills
git add .
git commit -m "Update skill: my-skill"
git push
```

---

## 🆘 Skill 故障排除

### 问题 1：Skill 无法触发

```
检查清单：
□ 文件位置：~/.claude/skills/
□ 文件名格式：my-skill.md 或 my-skill/SKILL.md
□ 重启 Claude Code
□ 检查拼写
```

### 问题 2：Skill 执行出错

```
原因可能：
- API 密钥配置不对（检查 settings.json）
- 文件权限问题 (chmod +x)
- 依赖库未安装 (npm install, pip install)
- 网络问题
```

### 问题 3：Skill 结果不符合预期

```
调试步骤：
1. 检查 settings.json 的环境变量
2. 阅读 skill 源文件中的注释
3. 尝试更详细的提示词
4. 用 /skill xxx --debug 启用调试模式（如果支持）
```

---

## 📞 获取帮助

- 查看每个 skill 内部的文档（`.md` 文件）
- 查看 `configurations/` 目录下的配置说明
- 查看 [README.md](./README.md)
- 在 Claude Code 中直接提问

---

**最后更新**：2026-05-11  
**Skills 总数**：98+  
**推荐开始**：gaoyan-daily-report, gaoyan-ingest, web-access
