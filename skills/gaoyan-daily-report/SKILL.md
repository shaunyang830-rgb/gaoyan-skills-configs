---
name: gaoyan-daily-report
triggers:
  - 餐饮日报
description: 生成高岩科技餐饮日报（双轨采集：WebSearch全网 + CDP垂类媒体 → Markdown → 信息图）
---

# 高岩科技餐饮日报生成 Skill

你是高岩科技的餐饮行业分析师。执行以下步骤生成今日餐饮日报，**日期变量 {YYYY-MM-DD} 替换为今天实际日期**。

---

## ⚡ 执行原则（必须遵守）

- **全程无需用户确认**：每步完成后立即执行下一步，不要停下来等用户
- **Step 1A + Step 1B 并行执行**：WebSearch 和 CDP 同时启动，互不等待
- **Step 1B 必须同步阻塞执行**（`run_in_background: false`，timeout: 120000）
- **任何步骤失败立即报错并说明原因**，不要沉默等待

---

## Step 1: 新闻采集（双轨架构）

### 架构说明

```
轨道A（WebSearch）: 全网搜索 → 发现热点事件、突发新闻、跨平台舆情
轨道B（CDP）:       定向爬取20个垂类媒体 → 深度行业内容、官方数据
         ↓                    ↓
         └──────── 合并 ───────┘
                    ↓
           v2 评分 + 去重 → 精选10条
```

### Step 1A: WebSearch 轨道（先执行，写入文件供 1B 读取）

加载 `/web-access` skill，然后对以下查询组逐一执行 WebSearch，将结果合并写入 `websearch-results.json`：

**搜索查询组**（按优先级执行，每组取前5条相关结果）：

| 优先级 | 查询词 | tag |
|--------|--------|-----|
| P1 | `餐饮 新闻 今日` | 下游 |
| P1 | `连锁餐饮 最新动态` | 下游 |
| P1 | `餐饮品牌 融资 上市 {YYYY}` | 资本 |
| P2 | `茶饮 咖啡 奶茶 新闻` | 茶饮咖啡 |
| P2 | `预制菜 供应链 食材 最新` | 中游 |
| P2 | `餐饮 食品安全 政策 法规` | 政策 |
| P2 | `社会消费品零售 餐饮收入` | 政策 |
| P2 | `海底捞 瑞幸 蜜雪冰城 喜茶 最新` | 下游 |
| P3 | `麦当劳 肯德基 星巴克 中国 新闻` | 下游 |
| P3 | `餐饮行业 报告 数据 {YYYY}` | 趋势 |

**结果写入格式**（`websearch-results.json`）：
```json
[
  {
    "title": "新闻标题（≤50字）",
    "tag": "下游",
    "summary": "摘要或标题",
    "source": "来源媒体名",
    "url": "https://...",
    "date": "{YYYY-MM-DD}",
    "verified": false,
    "eventKey": ""
  }
]
```

**过滤规则**：排除非餐饮内容（汽车/芯片/房地产等），只保留含餐饮直接关键词的结果。

**执行完成后，立即执行以下验证**（必须执行，不可跳过）：

```bash
# 验证 1：文件是否存在
if [ ! -f websearch-results.json ]; then
  echo "❌ 错误：websearch-results.json 不存在，重新执行 WebSearch"
  exit 1
fi

# 验证 2：JSON 是否有效
if ! jq . websearch-results.json > /dev/null 2>&1; then
  echo "❌ 错误：websearch-results.json 不是有效的 JSON，检查格式"
  exit 1
fi

# 验证 3：是否至少有 5 条结果
count=$(jq 'length' websearch-results.json)
if [ "$count" -lt 5 ]; then
  echo "⚠️ 警告：只有 $count 条结果（期望 ≥5），将在 Step 1B 中补充"
fi

# 验证 4：每条是否包含必需字段
missing=$(jq '.[] | select(.title == null or .url == null or .tag == null)' websearch-results.json | wc -l)
if [ "$missing" -gt 0 ]; then
  echo "❌ 错误：有 $missing 条记录缺少必需字段（title/url/tag），修复后重试"
  exit 1
fi

echo "✅ Step 1A 验证通过：$count 条 WebSearch 结果已写入 websearch-results.json"
```

**如果验证失败**：
- 文件不存在 → 检查 WebSearch 是否执行成功，重新执行
- JSON 无效 → 检查 WebSearch 输出格式，修复 JSON
- 结果 < 5 条 → 继续执行 Step 1B，CDP 会补充
- 缺少字段 → 补充缺失字段后重试

---

### Step 1B: CDP 轨道（同步执行，读取 1A 结果合并）

```bash
# 前置检查
if [ ! -f websearch-results.json ]; then
  echo "❌ 错误：Step 1A 未完成，websearch-results.json 不存在"
  exit 1
fi

# 执行 CDP 采集
cd "C:/Users/杨顺/Documents/Obsidian Vault/01 Projects/餐饮日报/assets"
node fetch-news.js {YYYY-MM-DD} > news-{YYYY-MM-DD}.json 2>log-{YYYY-MM-DD}.txt

# 验证脚本执行
if [ $? -ne 0 ]; then
  echo "❌ 错误：fetch-news.js 执行失败，检查日志："
  cat log-{YYYY-MM-DD}.txt
  exit 1
fi

# 验证输出文件
if [ ! -f news-{YYYY-MM-DD}.json ]; then
  echo "❌ 错误：news-{YYYY-MM-DD}.json 未生成"
  exit 1
fi

# 验证 JSON 有效性
if ! jq . news-{YYYY-MM-DD}.json > /dev/null 2>&1; then
  echo "❌ 错误：news-{YYYY-MM-DD}.json 不是有效的 JSON"
  exit 1
fi

# 验证结果数量
count=$(jq 'length' news-{YYYY-MM-DD}.json)
if [ "$count" -lt 5 ]; then
  echo "⚠️ 警告：只有 $count 条结果（期望 ≥5），执行 WebSearch 补充采集"
  # 执行补充采集逻辑
fi

echo "✅ Step 1B 验证通过：$count 条精选新闻已生成"
```

**如果验证失败**：
- 脚本执行失败 → 检查 `log-{YYYY-MM-DD}.txt` 中的错误信息，修复后重试
- 输出文件不存在 → 检查路径是否正确，重新执行脚本
- JSON 无效 → 检查脚本输出，修复格式
- 结果 < 5 条 → 检查 CDP 媒体是否都成功抓取，查看 log 中的失败原因

---

## Step 2: 内容审核（强制执行，不可跳过）

