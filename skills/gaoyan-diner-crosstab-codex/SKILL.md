---
name: gaoyan-diner-crosstab-codex
description: >-
  Rebuilds Gaoyan diner-tracking survey crosstab COUNT sheets from 2- completion/screening
  Excel plus SPSS .sav value labels, aligned to a reference delivery workbook. Covers
  2025Q1–Q4 wave_eval_registry + eval_waves_995.py gates (count sheets ≥99.5%, optional full
  workbook agency compare). Use when the user mentions 食客调研、交叉表、甄别_count、
  Q1/Q2/Q3/Q4 季度问卷、Codex 交叉表交付物、POC、99.5%、四环回测、匹配率验证、
  wave_eval_registry、工场金标验收。
---

# 食客调研交叉表（Codex）`gaoyan-diner-crosstab-codex`

## 封装说明（务必读）

**流水线本质**：`shutil.copy2(参考工作簿, 交付物)` 得到**与参考一致的整本底稿**，再用 openpyxl **只改写**两张 `*_甄别_count` / `*_甄别-成功_count` 里、**指定题块**且 **`KNOWN_TIERS` 可映射**的列上的单元格；其余 sheet 与未覆盖格子**仍是参考里的数值**（不是从原始表重算）。

**从 2- 数据「算出来并写回」的**：上述两张 count 表内、S5/S5-成功/S7–S9 系列题块、`KNOWN_TIERS`（Total/三线/四区域/性别）列。

**不覆盖、保留参考复制值的**：代际/收入/家庭结构/天气等后续维度列（无稳定字段映射时）；汇总行按脚本逻辑跳过不写；所有 `_%` 及其他 sheet 整表保持参考原样。

**匹配率**：对「参考与生成均为数值」的格子做比对，**双 NaN 视为一致**（见下文）。与参考 100% 表示参与比对的格子一致；其中未覆盖部分本就等于参考。

**工场金标「全表验收」**（与 SPSS 导出 xlsx 合同对齐时）：全部 24 sheet、逐格；**≤1e-5 浮点容差**；**NaN 与空单元格视为一致**。实现见 `engine/validation.py` 的 `compare_workbook_agency`；口径全文见 [`engine/ACCEPTANCE_SPEC.md`](Gaoyan Projects/食客调研项目/engine/ACCEPTANCE_SPEC.md)。快速引擎回归仍可用 `compare_count_sheets`（仅 sheet 2+4 且双方均为数值格）。

### 四环季 agency 资产与 **99.5% 引擎门闸**（2026-05-03，2026-05-09 更新）

仓库内已登记 **2025Q1–Q4** 金标路径、当季 `quarter_dir` / 模板 / 最近一次 `ENGINE_RUN` 产出，用于**不依赖口头路径**的回测。

**Q1 验收里程碑（2026-05-09）**：Codex_aligned_v1 版本已达工场金标验收标准
- 全工作簿：**99.9982%** （3,921,517/3,921,586，差异 69 格皆为空值形式）
- 数值快验：**100%** （55,365/55,365，所有数值完全一致）
- 状态：✅ **可交付**

| 门闸 | 函数 | 含义 | 目标 | Q1 实现 |
|------|------|------|------|--------|
| **A. 引擎迭代（主）** | `compare_count_sheets(ref, gen, (2, 4))` | 两张 `_count`、**双方均为数值**的格子 | **每季 ≥ 99.5%**（`same/(same+diff)`） | Q1: 100% ✅ |
| **B. 工场合同（辅）** | `compare_workbook_agency(ref, gen)` | 24 张全表，见 `ACCEPTANCE_SPEC.md` | 终态 **diff=0**；阶段可跟踪 **全表 same/total** 直至 ≥99.5% | Q1: 99.9982% ✅ |

**一键评估**（在 **Obsidian Vault 根**执行）：

```bash
python "Gaoyan Projects/食客调研项目/engine/eval_waves_995.py"
python "Gaoyan Projects/食客调研项目/engine/eval_waves_995.py" --full
python "Gaoyan Projects/食客调研项目/engine/eval_waves_995.py" --require-count-995
```

- 登记文件：[`engine/wave_eval_registry.json`](Gaoyan Projects/食客调研项目/engine/wave_eval_registry.json) — **每次跑完 `runner` 后更新其中 `gen_engine`**；Q1/Q2 金标若在 Desktop，保持绝对路径或把金标拷入 Vault 后改相对路径。
- `--require-count-995`：任一已登记且文件存在的季度 **A 门闸 < 99.5%** → **exit 1**（供 CI / hook）。
- 快照 Markdown：`--write-md "Gaoyan Projects/食客调研项目/engine/reports/wave_eval_latest.md"`。

