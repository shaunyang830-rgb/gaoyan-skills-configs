---
name: daily-report
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

### Step 1B: CDP 轨道（同步执行，读取 1A 结果合并）

```bash
# 必须同步执行，timeout 120s，不要用 run_in_background
cd "/c/Users/杨顺/Documents/Obsidian Vault/01 Projects/餐饮日报/assets"
node fetch-news.js {YYYY-MM-DD} > news-{YYYY-MM-DD}.json 2>log-{YYYY-MM-DD}.txt
```

**完成后**：立即进入 Step 2，不等用户。

脚本自动：
1. 读取 `websearch-results.json`（轨道A结果）
2. 优先连接已有 Chrome（端口 9222），否则自动启动调试模式 Chrome
3. 逐个访问下方媒体列表页，抓取 `<a>` 链接文本（轨道B）
4. 双轨结果合并，过滤非餐饮内容，交叉验证，评分排序，输出精选 **10 条** JSON

### 采集媒体清单（20个，含分类）

| 层级 | 媒体 | 默认tag |
|------|------|---------|
| **Tier0 官方** | 国家统计局 | 政策 |
| | 商务部 | 政策 |
| | 财联社 | 资本 |
| **Tier1 餐饮垂直** | 红餐网 | 下游 |
| | 餐饮老板内参 | 下游 |
| | 咖门 | 茶饮咖啡 |
| | 职业餐饮网 | 下游 |
| | 餐饮界 | 下游 |
| | 高岩科技（搜狗微信） | 趋势 |
| **Tier2 食品饮料** | Foodaily | 中游 |
| | FoodTalks | 中游 |
| | 小食代 | 中游 |
| | 食品伙伴网 | 中游 |
| | 中国食品报 | 政策 |
| | 预制菜洞察 | 中游 |
| | 乳业在线 | 中游 |
| | 冻品头条 | 中游 |
| **Tier4 综合商业** | 36氪 | 资本 |
| | 澎湃新闻 | 下游 |
| | 界面新闻 | 资本 |
| | 虎嗅 | 趋势 |
| | 亿欧 | 趋势 |
| | 新华社 | 政策 |

> Tier0（国家统计局/商务部/财联社）抓到的条目自动标记 `verified=true`，评分+15。官网有时 SSL/超时失败，失败不影响整体流程。

### 完整来源权重表（106个，用于评分，v2 分值）

**Tier0 = 30分**（官方权威）
国家统计局、商务部、财联社

**Tier1 = 25分**（餐饮垂直核心）
红餐网、餐饮老板内参、餐企老板内参、番茄资本、窄门餐眼、餐饮界、职业餐饮网、火锅餐见、咖门、餐饮供应链指南、新餐饮洞察、刺猬餐饮、餐宝典、鲸餐、漆点餐研社、高岩科技

**Tier2 = 20分**（茶饮咖啡烘焙 & 食品饮料）
饮力实验室、茶饮研究所、烘焙圈、伊莎莉卡烘焙网、中国饮品快报、深氪新消费、精品咖啡美学、FBIF食品饮料创新、FoodTalks、Foodaily每日食品、食品板、小食代、食研汇、食品商务网、食品伙伴网、中国食品报、新经销、快消、植提桥、全食在线、预制菜洞察、冷冻食品、调料家、乳业财经、酒业家

**Tier3 = 15分**（官方机构 & 数据研究）
中国饭店协会、中国烹饪协会、美团研究院、饿了么商业洞察、艾瑞咨询、欧睿 Euromonitor、英敏特 Mintel、沙利文 Frost & Sullivan、凯度消费者指数、尼尔森 Nielsen、智研咨询、前瞻产业研究院、中商产业研究院、观研天下、头豹研究院、易观分析、CBNData 第一财经商业数据中心、极海品牌监测

**Tier4 = 10分**（综合商业 & 新消费）
36氪、虎嗅、钛媒体、界面新闻、澎湃新闻、亿欧、刀法研究所、浪潮新消费、消费界、零售老板内参、品牌星球、增长黑盒、进击波财经、新华社