### 合格标准（必须满足其一）
1. 明确涉及餐饮/茶饮/咖啡/食品饮料/供应链/预制菜行业
2. 涉及餐饮品牌（TOP_BRANDS 列表或其他已知餐饮品牌）
3. 涉及餐饮行业政策、法规、市场数据

### 不合格情形（直接剔除）

- 眼镜、家电、汽车、房地产、科技硬件等非餐饮行业内容
- 纯展会报名/参展通知（无实质行业信息）
- 泛泛"消费"、"品牌"话题但与餐饮无关
- 标题无具体信息（纯导航词、栏目名）
- **产品列表页**：含价格标签（¥/元）、商品规格描述、购买链接的条目（如"文火小牛肉 加热即食 ¥0.00"）
- **保健食品/保健品**：保健食品注册、备案、审批等内容（≠餐饮食品），除非明确涉及餐饮渠道
- **同一事件重复**：同一事件的多条报道只保留信息量最大的一条，其余合并或剔除
- **与前一天日报重复的事件**：检查前一天 MD 文件，同一事件不重复收录，除非有实质性新进展（如"调查→处罚→回应"属于事件推进，可收录）

### ⏰ 时效性门禁（硬性要求，不可绕过）

**合格时间窗口（当日为 {YYYY-MM-DD}）：**

| 优先级 | 窗口 | 数量上限 |
|--------|------|----------|
| ✅ 必须优先 | 当日（{MM-DD}）或前一日（{MM-DD-1}）| 无限制 |
| ⚠️ 谨慎使用 | 前2日（{MM-DD-2}），仅当内容极高价值 | 最多2条 |
| ❌ 直接剔除 | 3天前或更早的内容 | 0条 |

**执行规则：**
1. 每条新闻必须确认发布日期（从原文URL、meta published_time或正文日期中验证），不可仅凭搜索摘要中的日期判断
2. 如果48小时内真实内容不足10条，**宁可出少于10条，不可降低时效门槛**
3. 月度汇总报告（"4月监管政策概述"/"4月FDA情况"等）均属旧内容，无论发布于何时均剔除——这类文章总结的是历史数据
4. 信息图Headline中使用的关键词/数据，同样必须来自48小时内的报道，不得使用旧内容凑数
5. **严禁AI幻觉数据**：无法通过WebFetch访问原文核实的具体数字（如"外卖增速180%"），不得使用——若只在搜索摘要中出现但无原文支撑，直接剔除

**时效性核实方法（对可疑日期强制执行）：**
```
1. 用 WebFetch 读取原文URL
2. 在原文中确认：URL路径含当期日期（如 /2026/05/09/）或文章元数据日期在窗口内
3. 核实失败（404/超时/无日期字段）→ 标注 ⚠️时效待确认 并剔除
```

**2026-05-10 血泪教训：**
- 海底捞脆鲩鱼"首家"店实际开业于2025年5月（一年前旧闻）——搜索摘要未显示年份
- "外卖小镇增速180%"数据无法在任何可信2026年一手来源中核实，疑似AI幻觉
- 雀巢/保乐力加的"最新"表态实际发生在2月-4月，被当作当日新闻使用
- 结论：凡是"听起来很有价值"但无法核实发布时间的内容，必须剔除

### 审核流程
1. 读取 `news-{YYYY-MM-DD}.json`，列出全部10条标题
2. 逐条判断是否合格，标注 ✅ / ❌
3. 不合格条目：记录原因 + 将关键词加入 `fetch-news.js` 的 EXCLUDE_KEYWORDS，然后**重新执行 Step 1**
4. 若合格条目 < 5 条，执行 **WebSearch 补充采集**（见下方），而非盲目重跑 CDP
5. **跨天去重**：对比前一天日报 `{前一天}-餐饮日报.md`，剔除已在前一天报道过的同一事件（标题关键词重叠≥3 或同一 eventKey）
5b. **年份核查（高风险类别强制执行）**：凡标题含以下关键词之一，必须核查新闻确实发生在当年（{YYYY}）：
   - **触发词**：IPO、超购、上市、全流通、H股、纳斯达克、年报、峰会、榜单、发布会
   - **核查方法（必须执行，不可跳过）**：
     1. **强制用 WebFetch 读取原文 URL**（不可仅凭搜索摘要判断）
     2. 在原文中确认以下任一条件：
        - URL 路径中含当年年份（如 `/2026/`）
        - 正文中明确出现"{YYYY}年"字样
        - 文章发布日期（publish date meta 或正文日期）确实在 {YYYY} 年内
     3. WebFetch 失败（404/超时）时：标注 `⚠️年份待确认` 并**剔除**，不得保留
   - **不通过**：标注 `⚠️年份待确认` 并**剔除**；不可因标注了日期（如"04-16"）就默认为当年——月/日相同的历史事件每年都会出现
   - **典型陷阱**：IPO 超购、连锁峰会榜单、品牌上市——这些是年度性事件，标题完全相同但年份不同，AI 采集时极易引入前一年数据
   - **禁止的捷径**：不得用"搜索摘要中看起来是今年的"作为通过依据；必须访问原文
6. **空洞标题改写**：对合格条目逐条检查标题质量，发现以下情况必须改写：
   - 标题无具体数字、无品牌事件动词（如"XX企业加速重塑行业价值"）
   - 标题是泛泛的采访/专访标题，但正文含有价值数据
   - 改写方法：用 WebFetch 读取原文链接，提取正文中的核心数据点/事件，改写标题和 summary
   - 改写规则：保留原品牌名，补充正文中最有价值的具体信息（数字、趋势、事件）
   - 示例：`海天味业：调味品企业加速重塑行业价值` → `海天味业加码餐饮端渠道，调味品B端占比持续提升`
   - 改写后直接更新 `news-{date}.json` 中对应条目的 title 和 summary
6. 所有合格条目标题质量达标后，才可进入 Step 3

### WebSearch 补充采集（CDP 不足时）

当 CDP 合格条目 < 5 条时（常见于周末、T1 媒体 DNS 失败），执行以下补充：

1. 检查 CDP log 中失败的媒体源，记录原因（DNS/超时/反爬）
2. 用 WebSearch 搜索以下关键词组合（每组 1 次，共 3-4 次）：
   - `"餐饮品牌 {品牌名} {月份}" `（针对 TOP_BRANDS 中的热门品牌）
   - `"餐饮行业 政策 {月份}"`
   - `"茶饮 咖啡 上市 融资 {年份}"`
   - `"食品安全 监管 {月份}"`
3. 从搜索结果中筛选符合合格标准的条目，用 WebFetch/CDP 读取原文提取数据
4. 补充条目写入 `news-{date}-final.json`，与 CDP 合格条目合并
5. 补充后总条目仍 < 5 条时，标注为"周末版"/"轻量版"，不强制凑数

