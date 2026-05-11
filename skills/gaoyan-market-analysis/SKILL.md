---
name: gaoyan-market-analysis
description: >-
  高岩科技餐饮市场分析 Skill。基于麦肯锡 Market Analysis Toolkit 方法论，
  结合高岩自有数据（门店、菜品、EGPM），为客户生成完整的市场分析报告。
  输入品类+市场+菜系，输出结构化 MD 报告 + 高岩品牌 PPT。
  适用场景：7.x 定制化咨询、3.x 销售支持、1.x 行业洞察。
  只要用户提到品类分析、市场调研、竞品研究、餐饮赛道、品牌对比、市场规模、
  消费趋势，即使没有明确说"报告"，也应触发此 skill。
---

# Gaoyan Market Analysis Skill

> **Version**: 1.0.0 · **Author**: 高岩科技
>
> **Required tools**: Skill(web-access), Read, Write, Bash, Skill(gaoyan-ppt-design)
>
> **方法论来源**: McKinsey/BCG/Bain Market Analysis Toolkit (310p)
> **参考文件**: `高岩知识库/咨询方法论/麦肯锡_Market_Analysis_Toolkit_入库笔记.md`

## When to Use This Skill

1. 客户需要**某个品类/市场/菜系的市场分析报告**
2. 内部需要做**品类进入/退出决策**的数据支撑
3. **提案准备**时需要市场背景分析
4. 任何"帮我分析一下 XX 市场"的请求

## 触发方式

```
/gaoyan-market-analysis 复合调味料 川菜赛道
/gaoyan-market-analysis 预制菜 华东市场
/gaoyan-market-analysis 咖啡 下沉市场 2026
"帮我做一个烘焙品类的市场分析"
"XX客户想了解火锅底料市场"
```

## 输入参数解析

从用户输入中提取以下参数（缺失的用合理默认值）：

| 参数 | 说明 | 默认值 | 示例 |
|------|------|--------|------|
| `category` | 品类/产品 | （必须） | 复合调味料、预制菜、咖啡 |
| `market` | 市场/区域 | 中国大陆 | 华东、东南亚、下沉市场 |
| `cuisine` | 菜系/渠道 | 全渠道 | 川菜、火锅、茶饮 |
| `client` | 客户名称 | （可选） | 某调味品品牌 |
| `year` | 分析年份 | 当前年份 | 2026 |
| `depth` | 分析深度 | standard | quick(5页) / standard(15页) / deep(30页) |

## 执行流程

**全程无需用户确认，每步完成立即进入下一步。**

---

### Phase 1: 问题定义与假设（5分钟）

#### Step 1.1: 构建分析框架

基于输入参数，自动生成：

1. **核心问题**（Main Question）：`{category}在{cuisine}/{market}的市场机会有多大？`
2. **3个子假设**（Hypotheses to Test）：
   - H1: 市场规模与增长 — `{category}市场是否仍在增长？增速如何？`
   - H2: 竞争格局 — `{category}的竞争格局是什么？有无空白机会？`
   - H3: 趋势与机会 — `{cuisine}对{category}的需求趋势是什么？`

#### Step 1.2: 确定数据源矩阵

| 数据维度 | 高岩自有数据 | 外部搜索 |
|----------|-------------|----------|
| 市场规模 | 餐观鹰眼门店数据 | web-access 行业报告 |
| 品类趋势 | 餐观星探菜品数据 | web-access 趋势文章 |
| 竞争格局 | EGPM品牌数据 | web-access 品牌动态 |
| 消费洞察 | 餐观客研数据 | web-access 消费者调研 |
| 渠道结构 | 门店数据库 | web-access 渠道报告 |

---

### Phase 2: 数据采集（10分钟）

#### Step 2.1: 搜索外部数据

**必须先加载 `/web-access` skill，所有联网操作通过 web-access 执行。**

依次执行以下搜索查询（每组提取 3-5 条关键数据点，记录来源）：