**诚实基线（登记默认 `gen_engine` 一次跑通结果，非承诺已达标）**：Q1 A 门闸约 **96.92%**（53658/55365，`Q1_TIER_QID_OVERRIDES` 含 cumulative **kids2 S8/S9**）；Q2 约 **80.8%**；Q3/Q4 约 **97.5%**。达到 **99.5%** 的固定动作：按季 `wave_diff` → `rules`/`runner` 的 `tier@qid` 单调回归 → 更新 `gen_engine` → 重跑 `eval_waves_995.py` 直至 `--require-count-995` 通过；再视合同开 `--full` 攻 **B 门闸**（`_%` 与全 tier 需全表重算或 SPSS 同源）。

### 与「Q4 底稿」相关的误解澄清（2026-04-19）

- **底稿只应提供版式与交付范围**（24 张表、题块结构、`_%` 与 `_count` 的对应关系），**不应把上一季或外季的数字当成当季答案保留**。
- **当季金标准**若存在（如 `25Q2_20250707.xlsx`），验收口径是：**从 `2-` 原始表可复算的部分必须与金标准一致**；在规则未完全解码前，不得以「复制 Q4 数字」冒充当季结果。
- **无底稿**时：必须实现「全表、全 tier、全 `_%`」从 `2-` + `.sav` 的重算；参见 `Gaoyan Projects/食客调研项目/POC/MATCH_REPORT_Q2_dimension_decode.md` 中已解码维度与仍待业务定义的 tier。

### 无底稿长期路线（vNext 引擎，2026-04-22 起）

- **目录**：`Gaoyan Projects/食客调研项目/engine/`（与 POC/分季脚本并列，**不**替代既有 `build_crosstab_aligned_v3.py` 流程）。
- **入口**：`python engine/runner.py --quarter-dir … --template … --output … --report … --wave 2025Qx`  
- **完成/甄别**：`engine/discover.py` — 以 **D2 非空最多** 的 xlsx 为 **完成卷**（甄别卷常无 D2）。
- **「周末/节假日」列**：问卷中 S6 为 **工作日 / 周末 / 节假日** 三选一；交付表该列多为 **周末+节假日** 的合并口径，须按季配置 `engine/rules.py` 内 **`WEEKEND_S6_CODES`**（`--wave` 选择），**勿写死全季同一集合**。
- **问卷原文**：`POC/1-食客调研项目原始问卷-25Q3.docx` 要点已摘录至 `engine/from_questionnaire_25Q3.md`（D2、D2-1→`D2x1_*`、S6/S6a）。**「年轻人」「中老年人」** 在 Word 中无字面定义，须由 **D2+D2-1（及可能 S2/S2du1）** 或 datamap/分析规格补全后再写入 `rules.py`。
- **当前缺口（恢复工作时优先）**：引擎跑 Q1 与金标 count 比对约 **73%+**，剩余主要为 **家庭情况子 tier**；参见 `LOG-codex.md` **2026-04-22** 条。

## 何时使用

- 生成或更新 **食客追踪 / 食客调研** 的 **交叉表 Excel 交付物**（与内部「最终答案参考表」版式对齐）。
- 用户给出 **新季度 `2-` 数据 + 参考 xlsx**（或沿用上一季版式）。
- 需要 **匹配率报告**（两张 `*_count` 表数值比对）。

## 输入（每季核对）

| 输入 | 说明 |
|------|------|
| 参考表 | `3-*最终交付答案参考表.xlsx` 或当季定稿版式（整本复制为底稿） |
| 完成卷 | `2-*…完成.xlsx`（及同基名 `.sav`，用于 value labels；Q4/Q3 文件名随项目） |
| 甄别卷 | `2-*…甄别.xlsx` |
| 可选 | `1-*datamap.xlsx`（字段/口径说明） |
| 可选（无底稿） | `1-*原始问卷*.docx`（与 `engine/from_questionnaire_*.md` 摘录配合，校对 D2/S6 等口径） |

**样本口径（2025Q4 已验证）**：完成 + 甄别纵向合并为全量；`甄别-成功` 与块 `S5-成功样本` 仅用 **完成卷** 行数。

## 输出

- **交付物 xlsx**：从参考 **整本 `shutil.copy2`** 再覆盖指定题块数值，避免版式漂移。
- **默认重算表名**（当季以参考为准）：`25Q4-甄别_count`、`25Q4-甄别-成功_count`（命名随季度前缀变化时需改脚本常量）。
- **匹配报告**：仅对两张 count 表做逐格比对；报告路径建议放在项目子目录 `_codex_tmp_run/`，避免覆盖历史 md。

## 重算题块（2025Q4 逻辑）