**此步骤为强制质量门，不得跳过或快速略过。**

**完成后立即进入 Step 3，不等用户。**

---

## Step 3: 生成 Markdown 日报

```bash
cd "C:\Users\杨顺\Documents\Obsidian Vault\01 Projects\餐饮日报\assets"
node generate-md.js {YYYY-MM-DD}
```

输出到 `01 Projects/餐饮日报/日报/{YYYY}/{MM}/{YYYY-MM-DD}-餐饮日报.md`。

MD 中图片嵌入路径格式（固定，不要改）：
```
![[01 Projects/餐饮日报/日报-assets/{YYYY}/{MM}/{YYYY-MM-DD}-餐饮日报.png]]
```

### MD 内容质量要求（v2 · 2026-04-19 起执行）

**每条新闻必须包含以下三层内容，不可只复制标题：**

1. **深度 summary**（2-3 句）：不是标题的重复，而是补充标题未涵盖的关键数据、背景、影响。如果原文有具体数字（金额、增长率、门店数），必须提取到 summary 中。
2. **🔷 高岩视角**（1-2 句）：从高岩科技的业务角度分析该新闻对高岩客户（B端食品/餐饮企业）的影响，或对高岩产品线（餐观大数据、餐饮垂类Agent、出海研究）的参考价值。
3. **来源标注**：格式 `> 来源：{媒体名} · {URL}`，多个关联报道用 `> 关联报道：` 追加。

**禁止的做法：**
- summary 直接复制标题（如 title="XX发布财报" → summary="XX发布财报"）
- 所有条目统一标注"⚠️待核查"（应区分：已交叉验证的标"多源验证"，单一来源的标"待核查"）
- 缺少高岩视角（这是日报区别于普通新闻聚合的核心价值）
- **高岩视角模板化复用**（硬性禁止）：多条新闻使用同一段或高度相似的高岩视角。每条视角必须针对该条新闻的具体数据/事件做定制分析，不得将"监管趋严会倒逼平台与门店提升合规……"等通用表述复制到多条。如写完后发现两条视角意思雷同，必须重写其中一条。

**高岩视角的 5 个模板（每条新闻选择最匹配的一个）**：

#### 模板 A：财务数据驱动（用于财报、融资新闻）
```
{品牌} 的 {财务指标}（{数字}）{趋势}，说明 {行业规律}。
高岩 {客户类型} 客户在 {业务维度} 上需要 {具体调整}。
```

**示例**：
- ✅ "瑞幸联营门店收入增速（+44.9%）远超自营（+32.6%），说明加盟扩张仍是主要增长引擎。高岩供应链客户需要准备更大规模的原料采购需求。"
- ✅ "金龙鱼净利润增速（+51%）远超营收增速（+11%），说明原料成本压力有所缓解。高岩餐饮B端采购客户在年中合同谈判时可争取更优价格条件。"

#### 模板 B：品类创新驱动（用于新品、融合品类新闻）
```
{品牌} 推出 {新品类/新模式}，体现 {行业趋势}。
高岩 {客户类型} 客户的 {供应链维度} 需要随之调整。
```

**示例**：
- ✅ "瑞幸推出咖啡+奶茶融合饮品，体现品类融合加速的趋势。高岩咖啡豆、茶叶供应商客户需要调整采购策略以适应新品类需求。"
- ✅ "蜜雪冰城向综合饮品方向扩品，意味着天然果汁、果浆、奶制品的原料需求将大幅增加。高岩相关供应链客户应关注蜜雪的品类扩张节奏。"

#### 模板 C：政策监管驱动（用于政策、法规新闻）
```
{政策内容}，意味着 {行业影响}。
高岩 {客户类型} 客户应关注 {具体的合规/机遇点}。
```

**示例**：
- ✅ "商务部下发价格虚假宣传指导意见，意味着餐饮行业从'野蛮生长'走向'合规增长'。高岩B端客户应抓住这个时间窗口，提升合规性和透明度，成为行业标杆。"
- ✅ "食品安全法强化追溯制度，意味着餐饮企业对原料渠道的尽调要求提升。高岩供应链情报产品的需求会上升。"

#### 模板 D：市场数据驱动（用于行业数据、趋势新闻）
```
{市场数据}（{数字}）显示 {市场规律}。
高岩 {客户类型} 客户在 {地域/品类/渠道} 上的 {战略调整} 需要加速。
```

**示例**：
- ✅ "五一期间小镇市场外卖订单增速（+180%）远超一线城市（+85%），显示小镇市场成为主要增量。高岩下沉市场布局的客户需要加速三四线城市的门店扩张。"
- ✅ "一季度现制饮品整体销售额同比增长 35%，但新品类增速达 78%，说明消费者对创新品类的需求强劲。高岩新品孵化客户应加强创新节奏。"

#### 模板 E：融资/资本驱动（用于融资、并购新闻）
```
{品牌} 获得 {融资/并购}，目标是 {战略方向}。
高岩 {客户类型} 客户需要关注 {竞争/合作机遇}。
```

**示例**：
- ✅ "库迪咖啡获得高瓴+腾讯新融资，目标是加速下沉市场布局。高岩咖啡供应链客户需要关注库迪的采购规模扩张和品类创新方向。"
- ✅ "呷哺呷哺完成大额融资，加速国际化布局。高岩出海研究团队应将其作为新的案例跟踪对象，研究跨境供应链整合模式。"

**质量检查（每条高岩视角必须通过）**：
- [ ] 是否包含具体的数字、品牌、事件？
- [ ] 是否明确指出了高岩客户的具体业务维度？
- [ ] 是否与其他条目的高岩视角不同？
- [ ] 是否可以被高岩客户直接理解和应用？

**禁止的表述**：
- ❌ "监管趋严会倒逼平台与门店提升合规……"（太泛泛）
- ❌ "建议高岩客户……"（不是观察，是建议）
- ❌ "这对高岩很重要"（没有具体说明为什么重要）
- ❌ 与前一条新闻的高岩视角相同或高度相似

**高岩视角的 5 个模板（每条新闻选择最匹配的一个）**：

#### 模板 A：财务数据驱动（用于财报、融资新闻）
```
{品牌} 的 {财务指标}（{数字}）{趋势}，说明 {行业规律}。
高岩 {客户类型} 客户在 {业务维度} 上需要 {具体调整}。
```
**示例**：
- ✅ "瑞幸联营门店收入增速（+44.9%）远超自营（+32.6%），说明加盟扩张仍是主要增长引擎。高岩供应链客户需要准备更大规模的原料采购需求。"

