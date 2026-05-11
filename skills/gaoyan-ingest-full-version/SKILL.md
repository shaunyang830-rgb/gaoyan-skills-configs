---
name: gaoyan-ingest-full-version
description: |
  高岩「全文专业入库」流程：面向厚报告、蓝皮书、数据密集型 PPTX/PDF 入库。当用户说「全文入库」「专业入库」「重点页全文」「/gaoyan-ingest-full-version」「详细版入库」「蓝皮书逐页结构化」「原文+摘要双文件」或已有一份含「## 逐页内容」「### Slide N」的合并 MD（OOXML+xlsb 抽取稿）需要拆成「重点页版 + 摘要 + 原文底稿」时必须使用本 skill。
  
  与 `gaoyan-ingest` 分工：MarkItDown 适合快速归档；本 skill 适合**需逐页检索、表格式交付、数值可审计**的完整版。不要替代法务/免责审阅；母版噪声页需人工抽查。
---

# 高岩全文专业入库（gaoyan-ingest-full-version）

## 何时用

- 厚 PPT 已用 `_pptx_full_extract.py`（或同类）生成**单文件合并 MD**：含 `## 逐页抽取`、`## 逐页内容`、`### Slide N`、图表 `tsv`。
- 用户要求：**每一页**都按「出品 / 页码 / 核心观点 / 要点摘要 / 表 / 数据来源 / 技术附录指向」交付；并另附**摘要 MD**。
- 触发词：`全文入库`、`专业入库`、`重点页全文`、`详细版入库`、`/gaoyan-ingest-full-version`、蓝皮书**逐页**结构化。

## 产出物（固定三件套 + 索引）

由脚本一次生成（勿手抄 58 遍）：

| 文件 | 作用 |
| --- | --- |
| `{基名}_原文.md` | 自 `## 逐页抽取` 起的 **OOXML + xlsb + chart 解析** 底稿，供审计与 Excel 复核。 |
| `{基名}_重点页全文.md` | **逐页** `## 重点页：Slide N｜标题`；机器抽取+规则清洗；脚注与口径见各页。 |
| `{基名}_摘要.md` | 报告级短摘要 + **逐页一句话**速览表。 |
| `{基名}_入库索引.md` | Obsidian 入口，双链到以上三份。 |

**母文件**（输入）：保留含 `## 逐页内容` 的合并 MD，供脚本重复运行；文首若已有手写「重点页」可与脚本产出并存，或删掉文首重复段以免维护两处。

## 执行步骤

### 1. 准备输入

- 输入 MD 必须包含：`## 逐页内容` 与 `### Slide 1` … `### Slide N`（与 PPT 页序一致）。
- 推荐同时含 `## 逐页抽取（OOXML + 图表底稿）`，以便写入 `_原文.md`。

### 2. 运行脚本（必须）

在 Vault 根或任意目录执行（路径改为实际文件）：

```bash
python .claude/skills/gaoyan-ingest-full-version/scripts/slide_appendix_to_structured.py "高岩知识库/高岩文件库/<合并入库文件>.md"
```

脚本路径亦可用绝对路径。依赖：仅 Python 3.10+ 标准库。

### 3. 人工抽查（建议）

- 随机 **5～10 页**与 PPT 视觉核对表头、单位、百分比。
- **母版污染页**（如误入英文医疗占位）：脚本已做英文块剔除，仍建议对照 `_ppt_export_.../slide_NNN.png` 若已导出。

### 4. Obsidian 收尾

- 在索引或公众号稿中加 `[[..._重点页全文]]`、`[[..._摘要]]`。
- 按需补 `## 高岩关联洞察`（脚本不自动生成业务洞察段）。

## 重点页版式（脚本输出模板）

每一页：

```markdown
## 重点页：Slide N｜{标题}

**核心观点**：{1～3 句，规则从正文首句抽取}

**要点摘要**

- …

### 表 m（若有 Markdown 表）

| … |

数据来源：…

**技术附录**：图表 `c:f`、xlsb `tsv` 见原文 [[…_原文]]（检索 `### Slide N`）。

---
```

## 与 `gaoyan-ingest` 的配合

1. **首次提取**：复杂 PPT 仍建议走仓库内 **OOXML + xlsb** 全量抽取（保证图表数与幻灯片一致），而非仅 MarkItDown。
2. **二次结构化**：对合并 MD 运行本 skill 的脚本 → 三件套。
3. **轻量材料**：单篇 PDF/短 DOCX 继续用 `gaoyan-ingest` + MarkItDown 即可，不必启用本流程。

## 脚本维护

- 路径：`.claude/skills/gaoyan-ingest-full-version/scripts/slide_appendix_to_structured.py`
- 调整标题/要点启发式时改脚本内 `infer_title`、`infer_thesis`、`strip_english_template_blocks`，勿在 SKILL 内堆长代码。
