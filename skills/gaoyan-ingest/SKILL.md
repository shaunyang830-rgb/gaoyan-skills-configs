---
name: gaoyan-ingest
description: |
  高岩科技知识库入库处理 skill。当用户说"入库"、"入库处理"、"帮我入库"、"处理这个文件"、"把这个加入知识库"、"归档这个"，或者提供了 PPTX/PDF/DOCX/XLSX/网页/录音转录文件并希望整理进 Obsidian vault 时，必须使用此 skill。
  
  支持所有文件类型：PDF、PPTX、DOCX、XLSX、HTML/网页、Markdown、DingTalk 录音转录文本。
  
  核心能力：使用 MarkItDown 提取文档内容（比手动解析更准确），生成标准 MD 笔记，补 frontmatter，加双链，关联高岩业务洞察。
  
  厚报告、蓝皮书、已存在「## 逐页内容 + ### Slide」合并抽取稿、需**逐页重点页 + 摘要 + 原文**三件套时，改用 **`gaoyan-ingest-full-version`**（见该 skill），勿用 MarkItDown 代替数据底稿。
---

# 高岩知识库入库处理

## 核心工具：MarkItDown

所有文档提取**优先使用 MarkItDown**，不要用 extract.py 或手动解析。

```python
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from markitdown import MarkItDown
md = MarkItDown()
result = md.convert(r"<文件绝对路径>")
print(result.text_content)
```

MarkItDown 支持：PDF、PPTX、DOCX、XLSX、HTML、音频（需 openai key）、YouTube URL。

**注意**：
- 复杂图表（Marimekko、气泡图等）的视觉部分会变成 `![图片 N](图片N.jpg)` 占位符，但图表的**底层数据文字**（数字、标签、百分比）通常会被提取出来——这对 RAG 已足够
- PPTX 输出格式：`<!-- Slide number: N -->` 分隔每页
- 如果 MarkItDown 失败（如加密 PDF），回退到 `pdfplumber` 或直接 Read 工具

## 入库流程

### Step 1：提取内容

```python
from markitdown import MarkItDown
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

md = MarkItDown()
result = md.convert(r"<文件绝对路径>")
content = result.text_content
print(content[:3000])  # 先看前3000字判断类型
```

### Step 2：判断类型和存放目录

| 内容类型 | 存放目录 | 文件名格式 |
|----------|----------|-----------|
| 行业报告、研究报告 | `高岩知识库/` | `{主题}_{来源}_{YYYYMMDD}.md` |
| 讲座、会议纪要、客户拜访 | `DingTalk/` | `{类型}_{标题}_{YYYYMMDD}.md` |
| 个人思考、灵感 | `Inspiration/` | `{标题}_{YYYYMMDD}.md` |
| 修行、佛学 | `个人知识库/佛学/` | `{标题}_{YYYYMMDD}.md` |
| 公司内部资料 | `01 Projects/` | `{标题}_{YYYYMMDD}.md` |

### Step 3：生成标准 MD 笔记

笔记结构：

```markdown
---
title: "文件标题"
tags: [标签1, 标签2, 标签3]
summary: "100字以内摘要"
links: [关键词1, 关键词2, 关键词3, 关键词4, 关键词5]
source: "原始文件名或来源URL"
date: "YYYY-MM-DD"
date_processed: "YYYY-MM-DD"
---

# 标题

## 核心内容

（提炼的主要内容，保留原文结构，用 Mermaid 还原图表，用 Markdown 表格还原数据表）

## 高岩关联洞察

（把外部内容与高岩业务连接：对餐观产品、客户报告、市场研究有何启发？）

## 待办事项

（如有行动项，用 ☐ 列出）
```

### Step 4：可视化格式保留规则

| 原始格式 | 转换方式 |
|----------|----------|
| 流程图/步骤图 | Mermaid `flowchart` |
| 树状/层级图 | Mermaid `graph TD` |
| 矩阵/象限图 | Mermaid `graph TB` + subgraph |
| 时间线 | Mermaid `flowchart LR` |
| 表格/数据对比 | Markdown 原生表格 |
| 复杂图表（Marimekko/气泡图等） | 保留 MarkItDown 提取的数字+标签文字，加注 `> 注：原图为复杂可视化，以下为提取的底层数据` |
| 带数据的柱状/饼图 | Mermaid `pie` 或 `xychart-beta`（如数据量合适） |

### Step 5：加双链