#### 模板 B：品类创新驱动（用于新品、融合品类新闻）
```
{品牌} 推出 {新品类/新模式}，体现 {行业趋势}。
高岩 {客户类型} 客户的 {供应链维度} 需要随之调整。
```
**示例**：
- ✅ "瑞幸推出咖啡+奶茶融合饮品，体现品类融合加速的趋势。高岩咖啡豆、茶叶供应商客户需要调整采购策略以适应新品类需求。"

#### 模板 C：政策监管驱动（用于政策、法规新闻）
```
{政策内容}，意味着 {行业影响}。
高岩 {客户类型} 客户应关注 {具体的合规/机遇点}。
```
**示例**：
- ✅ "商务部下发价格虚假宣传指导意见，意味着餐饮行业从'野蛮生长'走向'合规增长'。高岩B端客户应抓住这个时间窗口，提升合规性和透明度。"

#### 模板 D：市场数据驱动（用于行业数据、趋势新闻）
```
{市场数据}（{数字}）显示 {市场规律}。
高岩 {客户类型} 客户在 {地域/品类/渠道} 上的 {战略调整} 需要加速。
```
**示例**：
- ✅ "五一期间小镇市场外卖订单增速（+180%）远超一线城市（+85%），显示小镇市场成为主要增量。高岩下沉市场布局的客户需要加速三四线城市的门店扩张。"

#### 模板 E：融资/资本驱动（用于融资、并购新闻）
```
{品牌} 获得 {融资/并购}，目标是 {战略方向}。
高岩 {客户类型} 客户需要关注 {竞争/合作机遇}。
```
**示例**：
- ✅ "库迪咖啡获得高瓴+腾讯新融资，目标是加速下沉市场布局。高岩咖啡供应链客户需要关注库迪的采购规模扩张和品类创新方向。"

**质量检查（每条高岩视角必须通过）**：
- [ ] 是否包含具体的数字、品牌、事件？
- [ ] 是否明确指出了高岩客户的具体业务维度？
- [ ] 是否与其他条目的高岩视角不同？

**深度 summary 数据提取要求：**
- 有财报的新闻：必须提取营收/净利润/增速/门店数等核心财务数字，至少包含 3 个数据点
- 有政策的新闻：必须说明政策内容、生效时间、影响范围
- 有行业数据的新闻：必须提取市场规模/增速等关键指标

**条目排序规则（层次感）：**
当天新闻较多时，按以下逻辑排序，形成从终端→中游→上游→政策的叙事链：
1. 头部餐饮/茶饮品牌（消费终端）
2. 供应链/食品饮料上游企业（中游/上游）
3. 资本事件（IPO/融资）
4. 政策/监管
5. 行业趋势/数据

**数据速览表**（可选，有 3+ 个数据点时添加）：在所有新闻条目之后、数据来源之前，用 Markdown 表格汇总当日关键数据指标。

**今日主题段落（必填）：**
在数据速览表之后、数据来源之前，必须写一段"## 今日主题"叙事提炼：
- 格式：`## 今日主题：{主线标题}` + 1-2段话
- 内容：提炼当天所有新闻的共同规律/主线，用数据佐证，最后给出对高岩客户的一条具体启示
- 示例："4月29日是A股/港股财报披露密集日。核心规律：**营收增速普遍温和（5%-35%），但净利润增速显著高于营收**（金龙鱼+51%、伊利+37%、香飘飘+597%），反映原料成本压力缓解+产品结构升级的双重红利正在释放。对高岩客户的启示：上游盈利修复意味着供应商议价能力回升，下游餐饮采购方在年中合同谈判中需提前锁价。"
- 如当天新闻分散无明显主线，也必须写，但可以提炼2-3个独立议题并分别点评
- **禁止跳过此段落**

---

## Step 4: 生成信息图（v2 模板 · HTML + Puppeteer 截图）

### Step 4a: 生成 HTML

**执行**：
```bash
cd "C:/Users/杨顺/Documents/Obsidian Vault/01 Projects/餐饮日报/assets"
node build-html.js {YYYY-MM-DD}
```

**验证检查点（必须执行）**：
```bash
# 验证 1：脚本执行成功
if [ $? -ne 0 ]; then
  echo "❌ 错误：build-html.js 执行失败"
  exit 1
fi

# 验证 2：HTML 文件是否生成
if [ ! -f {YYYY-MM-DD}-餐饮日报.html ]; then
  echo "❌ 错误：{YYYY-MM-DD}-餐饮日报.html 未生成"
  exit 1
fi

# 验证 3：HTML 文件大小是否合理
size=$(wc -c < {YYYY-MM-DD}-餐饮日报.html)
if [ "$size" -lt 50000 ]; then
  echo "❌ 错误：HTML 文件过小（$size 字节，期望 > 50KB），检查是否正确读取了 JSON 数据"
  exit 1
fi

# 验证 4：HTML 是否包含必需的元素
if ! grep -q "logo-img" {YYYY-MM-DD}-餐饮日报.html; then
  echo "❌ 错误：HTML 缺少 logo 元素"
  exit 1
fi

if ! grep -q "headline" {YYYY-MM-DD}-餐饮日报.html; then
  echo "❌ 错误：HTML 缺少 headline 元素"
  exit 1
fi

if ! grep -q "kpi-row" {YYYY-MM-DD}-餐饮日报.html; then
  echo "❌ 错误：HTML 缺少 KPI 元素"
  exit 1
fi

if ! grep -q "section" {YYYY-MM-DD}-餐饮日报.html; then
  echo "❌ 错误：HTML 缺少新闻板块"
  exit 1
fi

echo "✅ Step 4a 验证通过：HTML 已生成，包含所有必需元素（文件大小 $(($size / 1024))KB）"
```

---

### Step 4b: 截图

**前置条件**：Step 4a 已验证成功

**执行**：
```bash
cd "C:/Users/杨顺/Documents/Obsidian Vault/01 Projects/餐饮日报/assets"
node screenshot.js {YYYY-MM-DD}
```

