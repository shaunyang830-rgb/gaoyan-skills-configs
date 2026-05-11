---
name: gaoyan-ppt-design
description: >-
  Create professional presentations in Gaoyan Technology (高岩科技) brand style using
  GaoyanEngine (python-pptx wrapper). Use when user asks to create slides, reports,
  pitch decks, industry analysis, or any PPTX in Gaoyan visual identity — even if they
  just say "做个PPT" or "出个报告". Supports 22 layout methods across 8 categories.
  Trigger on: 高岩PPT, 高岩报告, 高岩幻灯片, Gaoyan slides, 品牌PPT, 客户报告, 行业报告PPT.
---

# 高岩科技 PPT 设计引擎 (GaoyanEngine)

> **Version**: 1.0.0 · **Author**: 高岩科技
>
> **Required tools**: Read, Write, Bash · **Requires**: python3, pip

## Overview

GaoyanEngine 是高岩科技品牌视觉体系的 PPT 生成引擎，基于 255 页官方模板 + 42 页设计培训讲义。与 MckEngine（McKinsey 风格）的核心差异：

| 维度 | McKinsey (MckEngine) | 高岩 (GaoyanEngine) |
|------|---------------------|---------------------|
| 图形风格 | 直角矩形 | **圆角矩形** |
| 中文字体 | KaiTi 楷体 | **微软雅黑** |
| 英文字体 | Georgia | **Century Gothic** |
| 标题风格 | Action Title + 下划线 | **绿色标签条 + Action Title + 子结论条** |
| 主色 | NAVY #051C2C | **高岩蓝 #061F32 + 高岩绿 #01EFC1** |
| 品牌元素 | 无 | **右下角 "高岩 GAOYAN" + 页码** |

## 设计上下文优先原则（必须遵守）

> **"好设计不从零开始——它根植于已有的设计上下文。"**
> 从零 Mock 完整产品是最后手段，会导致设计效果差。

**开始生成前，必须按顺序执行：**

1. **读取品牌资产**（按优先级）：
   - 检查 `01 Projects/` 是否有品牌文件、VI 规范、现有 PPT
   - 检查 vault 中是否有客户/项目相关的已有设计文件
   - 检查用户是否提供了参考文件路径

2. **读取内容上下文**：
   - 相关行业报告（`高岩知识库/`）
   - 相关日报/分析（`01 Projects/日报/`）
   - 用户提到的具体数据来源

3. **找不到上下文时，必须问用户**：
   - 目标受众是谁？
   - 有没有参考风格或现有文件？
   - 核心结论是什么（不是主题，是结论）？

4. **给出 2-3 个结构变体**供用户选择，再动手生成。

**禁止行为**：不读任何现有文件就直接开始写代码生成 PPT。

---

## When to Use This Skill

1. 用户要求创建**高岩科技品牌**风格的PPT
2. 制作**餐饮行业分析报告**（日报、周报、行业白皮书）
3. 制作**客户提案**（赋能陪跑方案、数据分析报告）
4. 制作**公司介绍**（融资BP、公司简介）
5. 任何需要**高岩绿+蓝色系**视觉风格的PPT

## 设计上下文优先原则（必须执行）

> "Good hi-fi designs do not start from scratch — they are rooted in existing design context."
> — Claude Design 系统提示词

**从零开始 Mock 是最后手段，会导致设计效果差。**

### 开始前必须做的事（按顺序）

1. **读取品牌资产**：检查以下路径是否存在相关文件：
   - `01 Projects/` — 公司资料、历史PPT、品牌文件
   - `高岩知识库/` — 行业报告原件（PPTX/PDF）
   - 用户当前提到的任何参考文件

2. **读取历史同类PPT**：如果是客户报告，找同一客户的历史文件；如果是行业报告，找同品类的历史报告。

3. **提取设计上下文**：从已有文件中提取：
   - 客户名称、行业、品牌色偏好
   - 报告结构惯例（几页、哪些章节）
   - 数据来源标注格式

4. **找不到上下文时**：向用户询问以下信息再开始：
   - 受众是谁（内部/客户/投资人）
   - 报告目的（说服/汇报/提案）
   - 有无参考文件或历史版本

### 禁止行为
- ❌ 不读任何现有文件就直接开始生成
- ❌ 用通用占位内容填充客户专属页面
- ❌ 忽略用户提到的参考文件或历史版本

## Setup

```bash
pip install python-pptx lxml
```

## Quick Start