- 扫描已有 Wiki 页（`高岩知识库/` 中的概念页）
- 在笔记中用 `[[概念页名]]` 链接相关概念
- 如果某个反复出现的概念没有 Wiki 页，新建一个

### Step 6：写入 vault

用 Write 工具写入目标路径。路径用相对路径。

### Step 7：告知归档

原始文件（PPTX/PDF/DOCX）不要删除，告知用户将原始文件移至对应"已处理"子目录（Bash 无文件移动权限，由用户手动操作）。

### Step 8：验证报告（必须执行）

入库完成后，立即对生成的 MD 文件运行以下验证，输出简洁的验证报告：

```python
import re, sys
sys.stdout = __import__('io').TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

path = r"<生成的MD文件绝对路径>"
try:
    content = open(path, encoding='utf-8').read()
    word_count = len(content)
    fm_fields = ['title', 'tags', 'summary', 'links', 'date_processed']
    checks = {
        "文件存在": True,
        "frontmatter 完整（5字段）": all(f in content for f in fm_fields),
        "字数 > 300": word_count > 300,
        "含高岩关联洞察章节": "高岩关联洞察" in content,
    }
except FileNotFoundError:
    checks = {"文件存在": False, "frontmatter 完整（5字段）": False, "字数 > 300": False, "含高岩关联洞察章节": False}

print("\n── 入库验证报告 ──")
all_pass = True
for k, v in checks.items():
    icon = "✅" if v else "❌"
    print(f"{icon} {k}")
    if not v:
        all_pass = False
if all_pass:
    print("\n✅ 全部通过，入库完成。")
else:
    print("\n⚠️  存在未通过项，需要补充后重新验证。")
```

---

## 快速参考：常见文件类型处理

### PPTX
- MarkItDown 提取效果好，每页有 `<!-- Slide number: N -->` 标记
- 图片变成占位符，但文字数据完整
- 重点提炼每页核心观点，不要逐字复制

### PDF（中文）

**提取策略（按优先级）：**

1. **普通 PDF（文字层完整）**：优先 MarkItDown，速度快，段落结构保留好
2. **含数据表格的报告**：改用 pdfplumber，表格提取质量明显更高
3. **扫描件 / 图片型 PDF**：用 pytesseract OCR
4. **加密 PDF**：先解密再提取

```python
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ① 先用 MarkItDown 快速提取，看前3000字判断是否有表格
from markitdown import MarkItDown
md = MarkItDown()
result = md.convert(r"<路径>")
print(result.text_content[:3000])
```

**如果报告含大量数据表格，切换 pdfplumber：**

```python
import pdfplumber, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with pdfplumber.open(r"<路径>") as pdf:
    for i, page in enumerate(pdf.pages):
        # 提取文字
        text = page.extract_text() or ""
        # 提取表格（返回 list of list）
        tables = page.extract_tables()
        if tables:
            print(f"\n--- 第{i+1}页 表格 ---")
            for table in tables:
                for row in table:
                    print(" | ".join(str(c or "") for c in row))
        if text:
            print(f"\n--- 第{i+1}页 文字 ---")
            print(text)
```

**如果是扫描件（MarkItDown 提取为空或乱码），用 OCR：**

```python
# 需要：pip install pytesseract pdf2image
# 需要：安装 Tesseract（含中文语言包 chi_sim）
import pytesseract
from pdf2image import convert_from_path
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

images = convert_from_path(r"<路径>")
for i, img in enumerate(images):
    text = pytesseract.image_to_string(img, lang='chi_sim+eng')
    print(f"\n--- 第{i+1}页 ---\n{text}")
```

### DOCX
- MarkItDown 直接支持，表格和标题层级保留

### XLSX
- MarkItDown 转为 Markdown 表格
- 如数据量大，只提取关键 sheet 或摘要统计

### DingTalk 录音转录（TXT/DOCX）
- 直接 Read 工具读取
- 判断类型：讲座/会议/拜访/个人思考
- 提炼要点，不要全文复制

---

## 高岩关联洞察写法

每篇入库笔记必须有"高岩关联洞察"章节，把外部内容与高岩业务连接：

- **餐观产品**：这个内容对餐观的数据分析功能、用户体验、产品路线图有何启发？
- **客户报告**：可以用在哪类客户报告中？支持哪些论点？
- **市场研究**：印证或挑战了哪些行业判断？
- **竞争格局**：涉及竞争对手或市场机会的信息

如果内容与高岩业务无关（如佛学笔记），此章节可省略。
