
## Common Issues & Solutions

### Problem 1: PPT Won't Open / "File Needs Repair"

**Cause**: Shapes or connectors carry `<p:style>` with `effectRef idx="2"`, referencing theme effects (shadows/3D)

**Solution** (three-layer defense):
1. **Never use connectors** — use `add_hline()` (thin rectangle) instead of `add_connector()`
2. **Inline cleanup** — every `add_rect()` and `add_oval()` calls `_clean_shape()` to remove `p:style`
3. **Post-save cleanup** — `full_cleanup()` removes ALL `<p:style>` from every slide XML + theme effects

### Problem 2: Text Not Displaying Correctly in PowerPoint

**Cause**: Chinese characters rendered as English font instead of KaiTi

**Solution**:
- Use `set_ea_font(run, 'KaiTi')` in every paragraph with Chinese text
- Call it inside the loop that creates runs:
  ```python
  for run in p.runs:
      set_ea_font(run, 'KaiTi')
  ```

### Problem 3: Font Sizes Inconsistent Across Slides

**Cause**: Using custom sizes instead of defined hierarchy

**Solution**:
- Define constants:
  ```python
  TITLE_SIZE = Pt(22)
  BODY_SIZE = Pt(14)
  SUB_HEADER_SIZE = Pt(18)
  LABEL_SIZE = Pt(14)
  SMALL_SIZE = Pt(9)
  ```
- Use these constants everywhere
- Never use arbitrary sizes like `Pt(13)` or `Pt(15)`

### Problem 4: Columns/Lists Not Aligning Vertically

**Cause**: Mixing different line spacing or not accounting for text height

**Solution**:
- Use consistent `line_spacing=Pt(N)` in `add_text()` calls
- Calculate row heights in tables based on actual text size:
  - For 14pt text with spacing: use 1.0" height minimum
  - For lists with bullets: use 0.35" height per line + 8pt spacing
- Test by saving and opening in PowerPoint to verify alignment

### Problem 5: Chinese Multi-Line Text Overlapping (v1.5.0 Fix)

**Cause**: `add_text()` only set `space_before` (paragraph spacing) but did NOT set `p.line_spacing` (the actual line height / `<a:lnSpc>` in OOXML). When Chinese text wraps within a paragraph, lines overlap because PowerPoint has no explicit line height to follow.

**Solution** (fixed in v1.5.0, refined in v1.10.3):
- `add_text()` sets `p.line_spacing` for every paragraph with a **two-tier strategy**:
  - **Titles (font_size ≥ 18pt)**: `p.line_spacing = 0.93` — multiple spacing for tighter, more professional title rendering
  - **Body text (font_size < 18pt)**: `p.line_spacing = Pt(font_size.pt * 1.35)` — fixed Pt spacing to prevent CJK overlap
- Title multiple spacing (`0.93`) maps to `<a:lnSpc><a:spcPct val="93000"/>` in OOXML
- Body fixed spacing maps to `<a:lnSpc><a:spcPts>` in OOXML

### Problem 6: Content Overflowing Container Boxes (v1.9.0)

**Cause**: Text placed inside a colored rectangle (`add_rect`) with identical coordinates to the box itself, so text runs to the very edge and may visually overflow, especially with CJK characters that have wider natural widths.

**Solution**: Always inset text boxes by at least 0.15" on left/right within their container:
```python
# Box at (box_x, box_y, box_w, box_h)
add_rect(s, box_x, box_y, box_w, box_h, BG_GRAY)
# Text inset by 0.3" on each side
add_text(s, box_x + Inches(0.3), box_y, box_w - Inches(0.6), box_h, text, ...)
```
For tight spaces, reduce font_size by 1-2pt rather than reducing padding below 0.15".

### Problem 7: Chart Legend Colors Mismatch (v1.9.0)

**Cause**: Legend text uses Unicode "■" character in black, while actual chart bars/areas use NAVY/ACCENT_RED/ACCENT_GREEN — creating confusion about which color maps to which series.

**Solution**: Replace text-only legends with `add_rect()` color squares. See **Production Guard Rails Rule 4** for the standard pattern. Each legend item = colored square (0.15" × 0.15") + label text.

### Problem 8: Inconsistent Title Bar Styles (v1.9.0)

