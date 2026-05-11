
## MckEngine API Reference

All 67 public methods on `MckEngine`. Every method creates exactly one slide (except `save()`).

### Initialization

```python
eng = MckEngine(total_slides=N)  # N = planned slide count (for page numbering)
```

### Save

```python
eng.save('output/deck.pptx')  # Auto-runs full_cleanup (p:style, shadow, 3D removal)
```

### Structure

**`eng.cover(title, subtitle='', author='', date='', cover_image=None)`**
> #1 Cover Slide — title, subtitle, author, date, accent line, optional AI-generated cover image.
> cover_image: `None` (no image, default), `'auto'` (AI-generated via Hunyuan 2.0), or `'path.png'` (custom image file).
> When `cover_image='auto'`: generates a McKinsey-style cover illustration automatically.
> Requires env vars: `TENCENT_SECRET_ID`, `TENCENT_SECRET_KEY`.

**`eng.toc(title='目录', items=None, source='')`**
> #6 Table of Contents — numbered items with descriptions.
> items: list of (num, title, description)

**`eng.section_divider(section_label, title, subtitle='')`**
> #5 Section Divider — navy left bar, large title.

**`eng.appendix_title(title, subtitle='')`**
> #7 Appendix Title — centered title with accent lines.

**`eng.closing(title, message='', source_text='')`**
> #36 Closing / Thank You slide.


### Data & Stats

**`eng.big_number(title, number, unit='', description='', detail_items=None, source='', bottom_bar=None)`**
> #8 Big Number — large stat with context.
> detail_items: list[str] bullet points shown below.
> bottom_bar: (label, text) or None.

**`eng.two_stat(title, stats, detail_items=None, source='')`**
> #9 Two-Stat Comparison — two big numbers side by side.
> stats: list of (number, label, is_navy:bool)

**`eng.three_stat(title, stats, detail_items=None, source='')`**
> #10 Three-Stat — three big numbers in a row.
> stats: list of 3 (number, label, is_navy:bool)

**`eng.data_table(title, headers, rows, col_widths=None, source='', bottom_bar=None)`**
> #11 Data Table — header row + data rows with separators.
> headers: list[str], rows: list[list[str]], col_widths: list[Inches] or auto.

**`eng.metric_cards(title, cards, source='')`**
> #12 Metric Cards — 3-4 accent-colored cards.
> cards: list of (letter, card_title, description, accent_color, light_bg)
> or (letter, card_title, description) — auto-colors from ACCENT_PAIRS.

**`eng.metric_comparison(title, metrics, source='')`**
> #62 Metric Comparison — before/after row cards with delta badges.
> metrics: list of (label, before_val, after_val, delta_str).


### Frameworks & Matrices

**`eng.matrix_2x2(title, quadrants, axis_labels=None, source='', bottom_bar=None)`**
> #13 2×2 Matrix — four quadrants.
> quadrants: list of 4 (label, bg_color, description).
> axis_labels: (x_label, y_label) or None.

**`eng.table_insight(title, headers, rows, insights, col_widths=None, insight_title='启示：', source='', bottom_bar=None)`**
> #71 Table+Insight — left data table + right insight panel with chevron icon.
> headers: list[str], rows: list[list[str]], insights: list[str].
> Supports **bold** markup in cell text. Replaces retired #14 Three-Pillar.

**`eng.pyramid(title, levels, source='', bottom_bar=None)`**
> #15 Pyramid — top-down widening layers.
> levels: list of (label, description, width_inches:float).

**`eng.process_chevron(title, steps, source='', bottom_bar=None)`**
> #16 Process Chevron — horizontal step flow with arrows.
> steps: list of (label, step_title, description).

**`eng.venn(title, circles, overlap_label='', right_text=None, source='')`**
> #17 Venn Diagram — overlapping rectangles for 2-3 sets.
> circles: list of (label, points:list[str], x, y, w, h) positioned rects.
> overlap_label: text for overlap zone.
> right_text: list[str] explanation on the right side.

**`eng.temple(title, roof_text, pillar_names, foundation_text, pillar_colors=None, source='')`**
> #18 Temple / House Framework — roof + pillars + foundation.
> pillar_names: list[str], pillar_colors: list[RGBColor] or auto.


### Comparison & Evaluation

**`eng.side_by_side(title, options, source='')`**
> #19 Side-by-Side Comparison — two columns with navy headers.
> options: list of 2 (option_title, points:list[str]).

**`eng.before_after(title, before_title, before_points, after_title, after_points, source='')`**
> #20 Before/After — gray (before) + navy (after) with arrow.

**`eng.pros_cons(title, pros_title, pros, cons_title, cons, conclusion=None, source='')`**
> #21 Pros/Cons — two-column layout.
> pros, cons: list[str].
> conclusion: (label, text) or None.

**`eng.rag_status(title, headers, rows, source='')`**
> #22 RAG Status — table with red/amber/green status dots.
> headers: list[str], rows: list of (name, status_color, *values, note).

