# /crosstab-survey - 高岩食客调研交叉表自动化

## 触发

用户说"跑交叉表"、"生成交叉表"、"交叉表交付物"或 `/crosstab-survey` 时触发。

## 做什么

给定一份调研问卷数据（SPSS `.sav`）和当期官方参考交付物，自动生成标准 Excel 交叉表交付物（24 sheets，目标匹配率 ≥ 99.5%，Q4 已达 100%）。

---

## 执行流程

### Step 1：准备材料

确认以下文件存在于当期项目目录（如 `2025Q4/`）：

| 文件 | 说明 |
|------|------|
| `2-食客追踪项目数据Q{N}-完成.sav` | 完成样本 SPSS 数据 |
| `2-食客追踪项目数据Q{N}-甄别.sav` | 甄别样本 SPSS 数据 |
| `3-食客调研项目Q{N}最终交付答案参考表.xlsx` | **当期官方参考**（结构模板 + 验证基准）|
| `1-食客追踪项目数据Q{N}-datamap.xlsx` | 变量字典（辅助参考） |

> ⚠️ **关键**：必须使用**当期**官方参考作为结构模板，不能用上一期。每期问卷可能有新增选项（如 Q4 新增"京东"），用旧期结构会导致行偏移。

### Step 2：检查问卷变更

> ⚠️ **强制要求**：必须**逐字阅读**当期问卷模板（参考表 sheet 结构）和变量映射表（datamap），与上期对比，逐项确认每一题、每一选项、每一标签是否有变化。发现差异后必须相应调整引擎代码，不能跳过或凭记忆推断。

逐字检查清单：
- **选项增减**：每道题的 VL 值标签，是否有新增/删除的 code → 更新 `build_row_fn()` 的 VL 映射
- **题目增减**：是否有新增/删除的整道题 → 注册或移除对应 table 配置
- **标签文本变更**：选项文字有无修改（影响行匹配逻辑）
- **题目顺序变更**：是否有题目顺序调整（影响行偏移）
- **新增筛选条件**：是否有新的 s5f / base filter 逻辑
- **Banner 结构变更**：列数、列顺序、分组是否有变化

Q4 已知变更：A4 外卖平台新增"京东"（code=11）。

### Step 3：运行引擎

```bash
cd "C:\Users\杨顺\Documents\Obsidian Vault\_tmp"
python crosstab_q4_v3.py   # 生成 output_q4_v3.xlsx（Q4最终版，100%）
```

新季度时，复制上期引擎为 `crosstab_q{N}_v1.py`，修改顶部路径配置，然后逐步调试。

### Step 4：验证

```python
python verify_v2.py   # 逐 sheet 匹配率 + 总体
```

**目标**：总体 ≥ 99.5%，每个 sheet ≥ 99%

如有 mismatch，按下方「已知问题」排查。

### Step 5：输出

```bash
cp output_q4_v3.xlsx "Gaoyan Projects/食客调研项目/2025Q4/3-食客调研项目Q4交叉表交付.xlsx"
```

---

## 数据源映射（关键）

| Sheet 类型 | 数据源 | 说明 |
|-----------|--------|------|
| 甄别_count/% | **当期甄别.sav + 当期完成.sav** 合并 | base = 甄别(N-1) + 完成(N) ≈ 6825 |
| 甄别-成功_count/% | 当期完成.sav | base = 3400 |
| 甄别-渠道_count/% | 当期甄别.sav + 当期完成.sav 合并 | 同甄别 |
| 堂食和外卖/堂食/外卖 | 当期完成.sav | base = 3400 |
| 渠道系列 | 当期完成.sav | base group 需 per-meal 计算 |
| 人群画像 | 当期完成.sav | |
| 额外-堂食 | 当期完成.sav | Total = occasions 合计；基数列 = respondent-level |

---

## 已知问题与修复方案（Q4 经验教训）

### 问题1：甄别 sheet 基数错误
- **现象**：甄别 base 应为 6825，但输出 3425
- **根因**：甄别 = 当期甄别.sav + 当期完成.sav（不是跨季度合并）
- **修复**：`df_screen_combined = pd.concat([df_q4s, df_q4], ignore_index=True)`

### 问题2：渠道 sheets 基数组全为 3400
- **现象**：渠道 sheet 基数组 cols 3-7 全部输出 3400，应为 per-meal 人数
- **根因**：`process_sheet_channel` 基数组未按餐次过滤
- **修复**：基数组 col3-7 = `(df[S5_{meal}].isin(s5f)).sum()`
  - 堂食和外卖：早=890, 午=2730, 下午茶=1129, 晚=1410, 夜宵=794

### 问题3：行结构偏移（新增选项）
- **现象**：A4 之后所有行错位 1 行，匹配率骤降
- **根因**：用 Q3 ref 作为结构模板，但 Q4 新增了"京东"行
- **修复**：**始终用当期官方参考作为结构模板**

### 问题4：D2 重复标签"单身"
- **现象**：row48 单身=370（正确），row49 单身=425（错误，应=370）
- **根因**：同标签连续出现时，第二行是 NET 行，值与第一行相同
- **修复**：检测连续重复标签，第二次出现时复制上一行值

### 问题5：额外-堂食 Total 列语义
- **现象**：Total 列输出 3400（unique respondents），应为 3765
- **根因**：Total = 各场景 occasions 之和（2452+429+494+26+364=3765）
- **修复**：Total 列 = sum(per-scenario values)；'-' 单元格输出 '-' 不输出 0