```
搜索组1: "{category} 市场规模 数据 {year}"
搜索组2: "{category} {cuisine} 趋势 发展"
搜索组3: "{category} 品牌 竞争格局 市场份额"
搜索组4: "{category} {market} 渠道 餐饮"
搜索组5: "{category} 消费者 需求 洞察 {year}"
搜索组6: "{cuisine} 门店数量 增长 {year}"  （如指定了菜系）
```

**质量门**：每组搜索至少获得 2 条有效数据点（含具体数字），否则换关键词重搜。搜索无果时通过 web-access 的 CDP 模式直接访问一手来源（行业协会、官方统计）。

#### Step 2.2: 查询高岩知识库

在 vault 中搜索相关已有数据：

```
vault搜索1: "{category}" — 找已有报告和数据
vault搜索2: "{cuisine}" — 找菜系相关分析
vault搜索3: "{client}" — 找客户历史项目（如有）
```

#### Step 2.3: 数据汇总

将所有数据点整理为结构化表格，作为后续分析的输入。每条数据标注来源和可信度（高/中/低）。

---

### Phase 3: 分析与综合（15分钟）

#### Step 3.1: 定量分析模块

**市场规模模型**（Market Sizing）：

```
TAM (Total Addressable Market)
  └→ {category} 在中国/目标市场的总规模
SAM (Serviceable Available Market)
  └→ {category} 在 {cuisine}/{market} 的可服务市场
SOM (Serviceable Obtainable Market)
  └→ 客户可触达的市场份额
```

**增长趋势分析**：
- 历史增速（过去3-5年CAGR）
- 预测增速（未来3年）
- 增长驱动因素

**市场结构分析**：
- 按品类细分的市场份额
- 按渠道的分布（餐饮/零售/电商）
- 按区域的分布

#### Step 3.2: 定性分析模块

**趋势分析**（3-5个关键趋势）：
- 消费端趋势（口味偏好、健康意识、便捷化）
- 供给端趋势（品牌集中度、供应链变革、技术创新）
- 渠道趋势（外卖渗透、社区团购、即时零售）

**竞争格局分析**：
- 主要玩家识别（TOP5-10 品牌）
- 竞争定位矩阵（2x2：市场份额 vs 增长率）
- 差异化策略对比

#### Step 3.3: 高岩独有分析

**EGPM 视角**（如有数据）：
- 品类生命周期阶段判断（导入期/成长期/成熟期/衰退期）
- 品味趋势预测（上升/平稳/下降）

**餐饮渠道视角**：
- 渠道渗透率（该品类在餐饮渠道的占比）
- 菜系关联度（该品类在目标菜系中的使用频率）
- 门店密度与分布

---

### Phase 4: 报告生成

#### Step 4.1: 生成结构化 MD 报告

输出路径：`高岩知识库/高岩Agent+Skill/outputs/{category}_{market}_市场分析_{YYYYMMDD}.md`

**报告结构**（遵循麦肯锡 Pyramid Principle）：

```markdown
---
title: "{category}{market}市场分析报告"
tags: [市场分析, {category}, {cuisine}, {market}, 高岩科技, Gaoyan-market-analysis]
summary: "..."
links: [...]
report_type: "市场分析"
client: "{client}"
date_processed: {YYYY-MM-DD}
skill_version: "gaoyan-market-analysis-v1.0"
---

# {category}{market}市场分析报告

> 核心发现摘要（3句话）

## 1. Executive Summary
- 关键结论1（粗体）+ 支撑数据
- 关键结论2（粗体）+ 支撑数据
- 关键结论3（粗体）+ 支撑数据
- 建议行动

## 2. 市场规模与增长
### 2.1 市场总览
- TAM/SAM/SOM 分析
- 市场规模数据 + 来源
### 2.2 增长趋势
- 历史增速 + 预测
- 增长驱动因素

## 3. 市场结构
### 3.1 品类细分
### 3.2 渠道结构
### 3.3 区域分布

## 4. 竞争格局
### 4.1 主要玩家
### 4.2 竞争定位
### 4.3 差异化分析

## 5. 趋势与洞察
### 5.1 消费端趋势
### 5.2 供给端趋势
### 5.3 渠道趋势

## 6. 餐饮渠道深度分析
### 6.1 {cuisine}赛道概览（如指定菜系）
### 6.2 品类在餐饮渠道的渗透
### 6.3 EGPM生命周期判断（如有数据）

## 7. 高岩观点与建议
### 7.1 机会点
### 7.2 风险提示
### 7.3 建议行动（分短期/中期/长期）

## 8. 方法论与数据源
- 数据来源清单
- 分析方法说明
- 局限性说明

## Related
- 关联知识库页面
```