**Tier5 = 5分**（国际媒体）
Nation's Restaurant News、Restaurant Business Online、Food Navigator Asia、Food Dive、The Spoon、QSR Magazine、Technomic、World Coffee Portal、Bakery & Snacks、Nikkei Asia、Inside Retail Asia、Bangkok Post、The Business Times Singapore、Vietnam Investment Review

> 以上为评分权重表，不代表全部都在采集清单里。采集清单（20个）是实际能 CDP 访问的媒体，权重表（106个）用于识别来源并打分。

### 过滤规则

**排除域名**（EXCLUDE_DOMAINS）：知乎、百度、豆瓣

**排除关键词**（EXCLUDE_KEYWORDS，标题含以下词直接丢弃）：
- 非餐饮行业：汽车、机器人、黑莓、手机、芯片、半导体、房地产、楼市、电动车、新能源、航空、航天、军事、游戏、电影、娱乐
- 品牌误判：理想汽车、东风日产、日产、宝马、奔驰、特斯拉、拉踩
- 低质量内容：如何挑选、家用推荐、好吃的地方、确认参展、展商名录

**餐饮相关词**（FOOD_KEYWORDS，标题必须含以下词之一才保留）：
餐饮、餐厅、茶饮、咖啡、奶茶、烘焙、预制菜、外卖、火锅、烧烤、快餐、食材、冷链、加盟、门店、瑞幸、蜜雪、喜茶、海底捞、星巴克、麦当劳、调味品、酱油、醋、豆瓣酱、乳制品、奶粉、冷冻食品、速冻、酒水、白酒、饮料、生鲜、水产等

### 评分排序规则（v2: 2026-04-14 重构）

**设计原则：「谁说的」降权，「说了什么」升权**

**总分 = 来源分(30%) + 内容分(40%) + 时效分(15%) + 稀缺分(15%)**，满分100

#### 来源分（满分30，缩小层级差距）

| Tier | 分数 | 媒体 |
|------|------|------|
| T0 | 30 | 国家统计局、商务部、财联社 |
| T1 | 25 | 红餐网、餐饮老板内参、咖门、餐饮界、职业餐饮网、火锅餐见、高岩科技等16家 |
| T2 | 20 | Foodaily、FoodTalks、小食代、食品伙伴网、中国食品报、预制菜洞察等22家 |
| T3 | 15 | 美团研究院、艾瑞咨询、中国饭店协会等18家 |
| T4 | 10 | 36氪、虎嗅、界面新闻、澎湃、亿欧、新华社等14家 |
| T5 | 5 | NRN、Food Dive、QSR Magazine等国际媒体 |

#### 内容分（满分40，最大权重）

| 信号 | 加分 | 示例 |
|------|------|------|
| 具体数字+单位 | +12 | "社零餐饮收入同比增长5.6%"、"突破6000店" |
| 知名品牌+事件动词 | +10 | "海底捞关闭300家门店"、"瑞幸收购xxx" |
| 融资/IPO/财报 | +10(取max22) | "锅圈食汇完成D轮融资" |
| 政策/法规/标准 | +8 | "预制菜国标正式发布" |
| 行业数据/报告/排名 | +8 | "2026中国茶饮TOP50" |
| 知名品牌(无动词) | +5 | "星巴克推出季节新品" |
| 事件动词(无品牌) | +3 | "某连锁品牌关店潮" |
| 交叉验证奖励 | +8 | 2家+不同媒体报道同一事件 |

品牌列表：海底捞、瑞幸、蜜雪冰城、喜茶、星巴克、麦当劳、肯德基、古茗、奈雪、库迪、塔斯汀、九毛九、呷哺、沪上阿姨、百胜、必胜客、汉堡王、达美乐、Tims、太二、西贝、老乡鸡、杨国福、张亮、绝味、周黑鸭、正新鸡排、华莱士、锅圈、美团、饿了么、盒马、叮咚、朴朴、山姆、海天、李锦记、老干妈、恒顺、伊利、蒙牛、光明、安井、三全、思念、湾仔码头、雀巢、茅台、五粮液、农夫山泉、元气森林、东方树叶

事件动词：开店/关店/融资/收购/上市/涨价/降价/倒闭/裁员/扩张/合并/发布/推出/签约/入驻/关闭/撤退/亏损/盈利/突破/暴涨/暴跌/翻倍

