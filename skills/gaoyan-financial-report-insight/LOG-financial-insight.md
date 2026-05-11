---
skill: gaoyan-financial-report-insight
updated: 2026-04-21
---

# 高岩财报解读 Skill — 交接与交付记录

## 2026-04-21｜霸王茶姬（CHAGEE）2025FY 样例打包

**目的**：独立项目交付路径与文件清单固化到 skill，便于下一轮对话直接复用目录结构与命名。

### 独立交付根目录

`Gaoyan Projects/高岩财报解读/`

### 本次产出清单

| 相对路径 | 类型 | 说明 |
|----------|------|------|
| `霸王茶姬-2025FY-财报解读-demo.md` | MD | 完整版（Executive Summary、数据卡、结构拆解、策略、口径声明） |
| `霸王茶姬-2025FY-客户汇报版.md` | MD | 客户汇报版（1页决策摘要 + 三图） |
| `chagee-2025-financial-flow.png` | PNG | 财务流向 Sankey（高岩色：收入蓝/费用灰/利润蓝绿） |
| `chagee-2025-kpi-yoy.png` | PNG | 收入、营业利润、净利润 2024FY vs 2025FY 柱图 |
| `chagee-2025-store-mix.png` | PNG | 加盟/直营门店结构堆叠对比 |

### 一手来源

- SEC Filing Index：`https://www.sec.gov/Archives/edgar/data/2013649/000110465926037353/0001104659-26-037353-index.htm`
- Exhibit 99.1：Press release + unaudited condensed consolidated statements（2025FY 数据以该附件为准）

### 复用约定（下一轮 Agent）

1. 新公司/新期间：在 `Gaoyan Projects/高岩财报解读/` 下按 `{公司}-{期间}-财报解读-demo.md` 与 `{公司}-{期间}-客户汇报版.md` 复制骨架。
2. 图表与 MD **同目录**，避免跨目录断链。
3. 执行前必读 `reference.md`（GMV vs Revenue、直营/加盟、GAAP/Non-GAAP）。
4. 风格对齐可参考 `examples.md`；本批 CHAGEE 文件为**已跑通的真实样例**。

### 已知限制（可选后续）

- SEC 直连下载偶发需 User-Agent；抓取失败时用 WebFetch 读 index + exhibit 或浏览器层兜底。
- Logo 若从官网裁切，需去导航深色底，避免黑框（见客户汇报版迭代过程）。