**`eng.scorecard(title, items, source='')`**
> #23 Scorecard — items with progress bars.
> items: list of (name, score_str, pct_float_0_to_1)

**`eng.checklist(title, columns, col_widths, rows, status_map=None, source='', bottom_bar=None)`**
> #61 Checklist / Status table.
> columns: list[str] header labels.
> col_widths: list[Inches].
> rows: list of tuples — last element is status key.
> status_map: dict of status_key → (label, color, bg_color).

**`eng.swot(title, quadrants, source='')`**
> #65 SWOT Analysis — 2×2 colored grid.
> quadrants: list of 4 (label, accent_color, light_bg, points:list[str]).


### Narrative

**`eng.executive_summary(title, headline, items, source='')`**
> #24 Executive Summary — navy headline + numbered items.
> headline: str, items: list of (num, item_title, description).

**`eng.key_takeaway(title, left_text, takeaways, source='')`**
> #25 Key Takeaway — left analysis + right gray panel.
> left_text: list[str], takeaways: list[str].

**`eng.quote(quote_text, attribution='')`**
> #26 Quote Slide — centered quote with accent lines.

**`eng.two_column_text(title, columns, source='')`**
> #27 Two-Column Text — lettered columns with bullet lists.
> columns: list of 2 (letter, col_title, points:list[str]).

**`eng.four_column(title, items, source='')`**
> #28 Four-Column Overview — 4 vertical cards.
> items: list of (num, col_title, description:str_or_list).

**`eng.numbered_list_panel(title, items, panel=None, source='')`**
> #69 Numbered List + Side Panel — left numbered list + right accent panel.
> items: list of (item_title, description).
> panel: dict with 'subtitle','big_number','big_label','metrics':list[(label,value)].


### Timeline & Process

**`eng.timeline(title, milestones, source='', bottom_bar=None)`**
> #29 Timeline / Roadmap — horizontal line with milestone nodes.
> milestones: list of (label, description).

**`eng.vertical_steps(title, steps, source='', bottom_bar=None)`**
> #30 Vertical Steps — top-down numbered steps.
> steps: list of (num, step_title, description).

**`eng.cycle(title, phases, right_panel=None, source='')`**
> #31 Cycle Diagram — rectangular nodes with arrows in a loop.
> phases: list of (label, x_inches, y_inches) — positioned boxes.
> right_panel: (panel_title, points:list[str]) or None.

**`eng.funnel(title, stages, source='')`**
> #32 Funnel — top-down narrowing bars.
> stages: list of (name, count_label, pct_float).

**`eng.value_chain(title, stages, source='', bottom_bar=None)`**
> #67 Value Chain / Horizontal Flow — stages with arrows.
> stages: list of (stage_title, description, accent_color).
> Stages fill the full content width; height fills available vertical space.


### Team & Cases

**`eng.meet_the_team(title, members, source='')`**
> #33 Meet the Team — profile cards in a row.
> members: list of (name, role, bio:str_or_list).

**`eng.case_study(title, sections, result_box=None, source='')`**
> #34 Case Study — S/A/R or custom sections.
> sections: list of (letter, section_title, description).
> result_box: (label, text) or None.

**`eng.action_items(title, actions, source='')`**
> #35 Action Items — cards with timeline + owner.
> actions: list of (action_title, timeline, description, owner).

**`eng.case_study_image(title, sections, image_label, kpis=None, source='')`**
> #45 Case Study with Image — left text sections + right image + KPIs.
> sections: list of (label, text, accent_color).
> kpis: list of (value, label) or None.


### Charts (BLOCK_ARC)

**`eng.donut(title, segments, center_label='', center_sub='', legend_x=None, summary=None, source='')`**
> #48 Donut Chart — BLOCK_ARC ring segments.
> segments: list of (pct_float, color, label).

**`eng.pie(title, segments, legend_x=None, summary=None, source='')`**
> #64 Pie Chart — BLOCK_ARC with inner_ratio=0 (solid).
> segments: list of (pct_float, color, label, sub_label).

**`eng.gauge(title, score, benchmarks=None, source='')`**
> #55 Gauge — semicircle rainbow arc with center score.
> score: int 0-100.
> benchmarks: list of (label, value_str, color) shown below gauge.


### Charts (Bar/Line)

**`eng.grouped_bar(title, categories, series, data, max_val=None, y_ticks=None, summary=None, source='')`**
> #37 Grouped Bar Chart — vertical bars grouped by category.
> categories: list[str] x-labels. series: list of (name, color).
> data: list[list[int]] — data[cat_idx][series_idx].
> summary: (label, text) or None.

**`eng.stacked_bar(title, periods, series, data, summary=None, source='')`**
> #38 Stacked Bar Chart — 100% stacked vertical bars.
> periods: list[str] x-labels. series: list of (name, color).
> data: list[list[int]] — percentages, data[period_idx][series_idx].
> summary: (label, text) or None.

**`eng.horizontal_bar(title, items, summary=None, source='')`**
> #39 Horizontal Bar Chart — labeled bars with percentage.
> items: list of (name, pct_int_0_to_100, bar_color).
> summary: (label, text) or None.