#### 时效分（满分15）

| 信号 | 分数 |
|------|------|
| Tier0 verified=true | 15 |
| 标题含"今日/今天/刚刚/最新/速报/突发/快讯" | 15 |
| 标题含当月"X月"或"Q1/Q2"等 | 12 |
| 标题含当年"2026" | 10 |
| 无时间信号（默认） | 5 |
| 标题含"去年/回顾/盘点/202X(非今年)" | 0 |

#### 稀缺分（满分15，贪心选择阶段动态计算）

| 信号 | 分数 |
|------|------|
| 唯一tag（该tag首条） | +10 |
| 稀有tag（该tag≤1条） | +5 |
| 同来源冗余惩罚（已入选≥1条） | -5 |

#### 贪心选择算法（取代简单 top-N）

按总分降序遍历候选池，逐条加入，约束：
- 同 tag ≤ 3 条
- 同来源 ≤ 2 条
- tag 类别数 ≥ 3（不足时日志警告）
- 不足 10 条时放宽约束填充

#### 历史去重优化

去掉高频词（餐饮/品牌/食品/消费/门店/市场/行业/中国/企业/发展/数据/报告/趋势/增长/下降/同比/环比/全国/连锁/加盟）后，剩余关键词重叠≥3 才判重复，降低误杀。

#### v1→v2 对比

| 维度 | v1 | v2 |
|------|-----|-----|
| 来源权重 | ~77% (100/130) | **30%** |
| 内容权重 | ~4% (5/130) | **40%** |
| 多样性 | 仅每媒体≤3条 | 每媒体≤2 + 每tag≤3 + tag覆盖≥3 |
| 时效性 | 无 | 15% |
| 历史去重 | 全词匹配≥3 | 去高频词后≥3 |
| 空内容降权 | 无 | 内容分=0时来源分打5折 |

> JSON 输出含 `_debug` 字段：`{src, content, time, scarcity, total}`，方便调试每条新闻得分明细

**⚠️ 已知坑：**
- `fetch-news.js` 用 CDP 控制真实 Chrome，**不是 Kimi API**，无需任何 API Key
- headless 模式会被反爬拦截，必须用真实 Chrome（connect 模式）
- 各媒体 JS 渲染，用 `domcontentloaded` + 3秒等待后抓 `<a>` 链接文本（超时30秒）

**质量门槛**（标题必须满足其一才保留）：
含具体数字（%/亿/万）、知名品牌名（瑞幸/海底捞/星巴克等TOP_BRANDS列表36个）、或明确事件动词（开店/关店/融资/收购/涨价/发布/推出等22个）。泛泛描述性标题直接丢弃。

**标题长度**：12-60字（太短无信息量，太长是摘要不是标题）

每个媒体最多保留 3 条，总输出经贪心选择后 **10 条**精选。

---

## Step 2: 内容审核（强制执行，不可跳过）

**逐条检查每一条新闻，判断是否符合「餐饮行业相关」标准：**

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

### 审核流程
1. 读取 `news-{YYYY-MM-DD}.json`，列出全部10条标题
2. 逐条判断是否合格，标注 ✅ / ❌
3. 不合格条目：记录原因 + 将关键词加入 `fetch-news.js` 的 EXCLUDE_KEYWORDS，然后**重新执行 Step 1**
4. 若合格条目 < 5 条，执行 **WebSearch 补充采集**（见下方），而非盲目重跑 CDP
5. **跨天去重**：对比前一天日报 `{前一天}-餐饮日报.md`，剔除已在前一天报道过的同一事件（标题关键词重叠≥3 或同一 eventKey）
5b. **年份核查（高风险类别强制执行）**：凡标题含以下关键词之一，必须核查新闻确实发生在当年（{YYYY}）：
   - **触发词**：IPO、超购、上市、全流通、H股、纳斯达克、年报、峰会、榜单、发布会
   - **核查方法（满足其一即通过）**：
     1. URL 中含当年年份（如 `/2026/`）
     2. 正文中明确出现"{YYYY}年"字样
     3. 文章发布日期（publish date）确实在 {YYYY} 年内
   - **不通过**：标注 `⚠️年份待确认` 并**剔除**；不可因标注了日期（如"04-16"）就默认为当年——月/日相同的历史事件每年都会出现
   - **典型陷阱**：IPO 超购、连锁峰会榜单、品牌上市——这些是年度性事件，标题完全相同但年份不同，AI 采集时极易引入前一年数据
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
node generate-md.js {YYYY-MM-DD}
```

输出到 `01 Projects/餐饮日报/{YYYY-MM-DD}-餐饮日报.md`。

MD 中图片嵌入路径格式（固定，不要改）：
```
![[01 Projects/餐饮日报/assets/{YYYY-MM-DD}-餐饮日报.png]]
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