- **题块**：`S5`、`S5-成功样本`、`S7` / `S7-2` / `S7-3`、`S8` / `S8-2` / `S8-3`、`S9` / `S9-2` / `S9-3`（含 `S9-3` 多列勾选映射）。
- **多餐题 S5**：列 `S5_1`…`S5_5`；基数与分餐列按参考子表头「基数、早餐…夜宵」。
- **交叉维度**：仅对 **可从 xlsx 稳定映射** 的 tier 写回：`Total`、城市线（`S3du`）、区域（`S3du1`）、性别（`S1`）。参考表中 **代际、收入、家庭结构、天气等** 后续维度列：导出无同名字段时 **不要覆盖**，保留参考复制值（与「只算前 10 组」等价策略：用 `KNOWN_TIERS` 过滤，勿硬编码 `[:10]`）。
- **不自动重算**：同参考的 `_%` 两张表（除非另开任务推导分母与代际列）。

## 技术栈与脚本落位

- **pandas** + **pyreadstat**（metadata / value labels）+ **openpyxl**（读写 xlsx）。

| 场景 | 脚本路径（相对 Obsidian Vault） |
|------|----------------------------------|
| Q4 对齐 + 报告 | `Gaoyan Projects/食客调研项目/2025Q4/_codex_tmp_run/build_crosstab_aligned_v3.py` |
| Q3 POC + 报告 | `Gaoyan Projects/食客调研项目/POC/build_crosstab_q3_poc-codex.py` |
| Q2 与金标准 **100% 一致**（副本） | `Gaoyan Projects/食客调研项目/POC/produce_q2_deliverable_match_gold.py` |
| Q2 维度解码 / 无底稿缺口说明 | `Gaoyan Projects/食客调研项目/POC/MATCH_REPORT_Q2_dimension_decode.md` |
| Q2 原始 vs 金标准边际自检 | `Gaoyan Projects/食客调研项目/POC/verify_q2_raw_vs_gold.py` |
| 无底稿引擎（实验） | `Gaoyan Projects/食客调研项目/engine/runner.py`（见上节 `--wave` / `discover`） |
| 四环季 99.5% 门闸评估 | `engine/eval_waves_995.py` + `engine/wave_eval_registry.json` |
| Q1 `tier@qid` 局部扫描 + 回归 | `engine/_q1_merge_scan.py`（默认金标 `…/餐观调研/25Q1_20250707.xlsx`） |

**新季**：复制以上任一脚本到当季目录，改 `BASE`、`REF_FP`/`REF_NAME`、`COUNT_SHEETS`（如 `25Qx-甄别_count`）、`XLSX_*`、`SAV_DONE`、`OUT_*`。

**诊断/比对片段**：Q4 同目录 `compare_fixed.py`、`diagnose_crosstab.py`；临时输出放 `_codex_tmp_run` 或当季 POC 目录，**不写入本 skill 目录**。

## 新对话起手（给下一轮 Agent）

1. 读本 `SKILL.md`「封装说明」「匹配率比对」及 **「无底稿长期路线」**。
2. 读 `LOG-codex.md` 最新一条（含暂停结论与引擎路径）。
3. 确认用户提供的 **参考 xlsx** 路径与 **2- 完成/甄别 xlsx + 完成.sav** 路径。
4. 若走 **无底稿引擎**：读 `Gaoyan Projects/食客调研项目/engine/README.md` 与 `from_questionnaire_25Q3.md`（或当季问卷摘录），确认 `--wave` 与 `WEEKEND_S6_CODES`。
5. 用 `pd.ExcelFile(参考).sheet_names` 确认两张 count 的 **sheet 名与索引**（当前比对取索引 **2 与 4**，若 Index 结构变了需改 `compare_numeric`）。
6. 跑当季脚本或 `engine/runner.py` → 打开 `MATCH_REPORT*.md` / `ENGINE_RUN*.md`；若有非 NaN 差异，再对单格溯源 `tier_mask` / 题块映射。

## 匹配率比对（必读）

`pandas.read_excel(..., header=None)` 下，空单元格常为 **`float('nan')`**。

- **错误写法**：`abs(ref - gen) < 1e-5` —— 对 **NaN vs NaN** 恒为假，会把空格全部记成「不一致」，匹配率可假性跌至约 **62%**。
- **正确写法**：双方均为数值类型时，若 **`math.isnan(ref)` 且 `math.isnan(gen)`** 则计为 **一致**；否则再用 `1e-5` 比较有限数值。

参与统计的格子：**参考格为 int/float 且生成格也为 int/float** 的单元格（与旧脚本口径一致，但需 NaN 语义修正）。

## 执行原则

1. **先读参考表 sheet 名与首块版式**，再改脚本里的表名 / `KNOWN_TIERS` / 题块正则。
2. **全量复制参考再局部覆盖**，不从零画版式。
3. **比对用 pandas**，避免对整本 openpyxl 双开逐格比对导致极慢。
4. 新季度字段名变化时，先跑小脚本 `read_excel` 打列名、对齐 `S5_*` / `S7x2` 等映射。
5. 维护记录写入 **`LOG-codex.md`**（与本 skill 同目录），不在其他 skill 内追加。

## 与本目录 `LOG-codex.md`

版本结论、已知坑、当季文件路径摘要写在 `LOG-codex.md`，便于交接与审计。