**验证检查点（必须执行）**：
```bash
# 验证 1：脚本执行成功
if [ $? -ne 0 ]; then
  echo "❌ 错误：screenshot.js 执行失败"
  exit 1
fi

# 验证 2：PNG 文件是否生成
if [ ! -f "{YYYY-MM-DD}-餐饮日报.png" ] && [ ! -f "../日报-assets/{YYYY}/{MM}/{YYYY-MM-DD}-餐饮日报.png" ]; then
  echo "❌ 错误：PNG 文件未生成"
  exit 1
fi

# 找到实际的 PNG 文件路径
PNG_FILE="{YYYY-MM-DD}-餐饮日报.png"
if [ ! -f "$PNG_FILE" ]; then
  PNG_FILE="../日报-assets/{YYYY}/{MM}/{YYYY-MM-DD}-餐饮日报.png"
fi

# 验证 3：PNG 文件大小是否合理
size=$(wc -c < "$PNG_FILE")
if [ "$size" -lt 100000 ]; then
  echo "❌ 错误：PNG 文件过小（$size 字节，期望 > 100KB），检查 Puppeteer 是否正确截图"
  exit 1
fi

# 验证 4：PNG 是否是有效的图片
if ! file "$PNG_FILE" | grep -q "PNG image"; then
  echo "❌ 错误：$PNG_FILE 不是有效的 PNG 图片"
  exit 1
fi

echo "✅ Step 4b 验证通过：PNG 已生成，文件大小 $(($size / 1024))KB"
```

---

### Step 4c: 复制到输出目录

**前置条件**：Step 4b 已验证成功

**执行**（如果截图脚本未自动复制）：
```bash
mkdir -p "C:\Users\杨顺\Documents\Obsidian Vault\01 Projects\餐饮日报\日报-assets\{YYYY}\{MM}"
cp "{YYYY-MM-DD}-餐饮日报.png" "C:\Users\杨顺\Documents\Obsidian Vault\01 Projects\餐饮日报\日报-assets\{YYYY}\{MM}\{YYYY-MM-DD}-餐饮日报.png"
```

**验证检查点**：
```bash
# 验证文件是否复制成功
if [ ! -f "C:\Users\杨顺\Documents\Obsidian Vault\01 Projects\餐饮日报\日报-assets\{YYYY}\{MM}\{YYYY-MM-DD}-餐饮日报.png" ]; then
  echo "❌ 错误：PNG 文件复制失败"
  exit 1
fi

echo "✅ Step 4c 验证通过：PNG 已复制到输出目录"
```

---

**⚠️ 严格禁止以下做法（过去反复踩坑）：**
- ❌ 复制前一天 HTML 再文本替换（会带入昨天的 KPI/标题数据，极难全量替换干净）
- ❌ 生成一次性的 `build-html-{YYYY-MM-DD}.js` 临时脚本（CSS 会丢失，KPI 容易被硬编码）
- ❌ 从零手写 HTML（CSS 不完整）
- ❌ 分段 Read 大 HTML 文件

`build-html.js` 已内嵌完整 v2 CSS，自动读取 logo base64，自动从 JSON 计算 headline/KPI/板块，**唯一入参是日期**，无需任何手工修改。

### 4a 的自动生成内容说明

`build-html.js` 自动处理以下内容，**禁止在外部手动覆盖**：

- **headline**：`buildHeadlineHtml()` 函数评分选主新闻 → 套叙事模板 → 提炼第二行关键词
  - 评分优先级：资本事件(收购/易主+25) > 财报数据(大数字) > 品牌+数字 > 行业数据
  - "首次/首度"词仅给 +8 分（已修复，不再+18抢占主新闻）
- **KPI 3格**：`extractKpisFromNews()` 按 万亿 > 亿 > 万家/万店 > % 优先级提炼，自动去重
- **subline**：自动汇总当日所有 tag 关键词
- **板块分组**：按 tagOrder（政策/资本/茶饮咖啡/中游/国际/下游）自动分组，无该 tag 的板块不渲染

### 4b. 信息图设计规范（2026-04-14 确认版 · v2 标准）

**⚠️ 此为固定设计标准，每天照此执行，不要自行修改设计。用户给出新修改建议时才更新此处。**

#### 整体布局

| 参数 | 值 |
|------|-----|
| 页面宽度 | `800px`（`.card`） |
| viewport | `<meta name="viewport" content="width=800">` |
| 页面背景 | `#f0ece7`（米白） |
| 卡片背景 | `#ffffff` |
| body padding | `32px 0 48px` |
| 内容左右 padding | `56px`（header / section / footer 统一） |
| 字体 | `'Microsoft YaHei', 'PingFang SC', sans-serif` |
| 主分割线 | `2px solid #0E0E0E`（header底、kpi-row底、footer顶） |
| 次分割线 | `1px solid #e8e4e0`（section间） |
| 最细分割线 | `1px solid #f0ece7`（news-item 间） |

#### 色彩系统

| 用途 | 色值 |
|------|------|
| 主文字 | `#0E0E0E` |
| 次级文字 | `#464646` |
| 辅助文字 | `#8C8C8C` |
| 最淡文字/序号 | `#c4c0bb` |
| **强调蓝（高岩蓝）** | `#246AFF` |
| KPI 箭头绿 | `#01EFC1` |
| 页面背景 | `#f0ece7` |
| 次级分割线 | `#e8e4e0` |

#### Logo 规范

- 使用 `高岩知识库/assets/高岩 Logo-中文 jpg.jpg`
- **必须 base64 内嵌**：`<img class="logo-img" src="data:image/jpeg;base64,{b64}" alt="高岩科技">`
- `logo-img` class 定义 `height: 40px; width: auto;`
- base64 读取方式（`高岩知识库/assets/logo_zh_b64.txt` 里有现成文本，直接读取拼接）：
  ```
  src="data:image/jpeg;base64," + fs.readFileSync(logo_zh_b64.txt, 'utf-8').trim()
  ```

#### Header 结构

```html
<div class="header">
  <div class="header-top">
    <div class="logo-area">
      <img class="logo-img" src="data:image/jpeg;base64,..." alt="高岩科技">
    </div>
    <div class="date-label">{YYYY.MM.DD} · 餐饮日报</div>
  </div>
  <div class="headline">{今日头条关键词} <span>{高亮品牌/数字}</span><br>{第二行}</div>
  <div class="subline">{关键词1} · {关键词2} · {关键词3} — 今日{N}条精选</div>
</div>
```

#### KPI 行（3格）

```html
<div class="kpi-row">  <!-- 3列 grid -->
  <div class="kpi-cell">
    <div class="kpi-tag">{KPI标签，11px大写}</div>
    <div class="kpi-num">{数字}<span class="unit">{单位}</span></div>
    <div class="kpi-desc">{描述} · {补充}</div>
  </div>
  <!-- 重复3个 -->
</div>
```

- KPI 数字：44px，高岩蓝 `#246AFF`
- 单位：20px，`opacity: 0.7`
- 上升箭头 `<span class="kpi-arrow">↑</span>`：颜色 `#01EFC1`

#### 板块结构（6个板块）