**数据速览表**（可选，有 3+ 个数据点时添加）：在所有新闻条目之后、数据来源之前，用 Markdown 表格汇总当日关键数据指标。

---

## Step 4: 生成信息图（v2 模板 · HTML + Puppeteer 截图）

**标准流程：复制前一天 HTML → 文本替换 → 截图。禁止从零重写 HTML。**

### 4a. 复制模板 + 文本替换

```bash
# 1. 复制前一天的 HTML 作为模板（保持完整 CSS + 结构不变）
powershell -Command "Copy-Item '...assets/{前一天}-餐饮日报.html' '...assets/{YYYY-MM-DD}-餐饮日报.html'"

# 2. 用 Node.js 脚本做文本替换（日期 + logo + 新闻内容）
# 不要用 Agent 从零写 HTML，不要分段读大文件
```

**替换内容清单（仅改文字，CSS 和 HTML 结构一律不动）：**

1. **日期**：`前一天日期 → {YYYY.MM.DD}`，`星期X → 星期Y`
2. **Logo**：保持 base64 内嵌不变（已在模板里），确认 `<img class="logo-img" src="data:image/jpeg;base64,...">` 格式正确
3. **headline**：由 `build-html.js` 的 `buildHeadlineHtml()` 自动生成，**禁止手动拼数字**。
   - 逻辑：识别当天主要议题（品牌年报 > 行业报告 > 供应链 > 政策 > 出海融资），提炼"主题词 + 核心数字"组成有意义的句子
   - 第1行：`{主题词} <span>{核心数字}</span>`，如 `海底捞年报 <span>432亿</span>`
   - 第2行：从其余新闻提炼2-3个议题关键词，如 `外卖 · 连锁化`
   - **禁止**：把KPI三格的数字直接拼成标题（如"432亿·6800亿·747万家"）
4. **subline**：更新为今日关键词摘要，格式 `关键词1 · 关键词2 · 关键词3 — 今日N条精选`
5. **KPI 3格**：由 `build-html.js` 的 `extractKpisFromNews()` 自动从当日新闻动态提炼，**禁止硬编码**。
   - tag：品牌名+动词（如"海底捞年报"）或行业主题词（如"餐饮连锁化"、"预制菜"）
   - num：新闻中提取的核心数字
   - desc：新闻标题前18字摘要（不是来源名）
   - 优先级：万亿 > 亿 > 万家/万店 > % > 其他；同tag去重取最高优先级
6. **各板块新闻**：按分类替换（保持每条 news-item 的 HTML 结构不变，只改文字和 SVG 图标）
7. **footer 来源列表**：更新为今日实际来源

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

```bash
cd "...assets/"
node -e "
const puppeteer = require('C:\\Users\\杨顺\\Documents\\gaoyan-tools\\node_modules\\puppeteer-core');
const path = require('path');
(async () => {
  const b = await puppeteer.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
    headless: true, args: ['--no-sandbox']
  });
  const p = await b.newPage();
  await p.setViewport({ width: 800, height: 600, deviceScaleFactor: 2 });
  const f = 'file:///' + path.resolve('{YYYY-MM-DD}-餐饮日报.html').replace(/\\\\/g, '/');
  await p.goto(f, { waitUntil: 'networkidle0', timeout: 30000 });
  const h = await p.evaluate(() => document.querySelector('.card').scrollHeight);
  await p.setViewport({ width: 800, height: h, deviceScaleFactor: 2 });
  await p.screenshot({ path: '{YYYY-MM-DD}-餐饮日报.png', fullPage: true });
  await b.close();
})();
"
```