**Cause**: Mixing `add_navy_title_bar()` (navy background + white text) and `add_action_title()` (white background + black text + underline) on different slides within the same deck, creating visual inconsistency.

**Solution**: Use `add_action_title()` exclusively for all content slides. Remove `add_navy_title_bar()` usage. See **Production Guard Rails Rule 5**.

**Migration**: When converting `add_navy_title_bar()` → `add_action_title()`, adjust content start position from `Inches(1.0)` to `Inches(1.25)` since `add_action_title()` occupies slightly more vertical space.

### Problem 9: Axis Labels Off-Center in Matrix Charts (v1.9.0)

**Cause**: Y-axis label positioned at a fixed left offset, X-axis label at a fixed bottom offset — neither centered on the actual grid dimensions when grid position/size changes.

**Solution**: Calculate axis label positions from actual grid dimensions. See **Production Guard Rails Rule 6** for the centering formula.

### Problem 10: Bottom Whitespace Under Charts (v1.9.0)

**Cause**: Chart height calculated independently of the bottom summary bar position, leaving 0.5-1.0" of dead space between chart bottom and the summary bar.

**Solution**: Either extend chart height to fill the gap or move the bottom bar up. Target maximum 0.3" gap. See **Production Guard Rails Rule 3**.

### Problem 11: Cover Slide Title/Subtitle Overlap (v1.10.4)

**Cause**: Cover slide title textbox height is fixed (e.g. `Inches(1.0)`), but when the title contains `\n` (multi-line), two lines of 44pt text require ~1.66" of vertical space. The subtitle is positioned at a fixed `y` coordinate (e.g. `Inches(3.5)`), so the title overflows its textbox and visually overlaps the subtitle.

**Solution**: Calculate title height **dynamically** based on line count, then position subtitle/author/date relative to title bottom:

```python
# ✅ CORRECT: Dynamic title height on cover slides
lines = title.split('\n') if isinstance(title, str) else title
n_lines = len(lines) if isinstance(lines, list) else title.count('\n') + 1
title_h = Inches(0.8 + 0.65 * max(n_lines - 1, 0))  # ~0.65" per extra line

add_text(s, Inches(1), Inches(1.2), Inches(11), title_h,
         title, font_size=Pt(44), font_color=NAVY, bold=True, font_name='Georgia')

# Position subtitle BELOW the title dynamically
sub_y = Inches(1.2) + title_h + Inches(0.3)
if subtitle:
    add_text(s, Inches(1), sub_y, Inches(11), Inches(0.8),
             subtitle, font_size=Pt(24), font_color=DARK_GRAY)
    sub_y += Inches(1.0)
```

**Rule**: Never use fixed `y` coordinates for cover slide elements below the title. Always compute positions relative to title bottom.

### Problem 12: Action Title Text Not Flush Against Separator Line (v1.10.4)

**Cause**: `add_action_title()` uses `anchor=MSO_ANCHOR.MIDDLE` (vertical center alignment), so single-line titles float in the middle of the title bar, leaving a visible gap between the text baseline and the separator line at `Inches(1.05)`.

**Solution**: Change the text anchor from `MSO_ANCHOR.MIDDLE` to **`MSO_ANCHOR.BOTTOM`** so the text sits flush against the bottom of the textbox, right above the separator line:

```python
# ✅ CORRECT: Bottom-anchored action title — text sits flush against separator
def add_action_title(slide, text, title_size=Pt(22)):
    add_text(s, Inches(0.8), Inches(0.15), Inches(11.7), Inches(0.9), text,
             font_size=title_size, font_color=BLACK, bold=True, font_name='Georgia',
             anchor=MSO_ANCHOR.BOTTOM)  # ← BOTTOM, not MIDDLE
    add_hline(s, Inches(0.8), Inches(1.05), Inches(11.7), BLACK, Pt(0.5))
```

### Problem 13: Checklist Rows Overflowing Page Bottom (v1.10.4)