每个板块由 `.section` 包裹，板块标题用 `.section-head`：

```html
<div class="section">
  <div class="section-head">
    <div class="section-head-inner">
      <div class="section-label">
        <span class="tag-dot" style="background:{板块色};"></span>
        {板块名}
      </div>
      <div class="section-count">{N} 条</div>
    </div>
  </div>
  <!-- 新闻条目 -->
</div>
```

**6个标准板块及配色：**

| 板块 | tag-dot | icon 背景 | icon 颜色 | tag-pill class |
|------|---------|----------|----------|----------------|
| 政策监测 | `#0E0E0E` | `#EBF2FF` | `#246AFF` | `tag-policy`（黑底白字） |
| 国际动态 | `#464646` | `#EBEBEB` | `#464646` | `tag-intl`（深灰底白字） |
| 资本动向 | `#FABB00` | `#FFF8E1` | `#FABB00` | `tag-capital`（黄底黑字） |
| 中游供应链 | `#43A047` | `#E8F5E9` | `#43A047` | `tag-mid`（绿底绿字） |
| 茶饮咖啡 | `#FB8C00` | `#FFF3E0` | `#FB8C00` | `tag-tea`（橙底橙字） |
| 下游品牌 | `#c4c0bb` | `#F0ECE7` | `#8C8C8C` | `tag-down`（灰边米底） |

**板块可以按当天新闻灵活增减**，没有该分类的新闻就不出现该板块，但风格必须从上表选取。

#### 新闻条目结构（单条）

```html
<div class="news-item">
  <div class="news-icon" style="background:{icon背景}; color:{icon颜色};">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
      <!-- 语义化 SVG path，每条新闻不同 -->
    </svg>
  </div>
  <div class="news-index">{01/02/...}</div>
  <div class="news-body">
    <div class="news-title">{新闻标题}</div>
    <div class="news-meta">
      <span class="tag-pill {tag-类型}">{分类}</span>
      <span class="news-source">{来源}</span>
    </div>
  </div>
</div>
```

**SVG 图标规则：**
- 所有 SVG 统一：`viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"`
- **必须根据每条新闻内容语义定制图标**，不能同类共用
- 常用图标参考：

| 语义 | SVG path |
|------|----------|
| 政府大楼 | `<rect x="2" y="7" width="20" height="15"/><polyline points="2,7 12,2 22,7"/><rect x="9" y="13" width="6" height="9"/>` |
| 地球 | `<circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 014 10 15.3 15.3 0 01-4 10 15.3 15.3 0 01-4-10 15.3 15.3 0 014-10z"/>` |
| 麦克风 | `<path d="M12 1a3 3 0 00-3 3v8a3 3 0 006 0V4a3 3 0 00-3-3z"/><path d="M19 10v2a7 7 0 01-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/>` |
| 美元符号 | `<line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/>` |
| 热饮杯 | `<path d="M17 8h1a4 4 0 010 8h-1"/><path d="M3 8h14v9a4 4 0 01-4 4H7a4 4 0 01-4-4V8z"/><line x1="6" y1="2" x2="6" y2="4"/><line x1="10" y1="2" x2="10" y2="4"/><line x1="14" y1="2" x2="14" y2="4"/>` |
| 购物袋 | `<path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 01-8 0"/>` |
| 价签标签 | `<path d="M20.59 13.41l-7.17 7.17a2 2 0 01-2.83 0L2 12V2h10l8.59 8.59a2 2 0 010 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/>` |
| 礼物盒 | `<polyline points="20 12 20 22 4 22 4 12"/><rect x="2" y="7" width="20" height="5"/><line x1="12" y1="22" x2="12" y2="7"/><path d="M12 7H7.5a2.5 2.5 0 010-5C11 2 12 7 12 7z"/><path d="M12 7h4.5a2.5 2.5 0 000-5C13 2 12 7 12 7z"/>` |
| 餐碗 | `<path d="M12 2C6.48 2 2 6.48 2 12h20c0-5.52-4.48-10-10-10z"/><path d="M2 12c0 5.52 4.48 10 10 10s10-4.48 10-10"/>` |

#### Footer 结构

```html
<div class="footer">
  <div class="footer-note">
    数据来源：{来源1} · {来源2} · ...<br>
    ✓ 已核实  ⚠ 第三方媒体，发布前请自行核查
  </div>
  <div class="footer-brand">
    <div class="footer-brand-name">GAOYAN</div>
    <div class="footer-brand-sub">TECHNOLOGY · INSIGHT</div>
  </div>
</div>
```

#### 完整 CSS（固定，不要修改）

```css
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: #f0ece7; display: flex; justify-content: center; padding: 32px 0 48px; font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif; }
.card { width: 800px; background: #ffffff; }
.header { padding: 40px 56px 32px; border-bottom: 2px solid #0E0E0E; }
.header-top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }
.logo-area { display: flex; align-items: center; }
.logo-img { height: 40px; width: auto; display: block; }
.date-label { font-size: 13px; color: #8C8C8C; letter-spacing: 1px; }
.headline { font-size: 48px; font-weight: 700; color: #0E0E0E; line-height: 1.1; letter-spacing: -1px; }
.headline span { color: #246AFF; }
.subline { margin-top: 12px; font-size: 15px; color: #464646; line-height: 1.6; }
.kpi-row { display: grid; grid-template-columns: repeat(3, 1fr); border-top: 1px solid #e8e4e0; border-bottom: 2px solid #0E0E0E; }
.kpi-cell { padding: 28px 32px; border-right: 1px solid #e8e4e0; }
.kpi-cell:last-child { border-right: none; }
.kpi-tag { font-size: 11px; font-weight: 600; letter-spacing: 2px; color: #8C8C8C; text-transform: uppercase; margin-bottom: 10px; }
.kpi-num { font-size: 44px; font-weight: 700; color: #246AFF; line-height: 1; letter-spacing: -2px; }
.kpi-num .unit { font-size: 20px; font-weight: 400; letter-spacing: 0; color: #246AFF; opacity: 0.7; }
.kpi-desc { margin-top: 8px; font-size: 12px; color: #8C8C8C; line-height: 1.4; }
.kpi-arrow { display: inline-block; color: #01EFC1; font-weight: 700; margin-right: 2px; }
.section { padding: 0 56px; border-bottom: 1px solid #e8e4e0; }
.section-head { display: flex; align-items: center; justify-content: space-between; padding: 20px 0 0; border-bottom: 1px solid #e8e4e0; margin-bottom: 0; }
.section-head-inner { display: flex; align-items: center; justify-content: space-between; width: 100%; padding-bottom: 16px; }
.section-label { font-size: 11px; font-weight: 700; letter-spacing: 3px; text-transform: uppercase; color: #0E0E0E; }
.section-count { font-size: 11px; color: #8C8C8C; letter-spacing: 1px; padding-bottom: 20px; }
.tag-dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 10px; }
.news-item { display: flex; align-items: center; gap: 16px; padding: 18px 0; border-bottom: 1px solid #f0ece7; }
.news-item:last-child { border-bottom: none; }
.news-icon { width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.news-icon svg { width: 22px; height: 22px; }
.news-index { font-size: 11px; color: #c4c0bb; min-width: 20px; font-variant-numeric: tabular-nums; }
.news-body { flex: 1; min-width: 0; }
.news-title { font-size: 17px; color: #0E0E0E; line-height: 1.5; font-weight: 500; }
.news-meta { margin-top: 6px; display: flex; align-items: center; gap: 10px; }
.news-source { font-size: 13px; color: #8C8C8C; }
.tag-pill { font-size: 10px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; padding: 2px 7px; border-radius: 2px; }
.tag-policy { background: #0E0E0E; color: #fff; }
.tag-capital { background: #FABB00; color: #0E0E0E; }
.tag-down { background: #f0ece7; color: #0E0E0E; border: 1px solid #c4c0bb; }
.tag-intl { background: #464646; color: #fff; }
.tag-mid { background: #E8F5E9; color: #2E7D32; }
.tag-tea { background: #FFF3E0; color: #E65100; }
.footer { padding: 24px 56px; display: flex; align-items: center; justify-content: space-between; border-top: 2px solid #0E0E0E; }
.footer-note { font-size: 11px; color: #8C8C8C; line-height: 1.7; }
.footer-brand { text-align: right; }
.footer-brand-name { font-size: 14px; font-weight: 700; letter-spacing: 3px; color: #246AFF; }
.footer-brand-sub { font-size: 10px; color: #c4c0bb; letter-spacing: 1px; margin-top: 2px; }
```