**⚠️ 截图已知坑：**
1. **sandbox 限制**：如果 Bash 工具报 Chrome 路径被拒，用 Agent 子进程执行截图
2. **验证尺寸**：`file` 命令确认 `800 x XXXX`（@2x 实际 1600 宽），不是 `800 x 1440`（那是 AI 生图）
3. **Obsidian 缓存**：文件替换后 Obsidian 可能不刷新，关掉重开笔记即可

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

- 2026-04-19（年份核查规则）：
  - **根本问题**：IPO/上市/峰会榜单等年度性事件，标题月/日相同但年份不同，AI 采集时引入前一年数据（如绿茶集团IPO超购118倍实为2025年事件）
  - **修复**：Step 2 审核流程新增步骤 5b「年份核查」——触发词（IPO/超购/上市/全流通/年报/峰会/榜单）命中时，必须通过 URL 年份、正文年份或发布日期三选一验证，不通过直接剔除

- 2026-04-20（周报内容核查实践 + 趋势表折行修复）：
  - **实践案例**：W16 周报在人工复核时发现 3 条错误年份新闻——绿茶集团 IPO 超购（2025年）、安井食品/锅圈资本化（餐饮界合集内混入2025数据）、多行业年报分化（5b 触发词"年报"应触发核查），分别替换为：泸溪河A+轮融资（小食代 URL 含 /2026/04/09/）、FBIC 2026 无锡创新博览会（04-15~17, Foodaily）
  - **陷阱提示**：餐饮界"大事件合集"体裁（如 canyinj.com/news/2278X.html）会把多个事件合并进一篇，单条事件的年份无法从 URL 判断，须逐条核查正文年份
  - **CSS 修复**：趋势表 `.trend-badge` 加 `white-space: nowrap`，防止表格列宽压缩时强度标签（"爆发"/"上升"）被折成两行

- 2026-04-19（周末版质量问题修复 + MD 深度要求）：
  - **根本问题1**：CDP 周末采集质量差（T1 媒体 DNS 失败，仅 7 条，其中 3 条垃圾），无补充机制
  - **修复1**：Step 2 新增 WebSearch 补充采集流程——CDP 合格 < 5 条时，用 WebSearch 搜索 3-4 组关键词补充，目标 5-8 条
  - **根本问题2**：不合格情形规则不完整，产品列表页（含价格标签）和保健食品通过了审核
  - **修复2**：Step 2 不合格情形新增"产品列表页"和"保健食品/保健品"两条规则
  - **根本问题3**：跨天去重只在 fetch-news.js 层做，Step 2 审核未再次检查，导致前一天已报道的事件重复出现
  - **修复3**：Step 2 审核流程新增第5步"跨天去重"——对比前一天 MD 文件，同一事件不重复收录
  - **根本问题4**：MD 日报 summary = 标题复制，缺少深度分析和高岩视角
  - **修复4**：Step 3 新增 MD 内容质量要求——每条必须有深度 summary（含数据）+ 🔷 高岩视角 + 来源标注；禁止 summary 复制标题；有 3+ 数据点时加数据速览表

- 2026-04-19（Step 2 审核强化 + Step 3 深度要求 + WebSearch 补充流程）：
  - **根本问题1**：CDP 周末采集质量差（T1 媒体 DNS 失败），7条中3条是垃圾（产品列表页、保健食品、展会通知），无兜底机制
  - **修复1**：Step 2 不合格情形新增"产品列表页"、"保健食品"、"同一事件重复"、"与前一天日报重复的事件"四类排除规则
  - **修复2**：新增 WebSearch 补充采集流程——CDP 合格 < 5 条时，用 WebSearch 搜索 3-4 组关键词补充，目标 5-8 条；周末版可接受 5 条，不强制凑数
  - **根本问题2**：MD 日报 summary 直接复制标题，无增量信息；缺少高岩视角，日报与普通新闻聚合无差异
  - **修复3**：Step 3 新增 MD 内容质量要求（v2）：每条必须有深度 summary（含原文数据）+ 🔷 高岩视角（业务相关性分析）；禁止 summary 复制标题；区分"多源验证"和"待核查"标注
  - **修复4**：Step 2 审核流程第4步改为"先检查 log → 重跑 → 仍不足则 WebSearch 补充"，不再盲目重跑 CDP

