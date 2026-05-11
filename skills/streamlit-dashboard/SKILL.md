---
name: streamlit-dashboard
description: Use when given a data file (Excel/CSV) and asked to visualize, analyze, or create an interactive dashboard. Generates a Streamlit + Plotly dashboard with auto-detected filters, KPI cards, and charts, then launches it locally.
---

# Streamlit Dashboard

## Overview

Given any Excel or CSV file, auto-detect column types → generate a full Streamlit + Plotly dashboard → launch at localhost:8501.

No Tableau license needed. Interactive hover/filter/zoom out of the box.

## When to Use

- User provides a data file and asks for "visualization", "dashboard", "Tableau-like", "interactive charts"
- User wants to explore data with filters
- Output needs to be shareable as a local web app

## Core Pattern

### Step 1 — Auto-detect structure

```python
import pandas as pd
df = pd.read_excel("file.xlsx")  # or read_csv

# Classify columns
categorical = [c for c in df.columns if df[c].dtype == 'object' and df[c].nunique() < 50]
numeric = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
date_cols = [c for c in df.columns if 'date' in c.lower() or pd.api.types.is_datetime64_any_dtype(df[c])]
```

### Step 2 — Dashboard template

```python
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="数据分析", layout="wide")

@st.cache_data
def load():
    df = pd.read_excel(r"PATH")
    # parse dates, fill nulls
    return df

df = load()

# ── Sidebar filters (auto from categorical cols) ──────────────
with st.sidebar:
    st.title("筛选器")
    filters = {}
    for col in categorical[:5]:  # max 5 filters
        opts = ['全部'] + sorted(df[col].dropna().unique().tolist())
        sel = st.selectbox(col, opts)
        filters[col] = sel

fdf = df.copy()
for col, val in filters.items():
    if val != '全部':
        fdf = fdf[fdf[col] == val]

# ── KPI row ───────────────────────────────────────────────────
cols = st.columns(len(numeric[:5]))
for i, col in enumerate(numeric[:5]):
    cols[i].metric(col, f"{fdf[col].sum():,.0f}")

st.markdown("---")

# ── Charts ────────────────────────────────────────────────────
if categorical and numeric:
    top_col = st.columns(2)
    agg = fdf.groupby(categorical[0])[numeric[0]].sum().sort_values(ascending=True).tail(10)
    top_col[0].plotly_chart(
        px.bar(agg.reset_index(), x=numeric[0], y=categorical[0],
               orientation='h', title=f"{categorical[0]} × {numeric[0]}"),
        use_container_width=True
    )
    if len(categorical) > 1:
        pie_data = fdf.groupby(categorical[1])[numeric[0]].sum().reset_index()
        top_col[1].plotly_chart(
            px.pie(pie_data, values=numeric[0], names=categorical[1],
                   hole=0.4, title=f"{categorical[1]} 占比"),
            use_container_width=True
        )
```

### Step 3 — Launch

```bash
STREAMLIT="C:/Users/杨顺/AppData/Roaming/Python/Python314/Scripts/streamlit.exe"
"$STREAMLIT" run dashboard.py --server.port 8501 --server.headless true &
sleep 4 && echo "Open: http://localhost:8501"
```

## Chart Type Selection

| 数据特征 | 推荐图表 | Plotly函数 |
|----------|----------|------------|
| 排名/TOP N | 横向条形图 | `px.bar(orientation='h')` |
| 占比/结构 | 环形饼图 | `px.pie(hole=0.4)` |
| 时间趋势 | 折线图 | `px.line` |
| 两个分类交叉 | 热力图 | `px.imshow` |
| 分布/漏斗 | 漏斗图 | `px.funnel` |
| 月度对比 | 分组柱状图 | `px.bar(barmode='group')` |
| 散点关系 | 散点图 | `px.scatter` |

## 高岩餐饮数据专属维度

常用筛选字段：`城市等级` `连锁规模标签` `客单价标签` `菜系标签` `category`

常用分析轴：`采购金额` `采购数量` `采购单价` by `sku_brand` / `category_1` / `city`

## 文件存放

- Dashboard 脚本：vault 根目录 `dashboard.py`
- 清洗后数据：`酒水饮料_cleaned.xlsx`（已含衍生标签）

## 依赖安装

```bash
pip install streamlit plotly pandas openpyxl
```

## 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| 中文乱码 | 字体缺失 | `import matplotlib; fm.findSystemFonts()` 找 simhei |
| Port in use | 端口占用 | 换 `--server.port 8502` |
| 数据太慢 | 未用 cache | 加 `@st.cache_data` |
| 图表空白 | 筛选后数据为空 | 加 `if len(fdf) == 0: st.warning(...)` |