**`eng.line_chart(title, x_labels, y_labels, values, legend_label='', summary=None, source='')`**
> #50 Line Chart — single line with dot approximation.
> x_labels: list[str], y_labels: list[str], values: list[float] 0.0-1.0 normalized.

**`eng.waterfall(title, items, max_val=None, legend_items=None, summary=None, source='')`**
> #49 Waterfall Chart — bridge from start to end.
> items: list of (label, value, type) — type: 'base'|'up'|'down'.

**`eng.pareto(title, items, max_val=None, summary=None, source='')`**
> #51 Pareto Chart — descending bars with value/pct labels.
> items: list of (label, value).

**`eng.stacked_area(title, years, series_data, max_val=None, summary=None, source='')`**
> #70 Stacked Area Chart — stacked columns for area approximation.
> years: list[str] x-labels.
> series_data: list of (name, values:list[int], color).


### Charts (Advanced)

**`eng.bubble(title, bubbles, x_label='', y_label='', legend_items=None, summary=None, source='')`**
> #53 Bubble / Scatter — positioned circles on XY plane.
> bubbles: list of (x_pct, y_pct, size_inches, label, color).

**`eng.kpi_tracker(title, kpis, summary=None, source='')`**
> #52 KPI Tracker — progress bars with status dots.
> kpis: list of (name, pct_float, detail, status_key).
> status_key: 'on'|'risk'|'off'.

**`eng.risk_matrix(title, grid_colors, grid_lights, risks, y_labels=None, x_labels=None, notes=None, source='')`**
> #54 Risk Matrix — 3×3 heatmap grid with risk labels.
> grid_colors: 3×3 list[list[RGBColor]] dot colors.
> grid_lights: 3×3 list[list[RGBColor]] cell backgrounds.
> risks: list of (row, col, name).
> notes: list[str] or None for bottom panel.

**`eng.harvey_ball_table(title, criteria, options, scores, legend_text=None, summary=None, source='')`**
> #56 Harvey Ball Table — matrix with Harvey Ball indicators.
> criteria: list[str] row labels. options: list[str] column headers.
> scores: list[list[int]] — scores[row][col], 0-4.


### Dashboards

**`eng.dashboard_kpi_chart(title, kpi_cards, chart_data=None, summary=None, source='')`**
> #57 Dashboard KPI + Chart — top KPI cards + bottom mini chart.
> kpi_cards: list of (value, label, detail, accent_color).
> chart_data: dict with 'labels','actual','target','max_val','legend'.

**`eng.dashboard_table_chart(title, table_data, chart_data=None, factoids=None, source='')`**
> #58 Dashboard Table + Chart — left table + right mini chart + bottom facts.
> table_data: dict with 'headers','col_widths','rows'.
> chart_data: dict with 'title','items':(name, value, max_val).
> factoids: list of (value, label, color).


### Image Layouts

**`eng.content_right_image(title, subtitle, bullets, takeaway='', image_label='Image', source='')`**
> #40 Content + Right Image.

**`eng.three_images(title, items, source='')`**
> #42 Three Images — three image+caption columns.
> items: list of (caption_title, description, image_label).

**`eng.image_four_points(title, image_label, points, source='')`**
> #43 Image + 4 Points — center image with 4 corner cards.
> points: list of 4 (point_title, description, accent_color).

**`eng.full_width_image(title, image_label, overlay_text='', attribution='', source='')`**
> #44 Full-Width Image — edge-to-edge image with text overlay.

**`eng.quote_bg_image(image_label, quote_text, attribution='', source='')`**
> #46 Quote with Background Image — image top + quote bottom.

**`eng.goals_illustration(title, goals, image_label, source='')`**
> #47 Goals with Illustration — left numbered goals + right image.
> goals: list of (goal_title, description, accent_color).

**`eng.two_col_image_grid(title, items, source='')`**
> #68 Two-Column Image + Text Grid — 2×2 image-text cards.
> items: list of (card_title, description, accent_color, image_label).


### Special

**`eng.icon_grid(title, items, cols=3, source='')`**
> #63 Icon Grid — grid of icon cards.
> items: list of (item_title, description, accent_color).

**`eng.stakeholder_map(title, quadrants, x_label='影响力 →', y_label='关注度 ↑', summary=None, source='')`**
> #59 Stakeholder Map — 2×2 quadrant with stakeholder lists.
> quadrants: list of 4 (label_cn, label_en, bg_color, members:list[str]).

**`eng.decision_tree(title, root, branches, right_panel=None, source='')`**
> #60 Decision Tree — root → L1 → L2 hierarchy with connector lines.
> root: (label,).
> branches: list of (L1_title, L1_metric, L1_color, children:list[(name, metric)]).
> right_panel: (panel_title, points:list[str]) or None.

**`eng.agenda(title, headers, items, footer_text='', source='')`**
> #66 Agenda — table-style meeting agenda.
> headers: list of (label, width).
> items: list of (*values, item_type) — type: 'key'|'normal'|'break'.