- 2026-04-18（事件指纹去重 + 空洞标题改写）：
  - **根本问题1**：跨天重复——同一事件不同媒体报道，或换个说法就绕过关键词重叠≥3的去重逻辑
  - **修复1**：`fetch-news.js` 新增 `extractEventKey()` 函数，从标题提取"品牌_动词"事件指纹；`loadHistoryTitles()` 改为 `loadHistory()`，同时加载历史 title 和 eventKey；去重双重检查：eventKey 精确匹配 OR 关键词重叠≥3
  - **修复2**：JSON 输出新增 `eventKey` 字段，兼容旧 JSON（无 eventKey 时动态提取）
  - **根本问题2**：标题空洞但内容有价值（如"XX企业加速重塑行业价值"），summary 直接复制标题无增量信息
  - **修复3**：Step 2 审核流程新增第5步"空洞标题改写"——用 WebFetch 读原文提取核心数据点，改写 title 和 summary 后更新 JSON

- 2026-04-18（信息图生成脚本化 + 截图脚本重写）：
  - **新增 `build-html.js`**：从 `news-{date}.json` 直接生成当日信息图 HTML，自动读取 logo base64、按 tag 分组、生成 KPI 行、板块、footer，完整 v2 CSS 内嵌。用法：`node build-html.js 2026-04-18`
  - **重写 `screenshot.js`**：改用 CDP connect 模式（`puppeteer.connect({ browserURL: 'http://127.0.0.1:9222' })`），不再 launch 新 Chrome 实例。用法：`node screenshot.js 2026-04-18`。需先确保 Chrome 调试模式已启动（fetch-news.js 会自动启动）
  - **Step 4 流程更新**：不再强制复制前一天 HTML + 文本替换，改为 `node build-html.js {date}` 直接生成 → `node screenshot.js {date}` 截图，更可靠
  - **注意**：`fetch-news.js` 的 Tier0 日期阈值保持 `diffDays < 1.5`（当天或昨天），周末不放宽

- 2026-04-16（Tier0 宏观数据强制收录）：
  - **根本问题**：国家统计局社零月报/季报标题不含"餐饮"关键词（如"2026年3月份社会消费品零售总额增长1.7%"），被 `isFoodRelated()` 过滤掉，但该报告内含餐饮收入分项数据（Q1餐饮收入14623亿 +4.2%），是日报/周报必须包含的核心数据
  - **修复1**：`fetch-news.js` 新增 `TIER0_MUST_CAPTURE` 列表（社会消费品零售/居民收入和消费支出/国民经济/消费品市场），Tier0 来源标题命中即强制通过
  - **修复2**：质量门槛（hasQuality）对 Tier0 来源豁免（宏观数据标题无品牌/动词，但数据本身极重要）
  - **规则**：国家统计局每月/每季度发布的餐饮收入数据，是日报和周报必须包含的信息

- 2026-04-16（内容审核强化）：
  - **根本问题**：Step 2 只是"快速检查"，没有强制逐条判断和剔除机制，不合格内容（眼镜、家电等）直接流入日报
  - **修复**：Step 2 改为强制质量门：逐条标注 ✅/❌，不合格条目加入 EXCLUDE_KEYWORDS 后**必须重跑 Step 1**，合格 < 5 条时整体重跑
  - 同步修复 `fetch-news.js` 的 FOOD_KEYWORDS：增加限定性行业词，isFoodRelated() 加强来源感知判断

- 2026-04-16（执行原则修复）：
  - **根本问题**：Step 1 用了 `run_in_background: true`，脚本跑完后 AI 没有主动推进，卡在等通知状态
  - **修复**：Step 1 必须同步执行（`run_in_background: false`），每步完成立即进入下一步，全程不等用户确认
  - 在 skill 顶部新增"执行原则"段落，明确禁止后台执行新闻采集和中途停下等待用户