**Cause**: `#61 Checklist / Status` uses a fixed `row_h = Inches(0.55)` or `Inches(0.85)`. With 7+ rows, total height = `0.85 * 7 = 5.95"`, starting from `~Inches(1.45)` extends to `Inches(7.4)` — exceeding page height (7.5") and overlapping with source/page number areas.

**Solution**: Calculate `row_h` dynamically based on available vertical space, and switch to smaller font when rows are tight:

```python
# ✅ CORRECT: Dynamic row height for checklist
bottom_limit = BOTTOM_BAR_Y - Inches(0.1) if bottom_bar else SOURCE_Y - Inches(0.05)
available_h = bottom_limit - (header_y + Inches(0.5))
row_h = min(Inches(0.85), available_h / max(len(rows), 1))  # cap at 0.85" max

# Use smaller font when rows are tight
row_font = SMALL_SIZE if row_h < Inches(0.65) else BODY_SIZE
```

**Rule**: For any layout with a variable number of rows/items, ALWAYS compute item height dynamically: `item_h = min(MAX_ITEM_H, available_space / n_items)`. Never use a fixed height that assumes a specific item count.

### Problem 14: Value Chain Stages Not Filling Content Area (v1.10.4)

**Cause**: `#67 Value Chain` uses a fixed `stage_w = Inches(2.0)` and centers stages. With 4 stages, total width = `4*2.0 + 3*0.4 = 9.2"`, centered in `CW=11.73"` leaves ~1.27" empty on each side. Stage height is also fixed at `Inches(2.8)`, leaving ~3.3" of dead space below.

**Solution**: Calculate stage width and height dynamically to fill the entire content area:

```python
# ✅ CORRECT: Dynamic stage sizing — fills full content width and height
n = len(stages)
arrow_w = Inches(0.35)
stage_w = (CW - arrow_w * (n - 1)) / n  # fill entire content width
stage_y = CONTENT_TOP + Inches(0.1)
# Fill down to bottom_bar or source area
stage_h = (BOTTOM_BAR_Y - Inches(0.15) - stage_y) if bottom_bar else (SOURCE_Y - Inches(0.15) - stage_y)
```

**Rule**: For layouts with N equally-sized elements arranged horizontally, compute width as `(CW - gap * (N-1)) / N`, not a fixed `Inches(2.0)`. For vertical space, fill down to the bottom bar or source line.

### Problem 15: Closing Slide Bottom Line Too Short (v1.10.4)

**Cause**: The closing slide's bottom decorative line uses a fixed width like `Inches(3)`, which only spans a small portion of the slide — looking unfinished and asymmetric.

**Solution**: Use `CW` (content width) as the line width, and `LM` (left margin) as the starting x, so the line spans the full content area:

```python
# ❌ WRONG: Fixed short width
add_hline(s, Inches(1), Inches(6.8), Inches(3), NAVY, Pt(2))

# ✅ CORRECT: Full content width
add_hline(s, LM, Inches(6.8), CW, NAVY, Pt(2))
```

**Rule**: Decorative horizontal lines on structural slides (cover, closing) should span the full content width (`CW`), not arbitrary fixed widths.

### Problem 16: Donut/Pie Charts Made of Hundreds of Tiny Rect Blocks (v2.0)

**Cause**: Using nested loops with `math.cos/sin` + `add_rect()` to approximate circles/arcs creates 100-2800 shapes per chart. This inflates PPTX file size by 60-80%, causes generation timeouts (2+ minutes), and produces visible gaps and jagged edges.

**Solution**: Use `BLOCK_ARC` preset shapes with XML `adj` parameter control. Each segment = 1 shape:

```python
# ❌ WRONG: Hundreds of tiny blocks (slow, large file, jagged)
for deg in range(0, 360, 2):
    rad = math.radians(deg)
    for r in range(0, int(radius), int(block_sz)):
        bx = cx + int(r * math.cos(rad))
        add_rect(s, bx, by, block_sz, block_sz, color)  # → 2000+ shapes!

# ✅ CORRECT: One BLOCK_ARC per segment (fast, clean, 4 shapes total)
add_block_arc(s, cx - r, cy - r, r * 2, r * 2,
              start_deg, end_deg, inner_ratio, color)
```

See **Production Guard Rails Rule 9** for the complete `add_block_arc()` helper and usage patterns.

### Problem 17: Gauge Arc Renders Vertically Instead of Horizontally (v2.0)

**Cause**: Using math convention angles (0°=right, 90°=top, CCW) instead of PPT convention (0°=top, 90°=right, CW). A "horizontal rainbow" gauge using `math.radians(0)` to `math.radians(180)` renders as a **vertical** arc in PowerPoint because the coordinate systems are incompatible.

**Solution**: Use PPT's native clockwise-from-12-o'clock coordinate system directly:

```python
# PPT angle mapping for horizontal rainbow (opening upward ⌢):
#   Left  = 270° PPT
#   Top   = 0° (or 360°) PPT
#   Right = 90° PPT
# Total sweep: 270° → 0° → 90° = 180° clockwise

# ❌ WRONG: Math convention angles
ppt_angle = (90 - math_angle) % 360  # Fragile, error-prone conversion

# ✅ CORRECT: Think directly in PPT coordinates
ppt_cum = 270  # start at left
for pct, color in gauge_segs:
    sweep = pct * 180
    add_block_arc(s, ..., ppt_cum % 360, (ppt_cum + sweep) % 360, ...)
    ppt_cum += sweep
```

### Problem 18: Donut Center Text Unreadable Against Colored Ring (v2.0)

**Cause**: Center labels (e.g., "¥7,013亿", "总营收") use NAVY or MED_GRAY font color, which is invisible or low-contrast against the colored BLOCK_ARC ring segments behind them.

**Solution**: Use **WHITE** for center labels inside donut charts. The colored ring provides enough contrast:

```python
# ❌ WRONG: Navy text on navy/blue ring — invisible
add_text(s, ..., '¥7,013亿', font_color=NAVY, ...)

# ✅ CORRECT: White text, visible against any ring color
add_text(s, ..., '¥7,013亿', font_color=WHITE, bold=True,
         font_name='Georgia', ...)
add_text(s, ..., '总营收', font_color=WHITE, ...)
```

### Problem 19: Chart Elements Overlapping Title Bar — Body Content Too High (v2.0)

**Cause**: Chart area `chart_top` set to `Inches(1.0)` or `Inches(1.2)`, which places chart elements above the title separator line at `Inches(1.05)`. Applies to waterfall charts, line charts, bar charts, and other data visualization layouts.

**Solution**: All chart/content body areas must start at or below `Inches(1.3)`:

```python
# ❌ WRONG: Content starts above title separator
chart_top = Inches(1.0)   # overlaps title!

# ✅ CORRECT: Content respects title bar space
chart_top = Inches(1.3)   # safe start below title + separator + gap
```

**Rule**: Apply `Inches(1.3)` as minimum content start for ALL content slides (charts, tables, text blocks). The title bar occupies `Inches(0) → Inches(1.05)`, and `Inches(0.25)` gap is mandatory.

### Problem 20: Waterfall Chart Connector Lines Look Like Dots (v2.0)

**Cause**: Connector lines between waterfall bars are drawn using `add_hline()` with very short length (< 0.1"), making them appear as small dots instead of visible connection lines.

**Solution**: Ensure connector lines span the full gap between bars, and use consistent thin styling:

```python
# Between bar[i] and bar[i+1]:
connector_x = bx + bar_w  # start at right edge of current bar
connector_w = gap          # span the full gap to next bar
connector_y = running_top  # at the running total level
add_hline(s, connector_x, connector_y, connector_w, LINE_GRAY, Pt(0.75))
```

**Rule**: Waterfall connector lines must have `width >= gap_between_bars` and use `Pt(0.75)` line weight for visibility.

---

## Edge Cases

### Handling Large Presentations (20+ Slides)

- Break generation into batches of 5-8 slides, saving and verifying after each batch
- Always call `full_cleanup()` once at the end, not per-batch
- Memory: python-pptx holds the entire presentation in memory; for 50+ slides, monitor usage

### Font Availability

- **KaiTi / SimSun** may not be installed on non-Chinese systems — the presentation will render but fall back to a default CJK font
- **Georgia** is available on Windows/macOS by default; on Linux, install `ttf-mscorefonts-installer`
- If target audience uses macOS only, consider using `PingFang SC` as `ea_font` fallback

### Slide Dimensions

- All layouts assume **13.333" × 7.5"** (widescreen 16:9). Using 4:3 or custom sizes will break coordinate calculations
- If custom dimensions are required, scale all `Inches()` values proportionally

### PowerPoint vs LibreOffice

- Generated files are optimized for **Microsoft PowerPoint** (Windows/macOS)
- LibreOffice Impress may render fonts and spacing slightly differently
- `full_cleanup()` is still recommended for LibreOffice compatibility

---

## Best Practices

1. **Use MckEngine** — Never write raw `add_shape()` / coordinate code. Call `eng.xxx()` methods.
2. **One script, all slides** — Generate ALL planned slides in a single script run. Do not truncate.
3. **Set `total_slides` accurately** — This controls page number display (e.g., "Page 5/12").
4. **Use constants** — Import from `mck_ppt.constants`: `NAVY`, `ACCENT_BLUE`, `BG_GRAY`, `Inches`, etc.
5. **Layout diversity** — Each content slide MUST use a DIFFERENT layout from its neighbors.
6. **Chart priority** — When data has dates + values, use chart methods (`eng.grouped_bar`, `eng.donut`, etc.).
7. **Image priority** — For case studies / product showcases, use image layouts (`eng.content_right_image`, etc.).
8. **TOC completeness** — The TOC slide must list ALL content sections by number and title.
9. **`eng.save()` is sufficient** — It auto-runs `full_cleanup()`. No manual XML processing needed.

### Code Efficiency with MckEngine

MckEngine already handles constants, helpers, and cleanup internally. Your script only needs:

```python
import sys, os
sys.path.insert(0, os.path.expanduser('~/.workbuddy/skills/mck-ppt-design'))
from mck_ppt import MckEngine
from mck_ppt.constants import *
from pptx.util import Inches

eng = MckEngine(total_slides=N)
# ... eng.cover() / eng.toc() / eng.xxx() calls ...
eng.save('output/deck.pptx')
```

No need to define `add_text()`, `add_rect()`, `add_hline()`, `_clean_shape()`, `full_cleanup()` — they are all encapsulated in the engine.

---

## Dependencies

- **python-pptx** >= 0.6.21
- **lxml** — XML processing for theme cleanup
- Python 3.8+

```bash
pip install python-pptx lxml
```

---

## Example: Complete Minimal Presentation

```python
import sys, os
sys.path.insert(0, os.path.expanduser('~/.workbuddy/skills/mck-ppt-design'))
from mck_ppt import MckEngine
from mck_ppt.constants import *

eng = MckEngine(total_slides=5)
eng.cover(title='示例演示', subtitle='McKinsey Design Framework', date='2026')
eng.toc(items=[('1', '数据概览', '核心指标'), ('2', '分析', '趋势洞见')])
eng.big_number(title='核心发现', number='42%', description='年增长率',
    source='Source: 内部数据')
eng.table_insight(title='核心发现',
    headers=['维度', '现状', '目标'],
    rows=[['创新', '产品迭代中', 'AI赋能'],
          ['增长', '市场扩张中', '客户深耕'],
          ['效率', '流程优化中', '全面自动化']],
    insights=['创新驱动增长', '效率保障可持续'],
    source='Source: 战略部')
eng.closing(title='谢谢')
eng.save('output/demo.pptx')
```

---

## File References

```
~/.workbuddy/skills/mck-ppt-design/
├── SKILL.md                 # This file (design spec + API reference)
├── mck_ppt/
│   ├── __init__.py          # from mck_ppt import MckEngine
│   ├── engine.py            # 67 layout methods
│   ├── core.py              # Drawing primitives + XML cleanup
│   └── constants.py          # Colors, typography, grid constants
└── output/                  # Default output directory
```

---

## Channel Delivery (v1.10)

When users interact via a **messaging channel** (Feishu/飞书, Telegram, WhatsApp, Discord, Slack, etc.), the generated PPTX file **MUST** be sent back to the chat — not just saved to disk.

### Why This Matters

Users on mobile or messaging channels cannot access server file paths. Saving a file to `./output/` is invisible to them. The file must be delivered through the same channel the user is talking on.

### Delivery Method

After `prs.save(outpath)` and `full_cleanup(outpath)`, use the OpenClaw media pipeline to send the file:

```bash
openclaw message send --media <outpath> --message "✅ PPT generated — <N> slides, <size> bytes"
```

### Python Helper

```python
import subprocess, shutil

def deliver_to_channel(outpath, slide_count):
    """Send generated PPTX back to user's chat channel via OpenClaw media pipeline.
    Falls back gracefully if not running in a channel context."""
    if not shutil.which('openclaw'):
        print(f'[deliver] openclaw CLI not found, skipping channel delivery')
        print(f'[deliver] File saved locally: {outpath}')
        return False
    
    size_kb = os.path.getsize(outpath) / 1024
    caption = f'✅ PPT generated — {slide_count} slides, {size_kb:.0f} KB'
    
    try:
        result = subprocess.run(
            ['openclaw', 'message', 'send',
             '--media', outpath,
             '--message', caption],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            print(f'[deliver] Sent to channel: {outpath}')
            return True
        else:
            print(f'[deliver] Channel send failed: {result.stderr}')
            print(f'[deliver] File saved locally: {outpath}')
            return False
    except Exception as e:
        print(f'[deliver] Error: {e}')
        print(f'[deliver] File saved locally: {outpath}')
        return False
```

### Integration with Generation Flow

The complete post-generation sequence is:

```python
# 1. Save
prs.save(outpath)

# 2. Clean (mandatory)
full_cleanup(outpath)

# 3. Deliver to channel (if available)
slide_count = len(prs.slides)
deliver_to_channel(outpath, slide_count)

# 4. Confirm
print(f'Created: {outpath} ({os.path.getsize(outpath):,} bytes)')
```

### Rules

1. **Always attempt delivery** — after every successful generation, call `deliver_to_channel()`
2. **Graceful fallback** — if `openclaw` CLI is not available (e.g., running in IDE or CI), skip silently and print the local path
3. **Caption required** — always include slide count and file size so the user knows what they received
4. **No duplicate sends** — call `deliver_to_channel()` exactly once per generation
5. **File type** — `.pptx` is classified as "document" in OpenClaw's media pipeline (max 100MB), well within limits for any presentation

### Channel-Specific Notes

| Channel | File Support | Max Size | Notes |
|---------|-------------|----------|-------|
| Feishu/飞书 | ✅ Document | 100MB | Renders as downloadable file card |
| Telegram | ✅ Document | 100MB | Shows as file attachment |
| WhatsApp | ✅ Document | 100MB | Delivered as document message |
| Discord | ✅ Attachment | 100MB | Appears in chat as file |
| Slack | ✅ File | 100MB | Shared as file snippet |
| Signal | ✅ Attachment | 100MB | Sent as generic attachment |
| Others | ✅ Document | 100MB | All OpenClaw channels support document type |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.3.0 | 2026-03-27 | **Guard Rail Rule 10 — Horizontal Item Overflow Protection**: Fixed `process_chevron()` negative-gap crash when N≥5 steps (step_w×N > CW → negative arrow width → PowerPoint "file needs repair"). Now computes `step_w` dynamically: `min(PREFERRED, (CW - MIN_GAP*(N-1))/N)`. Adaptive font sizing (sub-header→body→small) when boxes shrink. Arrow width floor at 0.2". Documented as Rule 10 in Production Guard Rails with root-cause analysis, validation formula, and affected-methods list. Updated Process Chevron spec: 2–7 steps supported (was 3–5). |
| 2.2.0 | 2026-03-22 | **AI Cover Image Generation**: New `mck_ppt/cover_image.py` module. `eng.cover()` gains `cover_image` parameter (`None`/`'auto'`/`'path.png'`). When `'auto'`: Tencent Hunyuan 2.0 async API (`SubmitHunyuanImageJob`) generates 1024×1024 product photo → `rembg` professional background removal → cool grey-blue tint (desat 30%, R×0.85/G×0.92/B×1.18) + 50% lighten → subject placed at right-center of 1920×1080 transparent canvas → 24 McKinsey-style cubic Bézier ribbon curves with silk-fold twist at center → full-bleed RGBA PNG embedded as bottom layer. `_METAPHOR_MAP` maps 24 industry keywords to realistic product descriptions (GPU, capsules, bank card, solar panel, etc.). Prompt enforces: real product photography, sharp edges, white background, studio lighting. `__init__.py` exports `generate_cover_image`. Dependencies: `tencentcloud-sdk-python`, `rembg`, `pillow`, `numpy`. |
| 2.0.5 | 2026-03-21 | **#15 Staircase Evolution v3**: PNG icon support (auto-detect `.png` paths, overlay on navy circle with 0.08" inset). Single-line detail_rows = no bullet; multi-line = bullet. Icon library (6 icons in `assets/icons/`). New example: `staircase_civilization.py`. Unified release: merged v2.0.4 engine + v2.1 SKILL.md rewrite + #14→#71 cleanup. |
| 2.0.4 | 2026-03-19 | **#14 Three-Pillar RETIRED**: Removed `three_pillar` method from engine.py and its documentation from SKILL.md. All former #14 use cases now served by **#71 Table+Insight Panel** (`table_insight`). Updated Layout Diversity table, Opening Slide Priority Rule, and recommended slide structure. |
| 2.0.3 | 2026-03-19 | **3 Template Updates — Category M: Editorial Narrative**: (1) **#20 Before/After rewrite** (v2.0.1) — replaced BG_GRAY+NAVY color blocks with clean white-bg + black vertical divider + black circle `>` arrow + structured data rows (dict: label/brand/val/extra) + formula cards (dict: title/desc/cases with underline), new params: `corner_label`, `bottom_bar`, `left_summary`, `right_summary`, `right_summary_color`; (2) **#71 Table+Insight Panel** (NEW) — left data table (~60%) + middle CHEVRON shape icon (0.7") + right gray-bg (#F2F2F2) insight panel (~32%) with "启示：" title + `•` bullet points, supports `**bold**` markup in cells, self-adaptive row height; (3) **#72 Multi-Bar Panel Chart** (NEW) — 2-3 side-by-side bar panels with auto-numbered titles, CAGR trend arrows following actual bar-top slopes (RIGHT_ARROW shape, ~1.5px shaft, ±0.27" offset), per-bar value labels, green/red CAGR coloring. **OPENING SLIDE PRIORITY RULE** added: Slides 2-5 strongly prefer #71, #8, #14, #25. New Category M in layout-catalog.md. Total patterns: **72**. |
| 2.0.2 | 2026-03-19 | **Adaptive Row Height**: `data_table` / `vertical_steps` dynamically calculate row_h to prevent overflow. Font shrinks to Pt(10) for compact rows. |
| 2.0.1 | 2026-03-19 | **Before/After Rewrite**: White editorial layout with structured data rows (label/brand/val/extra), formula cards, left/right summaries. Fixed `set_ea_font` import in core.py. |
| 2.0.0 | 2026-03-19 | **BLOCK_ARC Chart Engine**: Donut (#48), Pie (#64), and Gauge (#55) charts rewritten from hundreds of `add_rect()` blocks to native BLOCK_ARC shapes — 3-4 shapes per chart instead of 100-2800. File size reduced 60-80%. New `add_block_arc()` helper function with PPT coordinate system documentation. **Guard Rail Rule 9**: mandatory BLOCK_ARC for all circular charts. **5 new Common Issues** (Problems 16-20): rect-block charts, vertical gauge, unreadable donut center text, body content above title bar, waterfall connector dots. Donut center labels changed to WHITE for contrast. Gauge uses correct PPT angle mapping (270°→0°→90° for horizontal rainbow). |
| 1.10.4 | 2026-03-19 | **5 New Bug Fixes + Guard Rail Rule 8**: (1) Cover slide title/subtitle overlap — dynamic title height from line count; (2) Action title anchor changed to `MSO_ANCHOR.BOTTOM` for flush separator alignment; (3) Checklist `#61` dynamic `row_h` prevents page overflow with 7+ rows; (4) Value Chain `#67` dynamic `stage_w` and `stage_h` fill content area instead of fixed 2.0" width; (5) Closing `#36` bottom line changed from `Inches(3)` to `CW` for full-width. New **Production Guard Rails Rule 8**: dynamic sizing for variable-count layouts. **5 new Common Issues** (Problems 11-15). Updated code examples for #1, #36, #61, #67. |
| 1.10.3 | 2026-03-18 | **Title Line Spacing Optimization**: Titles (≥18pt) now use `0.93` multiple spacing instead of fixed `Pt(fs*1.35)`, producing tighter, more professional title rendering. Body text (<18pt) retains fixed Pt spacing. Updated Problem 5 documentation. Thanks to **冯梓航 Denzel** for detailed feedback. |
| 1.10.2 | 2026-03-18 | **#54 Matrix Side Panel Variant**: Added compact grid + side panel layout variant for Pattern #54 (Risk/Heat Matrix). When matrix needs a companion insight panel, `cell_w` shrinks from 3.0" to 2.15" and `axis_label_w` from 1.8" to 0.65", yielding ~4.2" panel width. Includes layout math, ASCII wireframe, code example, and minimum-width rule. |
| 1.10.1 | 2026-03-18 | **Frontmatter Fix**: Fixed "malformed YAML frontmatter" error on Claude install. Removed unsupported fields (`license`, `version`, `metadata` with emoji, etc.) — Claude only supports `name` + `description`. Used YAML folded block scalar (`>-`) for description. Metadata relocated to document body. |
| 1.10.0 | 2026-03-18 | **Channel Delivery**: New `deliver_to_channel()` helper sends generated PPTX back to user's chat via `openclaw message send --media`. Supports Feishu/飞书, Telegram, WhatsApp, Discord, Slack, Signal and all OpenClaw channels. Graceful fallback when not in channel context. Updated example scripts. |
| 1.9.0 | 2026-03-15 | **Production Guard Rails**: 7 mandatory rules derived from real-world feedback — spacing/overflow protection, legend color consistency, title style uniformity (`add_action_title()` only), axis label centering, image placeholder page requirement, bottom whitespace elimination, content overflow detection. **Code Efficiency Guidelines**: variable reuse, helper function patterns, short abbreviation table, batch data structures, auto page numbering. **5 new Common Issues** (Problems 6-10). |
| 1.8.0 | 2026-03-15 | **Massive layout expansion**: 39 → **70 patterns** across 8 → **12 categories**. Added Category I (Image+Content, #40-#47), Category J (Advanced Data Viz, #48-#56), Category K (Dashboards, #57-#58), Category L (Visual Storytelling, #59-#70). New `add_image_placeholder()` helper. Image Priority Rule added. Layout Diversity table expanded. Based on McKinsey PowerPoint Template 2023 analysis. |
| 1.7.0 | 2026-03-13 | **Category H: Data Charts**: Added 3 new chart layout patterns (#37 Grouped Bar, #38 Stacked Bar, #39 Horizontal Bar) using pure `add_rect()` drawing. Added Chart Priority Rule to Layout Diversity table — when data contains dates + values/percentages, chart patterns are mandatory. Total patterns: 39. |
| 1.6.0 | 2026-03-08 | **Cross-model quality alignment**: Added Accent Color System (4 accent + 4 light BG colors), Presentation Planning section (structure templates, layout diversity rules, content density requirements, mandatory slide elements, page number helper). Based on comparative analysis across Opus/Minimax/Hunyuan/GLM5 outputs. |
| 1.5.0 | 2026-03-08 | **Critical fix**: `add_text()` now sets `p.line_spacing = Pt(font_size.pt * 1.35)` to prevent Chinese multi-line text overlap. Added Problem 5 to Common Issues. |
| 1.3.0 | 2026-03-04 | ClawHub release: optimized description for discoverability, added metadata/homepage, added Edge Cases & Error Handling sections |
| 1.2.0 | 2026-03-04 | Fixed circle shape number font inconsistency; `add_oval()` now sets `font_name='Arial'` + `set_ea_font()` for consistent typography |
| | | - Circle numbers simplified: use `1, 2, 3` instead of `01, 02, 03` |
| | | - Removed product-specific references from skill description |
| 1.1.0 | 2026-03-03 | **Breaking**: Replaced connector-based lines with rectangle-based `add_hline()` |
| | | - `add_line()` deprecated, use `add_hline()` instead |
| | | - `add_circle_label()` renamed to `add_oval()` with bg/fg params |
| | | - `add_rect()` now auto-removes `p:style` via `_clean_shape()` |
| | | - `cleanup_theme()` upgraded to `full_cleanup()` (sanitizes all slide XML) |
| | | - Three-layer defense against file corruption |
| | | - `add_text()` bullet param removed; use `'\u2022 '` prefix in text |
| 1.0.0 | 2026-03-02 | Initial complete specification, all refinements documented |
| | | - Color palette finalized (NAVY primary) |
| | | - Typography hierarchy locked (22pt title, 14pt body) |
| | | - Line treatment standardized (no shadows) |
| | | - Theme cleanup process documented |
| | | - All helper functions optimized |
