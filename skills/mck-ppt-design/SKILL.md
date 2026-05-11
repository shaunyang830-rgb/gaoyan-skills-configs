---
name: mck-ppt-design
description: >-
  Create professional, consultant-grade PowerPoint presentations from scratch
  using MckEngine (python-pptx wrapper) with McKinsey-style design. Use when
  user asks to create slides, pitch decks, business presentations, strategy
  decks, quarterly reviews, board meeting slides, or any professional PPTX.
  AI calls eng.cover(), eng.donut(), eng.timeline() etc — 67 high-level methods
  across 12 categories (structure, data, framework, comparison, narrative,
  timeline, team, charts, images, advanced viz, dashboards, visual storytelling),
  consistent typography, zero file-corruption issues, BLOCK_ARC native shapes
  for circular charts (donut, pie, gauge), production-hardened guard rails
  for spacing, overflow, legend consistency, title style uniformity,
  dynamic sizing for variable-count layouts, horizontal item overflow
  protection, chart rendering, and
  AI-generated cover images via Tencent Hunyuan 2.0 with professional cutout,
  cool grey-blue tint, and McKinsey-style Bézier ribbon decoration.
---

# McKinsey PPT Design Framework

> **Copyright © 2024-2026 Kaku Li (https://github.com/likaku).** Licensed under Apache 2.0. See [NOTICE](NOTICE).

> **Version**: 2.2.0 · **License**: Apache-2.0 · **Author**: [likaku](https://github.com/likaku/Mck-ppt-design-skill)
>
> **Required tools**: Read, Write, Bash · **Requires**: python3, pip

## Overview

This skill encodes the complete design specification for **professional business presentations** — a consultant-grade PowerPoint framework based on McKinsey design principles. It includes:

- **65 layout patterns** across 12 categories (structure, data, framework, comparison, narrative, timeline, team, charts, **images**, **advanced viz**, **dashboards**, **visual storytelling**)
- **Color system** and strict typography hierarchy
- **Python-pptx code patterns** ready to copy and customize
- **Three-layer defense** against file corruption (zero `p:style` leaks)
- **Chinese + English font handling** (KaiTi / Georgia / Arial)
- **Image placeholder system** for image-containing layouts (v1.8)
- **BLOCK_ARC native shapes for charts** — donut, pie, gauge rendered with 3-4 shapes instead of hundreds of blocks, 60-80% smaller files (v2.0)
- **Production Guard Rails** — 10 mandatory rules including spacing/overflow protection, legend color consistency, title style uniformity, axis label centering, dynamic sizing, BLOCK_ARC chart rendering, horizontal item overflow protection (v1.9+v2.0+v2.3)
- **Code Efficiency guidelines** — variable reuse patterns, constant extraction, loop optimization for faster generation (v1.9)
- **AI-generated cover images** — Tencent Hunyuan 2.0 text-to-image → rembg professional cutout → cool grey-blue tint + 50% lighten → McKinsey-style Bézier ribbon curves → transparent RGBA PNG full-bleed background (v2.2)

All specifications have been refined through iterative production feedback to ensure visual consistency, professional polish, and zero-defect output.

---

## When to Use This Skill

Use this skill when users ask to:

1. **Create presentations** — pitch decks, strategy presentations, quarterly reviews, board meeting slides, consulting deliverables, project proposals, business plans
2. **Generate slides programmatically** — using python-pptx to produce .pptx files from scratch
3. **Apply professional design** — McKinsey / BCG / Bain consulting style, clean flat design, no shadows or gradients
4. **Build specific slide types** — cover pages, data dashboards, 2x2 matrices, timelines, funnels, team introductions, executive summaries, comparison layouts
5. **Fix PPT issues** — file corruption ("needs repair"), shadow/3D artifacts, inconsistent fonts, Chinese text rendering problems
6. **Maintain design consistency** — unified color palette, font hierarchy, spacing, and line treatments across all slides

---


---

## MckEngine Quick Start (v2.0)

v2.0 introduces a **Python runtime engine** (`mck_ppt/`) that encapsulates all 67 layout methods. Instead of writing raw `add_shape()` / `add_text()` coordinate code, the AI calls high-level methods like `eng.cover()`, `eng.donut()`, `eng.timeline()`.

### Why Use MckEngine

| | v1.x (inline code) | v2.0 (MckEngine) |
|---|---|---|
| Code generation | AI writes `add_shape()` + coordinate math per slide | AI calls `eng.cover()`, `eng.donut()` etc. |
| Output tokens per 30-slide deck | 40,000–60,000 | 9,000–12,000 |
| Rounds per deck | 10–15 | 3–4 |
| Chart rendering | `add_rect()` stacking (100–2,800 shapes) | `BLOCK_ARC` native arcs (3–4 shapes) |
| File corruption risk | Manual cleanup needed | Automatic three-layer defense |

### Setup

```bash
pip install python-pptx lxml
```

The `mck_ppt/` package lives inside the skill directory. Before generating any presentation, the AI MUST:

```python
import sys, os
sys.path.insert(0, os.path.expanduser('~/.workbuddy/skills/mck-ppt-design'))
from mck_ppt import MckEngine
```

### Complete Generation Pattern

Every presentation script follows this exact pattern:

```python
import sys, os
sys.path.insert(0, os.path.expanduser('~/.workbuddy/skills/mck-ppt-design'))
from mck_ppt import MckEngine
from mck_ppt.constants import *  # NAVY, ACCENT_BLUE, etc.
from pptx.util import Inches

eng = MckEngine(total_slides=12)  # Set total for page numbering

# ── Structure ──
eng.cover(title='Q1 2026 战略回顾', subtitle='董事会汇报', author='战略部', date='2026年3月', cover_image='auto')
eng.toc(items=[('1', '市场概览', '当前竞争格局'),
               ('2', '财务分析', '营收与利润趋势'),
               ('3', '战略建议', '三大核心行动')])

# ── Content slides ──
eng.section_divider(section_label='第一部分', title='市场概览')
eng.big_number(title='市场规模', number='¥850亿', description='2026年预估市场总量',
    detail_items=['同比增长23%', '线上渠道占比突破60%'], source='Source: 行业报告 2026')
eng.donut(title='市场份额分布',
    segments=[(0.35, NAVY, '我们'), (0.25, ACCENT_BLUE, '竞品A'),
              (0.20, ACCENT_GREEN, '竞品B'), (0.20, ACCENT_ORANGE, '其他')],
    center_label='35%', center_sub='市占率', source='Source: 市场调研 2026')

eng.section_divider(section_label='第二部分', title='财务分析')
eng.grouped_bar(title='季度营收趋势',
    categories=['Q1', 'Q2', 'Q3', 'Q4'],
    series=[('产品', NAVY), ('服务', ACCENT_BLUE)],
    data=[[120, 80], [145, 95], [160, 110], [180, 130]],
    max_val=200, source='Source: 财务部')

eng.section_divider(section_label='第三部分', title='战略建议')
eng.table_insight(title='三大战略方向对比',
    headers=['战略方向', '核心举措', '预期成效'],
    rows=[['产品创新', 'AI赋能 + 用户体验升级', '市场份额+15%'],
          ['市场拓展', '进入3个新行业 + 海外布局', '营收增长30%'],
          ['运营卓越', '成本优化20% + 数字化覆盖85%', '利润率+8pp']],
    insights=['三大方向协同发力，形成增长飞轮', '产品创新为引擎，市场拓展为杠杆', '运营卓越为底座，确保可持续性'],
    source='Source: 战略部')
eng.timeline(title='执行路线图',
    milestones=[('Q1', '方案设计'), ('Q2', '试点验证'),
                ('Q3', '规模推广'), ('Q4', '效果评估')],
    source='Source: PMO')

# ── Closing ──
eng.closing(title='谢谢', message='期待与您进一步交流')

# ── Save (auto cleanup) ──
eng.save('output/q1_strategy_review.pptx')
print('Done! 12 slides generated.')
```

### Key Rules

1. **One method = one slide**. `eng.cover()` creates slide 1, `eng.toc()` creates slide 2, etc.
2. **`eng.save()` handles everything** — XML cleanup, shadow removal, p:style sanitization. No manual `full_cleanup()` needed.
3. **Page numbers are automatic** — the engine tracks `_page` internally.
4. **All guard rails are built-in** — dynamic sizing, overflow protection, CJK font handling.
5. **Use constants from `mck_ppt.constants`** — `NAVY`, `ACCENT_BLUE`, `BG_GRAY`, `BODY_SIZE`, etc.

---

## Core Design Philosophy

### McKinsey Design Principles

1. **Extreme Minimalism** - Remove all non-essential visual elements
   - No color blocks unless absolutely necessary
   - Lines: thin, flat, no shadows or 3D effects
   - Shapes: simple, clean, no gradients
   - Text: clear hierarchy, maximum readability

2. **Consistency** - Repeat visual language across all slides
   - Unified color palette (navy + cyan + grays)
   - Consistent font sizes and weights for same content types
   - Aligned spacing and margins
   - Matching line widths and styles

3. **Hierarchy** - Guide viewer through information
   - Title bar (22pt) → Sub-headers (18pt) → Body (14pt) → Details (9pt)
   - Navy for primary elements, gray for secondary, black for divisions
   - Visual weight through bold, color, size (not through effects)

4. **Flat Design** - No 3D, shadows, or gradients
   - Pure solid colors only
   - All lines are simple strokes with no effects
   - Shapes have no shadow or reflection effects
   - Circles are solid fills, not 3D spheres

---

## Design Specifications

### Color Palette

All colors in RGB format for python-pptx:

| Color Name | Hex | RGB | Usage | Notes |
|-----------|-----|-----|-------|-------|
| **NAVY** | #051C2C | (5, 28, 44) | Primary, titles, circles | Corporate, formal tone |
| **CYAN** | #00A9F4 | (0, 169, 244) | Originally used in v1 | **DEPRECATED** - Use NAVY for consistency |
| **WHITE** | #FFFFFF | (255, 255, 255) | Backgrounds, text | On navy backgrounds only |
| **BLACK** | #000000 | (0, 0, 0) | Lines, text separators | For clarity and contrast |
| **DARK_GRAY** | #333333 | (51, 51, 51) | Body text, descriptions | Main content text |
| **MED_GRAY** | #666666 | (102, 102, 102) | Secondary text, labels | Softer tone than DARK_GRAY |
| **LINE_GRAY** | #CCCCCC | (204, 204, 204) | Light separators, table rows | Table separators only |
| **BG_GRAY** | #F2F2F2 | (242, 242, 242) | Background panels | Takeaway/highlight areas |

**Key Rule**: Use navy (#051C2C) everywhere, especially for:
- All circle indicators (A, B, C, 1, 2, 3)
- All action titles
- All primary section headers
- All TOC highlight colors

#### Accent Colors (for multi-item differentiation)

When a slide contains **3 or more parallel items** (e.g., comparison cards, pillar frameworks, multi-category overviews), use these accent colors to create visual distinction between items. Without accent colors, parallel items become visually indistinguishable.

| Accent Name | Hex | RGB | Paired Light BG | Usage |
|-------------|-----|-----|-----------------|-------|
| **ACCENT_BLUE** | #006BA6 | (0, 107, 166) | #E3F2FD | First item accent |
| **ACCENT_GREEN** | #007A53 | (0, 122, 83) | #E8F5E9 | Second item accent |
| **ACCENT_ORANGE** | #D46A00 | (212, 106, 0) | #FFF3E0 | Third item accent |
| **ACCENT_RED** | #C62828 | (198, 40, 40) | #FFEBEE | Fourth item / warning |

**Accent Color Rules**:
- Use accent colors for: **card top accent borders** (thin 0.06" rect), **circle labels** (`add_oval()` bg param), **section sub-headers** (font_color)
- Use paired light BG for: **card background fills** only
- Body text inside cards ALWAYS remains **DARK_GRAY (#333333)**
- NAVY remains the primary color for **single-focus** elements (one card, one stat, cover title)
- Use accent colors **ONLY** when the slide has 3+ parallel items that need visual distinction
- The fourth item (D) can use NAVY instead of ACCENT_RED if red feels inappropriate for the content

```python
# Accent color constants
ACCENT_BLUE   = RGBColor(0x00, 0x6B, 0xA6)
ACCENT_GREEN  = RGBColor(0x00, 0x7A, 0x53)
ACCENT_ORANGE = RGBColor(0xD4, 0x6A, 0x00)
ACCENT_RED    = RGBColor(0xC6, 0x28, 0x28)
LIGHT_BLUE    = RGBColor(0xE3, 0xF2, 0xFD)
LIGHT_GREEN   = RGBColor(0xE8, 0xF5, 0xE9)
LIGHT_ORANGE  = RGBColor(0xFF, 0xF3, 0xE0)
LIGHT_RED     = RGBColor(0xFF, 0xEB, 0xEE)
```

---

### Typography System

#### Font Families

```
English Headers:  Georgia (serif, elegant)
English Body:     Arial (sans-serif, clean)
Chinese (ALL):    KaiTi (楷体, traditional brush style)
                  (fallback: SimSun 宋体)
```

**Critical Implementation**:
```python
def set_ea_font(run, typeface='KaiTi'):
    """Set East Asian font for Chinese text"""
    rPr = run._r.get_or_add_rPr()
    ea = rPr.find(qn('a:ea'))
    if ea is None:
        ea = rPr.makeelement(qn('a:ea'), {})
        rPr.append(ea)
    ea.set('typeface', typeface)
```

Every paragraph with Chinese text MUST apply `set_ea_font()` to all runs.

#### Font Size Hierarchy

| Size | Type | Examples | Notes |
|------|------|----------|-------|
| **44pt** | Cover Title | "项目名称" | Cover slide only, Georgia |
| **28pt** | Section Header | "目录" (TOC title) | Largest body content, Georgia |
| **24pt** | Subtitle | Tagline on cover | Cover slide only |
| **22pt** | Action Title | Slide title bars | Main content titles, **bold**, Georgia |
| **18pt** | Sub-Header | Column headers, section names | Supporting titles |
| **16pt** | Emphasis Text | Bottom takeaway on slide 8 | Callout text, bold |
| **14pt** | Body Text | Tables, lists, descriptions | **PRIMARY BODY SIZE**, all main content |
| **9pt** | Footnote | Source attribution | Smallest, gray color only |

**No other sizes should be used** - stick to this hierarchy exclusively.

---

### Line Treatment (CRITICAL)

#### Line Rendering Rules

1. **All lines are FLAT** - no shadows, no effects, no 3D
2. **Remove theme style references** - prevents automatic shadow application
3. **Solid color only** - no gradients or patterns
4. **Width varies by context** - see table below

#### Line Width Specifications

| Usage | Width | Color | Context |
|-------|-------|-------|---------|
| **Title separator** (under action titles) | 0.5pt | BLACK | Below 22pt title |
| **Column/section divider** (under headers) | 0.5pt | BLACK | Below 18pt headers |
| **Table header line** | 1.0pt | BLACK | Between header and first row |
| **Table row separator** | 0.5pt | LINE_GRAY (#CCCCCC) | Between table rows |
| **Timeline line** (roadmap) | 0.75pt | LINE_GRAY | Background for phase indicators |
| **Cover accent line** | 2.0pt | NAVY | Decorative bottom-left on cover |
| **Column internal divider** | 0.5pt | BLACK | Between "是什么" and "独到之处" |

#### Code Implementation (v1.1 — Rectangle-based Lines)

**CRITICAL**: Do NOT use `slide.shapes.add_connector()` for lines. Connectors carry `<p:style>` elements that reference theme effects and cause file corruption. Instead, draw lines as ultra-thin rectangles:

```python
def add_hline(slide, x, y, length, color=BLACK, thickness=Pt(0.5)):
    """Draw a horizontal line using a thin rectangle (no connector, no p:style)."""
    from pptx.util import Emu
    h = max(int(thickness), Emu(6350))  # minimum ~0.5pt
    return add_rect(slide, x, y, length, h, color)
```

**IMPORTANT**: Never use `add_connector()` — it causes file corruption. Always use `add_hline()` (thin rectangle).

#### Post-Save Full Cleanup (v1.1 — Nuclear Sanitization)

After `prs.save(outpath)`, ALWAYS run full cleanup that sanitizes **both** theme XML **and** all slide XML:

```python
import zipfile, os
from lxml import etree

def full_cleanup(outpath):
    """Remove ALL p:style from every slide + theme shadows/3D."""
    tmppath = outpath + '.tmp'
    with zipfile.ZipFile(outpath, 'r') as zin:
        with zipfile.ZipFile(tmppath, 'w', zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename.endswith('.xml'):
                    root = etree.fromstring(data)
                    ns_p = 'http://schemas.openxmlformats.org/presentationml/2006/main'
                    ns_a = 'http://schemas.openxmlformats.org/drawingml/2006/main'
                    # Remove ALL p:style elements from all shapes/connectors
                    for style in root.findall(f'.//{{{ns_p}}}style'):
                        style.getparent().remove(style)
                    # Remove shadows and 3D from theme
                    if 'theme' in item.filename.lower():
                        for tag in ['outerShdw', 'innerShdw', 'scene3d', 'sp3d']:
                            for el in root.findall(f'.//{{{ns_a}}}{tag}'):
                                el.getparent().remove(el)
                    data = etree.tostring(root, xml_declaration=True,
                                          encoding='UTF-8', standalone=True)
                zout.writestr(item, data)
    os.replace(tmppath, outpath)
```

---

### Text Box & Shape Treatment

#### Text Box Padding

All text boxes must have consistent internal padding to prevent text touching edges:

```python
bodyPr = tf._txBody.find(qn('a:bodyPr'))
# All margins: 45720 EMUs = ~0.05 inches
for attr in ['lIns','tIns','rIns','bIns']:
    bodyPr.set(attr, '45720')
```

#### Vertical Anchoring

Text must be anchored correctly based on usage:

| Content Type | Anchor | Code | Notes |
|--------------|--------|------|-------|
| Action titles | MIDDLE | `anchor='ctr'` | Centered vertically in bar |
| Body text | TOP | `anchor='t'` | Default, aligns to top |
| Labels | CENTER | `anchor='ctr'` | For circle labels |

```python
anchor_map = {
    MSO_ANCHOR.MIDDLE: 'ctr', 
    MSO_ANCHOR.BOTTOM: 'b', 
    MSO_ANCHOR.TOP: 't'
}
bodyPr.set('anchor', anchor_map.get(anchor, 't'))
```

#### Shape Styling

All shapes (rectangles, circles) must have:
- Solid fill color (no gradients)
- NO border/line (`shape.line.fill.background()`)
- **p:style removed** immediately after creation (`_clean_shape()`)
- No shadow effects (enforced by both inline cleanup and post-save full_cleanup)

```python
def _clean_shape(shape):
    """Remove p:style from any shape to prevent effect references."""
    sp = shape._element
    style = sp.find(qn('p:style'))
    if style is not None:
        sp.remove(style)

shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
shape.fill.solid()
shape.fill.fore_color.rgb = BG_GRAY
shape.line.fill.background()  # CRITICAL: removes border
_clean_shape(shape)            # CRITICAL: removes p:style
```

---

## Presentation Planning

This section provides **mandatory guidance** for planning presentation structure, selecting layouts, and ensuring adequate content density. These rules dramatically improve output quality across different LLM models.

### Recommended Slide Structures

When creating a presentation, follow these templates unless the user explicitly specifies a different structure:

#### Standard Presentation (10-12 slides)

```
 Slide 1:  Cover Slide (Pattern #1 or #4)
 Slide 2:  Table of Contents (Pattern #6) — list ALL content sections
 Slide 3:  Executive Summary / Core Thesis (Pattern #24 or #8+#10)
 Slides 4-7:  Supporting Arguments (one per slide, vary layouts)
 Slides 8-10: Case Studies / Evidence (Pattern #33 or #19)
 Slide 11: Synthesis / Roadmap (Pattern #29 or #16)
 Slide 12: Key Takeaways + Closing (Pattern #34 or #36)
```

#### Short Presentation (6-8 slides)

```
 Slide 1:  Cover Slide
 Slide 2:  Executive Summary (Pattern #24)
 Slides 3-5: Core Content (vary layouts: #8, #71, #19, #33)
 Slide 6:  Synthesis / Timeline (Pattern #29)
 Slide 7:  Key Takeaways (Pattern #34)
 Slide 8:  Closing (Pattern #36)
```

**CRITICAL RULES**:
- **Minimum slide count**: 8 slides for any substantive topic. If the user's content supports 10+, generate 10+.
- **Never stop early**: Generate ALL planned slides in a single script. Do not truncate.
- **TOC must list ALL sections**: The Table of Contents slide must enumerate every content slide by number and title.

### Layout Diversity Requirement

**Each content slide MUST use a DIFFERENT layout pattern from its neighbors.** Repeating the same layout on consecutive slides makes the presentation feel monotonous and unprofessional.

Match content type to the optimal layout pattern:

| Content Type | Recommended Layouts | Avoid |
|---|---|---|
| Single key statistic | Big Number (#8) | Plain text |
| 2 options comparison | Side-by-Side (#19), Before/After (#20), Metric Comparison Row (#62) | Two-column text |
| 3-4 parallel concepts | Table+Insight (#71), Four-Column (#27), Metric Cards (#10), Icon Grid (#63) | Bullet list |
| Process / steps | Process Chevron (#16), Vertical Steps (#30), Value Chain (#67) | Numbered text |
| Timeline | Timeline/Roadmap (#29), Cycle (#31) | Bullet list |
| Data table | Data Table (#9), Scorecard (#22), Harvey Ball Table (#56) | Plain text |
| Case study | Case Study (#33), Case Study with Image (#45) | Two-column text |
| Summary / conclusion | Executive Summary (#24), Key Takeaway (#25) | Bullet list |
| Multiple KPIs | Three-Stat Dashboard (#12), Two-Stat Comparison (#11), KPI Tracker (#52), Dashboard (#57) | Plain text |
| **Time series + values/percentages** | **Grouped Bar (#37), Stacked Bar (#38), Line Chart (#50), Stacked Area (#70)** | **Data Table, Scorecard** |
| **Category ranking / comparison** | **Horizontal Bar (#39), Grouped Bar (#37), Pareto (#51)** | **Bullet list, Plain text** |
| **Part-of-whole / composition** | **Donut (#48), Pie (#64), Stacked Bar (#38)** | **Bullet list** |
| **Content with visual / photo** | **Content+Right Image (#40), Left Image+Content (#41), Three Images (#42)** | **Text-only layouts** |
| **Risk / evaluation matrix** | **Risk Matrix (#54), SWOT (#65), Harvey Ball (#56), 2x2 Matrix (#13)** | **Bullet list** |
| **Strategic recommendations** | **Numbered List+Panel (#69), Decision Tree (#60), Checklist (#61)** | **Two-column text** |
| **Multi-KPI executive dashboard** | **Dashboard KPI+Chart (#57), Dashboard Table+Chart (#58)** | **Simple table** |
| **Stakeholder / relationship** | **Stakeholder Map (#59)** | **Bullet list** |
| **Meeting agenda** | **Agenda (#66)** | **Plain text** |
| **Opening analysis / key arguments** | **Table+Insight (#71), Key Takeaway (#25)** | **Bullet list, Plain text** |

**NEVER** use Two-Column Text (#26) for more than 1 slide per deck. It is the least visually engaging layout.

**OPENING SLIDE PRIORITY RULE**: For **Slides 2–5** (the first few content slides after cover/TOC), **strongly prefer high-impact editorial layouts** that set the tone for the entire presentation. Prioritized layouts for opening slides (in order of preference):
1. **Table+Insight (`table_insight`, #71)** — structured arguments with gray-bg right-panel takeaways + chevron icon
2. **Big Number (#8)** — single impactful statistic
3. **Key Takeaway (#25)** — left detail + right summary

These layouts create a strong visual opening that hooks the audience. Avoid starting presentations with plain text or simple bullet lists.

**CHART PRIORITY RULE**: When data contains dates/periods + numeric values or percentages (e.g., `3/4 正面 20% 中性 80%` or `Q1: ¥850万`), you **MUST** use a Chart pattern (#37-#39, #48-#56, #64, #70) instead of a text-based layout. Charts maximize data-ink ratio and are the most visually compelling way to present time-series data.

**IMAGE PRIORITY RULE** (v1.8): When the content involves case studies, product showcases, location overviews, or any scenario where a visual/photo would strengthen the narrative, prefer Image+Content layouts (#40-#47, #68) over text-only layouts. The `add_image_placeholder()` function creates gray placeholder boxes that users replace with real images after generation.

### Content Density Requirements

"Minimalism" in McKinsey design means **removing decorative noise** (shadows, gradients, clip-art), NOT removing content. A slide with 80% whitespace is not minimalist — it is EMPTY.

**Mandatory minimums per content slide**:

1. **At least 3 distinct visual blocks** — e.g., title bar + content area + takeaway box, or title + left panel + right panel
2. **Body text area utilization ≥ 50%** of the available content space (between title bar at 1.4" and source line at 7.05")
3. **Action Title must be a FULL SENTENCE** expressing the slide's key insight:
   - ✅ `"连接组约束的AI模型将自由参数减少90%，实现单细胞精度预测"`
   - ❌ `"连接组约束的AI模型"`
4. **Use specific data points** when the user provides them (numbers, percentages, names) — display them prominently with Big Number or Metric Card patterns
5. **Source attribution** (`add_source()`) on every content slide with specific references, not generic labels

### Production Guard Rails (v1.9 / v2.0)

These rules address **recurring production defects** observed across multiple presentation generations. Each rule is derived from real-world user feedback and must be followed without exception.

#### Rule 1: Spacing Between Content Blocks and Bottom Bars

**Problem observed**: Tables, charts, or content grids placed immediately above a bottom summary/action bar (e.g., "行动公式", "趋势判读", "风险提示") with zero vertical gap, making them visually merged.

**MANDATORY**: There MUST be **at least 0.15" vertical gap** between the last content block and any bottom bar/summary box. Calculate positions explicitly:

```python
# ❌ WRONG: content ends at Inches(6.15), bottom bar also at Inches(6.15)
last_content_bottom = content_top + num_rows * row_height
bar_y = last_content_bottom  # NO GAP!

# ✅ CORRECT: explicit gap
BOTTOM_BAR_GAP = Inches(0.2)
bar_y = last_content_bottom + BOTTOM_BAR_GAP
```

**Validation formula**: `bottom_bar_y >= last_content_bottom + Inches(0.15)`

#### Rule 2: Content Overflow Protection

**Problem observed**: Text or shapes extending beyond the right margin (left_margin + content_width) or bottom margin (source line at 7.05").

**MANDATORY** overflow checks:

1. **Right margin**: Every element's `left + width ≤ LM + CW` (i.e., `Inches(0.8) + Inches(11.733) = Inches(12.533)`)
2. **Bottom margin**: Every element's `top + height ≤ Inches(6.95)` (leaving room for source line at 7.05")
3. **Text in bounded boxes**: When placing text inside a colored `add_rect()` box, the text box MUST be **inset by at least 0.15"** on each side:

```python
# ✅ CORRECT: text inset within its container box
box_left = LM
box_width = CW
add_rect(s, box_left, box_y, box_width, box_h, BG_GRAY)
add_text(s, box_left + Inches(0.3), box_y, box_width - Inches(0.6), box_h,
         text, ...)  # 0.3" padding on each side
```

4. **Multi-column layouts**: When calculating column widths, account for inter-column gaps AND the right margin:
   ```python
   # total available = CW = Inches(11.733)
   num_cols = 3
   gap = Inches(0.2)
   col_w = (CW - gap * (num_cols - 1)) / num_cols  # NOT CW / num_cols
   ```

5. **Long text truncation**: If generated text may exceed box boundaries, reduce `font_size` by 1-2pt or abbreviate text. Never allow visible overflow.

#### Rule 3: Bottom Whitespace Elimination

**Problem observed**: Charts or content areas end at ~Inches(5.5) while the bottom bar sits at ~Inches(6.3), leaving ~0.8" of dead whitespace.

**MANDATORY**: The bottom summary bar should be positioned at **no higher than Inches(6.1)** and **no lower than Inches(6.4)**. Adjust chart/content heights to fill available space. Target: visible whitespace between content and bottom bar ≤ 0.3".

```python
# ✅ CORRECT: Compute bottom bar position dynamically
content_bottom = chart_top + chart_height
# Place bottom bar close to content (but with minimum gap)
bar_y = max(content_bottom + Inches(0.15), Inches(6.1))
bar_y = min(bar_y, Inches(6.4))  # don't push past safe zone
```

#### Rule 4: Legend Color Consistency

**Problem observed**: Chart legends using plain black text "■" symbols (`■ 基准值 ■ 增加 ■ 减少`) while actual chart bars use NAVY, ACCENT_RED, ACCENT_GREEN — colors don't match.

**MANDATORY**: Every legend indicator MUST use a **colored square** (`add_rect()`) matching the exact color used in the chart below it. Never use text-only legends with "■" character.

```python
# ❌ WRONG: Text-only legend with black squares
add_text(s, LM, legend_y, CW, Inches(0.25),
         '■ 基准值  ■ 增加  ■ 减少', ...)

# ✅ CORRECT: Color-matched legend squares
lgx = LM + Inches(5)
add_rect(s, lgx, legend_y, Inches(0.15), Inches(0.15), NAVY)
add_text(s, lgx + Inches(0.2), legend_y, Inches(0.9), Inches(0.25),
         '基准值', font_size=Pt(10), font_color=MED_GRAY)
add_rect(s, lgx + Inches(1.3), legend_y, Inches(0.15), Inches(0.15), ACCENT_RED)
add_text(s, lgx + Inches(1.5), legend_y, Inches(0.9), Inches(0.25),
         '增加', font_size=Pt(10), font_color=MED_GRAY)
# ... repeat for each series
```

**Legend placement**: Inline with or immediately below the chart subtitle line (typically at Inches(1.15)-Inches(1.20)). Legend squares are 0.15" × 0.15" with 0.05" gap to label text.

#### Rule 5: Title Style Consistency

**Problem observed**: Some slides using `add_navy_title_bar()` (full-width navy background + white text) while others use `add_action_title()` (white background + black text + underline), creating jarring visual inconsistency.

**MANDATORY**: Use **`add_action_title()`** (`aat()`) as the **ONLY** title style for ALL content slides. The navy title bar (`antb()`) is **DEPRECATED for content slides** and should only appear if explicitly requested by the user.

```python
# ❌ DEPRECATED: Navy background title bar
def add_navy_title_bar(slide, text):
    add_rect(s, 0, 0, SW, Inches(0.75), NAVY)
    add_text(s, LM, 0, CW, Inches(0.75), text, font_color=WHITE, ...)

# ✅ CORRECT: Consistent white-background action title (bottom-anchored)
def add_action_title(slide, text, title_size=Pt(22)):
    add_text(s, Inches(0.8), Inches(0.15), Inches(11.7), Inches(0.9), text,
             font_size=title_size, font_color=BLACK, bold=True, font_name='Georgia',
             anchor=MSO_ANCHOR.BOTTOM)  # BOTTOM: text sits flush against separator
    add_hline(s, Inches(0.8), Inches(1.05), Inches(11.7), BLACK, Pt(0.5))
```

**Note**: When `add_action_title()` is used, content starts at **Inches(1.25)** (not Inches(1.0)). Account for this when positioning grids, tables, or charts below the title.

#### Rule 6: Axis Label Centering in Matrix/Grid Charts

**Problem observed**: In 2×2 matrix layouts (#13, #59, #65), axis labels ("用户规模↑", "技术壁垒→") positioned at fixed offsets rather than centered on their respective axes, causing visual misalignment.

**MANDATORY**: Axis labels MUST be **centered on the full span** of their axis:

```python
# Grid dimensions
grid_left = LM + Inches(2.0)
grid_top = Inches(1.65)
cell_w = Inches(4.5)  # width of each quadrant
cell_h = Inches(2.0)  # height of each quadrant
grid_w = 2 * cell_w   # full grid width
grid_h = 2 * cell_h   # full grid height

# ✅ CORRECT: Y-axis label centered vertically on FULL grid height
add_text(s, LM, grid_top, Inches(1.8), grid_h,
         'Y轴标签↑', alignment=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# ✅ CORRECT: X-axis label centered horizontally on FULL grid width
add_text(s, grid_left, grid_top + grid_h + Inches(0.1), grid_w, Inches(0.3),
         'X轴标签 →', alignment=PP_ALIGN.CENTER)
```

#### Rule 7: Image Placeholder Slide Requirement

**Problem observed**: Presentations generated with zero image-containing slides, resulting in a wall of text/charts that feels monotonous and lacks visual relief.

**MANDATORY**: For presentations with **8+ slides**, at least **1 slide** must include image placeholders (using `add_image_placeholder()` or custom gray boxes with "请插入图片" labels). Preferred positions:

- After the first 2-3 content slides (as a visual break)
- For case studies, product showcases, or ecosystem overviews

**Standard placeholder style** (when not using `add_image_placeholder()` helper):

```python
# Large placeholder
img_l = LM; img_t = Inches(1.3); img_w = Inches(6.5); img_h = Inches(4.0)
add_rect(s, img_l, img_t, img_w, img_h, BG_GRAY)
add_rect(s, img_l + Inches(0.04), img_t + Inches(0.04),
         img_w - Inches(0.08), img_h - Inches(0.08), WHITE)
add_rect(s, img_l + Inches(0.08), img_t + Inches(0.08),
         img_w - Inches(0.16), img_h - Inches(0.16), RGBColor(0xF8, 0xF8, 0xF8))
add_text(s, img_l, img_t + img_h // 2 - Inches(0.3), img_w, Inches(0.5),
         '[ 请插入图片 ]', font_size=Pt(22), font_color=LINE_GRAY,
         bold=True, alignment=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, img_l, img_t + img_h // 2 + Inches(0.2), img_w, Inches(0.3),
         '图片描述标签', font_size=Pt(13), font_color=MED_GRAY,
         alignment=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
```

This triple-border style (BG_GRAY → WHITE → #F8F8F8) creates a professional, clearly identifiable placeholder that prompts users to insert real images.

#### Rule 8: Dynamic Sizing for Variable-Count Layouts (v1.10.4)

**Problem observed**: Layouts with a variable number of items (checklist rows, value chain stages, cover multi-line titles) use **fixed dimensions** that only work for a specific count. When item count differs, content either overflows past page boundaries or leaves excessive whitespace.

**MANDATORY**: For any layout where the number of items is variable, compute dimensions dynamically:

```python
# ✅ Horizontal items (value chain, flow): fill content width
n = len(items)
gap = Inches(0.35)
item_w = (CW - gap * (n - 1)) / n   # NOT a fixed Inches(2.0)

# ✅ Vertical items (checklist, table rows): fit within available height
bottom_limit = BOTTOM_BAR_Y if bottom_bar else SOURCE_Y - Inches(0.05)
available_h = bottom_limit - content_start_y
item_h = min(MAX_ITEM_H, available_h / max(n, 1))  # cap at comfortable max

# ✅ Multi-line titles: height scales with line count
n_lines = text.count('\n') + 1
title_h = Inches(0.8 + 0.65 * max(n_lines - 1, 0))
# Position following elements relative to title bottom, NOT at fixed y
```

**Anti-patterns** (❌ NEVER DO):
- `stage_w = Inches(2.0)` for N stages → use `(CW - gap*(N-1)) / N`
- `row_h = Inches(0.55)` for N rows → use `min(0.85, available / N)`
- `subtitle_y = Inches(3.5)` on cover → use `title_y + title_h + Inches(0.3)`

#### Rule 9: BLOCK_ARC Native Shapes for Circular Charts (v2.0)

**Problem observed**: Donut charts (#48), pie charts (#64), and gauge dials (#55) rendered with hundreds to thousands of small `add_rect()` blocks. This creates 100-2800 shapes per chart, inflates file size by 60-80%, slows generation to 2+ minutes, and produces visual artifacts (gaps between blocks, jagged edges).

**MANDATORY**: Use **BLOCK_ARC** preset shapes via `python-pptx` + XML adjustment for all circular/arc charts. Each segment = 1 shape (total: 3-5 shapes per chart vs. hundreds).

**BLOCK_ARC angle convention** (PPT coordinate system):
- Angles measured **clockwise from 12 o'clock** (top), in **60000ths of a degree**
- Top = 0°, Right = 90°, Bottom = 180°, Left = 270°
- Example: a full-circle donut segment from 12 o'clock CW to 3 o'clock = adj1=0, adj2=5400000

**Three adj parameters**:
- `adj1`: start angle (60000ths of degree, CW from top)
- `adj2`: end angle (60000ths of degree, CW from top)
- `adj3`: inner radius ratio (0 = solid sector / pie, 50000 = max / invisible ring)

```python
from pptx.oxml.ns import qn

def add_block_arc(slide, left, top, width, height, start_deg, end_deg, inner_ratio, color):
    """Draw a BLOCK_ARC shape with precise angle and ring-width control.

    Args:
        slide: pptx slide object
        left, top, width, height: bounding box (width == height for circular arc)
        start_deg: start angle in degrees, CW from 12 o'clock (0=top, 90=right, 180=bottom, 270=left)
        end_deg: end angle in degrees, CW from 12 o'clock
        inner_ratio: 0 = solid pie sector, 50000 = max (paper-thin ring).
                     For ~10px ring width: int((outer_r - Pt(10)) / outer_r * 50000)
        color: RGBColor fill color
    """
    from pptx.enum.shapes import MSO_SHAPE
    sh = slide.shapes.add_shape(MSO_SHAPE.BLOCK_ARC, left, top, width, height)
    sh.fill.solid()
    sh.fill.fore_color.rgb = color
    sh.line.fill.background()
    _clean_shape(sh)  # remove p:style to prevent file corruption

    sp = sh._element.find(qn('p:spPr'))
    prstGeom = sp.find(qn('a:prstGeom'))
    if prstGeom is not None:
        avLst = prstGeom.find(qn('a:avLst'))
        if avLst is None:
            avLst = prstGeom.makeelement(qn('a:avLst'), {})
            prstGeom.append(avLst)
        for gd in avLst.findall(qn('a:gd')):
            avLst.remove(gd)
        gd1 = avLst.makeelement(qn('a:gd'), {'name': 'adj1', 'fmla': f'val {int(start_deg * 60000)}'})
        gd2 = avLst.makeelement(qn('a:gd'), {'name': 'adj2', 'fmla': f'val {int(end_deg * 60000)}'})
        gd3 = avLst.makeelement(qn('a:gd'), {'name': 'adj3', 'fmla': f'val {inner_ratio}'})
        avLst.append(gd1)
        avLst.append(gd2)
        avLst.append(gd3)
    return sh
```

**Usage patterns**:

```python
# ── Donut chart: 4 segments, ~10px ring width ──
outer_r = Inches(1.6)
inner_ratio = int((outer_r - Pt(10)) / outer_r * 50000)  # ~10px ring
cum_deg = 0  # start at top (0° = 12 o'clock)
for pct, color, label in segments:
    sweep = pct * 360
    add_block_arc(s, cx - outer_r, cy - outer_r, outer_r * 2, outer_r * 2,
                  cum_deg, cum_deg + sweep, inner_ratio, color)
    cum_deg += sweep

# ── Pie chart (solid sectors): inner_ratio = 0 ──
add_block_arc(s, cx - r, cy - r, r * 2, r * 2, 0, 151.2, 0, NAVY)  # 42%

# ── Horizontal rainbow gauge (semi-circle, left→top→right) ──
# PPT coords: left=270°, top=0°, right=90°
gauge_segs = [(0.40, ACCENT_RED), (0.30, ACCENT_ORANGE), (0.30, ACCENT_GREEN)]
inner_ratio = int((outer_r - Pt(10)) / outer_r * 50000)
ppt_cum = 270  # start at left
for pct, color in gauge_segs:
    sweep = pct * 180
    add_block_arc(s, cx - outer_r, cy - outer_r, outer_r * 2, outer_r * 2,
                  ppt_cum % 360, (ppt_cum + sweep) % 360, inner_ratio, color)
    ppt_cum += sweep
```

**Anti-patterns** (❌ NEVER DO for circular charts):
- Nested `for deg in range(...): for r in range(...): add_rect(...)` — generates hundreds/thousands of tiny squares
- Drawing a white circle on top of a filled circle to "fake" a donut — fragile, misaligns on resize
- Using `math.cos/sin` + `add_rect()` loops for arcs — always use `BLOCK_ARC` instead

#### Rule 10: Horizontal Item Count Overflow Protection (v2.3)

**Problem observed**: Layouts that place N items **horizontally** across the slide (Process Chevron, Metric Cards, Icon Grid, Four-Column) compute `gap = (CW - item_w * N) / (N - 1)`. When N is large enough that `item_w * N > CW`, the gap becomes **negative**, producing shapes with negative widths. PowerPoint reports "file needs repair" and silently deletes the corrupt shapes.

**Root cause example** (Process Chevron with 5+ steps):
```python
# ❌ BROKEN: fixed step_w with high N
step_w = Inches(2.6)       # fixed width
n = 5                       # 5 steps
gap = (CW - step_w * n) / (n - 1)
#   = (11.733 - 13.0) / 4 = -0.317"  ← NEGATIVE!
# Arrow text box width = gap - 0.1" = -0.417" ← FILE CORRUPTION
```

**MANDATORY**: For any horizontal-item layout, **compute `item_w` dynamically** from the available content width, reserving a minimum gap:

```python
# ✅ CORRECT: dynamic item_w with floor gap
MIN_GAP = Inches(0.35)             # minimum inter-item gap
PREFERRED_W = Inches(2.6)          # ideal item width
max_item_w = (CW - MIN_GAP * max(n - 1, 1)) / max(n, 1)
item_w = min(PREFERRED_W, max_item_w)   # shrink if needed
gap = (CW - item_w * n) / max(n - 1, 1) # now guaranteed ≥ MIN_GAP
```

**Affected methods** (all already fixed in engine.py v2.3):
- `process_chevron()` — step boxes + arrow gaps
- `metric_cards()` — card columns
- `icon_grid()` — icon columns
- `four_column()` — text columns

**Additional safeguards**:
- When items shrink significantly (`item_w < Inches(2.0)`), reduce font sizes by one tier (sub-header → body, body → small) to prevent text overflow inside narrower boxes.
- Arrow/connector elements between items must use `max(gap - margin, Inches(0.2))` for their width — never raw `gap - margin` which may be tiny or negative.

**Validation formula**: `item_w * n + gap * (n - 1) ≈ CW` and `gap ≥ MIN_GAP` and `item_w > 0`.

### Mandatory Slide Elements

EVERY content slide (except Cover and Closing) MUST include ALL of these:

| Element | Function | Position |
|---------|----------|----------|
| Action Title | `add_action_title(slide, text)` | Top (0.15" from top) |
| Title separator line | Included in `add_action_title()` | 1.05" from top |
| Content area | Layout-specific content blocks | 1.4" to 6.5" |
| Source attribution | `add_source(slide, text)` | 7.05" from top |
| Page number | `add_page_number(slide, n, total)` | Bottom-right corner |

Page number helper function:
```python
def add_page_number(slide, num, total):
    add_text(slide, Inches(12.2), Inches(7.1), Inches(1), Inches(0.3),
             f"{num}/{total}", font_size=Pt(9), font_color=MED_GRAY,
             alignment=PP_ALIGN.RIGHT)
```

---

---

## Reference Files

Read these files as needed — do NOT load all at once:

| File | When to read |
|------|-------------|
|  | Choosing a layout or building a specific slide type (cover, donut, timeline, matrix, etc.) |
|  | Looking up MckEngine method signatures and parameters |
|  | Fixing file corruption, rendering issues, edge cases, version history |