### 4c. Puppeteer 截图

**截图输出路径**：`日报-assets/{YYYY}/{MM}/{YYYY-MM-DD}-餐饮日报.png`（不再放 `assets/` 根目录）

```bash
cd "C:/Users/杨顺/Documents/Obsidian Vault/01 Projects/餐饮日报/assets"
node screenshot.js {YYYY-MM-DD}
```

> `screenshot.js` 内部需要将输出路径改为 `../日报-assets/{YYYY}/{MM}/{YYYY-MM-DD}-餐饮日报.png`。
> 如果脚本还在写旧路径，手动指定输出路径参数或直接用 node -e 内联脚本：

```javascript
// 内联截图（路径已更新）
const puppeteer = require('C:/Users/杨顺/Documents/Obsidian Vault/node_modules/puppeteer-core');
const CHROME = 'C:/Users/杨顺/.cache/puppeteer/chrome-headless-shell/win64-146.0.7680.153/chrome-headless-shell-win64/chrome-headless-shell.exe';
const HTML = 'C:/Users/杨顺/Documents/Obsidian Vault/01 Projects/餐饮日报/assets/{YYYY-MM-DD}-餐饮日报.html';
const OUT  = 'C:/Users/杨顺/Documents/Obsidian Vault/01 Projects/餐饮日报/日报-assets/{YYYY}/{MM}/{YYYY-MM-DD}-餐饮日报.png';
(async () => {
  const b = await puppeteer.launch({ executablePath: CHROME, headless: true, args: ['--no-sandbox'] });
  const p = await b.newPage();
  await p.setViewport({ width: 800, height: 600, deviceScaleFactor: 2 });
  await p.goto('file:///' + HTML, { waitUntil: 'networkidle0', timeout: 30000 });
  const h = await p.evaluate(() => document.querySelector('.card').scrollHeight);
  await p.setViewport({ width: 800, height: h, deviceScaleFactor: 2 });
  await p.screenshot({ path: OUT, fullPage: true });
  await b.close();
  console.log('done:', OUT);
})();
```

**⚠️ 截图已知坑：**
1. **require 路径**：必须用绝对路径 `require('C:/Users/杨顺/Documents/Obsidian Vault/node_modules/puppeteer-core')`，裸模块名在 `assets/` 子目录下找不到
2. **Chrome 路径**：用 headless-shell（`~/.cache/puppeteer/chrome-headless-shell/...`），不用 `chrome.exe`
3. **验证尺寸**：确认 `800 x XXXX`（@2x 实际 1600 宽），不是 `800 x 1440`
4. **Obsidian 缓存**：文件替换后 Obsidian 可能不刷新，关掉重开笔记即可

### 4d. 信息图制作效率规则

**禁止以下低效做法：**
- ❌ 用 Agent 从零写整个 HTML（CSS 会丢失/不完整）
- ❌ 分段读大 HTML 文件（Read 工具 10000 token 限制会来回读几十次）
- ❌ 在主线程用 Read 反复读 v2 模板

**正确做法：**
- ✅ `Copy-Item` 复制前一天 HTML（1秒）
- ✅ Node.js 脚本精准文本替换（几秒）
- ✅ Puppeteer 截图（几秒）
- **总耗时应在 1 分钟内完成**

---

## Step 5: 验证完成

**每步必须验证，不能只看 exit code：**

```bash
# 验证新闻 JSON
wc -l ".../assets/news-{YYYY-MM-DD}.json"   # 应有内容

# 验证 MD 文件
ls -la ".../01 Projects/餐饮日报/{YYYY-MM-DD}-餐饮日报.md"

# 验证信息图（最重要）
file ".../01 Projects/餐饮日报/assets/{YYYY-MM-DD}-餐饮日报.png"
# 必须显示 900 x 9XX，不是 800 x 1440
```

完成后告知用户：
- ✅ 新闻采集：X 条（CDP，无 API Key）
- ✅ Markdown 日报：`01 Projects/餐饮日报/{YYYY-MM-DD}-餐饮日报.md`
- ✅ 信息图：`900 x XXX px`，`01 Projects/餐饮日报/assets/{YYYY-MM-DD}-餐饮日报.png`

---

## 周报任务（每周一触发）

每周一根据上周7期日报内容，汇总生成周报。

### 文件路径规范
| 文件 | 路径 |
|------|------|
| MD 周报 | `01 Projects/餐饮日报/周报/2026-W{NN}-餐饮周报.md` |
| 信息图 HTML | `01 Projects/餐饮日报/周报/assets/2026-W{NN}-餐饮周报.html` |
| 截图 PNG | `01 Projects/餐饮日报/周报/assets/2026-W{NN}-餐饮周报-screenshot.png` |