#### Step 4.2: 质量检查

逐项检查：
- [ ] Executive Summary 能否独立阅读并做决策？
- [ ] 每个章节标题是否为 Action Title（结论式标题）？
- [ ] 关键数据是否标注来源？
- [ ] 是否有高岩独有洞察（不是纯公开数据堆砌）？
- [ ] 建议是否具体可执行？

不合格项回到对应步骤重做。

#### Step 4.3b: 验证报告（必须执行，在写入文件后立即运行）

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
        "字数 > 1000": word_count > 1000,
        "含 Executive Summary": "Executive Summary" in content,
        "含高岩观点章节": "高岩观点" in content,
    }
except FileNotFoundError:
    checks = {k: False for k in ["文件存在", "frontmatter 完整（5字段）", "字数 > 1000", "含 Executive Summary", "含高岩观点章节"]}

print("\n── 报告验证报告 ──")
all_pass = True
for k, v in checks.items():
    icon = "✅" if v else "❌"
    print(f"{icon} {k}")
    if not v:
        all_pass = False
if all_pass:
    print("\n✅ 全部通过，报告生成完成。")
else:
    print("\n⚠️  存在未通过项，需要补充后重新验证。")
```

#### Step 4.3: 生成 PPT（可选）

如果用户需要 PPT 输出，调用 `/gaoyan-ppt-design`：

```
将 MD 报告转换为高岩品牌 PPT，结构如下：
- 封面（报告标题 + 客户名 + 日期）
- 目录
- Executive Summary（1-2页 key_insight）
- 市场规模（big_number + 柱状图/折线图数据页）
- 竞争格局（对比表 + 定位矩阵）
- 趋势分析（3-4个趋势的 key_insight 页）
- 餐饮渠道（数据页 + donut 图）
- 高岩观点（key_insight）
- 方法论（简要）
- 结尾页
```

---

## 输出物清单

| 输出物 | 格式 | 路径 |
|--------|------|------|
| 市场分析报告 | MD | `高岩知识库/高岩Agent+Skill/outputs/` |
| 品牌PPT（可选） | PPTX | `~/Desktop/` |

## 高岩行业知识注入

以下是高岩在餐饮分析中常用的行业分类体系，分析时优先采用：

### 餐饮渠道分类
- 正餐（中式正餐、西式正餐）
- 快餐小吃（中式快餐、西式快餐、小吃）
- 火锅（川渝火锅、粤式火锅、其他）
- 茶饮咖啡（新茶饮、咖啡、传统茶馆）
- 烘焙甜品
- 日料/韩餐/东南亚菜
- 烧烤/串串
- 团餐/食堂

### 供应链品类分类
- 调味品（基础调味料、复合调味料、酱料）
- 食用油脂
- 预制菜/半成品
- 冷冻食品
- 乳制品
- 肉禽蛋
- 水产品
- 粮油面粉
- 蔬菜/果蔬

### 竞争状态标签（高岩体系）
- 人无我有 → 独有优势，强化壁垒
- 人有我优 → 差异化优势，持续迭代
- 人有我有 → 同质竞争，找切入点
- 人无我无 → 空白市场，评估 ROI
- 人有我无 → 劣势，考虑合作
- 人比我优 → 明显劣势，避免正面竞争

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-04-18 | 初版，基于麦肯锡 Market Analysis Toolkit 方法论 |