- 2026-04-12（首版）：完整流程建立，CDP 采集 + HTML 截图方案确认
- 2026-04-14（评分系统v2重构）：
  - 评分公式从 `来源分+tag分+核实+数据` 改为 **来源分(30%)+内容分(40%)+时效分(15%)+稀缺分(15%)**
  - 来源分从 T0=100/T4=30 缩为 T0=30/T4=10，**来源权重从77%降至30%**
  - 新增 `calcContentScore()`: 按品牌+事件动词+数字+政策+融资等多信号加分，最高40分
  - 新增 `calcTimelinessScore()`: 按时间词判断时效性，最高15分
  - 新增 `greedySelect()` 贪心选择算法替代简单 top-N：同tag≤3、同来源≤2、tag覆盖≥3
  - 稀缺分在选择阶段动态计算：唯一tag+10、稀有tag+5、冗余惩罚-5
  - 历史去重增加 HIGH_FREQ_WORDS 过滤，降低误杀率
  - 标题长度从 10-80 改为 12-60
  - JSON 输出新增 `_debug` 字段显示每条得分明细
  - TOP_BRANDS 扩展至 36 个品牌
  - **内容分=0时来源分打5折**（空洞标题不靠来源撑排名）
  - **CDP超时从20s→30s，JS等待从2s→3s**（减少T1媒体超时失败）
- 2026-04-14（历史去重修复）：
  - `fetch-news.js` 新增 `loadHistoryTitles()` 函数，读取最近7天 `news-*.json`，采集时跳过已出现过的标题（关键词重叠≥3视为重复）
  - 解决问题：同一条新闻在多天日报中重复出现
- 2026-04-13（信息图重设计）：
  - 整体风格从深色报告模式改为**白底简洁排版**，背景米白 `#f0ece7`
  - 高亮色从厨人黄改为**高岩蓝 `#246AFF`**，箭头用青绿 `#01EFC1`
  - 右上角 Logo 使用真实 `高岩 Logo-中文 jpg.jpg`，**base64 内嵌**避免浏览器跨目录限制
  - 信息图**移除核实标注**（仅 MD 保留）
  - 每条新闻增加**语义化定制 SVG 图标**（40px 圆角方块），按具体内容设计，非通用 emoji
- 2026-04-14（信息图 v2 模板标准化）：
  - **Step 4 全面重写**：固定 v2 设计规范，包含完整 CSS、HTML 结构、色彩系统、板块配色表、SVG 图标库
  - **制作流程标准化**：复制前一天 HTML → Node.js 文本替换 → Puppeteer 截图，禁止从零重写
  - **效率规则写入**：禁止 Agent 重写 HTML、禁止分段读大文件，总耗时≤1分钟
  - **Logo 修复**：`<img>` 必须有 `class="logo-img"` 和 `src="data:image/jpeg;base64,..."` 完整格式
  - **6板块配色表固定**：政策/国际/资本/中游/茶饮/下游各有独立色系，按当天内容灵活增减板块
  - 信息图输出宽度从 900px 改为 **800px**（@2x = 1600px），与 viewport 匹配

---

## 文件结构速查

```
01 Projects/餐饮日报/
  assets/
    fetch-news.js          ← CDP 新闻采集脚本
    generate-md.js         ← MD 日报生成脚本
    build-html.js          ← 从 news JSON 生成信息图 HTML（v2 模板内嵌）
    screenshot.js          ← Puppeteer CDP 截图（connect 模式）
    render.js              ← 旧版简单截图（不用）
    {YYYY-MM-DD}-餐饮日报.png  ← 信息图（Obsidian 嵌入的目标文件）
    news-{YYYY-MM-DD}.json
    log-{YYYY-MM-DD}.txt
  {YYYY-MM-DD}-餐饮日报.md    ← Markdown 日报

infographic/catering-daily-report-{YYYYMMDD}/
  infographic.html         ← 手写信息图 HTML
  screenshot.js            ← Puppeteer 截图脚本
  infographic-v3.png       ← 截图输出（同步到上面 assets 目录）
  gen.js                   ← DashScope AI 生图（历史遗留，不用于日报）
```