MD 文件顶部（frontmatter 之后）必须嵌入截图：
```markdown
![[2026-W{NN}-餐饮周报-screenshot.png|900]]
```

### 信息图设计规范（Apple UI 深色风格）

**来源**：`/frontend-slides` skill 生成的 Apple UI 深色主题，非 `/daily-report` 日报模板。

**配色系统（已确认，不可随意改动）：**
| CSS 变量 | 值 | 说明 |
|----------|-----|------|
| `--black` | `#051C2C` | 高岩深海蓝，所有深色背景 |
| `--dark-surface` | `#0A2D45` | 卡片/深色板块背景（比主色浅一层） |
| `--apple-blue` / `--link-blue` / `--bright-blue` | `#05ADE5` | 高岩亮蓝，所有强调色/链接/badge |
| `--light-gray` | `#f5f5f7` | 浅色板块背景（不变） |
| `--white` | `#ffffff` | 文字/浅色板块（不变） |
| `--near-black` | `#1d1d1f` | 浅色板块上的文字（不变） |

品牌 badge（`.brand-type`）：`background: rgba(5,173,229,0.2); border: 0.5px solid rgba(5,173,229,0.4);`
Brands 区块背景：`#0A2D45`
Hero 辉光：`rgba(5,173,229,0.15)`
Nav 背景：`rgba(5,28,44,0.95)`

**板块结构（6段）：**
1. **Hero** — W{NN}大字、日期、关键词 tag pills
2. **数据概览**（黑底 `#05ADE5`）— 5个 stat-card，填当周真实数据
3. **本周主题**（浅灰底）— 6个 theme-card，从日报事件中提炼
4. **行业动态**（白底）— 12条 news-item，来自本周精选
5. **品牌追踪**（`#0490C2`底）— 6个 brand-card，含 metrics
6. **高岩洞察** + **趋势榜**（黑底）+ **洞察信号**（白底）+ **Footer**

### 截图规范（必须遵守，否则全黑）

**问题原因**：CSS 初始 `opacity: 0`，IntersectionObserver 不触发时内容不可见。

**正确截图脚本要点：**
```javascript
// 1. 注入样式禁用所有动画/过渡，强制 opacity:1
const style = document.createElement('style');
style.textContent = `* { animation: none !important; transition: none !important; opacity: 1 !important; transform: none !important; }
  .hero { min-height: auto !important; padding: 80px 24px 60px !important; }
  nav { position: relative !important; }`;
document.head.appendChild(style);

// 2. 强制 visible
document.querySelectorAll('.stat-card,.theme-card,.news-item,.brand-card,.insight-card,.signal-card')
  .forEach(el => el.classList.add('visible'));
document.querySelectorAll('.trends-table tbody tr').forEach(el => el.classList.add('visible'));
const q = document.querySelector('.insight-quote');
if (q) q.classList.add('visible');
```
- `setViewport` → `deviceScaleFactor: 2`（900×scrollHeight）
- 等待 500ms 后截图
- 用 `fullPage: false`（不用 true，避免重复渲染）
- CDP 不可用时自动 fallback 到 `puppeteer.launch` headless 模式

**信息图 CSS 已知必须项（生成时必须包含）：**
- `.trend-badge` 必须加 `white-space: nowrap`，否则表格列宽压缩时强度标签折行（如"爆\n发"）

---

## 每日迭代流程

用户每天会对日报提出修改意见（内容、排版、信息图样式等），按以下流程处理：

### 修改步骤
1. **理解意见** — 确认是一次性改动还是规则性改动
2. **执行修改** — 改 HTML/MD/脚本，重新截图，验证图片尺寸（`file` 命令）
3. **用户确认** — 等用户说"好的"/"可以"后，才算该条意见完成
4. **写入 skill** — 将确认通过的改动，更新到本文档的对应位置：
   - 排版/样式改动 → 更新"Step 4: 生成信息图"部分
   - 内容/分类改动 → 更新"Step 2: 内容审核"部分
   - 流程改动 → 更新对应 Step

### 迭代记录（按日期）

> 每次迭代后在此追加，格式：`{YYYY-MM-DD}：{改动摘要}`

- 2026-05-03：重命名 skill 为 `gaoyan-daily-report`；统一 Step 4 为 `node build-html.js` 单一流程；修复 Step 1B Windows 路径；修复 Step 3 工作目录；修复 `build-html.js` 「首次」评分 bug（+18→+10，须同时匹配品牌名）
- 2026-05-03：重构目录结构：日报 MD → `日报/{YYYY}/{MM}/`；信息图 → `日报-assets/{YYYY}/{MM}/`；周报统一在 `周报/`；`assets/` 只保留脚本和临时数据；截图脚本改用绝对路径 require + headless-shell
- 2026-05-03：重构目录结构：日报 MD → `日报/{YYYY}/{MM}/`；信息图 HTML+PNG → `日报-assets/{YYYY}/{MM}/`；周报统一在 `周报/` + `周报/assets/`；脚本和临时数据留在 `assets/`；更新 Step 3 输出路径、Step 4c 截图路径、文件结构速查；截图脚本改用绝对路径 require + headless-shell

---

## 文件结构速查

```
01 Projects/餐饮日报/
  assets/                          ← 脚本和临时数据（不迁移）
    fetch-news.js                  ← CDP 新闻采集脚本
    generate-md.js                 ← MD 日报生成脚本
    build-html.js                  ← 从 news JSON 生成信息图 HTML（v2 模板内嵌）
    screenshot.js                  ← Puppeteer 截图脚本
    news-{YYYY-MM-DD}.json         ← 当日新闻 JSON（临时）
    log-{YYYY-MM-DD}.txt           ← 采集日志（临时）
    {YYYY-MM-DD}-餐饮日报.html     ← 信息图 HTML（临时，截图后可留存）
    _archive/                      ← 历史临时文件归档
    .env / package.json            ← 配置文件（保留）
  日报/                            ← 日报 Markdown 正文（按年/月归档）
    YYYY/
      MM/
        YYYY-MM-DD-餐饮日报.md
  日报-assets/                     ← 日报信息图 HTML + PNG（按年/月归档）
    YYYY/
      MM/
        YYYY-MM-DD-餐饮日报.html
        YYYY-MM-DD-餐饮日报.png
  周报/                            ← 周报 Markdown 正文
    YYYY-WXX-餐饮周报.md
    assets/                        ← 周报信息图 HTML + PNG
      YYYY-WXX-餐饮周报.html
      YYYY-WXX-screenshot.png
      YYYY-WXX-餐饮周报-screenshot.png
```