### 问题6：S7 Mean 中位点映射
- **现象**：Mean=17.49，应为 16.85
- **根因**：频率量表中位点映射错误
- **修复**：`{1:30, 2:20, 3:10, 4:4, 5:2.5, 6:1}`（排除 code 7"其他"）

### 问题7：甄别 sheet 中老年人基数错误（Q4新增）
- **现象**：中老年人 base=186（应=630）
- **根因**：甄别数据（df_combined = df_scr + df）中，df_scr 没有 D2 字段，导致 `D2.isin([4,5]) & AGE>=45` 只能匹配 df 中的人
- **修复**：甄别专用 SG_screen，中老年人定义 = `AGE>=45`（不加 D2 过滤）

### 问题8：额外-堂食 基数列 respondent vs occasion 混用（Q4新增）
- **现象**：基数行基数列输出 4296（应=3400），数据行基数列异常重复
- **根因**：基数列（a1code=None）被计算成了 meal-occasion-level（多餐次叠加）
- **修复**：基数列统一改为 respondent-level = `len(df_data)`

---

## 核心引擎架构

**当前版本**：`_tmp/crosstab_q4_v3.py`（Q4最终版，OVERALL **100.0%**）

**设计原则**：
1. 用**当期官方参考**作为结构模板（行/列/标签全部从 ref 读取）
2. 只重新计算数值单元格，非数值内容原样复制
3. 配置驱动，零条件分支执行循环

**关键函数**：
- `build_row_fn(label, title)` — 根据行标签返回计算函数
- `meal_filter(df, mi, s5f)` — 按餐次和 S5 过滤
- `get_special_base_filter(title, s5f)` — 特殊 base（火锅/优惠券/饮品）
- `process_sheet_channel()` — 渠道 Banner（70 品类 × 6 餐次）
- `process_sheet_portrait()` — 人群画像（70 品类 × 60 小表）
- `process_sheet_extra()` — 额外-堂食（A1 场景 × 品类）

**fn 属性系统**：
- `_is_loop_single` / `_is_loop_multi` — 单/多选循环题
- `_is_multi_code_single` / `_is_multi_code_multi` — 多 code NET
- `_is_satisfaction` — 满意度题（含 Mean 特殊公式）
- `_is_per_meal_base` — 特殊 base filter（per-meal 过滤）

**关键规则**（从 Q3 继承）：
1. NET 标签匹配必须先于 VL 个体标签
2. 堂食/外卖 sheet 的 Total col 必须走 S5-aware 路径
3. 特殊 base table 子群组列必须 per-meal 过滤
4. satisfaction Mean = sum(所有餐次评分) / unique_respondents，round(2)

**SG（人群分组）关键规则**：
- 普通 SG（完成.sav）：中老年人 = `D2.isin([4,5]) & AGE>=45`
- SG_screen（甄别+完成合并）：中老年人 = `AGE>=45`（不加 D2 过滤，因 df_scr 无 D2 字段）

---

## 24 Sheets 结构

| # | Sheet 类型 | Banner | 数据源 |
|---|-----------|--------|--------|
| 1 | SYT | 封面 | 复制 ref |
| 2 | Index | 目录 | 复制 ref，替换 Q3→Q4 |
| 3-4 | 甄别_count/% | 28人口学×6餐 (169列) | 甄别+完成合并 |
| 5-6 | 甄别-成功_count/% | 同上 | 完成.sav |
| 7-8 | 甄别-渠道_count/% | 70品类×6餐 (421列) | 甄别+完成合并 |
| 9-10 | 堂食和外卖_count/% | 28人口学×6餐 | 完成.sav |
| 11-12 | 堂食和外卖-渠道_count/% | 70品类×6餐 | 完成.sav |
| 13-14 | 堂食_count/% | 28人口学×6餐 | 完成.sav, s5f={3} |
| 15-16 | 堂食-渠道_count/% | 70品类×6餐 | 完成.sav, s5f={3} |
| 17-18 | 外卖_count/% | 28人口学×6餐 | 完成.sav, s5f={2} |
| 19-20 | 外卖-渠道_count/% | 70品类×6餐 | 完成.sav, s5f={2} |
| 21-22 | 人群画像_count/% | 70品类 (71列) | 完成.sav |
| 23-24 | 额外-堂食_count/% | A1场景 (11列) | 完成.sav, s5f={3} |

---

## 新季度接入指南（Q2/Q3/Q5 等）

1. 复制 `crosstab_q4_v3.py` 为 `crosstab_q{N}_v1.py`
2. 修改顶部路径：`q4dir` → `q{N}dir`，文件名中 Q4 → Q{N}
3. 运行 `python crosstab_q{N}_v1.py`，看报错和 verify 结果
4. 核查问卷变更（新增/删除选项/题目）
5. 逐步修复 mismatch，参考「已知问题」列表
6. 验证达到 ≥99.5% 后输出交付文件

> 💡 **Q2 注意**：可能没有"甄别.sav"，需确认数据结构；也可能 S5 编码不同（堂食/外卖分组逻辑需核查）

---

## 参考文件

| 文件 | 说明 |
|------|------|
| `_tmp/crosstab_q4_v3.py` | **当前最终引擎**（Q4版，100%） |
| `_tmp/verify_v2.py` | 验证脚本 |
| `Gaoyan Projects/食客调研项目/交叉表自动化-经验教训.md` | Q3/Q4 开发经验教训 |
| `Gaoyan Projects/食客调研项目/2025Q4/` | Q4 项目目录 |
