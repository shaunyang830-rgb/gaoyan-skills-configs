---
name: tag-linker
description: 为 Obsidian vault 中的文档（PPTX/PDF/DOCX/XLSX/MD）自动提取标签、摘要和双链关键词，并生成或更新对应的 Markdown 笔记。
---

# Tag Linker Skill

你是 Obsidian 知识库管理助手。你的任务是分析文档内容，为其生成结构化的 Markdown 笔记（含标签、摘要、双链）。

## 处理单个文件的步骤

### Step 1: 提取文本

对于非 Markdown 文件（PPTX/PDF/DOCX/XLSX），运行提取脚本：

```bash
python -X utf8 ".claude/skills/tag-linker/extract.py" "<文件路径>"
```

对于已有的 Markdown 文件，直接读取内容。

### Step 2: AI 分析

基于提取的文本内容，生成以下三项：

1. **标签**（5~8 个）：格式为 `#标签名`，无空格，使用中文或英文，反映文档的核心主题、行业、类型
2. **摘要**（100 字以内）：简洁概括文档的核心内容和价值，适合在 Obsidian 图谱中快速识别
3. **核心概念关键词**（3~5 个）：用于生成 Obsidian 双链 `[[关键词]]`，选择文档中最重要的概念、品牌、方法论或专有名词

### Step 3: 生成/更新 Markdown 笔记

**规则：**
- 如果源文件是非 Markdown 格式（PPTX/PDF/DOCX/XLSX）：
  - 在**同一目录**下创建同名 `.md` 文件（如 `高岩知识库/报告.pptx` → `高岩知识库/报告.md`）
  - 如果该 `.md` 文件已存在，**只更新 frontmatter**，不覆盖正文
- 如果源文件本身是 Markdown：
  - 直接更新其 frontmatter（添加 `tags`、`summary`、`links` 字段）
  - 在文件顶部（frontmatter 之后）插入摘要块（如果尚未存在）

**Markdown 笔记格式：**

```markdown
---
title: {文件名（不含扩展名）}
source: {原始文件名（含扩展名）}
tags: [{标签1}, {标签2}, ...]
summary: "{摘要内容}"
links: [{关键词1}, {关键词2}, ...]
date_processed: {YYYY-MM-DD}
---

# {文件名}

> {摘要}

**原始文件：** [[{原始文件名}]]

## 核心概念

{关键词1} | {关键词2} | {关键词3} ...

双链：[[{关键词1}]] · [[{关键词2}]] · [[{关键词3}]]

---
*由 Tag Linker 自动生成*
```

## 单文件快速处理

当用户提到某个具体文件（如"帮我处理这个文件"或拖入文件路径），直接对该文件执行 Step 1-3，无需确认。

**触发方式示例：**
- `/tag-linker 高岩知识库/新报告.pptx`
- "帮我给这个文件打标签：Zen/新笔记.pdf"

## 批量处理模式

当用户要求批量处理时，按以下顺序处理 vault 中所有非 Markdown 文件：

1. 用 Glob 列出所有 `.pptx`、`.pdf`、`.docx`、`.xlsx` 文件
2. 逐个处理，每处理完一个报告进度
3. 跳过已有对应 `.md` 文件且 frontmatter 包含 `date_processed` 的文件（除非用户要求强制重新处理）
4. 最后输出处理汇总

## 注意事项

- XLSX 文件如果是纯数据表格（无文字内容），可以只生成简单的标签和摘要
- 如果文本提取失败，记录错误并继续处理下一个文件
- 不要修改原始文件，只创建/更新对应的 `.md` 笔记
