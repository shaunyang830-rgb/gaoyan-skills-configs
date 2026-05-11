
## Layout Patterns

### Slide Dimensions

```python
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
```

Widescreen format (16:9), standard for all presentations.

### Standard Margin/Padding

| Position | Size | Usage |
|----------|------|-------|
| **Left margin** | 0.8" | Default left edge |
| **Right margin** | 0.8" | Default right edge |
| **Top (below title)** | 1.4" | Content start position |
| **Bottom** | 7.05" | Source text baseline |
| **Title bar height** | 0.9" | Action title bar |
| **Title bar top** | 0.15" | From slide top |

### Slide Type Patterns

#### 1. Cover Slide (Slide 1)

Layout:
- Navy bar at very top (0.05" height)
- Main title (44pt, Georgia, navy) at y=1.2" — **height computed dynamically from line count**
- Subtitle (24pt, dark gray) positioned **below title dynamically**
- Date/info (14pt, med gray) follows subtitle
- Decorative navy line at x=1", y=6.8" (4" wide, 2pt)

Code template:
```python
# Without cover image (default, classic layout)
eng.cover(title='Q1 2026 战略回顾', subtitle='董事会汇报', author='战略部', date='2026年3月')

# With AI-generated cover image (McKinsey style)
eng.cover(title='Q1 2026 战略回顾', subtitle='董事会汇报', author='战略部', date='2026年3月', cover_image='auto')

# With custom image file
eng.cover(title='Q1 2026 战略回顾', subtitle='董事会汇报', author='战略部', date='2026年3月', cover_image='assets/my_cover.png')
```

**Cover Image Generation Pipeline** (`cover_image='auto'`):

When `cover_image='auto'`, the system automatically generates a McKinsey-style cover illustration:

1. **Keyword → Real Product Mapping**: Title keywords are matched to real-world product descriptions via `_METAPHOR_MAP` in `mck_ppt/cover_image.py` (e.g. `'AI'` → high-end triple-fan GPU, `'医药'` → stethoscope + capsules, `'金融'` → metal chip bank card, `'建筑'` → 3D-printed architectural model)
2. **Hunyuan 2.0 Generation**: Tencent Hunyuan 2.0 (`SubmitHunyuanImageJob` async API) generates a 1024×1024 product photo with prompt: "真实产品摄影照片，{product}，纯白色背景，轮廓清晰锐利，影棚灯光，超高清"
3. **Professional Cutout**: `rembg` removes background completely — only the product subject remains with transparent background
4. **Cool Grey-Blue Tint**: Desaturation (30%), channel shift (R×0.85, G×0.92, B×1.18), then 50% lighten by blending with white
5. **Canvas Placement**: Subject scaled to ~66% canvas height, placed at right-center of 1920×1080 transparent canvas
6. **Bézier Ribbon Curves**: 24 parallel cubic Bézier curves drawn from bottom-left to top-right, with a gentle twist/fold at center (lines cross over like a folded silk ribbon). Inner lines thicker+darker, outer lines thinner+lighter
7. **Full-bleed Embed**: Image added as first shape (bottom layer), all text rendered on top

**Requirements**: `pip install tencentcloud-sdk-python rembg pillow numpy` + env vars `TENCENT_SECRET_ID`, `TENCENT_SECRET_KEY`

**Standalone usage**:
```python
from mck_ppt.cover_image import generate_cover_image
path = generate_cover_image('AI的能力边界', output_path='cover.png')
```

#### 2. Action Title Slide (Most Content Slides)

Every main content slide has this structure:

```
┌─────────────────────────────────────────┐ 0.15"
│ ▌ Action Title (22pt, bold, black)      │ ← TITLE_BAR_H = 0.9"
├─────────────────────────────────────────┤ 1.05"
│                                         │
│  Content area (starts at 1.4")          │
│  [Tables, lists, text, etc.]            │
│                                         │
│                                         │
│  ──────────────────────────────────────  │ 7.05"
│  Source: ...                            │ 9pt, med gray
└─────────────────────────────────────────┘ 7.5"
```

Code pattern:
```python
s = prs.slides.add_slide(prs.slide_layouts[6])
add_action_title(s, 'Slide Title Here')
# Then add content below y=1.4"
add_source(s, 'Source attribution')
```

#### 3. Table Layout (Slide 4 - Five Capabilities)

Structure:
- Header row with column names (BODY_SIZE, gray, bold)
- 1.0pt black line under header
- Data rows (1.0" height each, 14pt text)
- 0.5pt gray line between rows
- 3 columns: Module (1.6" wide), Function (5.0"), Scene (5.1")

```python
# Headers
add_text(s4, left, top, width, height, text,
         font_size=BODY_SIZE, font_color=MED_GRAY, bold=True)

# Header line (thicker)
add_line(s4, left, top + Inches(0.5), left + full_width, top + Inches(0.5),
         color=BLACK, width=Pt(1.0))

# Rows
for i, (col1, col2, col3) in enumerate(rows):
    y = header_y + row_height * i
    add_text(s4, left, y, col1_w, row_h, col1, ...)
    add_text(s4, left + col1_w, y, col2_w, row_h, col2, ...)
    add_text(s4, left + col1_w + col2_w, y, col3_w, row_h, col3, ...)
    # Row separator
    add_line(s4, left, y + row_h, left + full_w, y + row_h,
             color=LINE_GRAY, width=Pt(0.5))
```

#### 4. Three-Column Overview (Slide 5)

Layout:
- Left column (4.1" wide): "是什么"
- Middle column (4.1" wide): "独到之处"
- Right 1/4 (2.5" wide) gray panel: "Key Takeaways"

```
0.8"  4.9"  5.3"  9.4"  10.0" 12.5"
|-----|-----|-----|-----|------|
│左 │ │ 中 │ │ 右 │
└─────────────────────────────┘
```

Code:
```python
left_x = Inches(0.8)
col_w5 = Inches(4.1)
mid_x = Inches(5.3)
takeaway_left = Inches(10.0)
takeaway_width = Inches(2.5)

# Left column
add_text(s5, left_x, content_top, col_w5, ...)
add_text(s5, left_x, content_top + Inches(0.6), col_w5, ..., 
              bullet=True, line_spacing=Pt(8))

# Right gray takeaway area
add_rect(s5, takeaway_left, Inches(1.2), takeaway_width, Inches(5.6), BG_GRAY)
add_text(s5, takeaway_left + Inches(0.15), Inches(1.35), takeaway_width - Inches(0.3), ...,
         'Key Takeaways', font_size=BODY_SIZE, color=NAVY, bold=True)
add_text(s5, takeaway_left + Inches(0.15), Inches(1.9), takeaway_width - Inches(0.3), ...,
              [f'{i+1}. {t}' for i, t in enumerate(takeaways)], line_spacing=Pt(10))
```

---

### 类别 A：结构导航

#### 5. Section Divider (章节分隔页)

**适用场景**: 多章节演示文稿的章节过渡页，用于视觉上分隔不同主题模块。

```
┌──┬──────────────────────────────────────┐
│N │                                      │
│A │  第一部分                             │
│V │  章节标题（28pt, NAVY, bold）          │
│Y │  副标题说明文字                        │
│  │                                      │
└──┴──────────────────────────────────────┘
```

```python
eng.section_divider(section_label='第一部分', title='市场分析', subtitle='当前格局与核心机会')
```

#### 6. Table of Contents / Agenda (目录/议程页)

**适用场景**: 演示文稿开头的目录或会议议程，列出各章节及说明。

```
┌─────────────────────────────────────────┐
│ ▌ 目录                                  │
├─────────────────────────────────────────┤
│                                         │
│  (1)  章节一标题     简要描述            │
│  ─────────────────────────────────────  │
│  (2)  章节二标题     简要描述            │
│  ─────────────────────────────────────  │
│  (3)  章节三标题     简要描述            │
│                                         │
└─────────────────────────────────────────┘
```

```python
eng.toc(items=[('1', '市场概览', '当前竞争格局'), ('2', '战略方向', '三大核心举措'), ('3', '执行路线', '时间表与责任人')])
```

#### 7. Appendix Title (附录标题页)

**适用场景**: 正文结束后的附录/备用材料分隔页。

```
┌─────────────────────────────────────────┐
│                                         │
│                                         │
│           附录                           │
│           Appendix                      │
│           ────────                      │
│           补充数据与参考资料              │
│                                         │
└─────────────────────────────────────────┘
```

```python
eng.appendix_title(title='附录', subtitle='补充数据与参考资料')
```

---

### 类别 B：数据统计

#### 8. Big Number / Factoid (大数据展示页)

**适用场景**: 用一个醒目的大数字引出核心发现或关键数据点。

```
┌─────────────────────────────────────────┐
│ ▌ Action Title                          │
├─────────────────────────────────────────┤
│                                         │
│  ┌─NAVY─────────┐                       │
│  │    95%        │   右侧上下文说明      │
│  │  子标题       │   详细解释数据含义     │
│  └──────────────┘                       │
│                                         │
│  ┌─BG_GRAY──────────────────────────┐   │
│  │  关键洞见：详细分析文字            │   │
│  └──────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

```python
eng.big_number(title='关键发现标题', number='95%', unit='', description='描述数据含义',
    detail_items=['洞见要点一', '洞见要点二', '洞见要点三'], source='Source: ...')
```

#### 9. Two-Stat Comparison (双数据对比页)

**适用场景**: 并排展示两个关键指标的对比（如同比、环比、A vs B）。

```
┌─────────────────────────────────────────┐
│ ▌ Action Title                          │
├─────────────────────────────────────────┤
│                                         │
│  ┌──NAVY───────┐    ┌──BG_GRAY────┐     │
│  │   $2.4B     │    │   $1.8B     │     │
│  │  2026年目标  │    │  2025年实际  │     │
│  └─────────────┘    └─────────────┘     │
│                                         │
│  分析说明文字                            │
└─────────────────────────────────────────┘
```

```python
eng.two_stat(title='对比标题',
    stats=[('$2.4B', '2026年目标', True), ('$1.8B', '2025年实际', False)],
    source='Source: ...')
```

#### 10. Three-Stat Dashboard (三指标仪表盘)

**适用场景**: 同时展示三个关键业务指标（如 KPI、季度数据）。

```
┌─────────────────────────────────────────┐
│ ▌ Action Title                          │
├─────────────────────────────────────────┤
│  ┌──NAVY──┐   ┌──BG_GRAY─┐  ┌──BG_GRAY─┐│
│  │  数字1  │   │  数字2   │  │  数字3   ││
│  │ 小标题  │   │  小标题  │  │  小标题  ││
│  └────────┘   └─────────┘  └─────────┘│
│                                         │
│  详细说明文字                            │
└─────────────────────────────────────────┘
```

```python
eng.three_stat(title='核心运营指标',
    stats=[('98.5%', '系统可用性', True), ('12ms', '平均响应时间', False), ('4.8', '用户满意度', True)],
    source='Source: ...')
```

#### 11. Data Table with Headers (数据表格页)

**适用场景**: 结构化数据展示，如财务数据、功能对比矩阵、项目清单。

```
┌─────────────────────────────────────────┐
│ ▌ Action Title                          │
├─────────────────────────────────────────┤
│  列1         列2         列3     列4    │
│  ═══════════════════════════════════    │
│  数据1-1     数据1-2     ...     ...    │
│  ───────────────────────────────────    │
│  数据2-1     数据2-2     ...     ...    │
│  ───────────────────────────────────    │
│  数据3-1     数据3-2     ...     ...    │
└─────────────────────────────────────────┘
```

```python
eng.data_table(title='五大核心能力',
    headers=['模块', '功能描述', '应用场景'],
    rows=[['AI Agent', '自主决策与执行', '客服自动化'],
          ['数据引擎', '实时数据处理', '风控决策']],
    source='Source: ...')
```

#### 12. Metric Cards Row (指标卡片行)

**适用场景**: 3-4个并排卡片展示独立指标，每个卡片含标题+描述。

```
┌─────────────────────────────────────────┐
│ ▌ Action Title                          │
├─────────────────────────────────────────┤
│ ┌─BG_GRAY─┐ ┌─BG_GRAY─┐ ┌─BG_GRAY─┐   │
│ │ (A)     │ │ (B)     │ │ (C)     │   │
│ │ 标题    │ │ 标题    │ │ 标题    │   │
│ │ ───     │ │ ───     │ │ ───     │   │
│ │ 描述    │ │ 描述    │ │ 描述    │   │
│ └─────────┘ └─────────┘ └─────────┘   │
└─────────────────────────────────────────┘
```

```python
eng.metric_cards(title='月度运营仪表盘',
    cards=[('98.5%', '可用性', '超越SLA目标'),
           ('¥2.3亿', '月营收', '同比+18%'),
           ('4.8/5', '满意度', '连续3月提升')],
    source='Source: ...')
```

---

### 类别 C：框架矩阵

#### 13. 2x2 Matrix (四象限矩阵)

**适用场景**: 战略分析（如 BCG 矩阵、优先级排序、风险评估）。

```
┌─────────────────────────────────────────┐
│ ▌ Action Title                          │
├─────────────────────────────────────────┤
│         高 Y轴                           │
│  ┌─NAVY──────┐  ┌─BG_GRAY───┐          │
│  │ 左上象限   │  │ 右上象限   │          │
│  └───────────┘  └───────────┘          │
│  ┌─BG_GRAY───┐  ┌─BG_GRAY───┐          │
│  │ 左下象限   │  │ 右下象限   │          │
│  └───────────┘  └───────────┘          │
│         低           高 X轴              │
└─────────────────────────────────────────┘
```

```python
eng.matrix_2x2(title='战略优先级矩阵',
    quadrants=[('高价值 / 低难度', ['快速推进项目A', '立即启动项目B']),
               ('高价值 / 高难度', ['重点攻关项目C']),
               ('低价值 / 低难度', ['委托执行项目D']),
               ('低价值 / 高难度', ['暂缓或放弃'])],
    source='Source: ...')
```

#### ~~14. Three-Pillar Framework~~ → RETIRED (v2.0.4)

> **已退役**：#14 布局已被 **#71 Table+Insight** 取代。请使用 `eng.table_insight()` 实现类似的三列对比需求，数据表达更清晰、视觉层级更强。

#### 15. Staircase Evolution (阶梯进化图) ⭐ v2.0.5

**适用场景**: 展示阶段性演进路径（如品牌进化、能力成长、战略升级），从左下到右上阶梯式上升。具有明显的阶梯台阶轮廓线。可选底部结构化详情表格。

```
┌──────────────────────────────────────────────────────┐
│ ▌ Action Title                                       │
├──────────────────────────────────────────────────────┤
│                              ●3● 远期标题             │
│                    ┌─────────┘                        │
│         ●2● 中期标题│  远期描述...                     │
│    ┌────┘          │                                  │
│  ●1● 近期标题 │ 中期描述...                            │
│  ─────────── │                                       │
│  近期描述... │                                        │
│──────────────────────────────────────────────────────│
│ 行标题1  │ • bullet1    │ • bullet1    │ • bullet1    │
│──────────────────────────────────────────────────────│
│ 行标题2  │ • bullet1    │ • bullet1    │ • bullet1    │
└──────────────────────────────────────────────────────┘
```

**Engine method**: `eng.pyramid()`

```python
eng.pyramid(
    title='品牌心智三层进化路径',
    levels=[
        ('层次一：2-3年', '"冰淇淋品类的操作系统"\nB端采购决策者', '1'),
        ('层次二：3-5年', '"冰淇淋界的Dolby"\n品质认知消费者', '2'),
        ('层次三：5-10年', '"美好甜蜜时刻的守护者"\n所有消费者', '3'),
    ],
    detail_rows=[
        ('核心策略', [
            ['AI数据+品类白皮书', '建立B端操作系统壁垒'],
            ['"日世品质"认证标识', '品质认知渗透消费端'],
            ['品牌情感化升级', '全渠道消费者心智占领'],
        ]),
        ('对标案例', [
            ['Intel Inside', 'B端技术标准→消费认知'],
            ['利乐 / 杜比', '品质认证→行业标配'],
            ['Gore-Tex', '专业品牌→大众信赖'],
        ]),
    ],
    source='对标: Intel Inside / 利乐 / 杜比 / Gore-Tex',
)
```

**Parameters**: `title`, `levels` (label, description, icon_text), `detail_rows` (row_label, [[col_texts]...]), `source`, `bottom_bar` (optional)

**设计特点**:
- **阶梯台阶轮廓线**：NAVY 颜色的水平台面线+垂直阶梯线，形成清晰的台阶外形
- **Icon + 标题同行**：NAVY 圆形 icon 在左，粗体标题在右，位于台面线上方
- **描述在台面线下方**：每阶段的详细描述文字在水平台面线下面
- **可选底部结构化表格**：行标题+各阶段 bullet 详情，居中对齐
- 兼容有/无 detail_rows 两种模式

#### 16. Process Chevron (流程箭头页)

**适用场景**: 线性流程展示（2-7步），如实施路径、业务流程、方法论步骤。推荐3-5步效果最佳；6-7步时方框和字体会自动缩小（Guard Rail Rule 10）。

```
┌─────────────────────────────────────────┐
│ ▌ Action Title                          │
├─────────────────────────────────────────┤
│                                         │
│  ┌NAVY┐ -> ┌GRAY┐ -> ┌GRAY┐ -> ┌GRAY┐  │
│  │ S1 │    │ S2 │    │ S3 │    │ S4 │  │
│  └────┘    └────┘    └────┘    └────┘  │
│   描述      描述      描述      描述    │
│                                         │
└─────────────────────────────────────────┘
```

```python
eng.process_chevron(title='客户旅程五步法',
    steps=['需求识别', '方案设计', '实施交付', '运营优化', '持续创新'],
    bottom_bar=('关键洞见', '端到端数字化覆盖率从30%提升至85%'),
    source='Source: ...')
```

#### 17. Venn Diagram Concept (维恩图概念页)

**适用场景**: 展示两三个概念的交集关系（如能力交叉、市场定位）。

```
┌─────────────────────────────────────────┐
│ ▌ Action Title                          │
├─────────────────────────────────────────┤
│          ┌──BG──┐                       │
│         ╱概念A  ╲                       │
│        ╱  ┌──┐   ╲      右侧说明       │
│       │   │交│    │                     │
│        ╲  └──┘   ╱                     │
│         ╲概念B  ╱                       │
│          └──────┘                       │
└─────────────────────────────────────────┘
```

```python
eng.venn(title='能力交叉模型',
    circles=[('技术', ['云计算', 'AI/ML'], 0.8, 1.5, 4.5, 3.5),
             ('业务', ['行业Know-how', '流程优化'], 3.5, 1.5, 4.5, 3.5)],
    overlap_label='数字化创新',
    source='Source: ...')
```

#### 18. Temple / House Framework (殿堂框架)

**适用场景**: 展示"屋顶-支柱-基座"的结构（如企业架构、能力体系）。

```
┌─────────────────────────────────────────┐
│ ▌ Action Title                          │
├─────────────────────────────────────────┤
│  ┌═══════════NAVY（愿景/屋顶）══════════┐│
│  ├────┤  ├────┤  ├────┤  ├────┤        ││
│  │支柱│  │支柱│  │支柱│  │支柱│        ││
│  │ 1  │  │ 2  │  │ 3  │  │ 4  │        ││
│  ├════╧══╧════╧══╧════╧══╧════╧════════┤│
│  │        基座（基础能力/文化）          ││
│  └──────────────────────────────────────┘│
└─────────────────────────────────────────┘
```

```python
eng.temple(title='企业架构框架',
    roof_text='企业愿景：成为全球领先的科技公司',
    pillar_names=['产品创新', '客户体验', '运营卓越', '人才发展'],
    foundation_text='数据驱动 · 敏捷组织 · 开放生态',
    source='Source: ...')
```

---

### 类别 D：对比评估

#### 19. Side-by-Side Comparison (左右对比页)

**适用场景**: 两个方案/选项/产品的并排对比分析。

```
┌─────────────────────────────────────────┐
│ ▌ Action Title                          │
├─────────────────────────────────────────┤
│  ┌──方案 A──────┐  ┌──方案 B──────┐     │
│  │ 标题（NAVY） │  │ 标题（NAVY） │     │
│  ├──────────────┤  ├──────────────┤     │
│  │ 优势         │  │ 优势         │     │
│  │ 劣势         │  │ 劣势         │     │
│  │ 成本         │  │ 成本         │     │
│  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────┘
```

```python
eng.side_by_side(title='方案A vs 方案B',
    options=[('方案A：自建', ['完全自主可控', '前期投入¥500万', '上线周期6个月']),
             ('方案B：SaaS', ['快速上线2周', '年费¥80万', '依赖供应商'])],
    source='Source: ...')
```

#### 20. Before / After (前后对比页) _(v2.0.1 rewrite)_

**适用场景**: 展示变革前后的对比（如行业退潮 vs 生存公式、流程优化、组织变革）。

**设计特征**:
- **白底清洁布局** — 无背景色块，纯白底
- **黑色竖线 + 圆圈箭头** — 中间细竖线分隔，竖线正中放黑色实心圆圈内含 `>` 箭头（Arial 字体，内边距0）
- **结构化数据行**（左侧）— 每行有 label/brand/value/extra，数值红色大字
- **公式卡片**（右侧）— 每条有 title/desc/cases，案例数字黑色+下划线
- **支持简单文字列表后备** — 如传入 `list[str]` 自动退化为简单 bullet 模式
- **可选虚线角标** — 右上角虚线框（如 `Part II > 退潮`）
- **可选底部总结条** — bottom_bar

```
┌──────────────────────────────────────────────┐
│ ▌ Action Title                   ┊Part II >┊ │
├──────────────────┬────┬──────────────────────┤
│  左侧标题        │    │  右侧标题            │
│                  │ ● │                      │
│  标签 品牌 数值   │ > │  1. 公式标题          │
│  ────────────── │ ● │     描述 + 案例下划线  │
│  标签 品牌 数值   │    │  ─────────────      │
│  ────────────── │    │  2. 公式标题          │
│  总结(灰粗体)    │    │     总结(红色粗体)    │
├──────────────────────────────────────────────┤
│ [关键洞察] 底部总结条                         │
└──────────────────────────────────────────────┘
```

**Engine method**: `eng.before_after()`

```python
eng.before_after(title='流程优化效果',
    before_title='优化前', before_points=['人工审批 3-5天', '错误率 8%', '满意度 65分'],
    after_title='优化后', after_points=['自动审批 2小时', '错误率 0.5%', '满意度 92分'],
    source='Source: ...')
```

**Parameters**:

| 参数 | 类型 | 说明 |
|------|------|------|
| `title` | str | 页面标题 |
| `before_title` | str | 左侧标题 |
| `before_points` | list[dict] 或 list[str] | 左侧数据行（dict: label/brand1/val1/brand2/val2/extra）或简单文字列表 |
| `after_title` | str | 右侧标题 |
| `after_points` | list[dict] 或 list[str] | 右侧公式卡片（dict: title/desc/cases）或简单文字列表 |
| `corner_label` | str | 右上角虚线角标文字（可选） |
| `bottom_bar` | tuple(str,str) | 底部条 (标签, 文字)（可选） |
| `left_summary` | str | 左侧底部总结文字（可选，灰色粗体） |
| `right_summary` | str | 右侧底部总结文字（可选，默认红色粗体） |
| `right_summary_color` | RGBColor | 右侧总结文字颜色（默认 ACCENT_RED） |
| `source` | str | 数据来源 |

#### 21. Pros and Cons (优劣分析页)

**适用场景**: 评估某个决策/方案的优势与风险。

```
┌─────────────────────────────────────────┐
│ ▌ Action Title                          │
├─────────────────────────────────────────┤
│  V 优势                  X 风险         │
│  ───────────             ──────────     │
│  • 要点1                 • 要点1        │
│  • 要点2                 • 要点2        │
│  • 要点3                 • 要点3        │
│                                         │
│  ┌──BG_GRAY 结论/建议───────────────┐   │
└─────────────────────────────────────────┘
```

```python
eng.pros_cons(title='并购方案评估',
    pros_title='优势', pros=['快速获取市场份额', '技术团队整合', '品牌协同效应'],
    cons_title='风险', cons=['整合成本高', '文化冲突', '监管审批不确定'],
    source='Source: ...')
```

#### 22. Traffic Light / RAG Status (红绿灯状态页)

**适用场景**: 多项目/多模块的状态总览（绿=正常、黄=关注、红=风险）。

```
┌─────────────────────────────────────────┐
│ ▌ Action Title                          │
├─────────────────────────────────────────┤
│  项目        状态    进度     备注       │
│  ═══════════════════════════════════    │
│  项目A       (G)    85%     按计划推进  │
│  ───────────────────────────────────    │
│  项目B       (Y)    60%     需关注资源  │
│  ───────────────────────────────────    │
│  项目C       (R)    30%     存在阻塞    │
└─────────────────────────────────────────┘
```

```python
eng.rag_status(title='项目健康度仪表盘',
    headers=['项目', '进度', '预算', '质量', '负责人'],
    rows=[('CRM升级', '🟢', '🟡', '🟢', '张三'),
          ('ERP迁移', '🟡', '🔴', '🟢', '李四')],
    source='Source: ...')
```

#### 23. Scorecard (计分卡页)

**适用场景**: 展示多项评估维度的得分/评级，如供应商评估、团队绩效。

```
┌─────────────────────────────────────────┐
│ ▌ Action Title                          │
├─────────────────────────────────────────┤
│  评估维度          得分   评级           │
│  ═══════════════════════════════════    │
│  客户满意度         92    ████████░░    │
│  产品质量           85    ███████░░░    │
│  交付速度           78    ██████░░░░    │
│  创新能力           65    █████░░░░░    │
└─────────────────────────────────────────┘
```

```python
eng.scorecard(title='数字化成熟度评估',
    items=[('数据治理', 85, '已建立完整数据标准'),
           ('流程自动化', 62, 'RPA覆盖40%核心流程'),
           ('AI应用', 45, '试点阶段，3个场景落地')],
    source='Source: ...')
```

---

### 类别 E：内容叙事

#### 24. Executive Summary (执行摘要页)

**适用场景**: 演示文稿的核心结论汇总，通常放在开头或结尾。

```
┌─────────────────────────────────────────┐
│ ▌ Action Title                          │
├─────────────────────────────────────────┤
│ ┌──NAVY（核心结论）────────────────────┐ │
│ │  一句话核心结论                       │ │
│ └──────────────────────────────────────┘ │
│                                         │
│  (1) 支撑论点一      详细说明           │
│  (2) 支撑论点二      详细说明           │
│  (3) 支撑论点三      详细说明           │
└─────────────────────────────────────────┘
```

```python
eng.executive_summary(title='执行摘要',
    headline='本季度实现营收¥8.5亿，同比增长23%，超额完成年度目标的52%',
    items=[('市场拓展', '新增客户127家，覆盖3个新行业'),
           ('产品迭代', '发布V3.0版本，NPS提升15个百分点'),
           ('运营效率', '人效比提升18%，交付周期缩短40%')],
    source='Source: ...')
```

#### 25. Key Takeaway with Detail (核心洞见页)

**适用场景**: 左侧详细论述 + 右侧灰底要点提炼，用于核心发现页。

```
┌─────────────────────────────────────────┐
│ ▌ Action Title                          │
├─────────────────────────────────────────┤
│                      ┌──BG_GRAY────────┐│
│  左侧正文内容        │ Key Takeaways   ││
│  详细分析论述        │ 1. 要点一        ││
│  数据与支撑          │ 2. 要点二        ││
│                      │ 3. 要点三        ││
│                      └─────────────────┘│
└─────────────────────────────────────────┘
```

```python
eng.key_takeaway(title='核心洞见',
    takeaway='数字化转型的关键不在技术，而在组织能力的重塑',
    details=['技术是enabler，组织是driver', '自上而下的战略共识是前提', '小步快跑优于大规模重构'],
    source='Source: ...')
```

#### 26. Quote / Insight Page (引言/洞见页)

**适用场景**: 突出一段重要引言、专家观点或核心洞察。

```
┌─────────────────────────────────────────┐
│                                         │
│            ──────────                   │
│                                         │
│      "引言内容，居中显示，               │
│       大字号强调核心观点"                │
│                                         │
│            ──────────                   │
│         — 来源/作者                      │
│                                         │
└─────────────────────────────────────────┘
```

```python
eng.quote(title='客户反馈',
    quote_text='这是我们见过的最专业、最高效的数字化转型方案。',
    attribution='张总, XX集团CEO',
    source='Source: ...')
```

#### 27. Two-Column Text (双栏文本页)

**适用场景**: 平衡展示两个主题/方面，每列独立标题+正文。

```
┌─────────────────────────────────────────┐
│ ▌ Action Title                          │
├─────────────────────────────────────────┤
│  (A) 左栏标题         (B) 右栏标题      │
│  ─────────────        ─────────────     │
│  左栏正文内容         右栏正文内容       │
│  详细分析             详细分析           │
│                                         │
└─────────────────────────────────────────┘
```

```python
eng.two_column_text(title='能力对比分析',
    columns=[('A', '核心能力', ['云原生架构设计', '大规模分布式系统', 'AI/ML工程化']),
             ('B', '待提升领域', ['前端体验设计', '国际化运营', '生态合作伙伴'])],
    source='Source: ...')
```

#### 28. Four-Column Overview (四栏概览页)

**适用场景**: 四个并列维度的概览（如四大业务线、四个能力域）。

```
┌─────────────────────────────────────────┐
│ ▌ Action Title                          │
├─────────────────────────────────────────┤
│  (1)       (2)       (3)       (4)      │
│  标题1     标题2     标题3     标题4     │
│  ────      ────      ────      ────     │
│  描述      描述      描述      描述      │
└─────────────────────────────────────────┘
```

```python
eng.four_column(title='四大战略方向',
    items=[('产品创新', '持续迭代核心产品线'),
           ('市场拓展', '进入3个新垂直行业'),
           ('运营卓越', '全流程数字化覆盖'),
           ('人才战略', '关键岗位100%到位')],
    source='Source: ...')
```

---

### 类别 F：时间流程

#### 29. Timeline / Roadmap (时间轴/路线图)

**适用场景**: 展示时间维度的里程碑计划（季度/月度/年度路线图）。

```
┌─────────────────────────────────────────┐
│ ▌ Action Title                          │
├─────────────────────────────────────────┤
│                                         │
│  (1)──────(2)──────(3)──────(4)         │
│  Q1       Q2       Q3       Q4         │
│  里程碑1  里程碑2  里程碑3  里程碑4     │
│                                         │
└─────────────────────────────────────────┘
```

```python
eng.timeline(title='项目路线图 2026',
    milestones=[('Q1', '需求调研与方案设计'),
                ('Q2', '核心功能开发与测试'),
                ('Q3', '灰度发布与用户反馈'),
                ('Q4', '全量上线与效果评估')],
    source='Source: ...')
```

#### 30. Vertical Steps (垂直步骤页)

**适用场景**: 从上到下的操作步骤或实施阶段。

```
┌─────────────────────────────────────────┐
│ ▌ Action Title                          │
├─────────────────────────────────────────┤
│  (1) 步骤一标题      详细说明           │
│  ─────────────────────────────────────  │
│  (2) 步骤二标题      详细说明           │
│  ─────────────────────────────────────  │
│  (3) 步骤三标题      详细说明           │
│  ─────────────────────────────────────  │
│  (4) 步骤四标题      详细说明           │
└─────────────────────────────────────────┘
```

```python
eng.vertical_steps(title='实施五步法',
    steps=[('1', '诊断评估', '全面了解现状与痛点'),
           ('2', '方案设计', '制定分阶段实施方案'),
           ('3', '试点验证', '选取2-3个场景快速验证'),
           ('4', '规模推广', '复制成功经验至全业务线'),
           ('5', '持续优化', '建立数据驱动的迭代机制')],
    source='Source: ...')
```

#### 31. Cycle / Loop (循环图页)

**适用场景**: 闭环流程或迭代循环（如 PDCA、敏捷迭代、反馈循环）。

```
┌─────────────────────────────────────────┐
│ ▌ Action Title                          │
├─────────────────────────────────────────┤
│         ┌──阶段1──┐                     │
│         │        │                      │
│  ┌阶段4┐│        │┌阶段2┐   右侧说明   │
│  │     │└────────┘│     │              │
│  └─────┘          └─────┘              │
│         ┌──阶段3──┐                     │
│         └────────┘                      │
└─────────────────────────────────────────┘
```

```python
eng.cycle(title='敏捷开发循环',
    phases=[('规划', 1.0, 2.0), ('开发', 5.0, 1.0),
            ('测试', 9.0, 2.0), ('发布', 5.0, 4.0)],
    source='Source: ...')
```

#### 32. Funnel (漏斗图页)

**适用场景**: 转化漏斗（如销售漏斗、用户转化路径）。

```
┌─────────────────────────────────────────┐
│ ▌ Action Title                          │
├─────────────────────────────────────────┤
│  ┌════════════════════════════┐  100%   │
│  │         认知               │         │
│  ├══════════════════════┤      60%      │
│  │       兴趣           │               │
│  ├════════════════┤           35%       │
│  │     购买       │                     │
│  ├══════════┤                 15%       │
│  │   留存   │                           │
│  └─────────┘                            │
└─────────────────────────────────────────┘
```

```python
eng.funnel(title='销售漏斗分析',
    stages=[('线索获取', '10,000', '100%'),
            ('需求确认', '3,500', '35%'),
            ('方案报价', '1,200', '12%'),
            ('合同签署', '480', '4.8%')],
    source='Source: ...')
```

---

### 类别 G：团队专题

#### 33. Meet the Team (团队介绍页)

**适用场景**: 团队成员/核心高管/项目组简介。

```
┌─────────────────────────────────────────┐
│ ▌ Action Title                          │
├─────────────────────────────────────────┤
│  ┌─BG──┐    ┌─BG──┐    ┌─BG──┐        │
│  │(头像)│    │(头像)│    │(头像)│        │
│  │ 姓名 │    │ 姓名 │    │ 姓名 │        │
│  │ 职位 │    │ 职位 │    │ 职位 │        │
│  │ 简介 │    │ 简介 │    │ 简介 │        │
│  └──────┘    └──────┘    └──────┘        │
└─────────────────────────────────────────┘
```

```python
eng.meet_the_team(title='核心团队',
    members=[('张三', 'CEO', '15年行业经验'),
             ('李四', 'CTO', '前Google高级工程师'),
             ('王五', 'VP Sales', '年销售额¥5亿+')],
    source='Source: ...')
```

#### 34. Case Study (案例研究页)

**适用场景**: 展示成功案例，按"情境-行动-结果"结构组织。

```
┌─────────────────────────────────────────┐
│ ▌ Action Title                          │
├─────────────────────────────────────────┤
│  ┌─Situation──┐ ┌─Approach──┐ ┌Result─┐ │
│  │ 背景/挑战  │ │ 采取行动  │ │ 成果  │ │
│  │            │ │           │ │       │ │
│  └────────────┘ └───────────┘ └───────┘ │
│                                         │
│  ┌──BG_GRAY 客户评价/关键指标──────────┐ │
└─────────────────────────────────────────┘
```

```python
eng.case_study(title='XX银行数字化转型案例',
    sections=[('S', '背景', '传统核心系统老化，无法支撑业务增长'),
              ('A', '行动', '分阶段微服务改造 + 数据中台建设'),
              ('R', '成果', '交易处理能力提升10倍，故障率下降90%')],
    result_box=('关键指标', 'ROI 380% | 12个月回本'),
    source='Source: ...')
```

#### 35. Action Items / Next Steps (行动计划页)

**适用场景**: 演示文稿结尾的下一步行动清单。

```
┌─────────────────────────────────────────┐
│ ▌ Action Title                          │
├─────────────────────────────────────────┤
│  ┌──NAVY──┐   ┌──NAVY──┐   ┌──NAVY──┐  │
│  │行动一  │   │行动二  │   │行动三  │  │
│  ├─BG─────┤   ├─BG─────┤   ├─BG─────┤  │
│  │ 时间   │   │ 时间   │   │ 时间   │  │
│  │ 描述   │   │ 描述   │   │ 描述   │  │
│  │ 负责人 │   │ 负责人 │   │ 负责人 │  │
│  └────────┘   └────────┘   └────────┘  │
└─────────────────────────────────────────┘
```

```python
eng.action_items(title='下一步行动计划',
    actions=[('启动数据治理项目', 'Q2 2026', '建立统一数据标准与质量体系', '张三'),
             ('招聘AI工程师团队', 'Q1-Q2 2026', '组建10人ML工程团队', '李四'),
             ('完成ERP云迁移', 'Q3 2026', '核心ERP系统迁移至云原生架构', '王五')],
    source='Source: ...')
```

#### 36. Closing / Thank You (结束页)

**适用场景**: 演示文稿结尾的致谢或总结收尾页。

```
┌─────────────────────────────────────────┐
│  ═══                                    │
│                                         │
│           核心总结语句                    │
│           ──────────                    │
│           结束寄语                       │
│                                         │
│  ─────                                  │
└─────────────────────────────────────────┘
```

```python
eng.closing(title='谢谢', message='期待与您进一步交流')
```

---

### 类别 H：数据图表

> **触发规则**：当用户提供的内容包含 **日期/时间 + 数值/百分比** 的结构化数据（如舆情变化、销售趋势、KPI 周报、转化率变化等），**必须优先使用本类别的图表模式**，而不是 Data Table (#11) 或 Scorecard (#23)。
>
> **识别信号**（满足任一即触发）：
> - 数据中出现 `日期 + 百分比` 或 `日期 + 数值` 的组合
> - 提示词含 `████` 进度条字符 + 百分比
> - 内容涉及"趋势"、"演变"、"变化"、"走势"、"周报"、"日报"等时序关键词
> - 数据行数 ≥ 3 且每行包含至少一个类别和一个数值

#### 37. Grouped Bar Chart（分组柱状图 / 情绪热力图）

**适用场景**: 多个类别在不同时间点的数值对比（如舆情情绪分布、多产品销售对比、多指标周变化）。

```
┌─────────────────────────────────────────┐
│ ▌ Action Title                          │
├─────────────────────────────────────────┤
│  100% ─                                 │
│   80% ─  ██                             │
│   60% ─  ██ ██                          │
│   40% ─  ██ ██      ██      ██          │
│   20% ─  ██ ██ ██   ██ ██   ██ ██       │
│    0% ────────────────────────────────  │
│         3/4   3/6   3/8   3/10          │
│                                         │
│  ■ 正面  ■ 中性  ■ 负面                 │
│                                         │
│  ┌─BG_GRAY 趋势总结──────────────────┐  │
│  │ 总结文字                           │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

**设计规范**:
- 柱状图使用 `add_rect()` 手工绘制，不依赖 matplotlib
- Y 轴标签（百分比）用 `add_text()` 左对齐
- X 轴标签（日期）用 `add_text()` 居中
- 每组柱子间留 0.3" 间距，组内柱子间留 0.05" 间距
- 图例用小矩形色块 + 文字标签，放在图表下方
- 底部可选趋势总结区（BG_GRAY）

**颜色分配**:
- 第一类别：NAVY (#051C2C) — 主要/正面
- 第二类别：LINE_GRAY (#CCCCCC) — 中性/基准
- 第三类别：MED_GRAY (#666666) — 次要/负面
- 第四类别：ACCENT_BLUE (#006BA6) — 扩展
- 若类别有语义色（如正面=NAVY, 负面=MED_GRAY），优先使用语义色

```python
eng.grouped_bar(title='季度营收趋势（按产品线）',
    categories=['Q1', 'Q2', 'Q3', 'Q4'],
    series=[('产品A', NAVY), ('产品B', ACCENT_BLUE)],
    data=[[120, 80], [145, 95], [160, 110], [180, 130]],
    y_max=200, y_step=50, y_unit='万',
    source='Source: ...')
```

#### 38. Stacked Bar Chart（堆叠柱状图 / 百分比占比图）

**适用场景**: 展示各类别在总体中的占比随时间变化（如市场份额演变、预算分配变化、渠道贡献占比）。适合强调"构成比例"而非"绝对值"。

```
┌─────────────────────────────────────────┐
│ ▌ Action Title                          │
├─────────────────────────────────────────┤
│  100% ─ ┌──┐  ┌──┐  ┌──┐  ┌──┐        │
│         │C │  │  │  │  │  │  │        │
│   50% ─ │B │  │B │  │  │  │  │        │
│         │  │  │  │  │B │  │B │        │
│         │A │  │A │  │A │  │A │        │
│    0% ──└──┘──└──┘──└──┘──└──┘────────  │
│         Q1    Q2    Q3    Q4            │
│                                         │
│  ■ A类  ■ B类  ■ C类                    │
│                                         │
│  ┌─BG_GRAY 关键发现──────────────────┐  │
│  │ 分析文字                           │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

**设计规范**:
- 每根柱子内部从底部到顶部依次堆叠各类别
- 柱子宽度统一为 0.8"~1.2"（比分组柱状图更宽）
- 各段之间无间距，直接堆叠
- 百分比标签写在对应色块内部（当色块高度足够时），或省略
- 右侧可选放置"直接标签"指向最后一根柱子的各段

**颜色分配**（从底到顶）:
- 第一层（最大/最重要）：NAVY (#051C2C)
- 第二层：ACCENT_BLUE (#006BA6)
- 第三层：LINE_GRAY (#CCCCCC)
- 第四层：BG_GRAY (#F2F2F2) + 细边框
- 更多层级：使用 ACCENT_GREEN, ACCENT_ORANGE

```python
eng.stacked_bar(title='营收构成变化趋势',
    periods=['2023', '2024', '2025', '2026E'],
    series=[('产品', NAVY), ('服务', ACCENT_BLUE), ('订阅', ACCENT_GREEN)],
    data=[[40, 35, 25], [35, 35, 30], [30, 35, 35], [25, 35, 40]],
    source='Source: ...')
```

#### 39. Horizontal Bar Chart（水平柱状图 / 排名图）

**适用场景**: 类别名称较长的排名对比（如部门绩效排名、品牌认知度、功能使用率排行）。横向柱状图在类别较多时可读性更好。

```
┌─────────────────────────────────────────┐
│ ▌ Action Title                          │
├─────────────────────────────────────────┤
│  类别 A    ████████████████████  92%    │
│  类别 B    ████████████████     85%     │
│  类别 C    ██████████████       78%     │
│  类别 D    ████████████         65%     │
│  类别 E    ████████             52%     │
│                                         │
│  ┌─BG_GRAY 说明──────────────────────┐  │
│  │ 分析文字                           │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

**设计规范**:
- 类别标签左对齐，柱子起始位置统一
- 最长柱子 = 100% 参考宽度
- 每根柱子右侧标注数值
- 第一名用 NAVY，其余用 BG_GRAY（或渐变灰色）
- 行间距均匀

```python
eng.horizontal_bar(title='各部门数字化成熟度排名',
    items=[('研发部', 92, NAVY), ('市场部', 78, ACCENT_BLUE), ('运营部', 65, ACCENT_GREEN),
           ('财务部', 58, ACCENT_ORANGE), ('HR', 45, MED_GRAY)],
    source='Source: ...')
```

---

### Category I: Image + Content Layouts

> **Image Placeholder Convention**: Since python-pptx cannot embed web images at generation time, all image positions use a **gray placeholder rectangle** with crosshair lines and a label. The user replaces these with real images after generation.

#### Helper: `add_image_placeholder()`

The `add_image_placeholder()` helper is available via `from mck_ppt.core import add_image_placeholder`. Image layouts in MckEngine call it automatically — you do not need to invoke it directly.

---

#### #40 — Content + Right Image

**Use case**: Text explanation on the left, supporting visual on the right — product screenshot, photo, diagram.

```
┌──────────────────────────────────────────────┐
│ [Action Title — full width, NAVY bg]         │
├───────────────────────┬──────────────────────┤
│  Heading              │                      │
│  • Bullet point 1     │   ┌──────────────┐   │
│  • Bullet point 2     │   │  IMAGE        │   │
│  • Bullet point 3     │   │  PLACEHOLDER  │   │
│                       │   └──────────────┘   │
│  Takeaway box (gray)  │                      │
├───────────────────────┴──────────────────────┤
│ Source | Page N/Total                         │
└──────────────────────────────────────────────┘
```

```python
eng.content_right_image(title='产品核心功能',
    subtitle='AI智能分析引擎',
    bullets=['实时数据处理', '自动异常检测', '智能决策推荐'],
    takeaway='准确率达到98.5%，领先行业平均水平20个百分点',
    image_label='产品截图',
    source='Source: ...')
```

---

#### #41 — Left Image + Content

**Use case**: Visual-first layout — image on left draws attention, text on right provides context.

```
┌──────────────────────────────────────────────┐
│ [Action Title — full width, NAVY bg]         │
├──────────────────────┬───────────────────────┤
│                      │  Heading              │
│  ┌──────────────┐    │  • Bullet point 1     │
│  │  IMAGE        │   │  • Bullet point 2     │
│  │  PLACEHOLDER  │   │  • Bullet point 3     │
│  └──────────────┘    │                       │
│                      │  Takeaway box (gray)  │
├──────────────────────┴───────────────────────┤
│ Source | Page N/Total                         │
└──────────────────────────────────────────────┘
```

```python
s = prs.slides.add_slide(prs.slide_layouts[6])

# ── Title bar ──
add_rect(s, Inches(0), Inches(0), Inches(13.333), Inches(0.75), NAVY)
add_text(s, LM, Inches(0), CONTENT_W, Inches(0.75),
         '客户旅程优化的关键触点分析',
         font_size=TITLE_SIZE, font_color=WHITE, bold=True,
         anchor=MSO_ANCHOR.MIDDLE)
add_hline(s, LM, Inches(0.75), CONTENT_W, BLACK, Pt(0.5))

# ── Left: image placeholder (45%) ──
img_w = Inches(5.4)
add_image_placeholder(s, LM, Inches(1.1), img_w, Inches(4.2), '客户旅程地图')

# ── Right: text content (55%) ──
rx = LM + img_w + Inches(0.3)
rw = CONTENT_W - img_w - Inches(0.3)
ty = Inches(1.1)

add_text(s, rx, ty, rw, Inches(0.4),
         '五个关键触点决定80%的客户满意度',
         font_size=Pt(18), font_color=NAVY, bold=True)

bullets = [
    '• 首次接触：品牌认知与第一印象建立',
    '• 产品体验：核心功能的易用性与稳定性',
    '• 售后服务：响应速度与问题解决率',
    '• 续约决策：价值感知与竞品比较',
]
add_text(s, rx, ty + Inches(0.5), rw, Inches(2.4),
         bullets, font_size=BODY_SIZE, font_color=DARK_GRAY, line_spacing=Pt(8))

# Takeaway box
add_rect(s, rx, Inches(4.5), rw, Inches(0.8), BG_GRAY)
add_text(s, rx + Inches(0.2), Inches(4.5), rw - Inches(0.4), Inches(0.8),
         '建议优先投资"首次接触"和"产品体验"两个高杠杆触点',
         font_size=BODY_SIZE, font_color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE)

add_source(s, 'Source: 客户满意度调研数据，2026 Q1')
add_page_number(s, 4, 12)
```

---

#### #42 — Three Images + Descriptions

**Use case**: Visual comparison of three products, locations, or concepts side by side.

```
┌──────────────────────────────────────────────┐
│ [Action Title — full width, NAVY bg]         │
├──────────────┬──────────────┬────────────────┤
│ ┌──────────┐ │ ┌──────────┐ │ ┌──────────┐  │
│ │  IMAGE 1 │ │ │  IMAGE 2 │ │ │  IMAGE 3 │  │
│ └──────────┘ │ └──────────┘ │ └──────────┘  │
│  Title 1     │  Title 2     │  Title 3      │
│  Description │  Description │  Description  │
├──────────────┴──────────────┴────────────────┤
│ Source | Page N/Total                         │
└──────────────────────────────────────────────┘
```

```python
eng.three_images(title='办公环境',
    items=[('总部大楼', '位于科技园区核心位置', '总部外景'),
           ('开放办公', '敏捷协作空间设计', '办公区域'),
           ('创新实验室', '前沿技术研发基地', '实验室')],
    source='Source: ...')
```

---

#### #43 — Image + Four Key Points

**Use case**: Central image/diagram with four callout points arranged around or beside it.

```
┌──────────────────────────────────────────────┐
│ [Action Title — full width, NAVY bg]         │
├──────────────────────────────────────────────┤
│  ┌─────┬──────────┐  ┌─────┬──────────┐     │
│  │ 01  │ Point A   │  │ 02  │ Point B   │   │
│  └─────┴──────────┘  └─────┴──────────┘     │
│         ┌──────────────────────┐              │
│         │    IMAGE PLACEHOLDER │              │
│         └──────────────────────┘              │
│  ┌─────┬──────────┐  ┌─────┬──────────┐     │
│  │ 03  │ Point C   │  │ 04  │ Point D   │   │
│  └─────┴──────────┘  └─────┴──────────┘     │
├──────────────────────────────────────────────┤
│ Source | Page N/Total                         │
└──────────────────────────────────────────────┘
```

```python
eng.image_four_points(title='核心优势',
    image_label='产品示意图',
    points=[('高性能', '毫秒级响应'),
            ('高可用', '99.99% SLA'),
            ('安全', '多层防护体系'),
            ('弹性', '自动扩缩容')],
    source='Source: ...')
```

---

#### #44 — Full-Width Image with Overlay Text

**Use case**: Hero image covering the slide with semi-transparent overlay text — for visual storytelling, case study intros.

```
┌──────────────────────────────────────────────┐
│                                              │
│           FULL-WIDTH IMAGE                   │
│           PLACEHOLDER                        │
│                                              │
│    ┌─────────────────────────────────────┐   │
│    │ Semi-transparent dark overlay        │   │
│    │ "Quote or headline text"            │   │
│    │  — Attribution                       │   │
│    └─────────────────────────────────────┘   │
│                                              │
├──────────────────────────────────────────────┤
│ Source | Page N/Total                         │
└──────────────────────────────────────────────┘
```

```python
eng.full_width_image(title='全球布局',
    image_label='世界地图',
    overlay_text='覆盖全球32个国家和地区',
    source='Source: ...')
```

---

#### #45 — Case Study with Image

**Use case**: Extended case study with a visual — Situation, Approach, Result + supporting image.

```
┌──────────────────────────────────────────────┐
│ [Action Title — full width, NAVY bg]         │
├───────────────────────┬──────────────────────┤
│  SITUATION            │                      │
│  Background text...   │  ┌──────────────┐    │
│                       │  │  IMAGE        │   │
│  APPROACH             │  │  PLACEHOLDER  │   │
│  Method text...       │  └──────────────┘    │
│                       │                      │
│  RESULT               │  ┌─────┬─────┐      │
│  Outcome metrics...   │  │ KPI1│ KPI2│      │
│                       │  └─────┴─────┘      │
├───────────────────────┴──────────────────────┤
│ Source | Page N/Total                         │
└──────────────────────────────────────────────┘
```

```python
eng.case_study_image(title='XX银行案例',
    sections=[('背景', '传统系统老化', ACCENT_BLUE),
              ('方案', '微服务改造', ACCENT_GREEN),
              ('成果', '效率提升10倍', ACCENT_ORANGE)],
    image_label='系统架构图',
    kpis=[('10x', '处理能力'), ('90%', '故障减少')],
    source='Source: ...')
```

---

#### #46 — Quote with Background Image

**Use case**: Inspirational quote or key insight with a subtle background visual — for keynote-style emphasis slides.

```
┌──────────────────────────────────────────────┐
│                                              │
│       ┌──────────────────────────┐           │
│       │  IMAGE PLACEHOLDER       │           │
│       │  (subtle / blurred)      │           │
│       └──────────────────────────┘           │
│                                              │
│  ──────────────────────────────────          │
│  "Quote text in large font"                  │
│  — Speaker Name, Title                       │
│  ──────────────────────────────────          │
│                                              │
├──────────────────────────────────────────────┤
│ Source | Page N/Total                         │
└──────────────────────────────────────────────┘
```

```python
eng.quote_bg_image(title='',
    quote_text='创新不是选择，而是生存的必需。',
    attribution='CEO, 2026年全员大会',
    image_label='背景图',
    source='')
```

---

#### #47 — Goals / Targets with Illustration

**Use case**: Strategic goals or OKRs with a supporting illustration — for goal-setting and planning slides.

```
┌──────────────────────────────────────────────┐
│ [Action Title — full width, NAVY bg]         │
├───────────────────────┬──────────────────────┤
│                       │                      │
│  ○ Goal 1 — desc      │  ┌──────────────┐   │
│  ○ Goal 2 — desc      │  │  IMAGE        │   │
│  ○ Goal 3 — desc      │  │  PLACEHOLDER  │   │
│  ○ Goal 4 — desc      │  └──────────────┘   │
│                       │                      │
│  Summary metric       │                      │
├───────────────────────┴──────────────────────┤
│ Source | Page N/Total                         │
└──────────────────────────────────────────────┘
```

```python
eng.goals_illustration(title='2026年度目标',
    goals=[('营收翻倍', '达到¥20亿年营收'),
           ('全球化', '进入5个海外市场'),
           ('IPO准备', '完成合规与治理升级')],
    image_label='目标愿景图',
    source='Source: ...')
```

---

### Category J: Advanced Data Visualization

> **Drawing Convention**: All charts are drawn with `add_rect()` and `add_oval()` — no matplotlib, no chart objects, no connectors. This ensures zero file corruption and full style control.

---

#### #48 — Donut Chart

**Use case**: Part-of-whole composition — market share, budget allocation, sentiment distribution. Up to 5 segments.

> **v2.0**: Uses BLOCK_ARC native shapes — only 4 shapes per chart (was hundreds of rect blocks). See Guard Rails Rule 9.

```
┌──────────────────────────────────────────────┐
│ [Action Title — full width, NAVY bg]         │
├───────────────────────┬──────────────────────┤
│                       │                      │
│    ┌───────────┐      │  ■ Segment A  45%    │
│    │  DONUT    │      │  ■ Segment B  28%    │
│    │ (BLOCK_   │      │  ■ Segment C  15%    │
│    │  ARC ×4)  │      │  ■ Segment D  12%    │
│    │  CENTER%  │      │                      │
│    └───────────┘      │  Insight text...     │
├───────────────────────┴──────────────────────┤
│ Source | Page N/Total                         │
└──────────────────────────────────────────────┘
```

```python
eng.donut(title='2026年上半年营收渠道构成',
    segments=[(0.45, NAVY, '线上直营'), (0.28, ACCENT_BLUE, '经销商'),
              (0.15, ACCENT_GREEN, '企业客户'), (0.12, ACCENT_ORANGE, '其他')],
    center_label='¥8.5亿', center_sub='总营收',
    summary='线上直营渠道占比同比提升12个百分点',
    source='Source: ...')
```

---

#### #49 — Waterfall Chart

**Use case**: Bridge from starting value to ending value showing incremental changes — revenue bridge, profit walk, budget variance.

```
┌──────────────────────────────────────────────┐
│ [Action Title — full width, NAVY bg]         │
├──────────────────────────────────────────────┤
│        ┌──┐                                  │
│  Start │  │ +A  -B  +C  -D  +E  ┌──┐ End   │
│        │  │ ┌┐  ┌┐  ┌┐  ┌┐  ┌┐  │  │       │
│        │  │ ││  ││  ││  ││  ││  │  │       │
│        │  │ └┘──└┘──└┘──└┘──└┘  │  │       │
│        └──┘                      └──┘       │
│  Takeaway text...                            │
├──────────────────────────────────────────────┤
│ Source | Page N/Total                         │
└──────────────────────────────────────────────┘
```

```python
eng.waterfall(title='利润变动瀑布图',
    items=[('2025年利润', 100, 'base'), ('营收增长', 35, 'up'),
           ('成本节省', 15, 'up'), ('新投资', -20, 'down'),
           ('2026年利润', 130, 'base')],
    source='Source: ...')
```

---

#### #50 — Line / Trend Chart

**Use case**: Time-series trends — revenue growth, user count, market share over time. Supports 1-4 series.

```
┌──────────────────────────────────────────────┐
│ [Action Title — full width, NAVY bg]         │
├──────────────────────────────────────────────┤
│  Y ─                                         │
│     ══════ Series A (black, bold) ═══ LabelA │
│     ══════ Series B (blue) ══════════ LabelB │
│     ══════ Series C (green) ═════════ LabelC │
│  0 ──────────────────────────────────        │
│     Q1'24  Q2'24  Q3'24  Q4'24  Q1'25       │
│  Takeaway text...                            │
├──────────────────────────────────────────────┤
│ Source | Page N/Total                         │
└──────────────────────────────────────────────┘
```

```python
eng.line_chart(title='月活用户趋势',
    x_labels=['1月','2月','3月','4月','5月','6月'],
    y_labels=['0','100万','200万','300万'],
    values=[0.4, 0.45, 0.5, 0.6, 0.7, 0.82],
    legend_label='月活用户',
    source='Source: ...')
```

---

#### #51 — Pareto Chart (Bar + Cumulative Line)

**Use case**: 80/20 analysis — identifying the vital few causes/items that account for most of the impact.

```
┌──────────────────────────────────────────────┐
│ [Action Title — full width, NAVY bg]         │
├──────────────────────────────────────────────┤
│  Y₁ ─                                  ─ Y₂ │
│     ┌──┐                          ----100%   │
│     │  │┌──┐               ------             │
│     │  ││  │┌──┐     ------                   │
│     │  ││  ││  │┌──┐-                         │
│     │  ││  ││  ││  │┌──┐┌──┐                 │
│     └──┘└──┘└──┘└──┘└──┘└──┘    80% line     │
│  Takeaway: Top 3 items account for 78%       │
├──────────────────────────────────────────────┤
│ Source | Page N/Total                         │
└──────────────────────────────────────────────┘
```

```python
eng.pareto(title='缺陷类型分析（帕累托）',
    items=[('UI问题', 45), ('性能', 28), ('兼容性', 15), ('安全', 8), ('其他', 4)],
    max_val=50,
    source='Source: ...')
```

---

#### #52 — Progress Bars / KPI Tracker

**Use case**: Multiple KPIs with target vs actual progress — project health, OKR tracking, sales pipeline.

```
┌──────────────────────────────────────────────┐
│ [Action Title — full width, NAVY bg]         │
├──────────────────────────────────────────────┤
│  KPI Name          Actual / Target    Status │
│  ════════████████████░░░░░░░░   78%   ● On   │
│  ════════████████░░░░░░░░░░░░   52%   ● Risk │
│  ════════██████████████████░░   92%   ● On   │
│  ════════████████████████░░░   85%   ● On   │
│  ════════█████░░░░░░░░░░░░░░   38%   ● Off  │
│  Summary / insight text                      │
├──────────────────────────────────────────────┤
│ Source | Page N/Total                         │
└──────────────────────────────────────────────┘
```

```python
eng.kpi_tracker(title='OKR进度追踪',
    kpis=[('营收目标', 0.78, '¥7.8亿 / ¥10亿', 'on'),
          ('客户增长', 0.92, '184家 / 200家', 'on'),
          ('NPS提升', 0.65, '72分 / 80分', 'risk')],
    source='Source: ...')
```

---

#### #53 — Bubble / Scatter Plot

**Use case**: Two-variable comparison with size encoding — market attractiveness vs competitive position, impact vs effort.

```
┌──────────────────────────────────────────────┐
│ [Action Title — full width, NAVY bg]         │
├──────────────────────────────────────────────┤
│  Y ─   High                                  │
│     ●(large)    ○(med)                       │
│              ●(small)    ○(large)             │
│     ○(med)         ●(med)                    │
│  0 ─   Low ──────────────────── High ─ X     │
│  Legend: ● Category A  ○ Category B          │
│  Takeaway text...                            │
├──────────────────────────────────────────────┤
│ Source | Page N/Total                         │
└──────────────────────────────────────────────┘
```

```python
eng.bubble(title='业务组合分析',
    bubbles=[(30, 70, 1.2, '产品A', NAVY),
             (60, 50, 0.8, '产品B', ACCENT_BLUE),
             (80, 30, 0.5, '产品C', ACCENT_GREEN)],
    x_label='市场份额 →', y_label='增长率 ↑',
    source='Source: ...')
```

---

#### #54 — Risk / Heat Matrix

**Use case**: Risk assessment — impact vs likelihood grid, with color-coded cells. Classic consulting risk register visualization.

```
┌──────────────────────────────────────────────┐
│ [Action Title — full width, NAVY bg]         │
├──────────────────────────────────────────────┤
│           Low Impact   Med Impact  High Impact│
│  High     ■ Yellow     ■ Orange   ■ Red      │
│  Prob     "Risk C"     "Risk A"   "Risk D"   │
│  Med      ■ Green      ■ Yellow   ■ Orange   │
│  Prob     "Risk F"     "Risk B"   "Risk E"   │
│  Low      ■ Green      ■ Green    ■ Yellow   │
│  Prob                              "Risk G"  │
│  Action items / mitigation plan              │
├──────────────────────────────────────────────┤
│ Source | Page N/Total                         │
└──────────────────────────────────────────────┘
```

```python
eng.risk_matrix(title='项目风险评估矩阵',
    grid_colors=[[ACCENT_GREEN,ACCENT_ORANGE,ACCENT_RED],
                 [ACCENT_GREEN,ACCENT_ORANGE,ACCENT_ORANGE],
                 [ACCENT_GREEN,ACCENT_GREEN,ACCENT_ORANGE]],
    grid_lights=[[None]*3]*3,
    risks=[('数据泄露', 2, 2), ('系统宕机', 1, 2)],
    y_labels=['高','中','低'], x_labels=['低','中','高'],
    source='Source: ...')
```

**Variant: Matrix + Side Panel** — When the matrix needs an accompanying insight panel (e.g. "Key Changes", "Action Items"), use a compact grid (~60% width) with a side panel (~38% width). This prevents the panel from being crushed by a full-width grid.

```
┌──────────────────────────────────────────────────┐
│ [Action Title]                                   │
├──────────────────────────────────────────────────┤
│ Axis │ Col1   Col2   Col3 │ ┌─────────────────┐ │
│  ──  │ ■■■    ■■■    ■■■  │ │ Insight Panel   │ │
│  ↑   │ ■■■    ■■■    ■■■  │ │ • Bullet 1      │ │
│      │ ■■■    ■■■    ■■■  │ │ • Bullet 2      │ │
│      │   → Axis label →   │ │ ┌─────────────┐ │ │
│      │                     │ │ │ Summary box │ │ │
│      │                     │ │ └─────────────┘ │ │
│      │                     │ └─────────────────┘ │
├──────────────────────────────────────────────────┤
│ Source | Page N/Total                             │
└──────────────────────────────────────────────────┘
```

Layout math for the side-panel variant:

```python
eng.risk_matrix(title='项目风险评估矩阵',
    grid_colors=[[ACCENT_GREEN,ACCENT_ORANGE,ACCENT_RED],
                 [ACCENT_GREEN,ACCENT_ORANGE,ACCENT_ORANGE],
                 [ACCENT_GREEN,ACCENT_GREEN,ACCENT_ORANGE]],
    grid_lights=[[None]*3]*3,
    risks=[('数据泄露', 2, 2), ('系统宕机', 1, 2)],
    y_labels=['高','中','低'], x_labels=['低','中','高'],
    source='Source: ...')
```

> **Rule**: When a matrix needs a companion panel, shrink `cell_w` to ~2.15" (from 3.0") and `axis_label_w` to ~0.65" (from 1.8"). This yields a panel width of ~4.2" — enough for 6+ bullet items with comfortable reading. Never let the panel shrink below Inches(2.5).

---

#### #55 — Gauge / Dial Chart

**Use case**: Single KPI health indicator — customer satisfaction, system uptime, quality score. Visual "speedometer" metaphor.

> **v2.0**: Uses BLOCK_ARC native shapes — only 3 shapes for the arc (was 180+ rect blocks + white overlay). Horizontal rainbow arc (left→top→right). See Guard Rails Rule 9.

```
┌──────────────────────────────────────────────┐
│ [Action Title — full width, NAVY bg]         │
├──────────────────────────────────────────────┤
│                                              │
│         ╭──── ── ── ── ── ────╮              │
│      Red│   Orange    Green   │              │
│         ╰─────────────────────╯              │
│               78 / 100                       │
│                                              │
│  ┃ 当前NPS  ┃ 行业平均  ┃ 去年同期  ┃ 目标  │
│  ┃ 78       ┃ 52        ┃ 65        ┃ 80    │
├──────────────────────────────────────────────┤
│ Source | Page N/Total                         │
└──────────────────────────────────────────────┘
```

```python
eng.gauge(title='客户满意度',
    score=78,
    benchmarks=[('行业平均', '65分', ACCENT_ORANGE), ('目标', '85分', ACCENT_GREEN)],
    source='Source: ...')
```

---

#### #56 — Harvey Ball Status Table

**Use case**: Multi-criteria evaluation matrix — feature comparison, vendor assessment, capability maturity with visual fill indicators.

```
┌──────────────────────────────────────────────┐
│ [Action Title — full width, NAVY bg]         │
├──────────────────────────────────────────────┤
│  Criteria     Option A   Option B   Option C │
│  ─────────────────────────────────────────── │
│  功能完整度     ●          ◕          ◑       │
│  用户体验       ◕          ●          ◔       │
│  技术可扩展     ◑          ◕          ●       │
│  实施成本       ◕          ◑          ●       │
│  供应商实力     ●          ◕          ◕       │
│  ─────────────────────────────────────────── │
│  Legend: ● Full  ◕ 75%  ◑ 50%  ◔ 25%  ○ 0% │
├──────────────────────────────────────────────┤
│ Source | Page N/Total                         │
└──────────────────────────────────────────────┘
```

```python
eng.harvey_ball_table(title='供应商能力评估',
    headers=['供应商', '技术', '交付', '价格', '服务'],
    rows=[('供应商A', 100, 75, 50, 100),
          ('供应商B', 75, 100, 75, 50)],
    source='Source: ...')
```

---

### Category K: Dashboard Layouts

> **Dashboard Convention**: Dashboards pack multiple visual elements (KPIs, charts, tables) into a single dense slide. Use 3-4 distinct visual blocks minimum. Background panels (BG_GRAY) create clear section boundaries.

---

#### #57 — Dashboard: KPIs + Chart + Takeaways

**Use case**: Executive summary dashboard — top KPI cards, a chart in the middle, and key takeaways at the bottom.

```
┌──────────────────────────────────────────────┐
│ [Action Title — full width, NAVY bg]         │
├────────┬────────┬────────┬───────────────────┤
│  KPI 1 │  KPI 2 │  KPI 3 │  KPI 4           │
│  ¥8.5B │  +25%  │  78    │  92%             │
│  营收   │  增长率 │  NPS   │  留存率          │
├────────┴────────┴────────┴───────────────────┤
│                                              │
│  ┌──── Bar/Line Chart Area ─────────┐        │
│  │    (any chart pattern here)       │        │
│  └───────────────────────────────────┘        │
│                                              │
│  ┌──── Takeaway Panel ──────────────┐        │
│  │ • Key insight 1   • Key insight 2 │        │
│  └───────────────────────────────────┘        │
├──────────────────────────────────────────────┤
│ Source | Page N/Total                         │
└──────────────────────────────────────────────┘
```

```python
eng.dashboard_kpi_chart(title='月度运营概览',
    kpi_cards=[('¥2.3亿', '月营收', '+18%', NAVY),
               ('98.5%', '可用性', '超SLA', ACCENT_GREEN),
               ('4.8', 'NPS', '+0.3', ACCENT_BLUE)],
    chart_data={'labels':['1月','2月','3月'], 'values':[180,210,230], 'color':NAVY},
    source='Source: ...')
```

---

#### #58 — Dashboard: Table + Chart + Factoids

**Use case**: Data-dense overview — left table, right chart, bottom factoid cards. For board-level reporting.

```
┌──────────────────────────────────────────────┐
│ [Action Title — full width, NAVY bg]         │
├───────────────────────┬──────────────────────┤
│                       │                      │
│  ┌── Data Table ───┐  │  ┌── Chart ───────┐  │
│  │ Rows of data    │  │  │ Bars or lines  │  │
│  │ with values     │  │  │                │  │
│  └─────────────────┘  │  └────────────────┘  │
│                       │                      │
├────────┬──────────┬───┴──────────┬───────────┤
│ Fact 1 │ Fact 2   │  Fact 3      │ Fact 4    │
│ "120+" │ "¥2.3B"  │  "Top 5%"   │ "99.9%"   │
├────────┴──────────┴──────────────┴───────────┤
│ Source | Page N/Total                         │
└──────────────────────────────────────────────┘
```

```python
eng.dashboard_table_chart(title='季度业务仪表盘',
    table_data={'headers':['指标','Q1','Q2','Q3'],
                'rows':[('营收','¥1.8亿','¥2.1亿','¥2.5亿'),
                        ('利润','¥0.3亿','¥0.4亿','¥0.5亿')]},
    source='Source: ...')
```

---

### Category L: Visual Storytelling & Special

> **Storytelling Convention**: These layouts emphasize visual narrative patterns commonly found in McKinsey decks — stakeholder maps, decision trees, checklists, and icon-driven grids. They add variety beyond standard charts and text layouts.

---

#### #59 — Stakeholder Map

**Use case**: Influence vs interest matrix for stakeholders — change management, project governance, communication planning.

```
┌──────────────────────────────────────────────┐
│ [Action Title — full width, NAVY bg]         │
├──────────────────────────────────────────────┤
│  Interest ↑                                  │
│  High  ┌─────────────┬──────────────┐        │
│        │ Keep Informed│ Manage Closely│       │
│        │  (name)      │  (name)      │       │
│        ├─────────────┼──────────────┤        │
│  Low   │ Monitor     │ Keep Satisfied│       │
│        │  (name)      │  (name)      │       │
│        └─────────────┴──────────────┘        │
│             Low        High → Influence       │
│  Action plan text...                         │
├──────────────────────────────────────────────┤
│ Source | Page N/Total                         │
└──────────────────────────────────────────────┘
```

```python
eng.stakeholder_map(title='干系人矩阵',
    quadrants=[('高关注 / 高影响', ['CEO', 'CTO']),
               ('高关注 / 低影响', ['项目经理', '产品经理']),
               ('低关注 / 高影响', ['监管机构']),
               ('低关注 / 低影响', ['普通员工'])],
    source='Source: ...')
```

---

#### #60 — Issue / Decision Tree

**Use case**: Breaking down a complex decision into sub-decisions — problem decomposition, MECE logic tree, diagnostic framework.

```
┌──────────────────────────────────────────────┐
│ [Action Title — full width, NAVY bg]         │
├──────────────────────────────────────────────┤
│                                              │
│  ┌────────┐                                  │
│  │ Root   │──┬── ┌────────┐──┬── ┌────────┐ │
│  │ Issue  │  │   │ Branch │  │   │ Leaf 1 │ │
│  └────────┘  │   │   A    │  │   └────────┘ │
│              │   └────────┘  └── ┌────────┐ │
│              │                    │ Leaf 2 │ │
│              │                    └────────┘ │
│              └── ┌────────┐──┬── ┌────────┐ │
│                  │ Branch │  │   │ Leaf 3 │ │
│                  │   B    │  └── └────────┘ │
│                  └────────┘                  │
├──────────────────────────────────────────────┤
│ Source | Page N/Total                         │
└──────────────────────────────────────────────┘
```

```python
eng.decision_tree(title='技术选型决策树',
    root='是否需要实时处理？',
    branches=[('是', ['流式计算', 'Kafka + Flink']),
              ('否', ['批处理', 'Spark + Hive'])],
    source='Source: ...')
```

---

#### #61 — Five-Row Checklist / Status

**Use case**: Task completion status, implementation checklist, audit findings — each row with status indicator.

```
┌──────────────────────────────────────────────┐
│ [Action Title — full width, NAVY bg]         │
├──────────────────────────────────────────────┤
│  # │ Task / Item         │ Owner │ Status    │
│  ──┼─────────────────────┼───────┼────────── │
│  1 │ Data migration       │ TechOps│ ✓ Done   │
│  2 │ UAT testing          │ QA    │ ✓ Done    │
│  3 │ Security audit       │ InfoSec│ → Active │
│  4 │ Training rollout     │ HR    │ ○ Pending │
│  5 │ Go-live sign-off     │ PMO   │ ○ Pending │
│  ──┼─────────────────────┼───────┼────────── │
│  Progress: 2/5 complete (40%)               │
├──────────────────────────────────────────────┤
│ Source | Page N/Total                         │
└──────────────────────────────────────────────┘
```

```python
eng.checklist(title='上线准备检查清单',
    columns=['检查项', '负责人', '截止日', '状态'],
    col_widths=[Inches(4.5), Inches(2.0), Inches(2.0), Inches(2.0)],
    rows=[('安全审计完成', '张三', '3/15', 'done'),
          ('性能压测通过', '李四', '3/20', 'wip'),
          ('文档更新', '王五', '3/25', 'todo')],
    status_map={'done': ('✅ 完成', ACCENT_GREEN, LIGHT_GREEN),
                'wip': ('🔄 进行中', ACCENT_ORANGE, LIGHT_ORANGE),
                'todo': ('⏳ 待开始', MED_GRAY, BG_GRAY)},
    source='Source: ...')
```

---

#### #62 — Metric Comparison Row

**Use case**: Before/after or multi-period comparison with large numbers — performance review, transformation impact, A/B test results.

```
┌──────────────────────────────────────────────┐
│ [Action Title — full width, NAVY bg]         │
├──────────────────────────────────────────────┤
│                                              │
│  ┌────────────┐   →   ┌────────────┐        │
│  │  BEFORE     │       │  AFTER      │       │
│  │  ¥5.2亿     │       │  ¥8.5亿     │       │
│  │  营收        │       │  营收        │       │
│  └────────────┘       └────────────┘        │
│  ┌────────────┐   →   ┌────────────┐        │
│  │  45天       │       │  28天       │       │
│  │  库存周转    │       │  库存周转    │       │
│  └────────────┘       └────────────┘        │
│  Summary text...                             │
├──────────────────────────────────────────────┤
│ Source | Page N/Total                         │
└──────────────────────────────────────────────┘
```

```python
eng.metric_comparison(title='数字化转型前后关键指标对比',
    metrics=[('营收规模', '¥5.2亿', '¥8.5亿', '+63%'),
             ('库存周转', '45天', '28天', '–38%'),
             ('客户NPS', '52', '78', '+50%')],
    source='Source: ...')
```

---

#### #63 — Icon Grid (4×2 or 3×3)

**Use case**: Capability overview, service catalog, feature grid — each cell with icon placeholder + title + description.

```
┌──────────────────────────────────────────────┐
│ [Action Title — full width, NAVY bg]         │
├──────────────┬──────────────┬────────────────┤
│  [icon]      │  [icon]      │  [icon]        │
│  Title A     │  Title B     │  Title C       │
│  Description │  Description │  Description   │
├──────────────┼──────────────┼────────────────┤
│  [icon]      │  [icon]      │  [icon]        │
│  Title D     │  Title E     │  Title F       │
│  Description │  Description │  Description   │
├──────────────┴──────────────┴────────────────┤
│ Source | Page N/Total                         │
└──────────────────────────────────────────────┘
```

```python
eng.icon_grid(title='产品功能矩阵',
    items=[('🔍', '智能搜索', '毫秒级全文检索'),
           ('📊', '数据分析', '实时BI仪表盘'),
           ('🤖', 'AI助手', '自然语言交互'),
           ('🔒', '安全防护', '多层加密体系')],
    source='Source: ...')
```

---

#### #64 — Pie Chart (Simple)

**Use case**: Simple part-of-whole with ≤5 segments — budget allocation, market share, time allocation.

> **v2.0**: Uses BLOCK_ARC native shapes with `inner_ratio=0` for solid pie sectors — only 4 shapes per chart (was 2000+ rect blocks). See Guard Rails Rule 9.

```
┌──────────────────────────────────────────────┐
│ [Action Title — full width, NAVY bg]         │
├───────────────────────┬──────────────────────┤
│                       │                      │
│    ┌───────────┐      │  ■ Segment A  42%    │
│    │   PIE     │      │  ■ Segment B  28%    │
│    │ (BLOCK_   │      │  ■ Segment C  18%    │
│    │  ARC ×4)  │      │  ■ Segment D  12%    │
│    └───────────┘      │                      │
│  Insight text box                            │
├───────────────────────┴──────────────────────┤
│ Source | Page N/Total                         │
└──────────────────────────────────────────────┘
```

```python
eng.pie(title='市场份额分布',
    segments=[(0.35, NAVY, '我们', ''), (0.25, ACCENT_BLUE, '竞品A', ''),
              (0.20, ACCENT_GREEN, '竞品B', ''), (0.20, ACCENT_ORANGE, '其他', '')],
    source='Source: ...')
```

---

#### #65 — SWOT Analysis

**Use case**: Classic strategic analysis — Strengths, Weaknesses, Opportunities, Threats in a 2×2 color-coded grid.

```
┌──────────────────────────────────────────────┐
│ [Action Title — full width, NAVY bg]         │
├──────────────────────┬───────────────────────┤
│  STRENGTHS (Blue)    │  WEAKNESSES (Orange)  │
│  • Point 1           │  • Point 1            │
│  • Point 2           │  • Point 2            │
├──────────────────────┼───────────────────────┤
│  OPPORTUNITIES (Green)│  THREATS (Red)        │
│  • Point 1           │  • Point 1            │
│  • Point 2           │  • Point 2            │
├──────────────────────┴───────────────────────┤
│ Source | Page N/Total                         │
└──────────────────────────────────────────────┘
```

```python
eng.swot(title='SWOT分析',
    quadrants=[('优势 Strengths', ['技术领先', '团队优秀', '资金充裕']),
               ('劣势 Weaknesses', ['品牌知名度低', '销售网络有限']),
               ('机会 Opportunities', ['市场快速增长', '政策利好']),
               ('威胁 Threats', ['巨头入场', '人才竞争激烈'])],
    source='Source: ...')
```

---

#### #66 — Agenda / Meeting Outline

**Use case**: Meeting agenda with time allocations, speaker assignments — for workshop facilitation, board meetings.

```
┌──────────────────────────────────────────────┐
│ [Action Title — full width, NAVY bg]         │
├──────────────────────────────────────────────┤
│  Time    │ Topic             │ Speaker │ Min  │
│  ────────┼───────────────────┼─────────┼──── │
│  09:00   │ Opening & Context │ CEO     │ 15   │
│  09:15   │ Market Analysis   │ VP Mkt  │ 30   │
│  09:45   │ Product Roadmap   │ CPO     │ 30   │
│  10:15   │ Break             │         │ 15   │
│  10:30   │ Financial Review  │ CFO     │ 30   │
│  11:00   │ Q&A & Next Steps  │ All     │ 30   │
├──────────────────────────────────────────────┤
│ Source | Page N/Total                         │
└──────────────────────────────────────────────┘
```

```python
eng.agenda(title='季度回顾会议议程',
    headers=[('议题', Inches(5.0)), ('时间', Inches(2.0)),
             ('负责人', Inches(2.0)), ('备注', Inches(2.5))],
    items=[('Q3业绩回顾', '09:00-09:30', '张总', '', 'key'),
           ('产品路线图更新', '09:30-10:00', '李总', '', 'normal'),
           ('茶歇', '10:00-10:15', '', '', 'break'),
           ('2026规划讨论', '10:15-11:00', '全员', '', 'key')],
    source='Source: ...')
```

---

#### #67 — Value Chain / Horizontal Flow

**Use case**: End-to-end value chain visualization — supply chain, service delivery pipeline, customer journey stages.

```
┌──────────────────────────────────────────────┐
│ [Action Title — full width, NAVY bg]         │
├──────────────────────────────────────────────┤
│                                              │
│ ┌───────┐  →  ┌───────┐  →  ┌───────┐  →  ┌───────┐  →  ┌───────┐ │
│ │Stage 1│     │Stage 2│     │Stage 3│     │Stage 4│     │Stage 5│ │
│ │ desc  │     │ desc  │     │ desc  │     │ desc  │     │ desc  │ │
│ │ KPI   │     │ KPI   │     │ KPI   │     │ KPI   │     │ KPI   │ │
│ └───────┘     └───────┘     └───────┘     └───────┘     └───────┘ │
│                                              │
│  Insight / bottleneck analysis               │
├──────────────────────────────────────────────┤
│ Source | Page N/Total                         │
└──────────────────────────────────────────────┘
```

```python
eng.value_chain(title='价值链分析',
    stages=[('研发', '产品设计与技术开发', ACCENT_BLUE),
            ('生产', '精益制造与质量管控', ACCENT_GREEN),
            ('营销', '品牌建设与渠道管理', ACCENT_ORANGE),
            ('服务', '客户支持与持续运营', NAVY)],
    source='Source: ...')
```

---

#### #68 — Two-Column Image + Text Grid

**Use case**: Visual catalog — 2 rows × 2 columns, each cell with image + title + description. Product showcase, location overview.

```
┌──────────────────────────────────────────────┐
│ [Action Title — full width, NAVY bg]         │
├──────────────────────┬───────────────────────┤
│ ┌──────┐ Title A     │ ┌──────┐ Title B      │
│ │IMAGE │ Description │ │IMAGE │ Description  │
│ └──────┘             │ └──────┘              │
├──────────────────────┼───────────────────────┤
│ ┌──────┐ Title C     │ ┌──────┐ Title D      │
│ │IMAGE │ Description │ │IMAGE │ Description  │
│ └──────┘             │ └──────┘              │
├──────────────────────┴───────────────────────┤
│ Source | Page N/Total                         │
└──────────────────────────────────────────────┘
```

```python
eng.two_col_image_grid(title='解决方案矩阵',
    items=[('智能客服', '7×24小时AI客服', ACCENT_BLUE, '客服系统截图'),
           ('数据分析', '实时BI仪表盘', ACCENT_GREEN, '分析面板'),
           ('流程自动化', 'RPA机器人流程', ACCENT_ORANGE, '自动化流程'),
           ('安全合规', '一站式合规管理', NAVY, '安全架构')],
    source='Source: ...')
```

---

#### #69 — Numbered List with Side Panel

**Use case**: Key recommendations or findings with a highlighted side panel — consulting recommendations, audit findings.

```
┌──────────────────────────────────────────────┐
│ [Action Title — full width, NAVY bg]         │
├────────────────────────┬─────────────────────┤
│                        │                     │
│  1  Recommendation A   │  ┌───────────────┐  │
│     Detail text...     │  │ HIGHLIGHT     │  │
│                        │  │ PANEL         │  │
│  2  Recommendation B   │  │               │  │
│     Detail text...     │  │ Key metric    │  │
│                        │  │ or quote      │  │
│  3  Recommendation C   │  │               │  │
│     Detail text...     │  └───────────────┘  │
│                        │                     │
├────────────────────────┴─────────────────────┤
│ Source | Page N/Total                         │
└──────────────────────────────────────────────┘
```

```python
eng.numbered_list_panel(title='战略建议',
    items=[('优先推进AI能力建设', '短期内集中资源打造AI核心竞争力'),
           ('建立数据治理体系', '统一数据标准，打通数据孤岛'),
           ('构建开放生态', '与合作伙伴共建行业解决方案')],
    panel=('战略目标', ['2026年AI渗透率达到60%', '数据资产价值提升3倍', '合作伙伴超过100家']),
    source='Source: ...')
```

---

#### #70 — Stacked Area Chart

**Use case**: Cumulative trends over time — market composition, revenue streams, resource allocation showing both individual and total trends.

```
┌──────────────────────────────────────────────┐
│ [Action Title — full width, NAVY bg]         │
├──────────────────────────────────────────────┤
│  Y ─                                         │
│     ████████████████████████████   Total      │
│     ████████████████████████  Series C        │
│     ██████████████████  Series B              │
│     ██████████  Series A                      │
│  0 ──────────────────────────────────        │
│     2020  2021  2022  2023  2024  2025       │
│  Takeaway text...                            │
├──────────────────────────────────────────────┤
│ Source | Page N/Total                         │
└──────────────────────────────────────────────┘
```

```python
eng.stacked_area(title='用户增长趋势',
    years=['2022', '2023', '2024', '2025', '2026E'],
    series_data=[('企业用户', [20, 35, 55, 80, 120], NAVY),
                 ('个人用户', [50, 80, 120, 160, 200], ACCENT_BLUE)],
    max_val=350, source='Source: ...')
```

---


---