```python
import sys
sys.path.insert(0, r'<vault>/.claude/skills/gaoyan-ppt-design')
from gaoyan_ppt import GaoyanEngine

eng = GaoyanEngine(total_slides=10)

# 封面
eng.cover('中国餐饮行业\n年度趋势报告', subtitle='Annual Trend Report',
          date='2026.04', author='高岩科技')

# 目录
eng.toc(items=[(1, '市场总览', 'Market Overview'),
               (2, '品类分析', 'Category Analysis'),
               (3, '趋势预测', 'Trend Forecast')])

# 章节页
eng.section_divider(section_label='PART 01', title='市场总览')

# 大数字页
eng.big_number('中国餐饮市场规模突破5万亿', number='5.2', unit='万亿元',
               description='同比增长12.3%，创历史新高',
               tag='市场总览', sub_conclusion='餐饮市场持续回暖',
               source='Source: 国家统计局, 2025')

# 洞察页
eng.key_insight('新茶饮赛道增速放缓但利润提升',
                left_content='新茶饮市场规模达3,000亿元...',
                right_takeaways=['头部品牌集中度提升', '下沉市场仍有空间', '供应链成为核心壁垒'],
                tag='品类分析', source='Source: 高岩餐观大数据')

# 环形图
eng.donut('中式正餐品类结构', segments=[
    {'label': '火锅', 'value': 35},
    {'label': '川菜', 'value': 25},
    {'label': '粤菜', 'value': 20},
    {'label': '其他', 'value': 20},
], center_label='品类占比', tag='品类分析',
   source='Source: 高岩餐观大数据')

# 结尾
eng.closing(title='THANKS!', message='数智餐饮 共创味来')

eng.save('output.pptx')
```

## 全部版式方法 (22个)

### A. 结构导航 (5个)

| 方法 | 用途 | 关键参数 |
|------|------|----------|
| `cover(title, subtitle, author, date, project)` | 封面页（左信息+右图片区） | title支持\n换行 |
| `cover_fullscreen(title, subtitle, date)` | 全屏背景封面 | 大图背景+右下角信息区 |
| `toc(title, items, source)` | 目录页 | items: list of (num, title, desc) |
| `section_divider(section_label, title, subtitle)` | 章节分隔页 | 深蓝背景 |
| `closing(title, message, source_text)` | 结尾感谢页 | |

### B. 数据统计 (3个)

| 方法 | 用途 | 关键参数 |
|------|------|----------|
| `big_number(title, number, unit, description, detail_items)` | 大数字突出展示 | detail_items: list of (label, value) |
| `three_stat(title, stats)` | 三指标仪表盘 | stats: list of {number, unit, label, trend} |
| `data_table(title, headers, rows, col_widths, highlight_cols)` | 数据表格 | highlight_cols: 高亮列索引 |

### C. 洞察 / Key Findings (2个)

| 方法 | 用途 | 关键参数 |
|------|------|----------|
| `key_insight(title, left_content, right_takeaways)` | 左内容+右洞察面板 | right_takeaways: list[str] |
| `chart_insight(title, chart_placeholder_label, takeaways)` | 图表+右洞察面板 | 左侧图表占位 |

### D. 对比评估 (3个)

| 方法 | 用途 | 关键参数 |
|------|------|----------|
| `side_by_side(title, options)` | N列并排对比 | options: list of {heading, points, color} |
| `before_after(title, before_title, before_points, after_title, after_points)` | 前后对比 | 红Before→绿After |
| `pros_cons(title, pros, cons, conclusion)` | 优劣分析 | 底部结论条 |

### E. 框架矩阵 (4个)

| 方法 | 用途 | 关键参数 |
|------|------|----------|
| `matrix_2x2(title, quadrants, axis_labels)` | 四象限矩阵 | quadrants: TL/TR/BL/BR, axis_labels: {top,bottom,left,right} |
| `process_chevron(title, steps)` | 横向流程箭头 | steps: list of {number, heading, description} |
| `vertical_steps(title, steps)` | 垂直步骤 | 左圆点+连接线+右内容 |
| `timeline(title, milestones)` | 时间线 | 上下交替里程碑 |

### F. 团队/案例 (2个)

| 方法 | 用途 | 关键参数 |
|------|------|----------|
| `meet_the_team(title, members)` | 团队介绍 | members: list of {name, role, description} |
| `case_study(title, sections, result_box)` | 案例研究 | sections: list of {heading, content}, result_box可选 |

### G. 图表 (4个)

| 方法 | 用途 | 关键参数 |
|------|------|----------|
| `grouped_bar(title, categories, series, data)` | 分组柱状图 | data[series_idx][cat_idx] |
| `stacked_bar(title, periods, series, data)` | 堆叠柱状图 | data[series_idx][period_idx] |
| `donut(title, segments, center_label, summary)` | 环形图(BLOCK_ARC) | segments: list of {label, value, color} |
| `horizontal_bar(title, items)` | 水平条形图 | items: list of {label, value, color} |

### H. 高岩特色 (2个)

| 方法 | 用途 | 关键参数 |
|------|------|----------|
| `egpm_flavor_card(title, chart_placeholder_label, flavor_cards)` | EGPM风味卡片 | flavor_cards: list of {title, description, image_label} |
| `three_column_insight(title, columns, takeaways)` | 三列+洞察面板 | columns: list of {heading, content} |

## 视觉 QA（必须执行）

**第一次渲染几乎不会完全正确。把 QA 当 bug hunt，不是确认步骤。**

### Step 1：内容 QA

```bash
python -m markitdown output.pptx
```

检查：内容是否完整、顺序是否正确、有无遗漏页面。

### Step 2：转图片

```bash
# 需要 LibreOffice（soffice）和 poppler（pdftoppm）
soffice --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
# 生成 slide-01.jpg, slide-02.jpg ...
```

Windows 下 LibreOffice 路径通常为：
```bash
"C:\Program Files\LibreOffice\program\soffice.exe" --headless --convert-to pdf output.pptx
```

### Step 3：用 Subagent 视觉检查

**必须用 Subagent**——你盯着代码看会产生预期偏差，Subagent 有新鲜视角。

```
用 subagent 视觉检查以下幻灯片图片，假设存在问题，找出所有问题：

检查项：
- 文字溢出或被截断（超出文本框边界）
- 元素重叠（文字穿过图形、线条穿过文字）
- 间距不均匀（某处留白过大，某处过于拥挤）
- 边距不足（距幻灯片边缘 < 0.5 英寸）
- 对齐不一致（同类元素未对齐）
- 低对比度文字（浅色文字在浅色背景上）
- 高岩绿标签条文字是否清晰可读
- 品牌元素（右下角"高岩 GAOYAN"）是否存在

图片路径：
1. slide-01.jpg
2. slide-02.jpg
...

列出所有问题，包括轻微问题。
```

### Step 4：修复循环

1. 列出发现的问题
2. 修复
3. 重新转图片（只转受影响的页）：
   ```bash
   pdftoppm -jpeg -r 150 -f N -l N output.pdf slide-fixed
   ```
4. 重新检查，直到一轮完整检查无新问题

**不要在完成至少一次修复-验证循环之前宣布完成。**

---

## 通用参数

所有详情页方法都支持以下可选参数：
- `tag`: str — 左上角绿色标签条文字（章节名）
- `sub_conclusion`: str — 标题下方子结论条文字
- `source`: str — 底部数据来源

## 设计规范要点

1. **标题必须是一句完整结论**，不是简单标签
2. **圆角矩形**为默认图形，不用直角
3. **颜色不使用渐变**，高亮色（绿色）仅点缀
4. **单页信息点 ≤ 3**，文字行数 ≤ 6
5. **字体严格层级**：Action Title 24pt → Sub-header 20pt → Body 14pt → Source 9pt
6. **CJK文字自动使用微软雅黑**，英文/数字用 Century Gothic

## 品牌色板

| 颜色 | HEX | 变量名 | 用途 |
|------|-----|--------|------|
| 高岩蓝 | #061F32 | GAOYAN_BLUE | 深色背景、标题 |
| 高岩绿 | #01EFC1 | GAOYAN_GREEN | 标签条、装饰、点缀 |
| 高岩灰 | #3E3939 | GAOYAN_GRAY | 正文文字 |
| 厨人黄 | #FCD200 | CHEF_YELLOW | 品牌延展色 |
| 数据蓝 | #2156C7 | DATA_BLUE_4 | 重要数据强调 |
| 警示红 | #FB440F | ACCENT_RED | 负面/风险 |
| 正面绿 | #00B050 | POSITIVE_GREEN | 正增长 |

## 文件结构

```
.claude/skills/gaoyan-ppt-design/
├── gaoyan_ppt/
│   ├── __init__.py       # from .engine import GaoyanEngine
│   ├── constants.py      # 所有设计常量、颜色、字号、坐标
│   ├── core.py           # 基础绘图原语 (add_rect, add_text, etc.)
│   └── engine.py         # GaoyanEngine 主引擎 (22个版式方法)
├── SKILL.md              # 本文件
└── storylines/           # 预设故事线模板
```
