---
name: gaoyan-weekly-review
description: 生成高岩科技餐饮周报（汇总本周日报要点 + 信息图 HTML + Puppeteer 截图 → Markdown 周报）
---

# 高岩科技餐饮周报生成器

你是高岩科技的知识管理助手。每周生成一份餐饮周报，包含信息图（Apple 深色 UI 9-section 全页）和 Markdown 周回顾。

## 触发方式

- `/gaoyan-weekly-review`
- `/gaoyan-weekly-review 2026-04-28`（指定某周）
- "帮我做本周周报"、"生成周报"

---

## Step 1: 确定时间范围

- 默认：本周一到今天
- 如果用户指定日期，以该日期所在周为准（周一至周日）
- 计算 ISO 周次（W18 = 第18周）

---

## Step 2: 采集本周内容

### 2.1 日报汇总
读取 `01 Projects/餐饮日报/日报/{YYYY}/{MM}/` 下本周的日报文件（格式 `YYYY-MM-DD-餐饮日报.md`）：
- 提取每天的"今日精选"标题和标签
- 识别本周高频话题和趋势
- 汇总 12 条代表性新闻（供信息图 NEWS section 使用）

### 2.2 报告进度
读取 `个人知识库/Report_Planner/` 下的报告任务：
- 筛选 status 为 "In progress" 或本周有更新的任务
- 提取 title、status、owner、due 信息

### 2.3 日记内容
读取 `日记/` 下本周的日记文件（格式 `YYYY-MM-DD.md`）：
- 提取关键记录和思考
- 注意隐私：只提炼要点，不要原文照搬敏感内容

### 2.4 知识库新增
用 PowerShell 检查本周新增或修改的文件：
```powershell
powershell -Command "Get-ChildItem -Path 'C:\Users\杨顺\Documents\Obsidian Vault' -Recurse -Filter '*.md' | Where-Object { $_.LastWriteTime -gt (Get-Date).AddDays(-7) -and $_.FullName -notmatch '\\.obsidian' } | Select-Object -ExpandProperty FullName"
```

---

## Step 3: 生成周报信息图（Apple 深色 UI 多分区全页风格）

**⚠️ 严格按此格式，不得使用 frontend-slides 模板、米白模板或任何其他模板。**

### 唯一参考模板

```
01 Projects/餐饮日报/周报/assets/2026-W17-餐饮周报.html
```

**每次生成新周报信息图，必须读取上方文件，复制其完整 CSS 和结构，仅替换内容。**
**W17 是经过验证的最新模板，包含正确的 logo 规则和完整的手机适配媒体查询。**

### 设计规范（已确认，不要自行修改）

| 参数 | 值 |
|------|----|
| 深色背景 | `--black: #051C2C`（深海军蓝，非纯黑） |
| 深色卡片 | `--dark-surface: #0A2D45` |
| 品牌深蓝 | `#0A2D45`（Brands section 背景） |
| 浅灰背景 | `--light-gray: #f5f5f7`（Themes / Insight section） |
| 纯白背景 | `--white: #ffffff`（News / Signals section） |
| 强调蓝 | `--apple-blue: #05ADE5` |
| 字体 display | `'Noto Serif SC', 'SF Pro Display', Helvetica, sans-serif` |
| 字体 body | `'Noto Sans SC', 'SF Pro Text', Helvetica, sans-serif` |
| 截图宽度 | `1440px`（deviceScaleFactor: 2，输出 @2x = 2880px 宽） |
| 手机截图宽度 | **`720px CSS`，deviceScaleFactor=1，fullPage=true，输出 720×N px** |

### ⚠️ HTML CSS 规范（严格对齐 W16，不得新增防溢出 hack）

```css
/* 正确：与 W16 完全一致 */
html { scroll-behavior: smooth; }           /* ← 不要加 overflow-x:hidden / max-width */
body { overflow-x: hidden; /* ...其他样式 */ }
/* 不要 .trends-wrapper。趋势表格直接用 <table class="trends-table">，不要包 div */
```

> **禁止** 在 `html` 元素上加 `overflow-x: hidden` 或 `max-width`：这会将 html 变成 scroll container，导致 Puppeteer fullPage 的 scrollHeight 计算错误，页面高度爆增 2.7x（实测 17864px vs 正常 13245px）。
>
> **禁止** `.trends-wrapper { overflow-x: auto }`：同上，嵌套 scroll container 同样触发 Puppeteer 高度错误。
>
> 720px 视口下 6 列趋势表恰好放入 700px section-inner，无需任何横向溢出处理。

### 内容结构（9 个 section，按顺序，不得省略）

1. **NAV** — 固定导航栏，含品牌名 + 锚链接 + W{N}·年份
2. **HERO** — 全屏深黑背景，高岩 logo + 周次大字（W{N} clamp 96-180px）+ 副标题 + 日期 + 话题标签
   - **⚠️ Logo 路径必须用绝对路径**（相对路径在 Puppeteer file:// 截图中会失效）：
     `<img src="C:/Users/杨顺/Documents/Obsidian Vault/01 Projects/餐饮日报/周报/assets/_archive/gaoyan-logo-hero.png" alt="高岩科技" />`
   - **⚠️ 字体不得使用 Google Fonts**（国内网络无法访问，导致页面崩溃）。改用系统字体：
     `--font-display: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft YaHei', 'PingFang SC', serif;`
     `--font-body: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft YaHei', 'PingFang SC', sans-serif;`
3. **STATS** — 深黑背景，5 个数据卡（`--dark-surface`），含数值/单位/标签/涨跌
4. **THEMES** — 浅灰背景，6 张白色主题卡，每张含 emoji + 标题 + 描述 + mini-tag
5. **NEWS** — 纯白背景，12 条新闻列表（category badge + 标题 + 描述 + 来源日期）
6. **BRANDS** — `#0A2D45` 深蓝背景，6 张品牌卡（左侧蓝色条纹 + 名称/类型 + 描述 + 3 组 metrics）
7. **TRENDS TABLE** — 深黑背景，8 行趋势榜表格（排名/方向/强度badge/验证事件/代表品牌/评级）
8. **SIGNALS** — 纯白背景，4 张洞察信号卡（彩色圆点 + 信号类型 + 标题 + 描述 + 链接）
9. **FOOTER** — 深黑背景，品牌名 + 版权说明 + 周次大字水印

> **⚠️ 高岩洞察（INSIGHT）不出现在信息图中。**
> 高岩洞察是面向内部的生意分析，仅在 **MD 文字版周报** 的「## 高岩洞察」章节中体现（含 4 条洞察卡：对高岩生意的意义和机会），不要放进 HTML 信息图。
> 信息图面向外部/分享场景，不含公司内部商业判断。

### 截图方法（使用本地 headless-shell，不依赖 CDP 连接）

**必须生成两张截图**。

> **⚠️ require 路径必须用绝对路径**：`puppeteer-core` 安装在 vault 根目录的 `node_modules`，不在 `assets/` 子目录，裸模块名 `require('puppeteer-core')` 会报 MODULE_NOT_FOUND。
>
> **⚠️ Chrome 路径必须用 headless-shell**：`chrome.exe` 在 headless 模式下可能有兼容问题，已验证可用的是 headless-shell：
> `C:\Users\杨顺\.cache\puppeteer\chrome-headless-shell\win64-146.0.7680.153\chrome-headless-shell-win64\chrome-headless-shell.exe`

#### ① 桌面截图（存档用，1440px）

```javascript
// screenshot-w{N}-desktop.js
const puppeteer = require('C:/Users/杨顺/Documents/Obsidian Vault/node_modules/puppeteer-core');
const CHROME    = 'C:/Users/杨顺/.cache/puppeteer/chrome-headless-shell/win64-146.0.7680.153/chrome-headless-shell-win64/chrome-headless-shell.exe';
const HTML_FILE = 'C:/Users/杨顺/Documents/Obsidian Vault/01 Projects/餐饮日报/周报/assets/{YYYY-WXX}-餐饮周报.html';
const OUT_FILE  = 'C:/Users/杨顺/Documents/Obsidian Vault/01 Projects/餐饮日报/周报/assets/{YYYY-WXX}-餐饮周报-screenshot.png';
(async () => {
  const browser = await puppeteer.launch({ executablePath: CHROME, headless: true, args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900, deviceScaleFactor: 2 });
  await page.goto('file:///' + HTML_FILE, { waitUntil: 'networkidle2', timeout: 30000 });
  await page.addStyleTag({ content: `*, *::before, *::after { animation-duration: 0s !important; transition-duration: 0s !important; } .stat-card, .theme-card, .news-item, .brand-card, .signal-card, .trends-table tbody tr { opacity: 1 !important; transform: none !important; }` });
  await page.evaluate(() => { document.querySelectorAll('.stat-card, .theme-card, .news-item, .brand-card, .signal-card, .trends-table tbody tr').forEach(el => { el.style.cssText += '; opacity: 1 !important; transform: none !important;'; }); });
  await new Promise(r => setTimeout(r, 2000));
  await page.screenshot({ path: OUT_FILE, fullPage: true });
  await browser.close();
  console.log('✅ 桌面截图完成 → ' + OUT_FILE);
})();
```

#### ② 手机截图（嵌入 MD 用，720px）— ⭐ 这是 Shaun 日常阅读的格式

**关键参数（已测试验证，不要改动）：**
- `width: 720, deviceScaleFactor: 1` → 输出 720px 宽 PNG
- `@media (max-width: 900px)` 在 720px 依然触发 → 单列布局 + 大字体
- 720px 下 6 列趋势表恰好放入 700px section-inner，无横向溢出
- `fullPage: true` 安全可用

```javascript
// screenshot-w{N}-mobile.js  ← 这才是嵌入 MD 的主图！
const puppeteer = require('C:/Users/杨顺/Documents/Obsidian Vault/node_modules/puppeteer-core');
const CHROME    = 'C:/Users/杨顺/.cache/puppeteer/chrome-headless-shell/win64-146.0.7680.153/chrome-headless-shell-win64/chrome-headless-shell.exe';
const HTML_FILE = 'C:/Users/杨顺/Documents/Obsidian Vault/01 Projects/餐饮日报/周报/assets/{YYYY-WXX}-餐饮周报.html';
const OUT_FILE  = 'C:/Users/杨顺/Documents/Obsidian Vault/01 Projects/餐饮日报/周报/assets/{YYYY-WXX}-screenshot.png';
(async () => {
  const browser = await puppeteer.launch({ executablePath: CHROME, headless: true, args: ['--no-sandbox', '--disable-setuid-sandbox'] });
  const page = await browser.newPage();
  await page.setViewport({ width: 720, height: 900, deviceScaleFactor: 1 });
  await page.goto('file:///' + HTML_FILE, { waitUntil: 'networkidle2', timeout: 30000 });
  await page.addStyleTag({ content: `*, *::before, *::after { animation-duration: 0s !important; transition-duration: 0s !important; } .stat-card, .theme-card, .news-item, .brand-card, .signal-card, .trends-table tbody tr { opacity: 1 !important; transform: none !important; }` });
  await page.evaluate(() => { document.querySelectorAll('.stat-card, .theme-card, .news-item, .brand-card, .signal-card, .trends-table tbody tr').forEach(el => { el.style.cssText += '; opacity: 1 !important; transform: none !important;'; }); });
  await new Promise(r => setTimeout(r, 2000));
  await page.screenshot({ path: OUT_FILE, fullPage: true });
  await browser.close();
  const fs = require('fs');
  const buf = Buffer.alloc(24); const fd = fs.openSync(OUT_FILE, 'r'); fs.readSync(fd, buf, 0, 24, 0); fs.closeSync(fd);
  console.log('✅ 手机截图完成：' + buf.readUInt32BE(16) + '×' + buf.readUInt32BE(20) + ' px → ' + OUT_FILE);
})();
```

---

## Step 4: 生成周报 MD 文件

### 文件路径（命名规范）

```
01 Projects/餐饮日报/周报/
  assets/
    {YYYY-WXX}-餐饮周报.html                ← HTML 信息图源文件
    {YYYY-WXX}-餐饮周报-screenshot.png      ← 桌面截图（1440px，存档）
    {YYYY-WXX}-screenshot.png               ← 手机截图（720px）← MD 嵌入用主图
  {YYYY-WXX}-餐饮周报.md                    ← 周报正文
```

### 周报 MD frontmatter + 嵌入格式

```markdown
---
title: 高岩科技餐饮周报
date: {YYYY-MM-DD}
week: {YYYY-WXX}
date_range: {YYYY-MM-DD} ~ {YYYY-MM-DD}
tags:
  - 餐饮周报
  - 高岩科技
type: weekly_report
summary: "{本周一句话摘要}"
---

# 高岩科技餐饮周报 | {YYYY}年第{N}周

<img src="./assets/{YYYY-WXX}-screenshot.png" width="720" alt="{YYYY}年第{N}周餐饮周报截图" />

**周期**：{YYYY.MM.DD} — {MM.DD}（共{N}期日报，精选12条）
```

**禁止用 `![[...]]` wikilink 格式嵌入截图——必须用 `<img>` HTML 标签，width="720"。**

### 周回顾正文格式

```markdown
## 📰 行业动态（日报汇总）

本周共发布 {N} 篇日报，核心话题：

- **{话题1}**：{一句话总结}
- **{话题2}**：{一句话总结}
- **{话题3}**：{一句话总结}

## 🔷 高岩洞察

> 本节为内部商业判断，不出现在信息图中。

- **洞察1**：{对高岩生意的意义和机会}
- **洞察2**：{对高岩生意的意义和机会}
- **洞察3**：{对高岩生意的意义和机会}
- **洞察4**：{对高岩生意的意义和机会}

## 📊 报告进度

| 报告 | 状态 | 负责人 | 截止日期 |
|------|------|--------|----------|
| {报告名} | {状态} | {owner} | {due} |

## 📝 本周记录

{从日记中提炼的关键思考和记录，2-5 条}

## 📁 知识库变动

本周新增/更新 {N} 个文件：
- {重要文件列表，最多 10 个}

## 💡 下周关注

{基于本周内容，建议下周关注的 2-3 个方向}

---
*由高岩科技 AI 助手生成 | {YYYY-MM-DD}*
```

---

## Step 5: 验证（脚本硬验证 + 内容自查）

### 5.1 脚本硬验证（真实验证，必须执行）

```bash
python3 -c "
import os, re, sys

week = '{YYYY-WXX}'  # 替换为实际周次，如 2026-W19
base = r'C:\Users\杨顺\Documents\Obsidian Vault\01 Projects\餐饮日报\周报'

md_file      = os.path.join(base, f'{week}-餐饮周报.md')
html_file    = os.path.join(base, 'assets', f'{week}-餐饮周报.html')
mobile_shot  = os.path.join(base, 'assets', f'{week}-screenshot.png')
desktop_shot = os.path.join(base, 'assets', f'{week}-餐饮周报-screenshot.png')

checks = {
    'MD 文件存在':       os.path.exists(md_file),
    'HTML 信息图存在':   os.path.exists(html_file),
    '手机截图存在':      os.path.exists(mobile_shot),
    '桌面截图存在':      os.path.exists(desktop_shot),
    'MD 文件非空(>1KB)': os.path.exists(md_file) and os.path.getsize(md_file) > 1024,
    '手机截图非空(>50KB)': os.path.exists(mobile_shot) and os.path.getsize(mobile_shot) > 50*1024,
}

# 读取 MD 内容做结构检查
if os.path.exists(md_file):
    with open(md_file, encoding='utf-8') as f: content = f.read()
    checks['frontmatter 完整'] = all(x in content for x in ['title:', 'week:', 'date_range:', 'summary:'])
    checks['含行业动态章节']   = '行业动态' in content
    checks['含高岩洞察章节']   = '高岩洞察' in content
    checks['含下周关注章节']   = '下周关注' in content
    checks['截图 img 标签存在'] = '<img src=' in content

failed = [k for k,v in checks.items() if not v]
if failed:
    print('❌ 验证失败：')
    for f in failed: print(f'  - {f}')
    sys.exit(1)
else:
    print(f'✅ 全部通过（{len(checks)} 项）')
"
```

**若任何一项失败，必须修复后重新运行，不得跳过。**

### 5.2 内容自查（Agent 自我评估，在 5.1 通过后执行）

- [ ] 如果某个板块本周没有内容，已标注"本周无更新"而不是留空
- [ ] 高岩洞察仅在 MD 中，未出现在 HTML 信息图里
- [ ] 下周关注基于实际内容，不是泛泛而谈

## 注意事项

- 日记内容注意隐私，只提炼工作相关要点
- 如果日报或日记为空，跳过对应板块
- "下周关注"要基于实际内容给出具体建议，不要泛泛而谈
- 高岩洞察仅在 MD 文字版中体现，**不放入信息图**

---

## 迭代记录

| 日期 | 变更 |
|------|------|
| 2026-05-03 | 从 weekly-review 重命名为 gaoyan-weekly-review，建立完整目录结构，统一路径为 `周报/assets/`，Step 2 采集改用 PowerShell 命令，补充高岩洞察章节规范 |
| 2026-05-03 | 参考模板从 W16 升级为 W17（`周报/assets/2026-W17-餐饮周报.html`）；修复 W18 HTML：补充 `.hero-logo img { height: 80px }` 规则 + 完整手机适配媒体查询（字体放大、单列布局）；W17 为当前标准模板 |
| 2026-05-03 | 参考模板从 W16 升级为 W17（`周报/assets/2026-W17-餐饮周报.html`）；修复 W18 信息图：补充 `.hero-logo img { height: 80px }` 规则 + 完整手机适配媒体查询（所有元素字体放大、单列布局）；W17 为当前标准模板 |
| 2026-05-03 | 修复截图脚本：`require('puppeteer-core')` → 绝对路径 `require('C:/Users/杨顺/Documents/Obsidian Vault/node_modules/puppeteer-core')`；Chrome 路径改为已验证的 headless-shell（`~/.cache/puppeteer/chrome-headless-shell/...`）；两处 ⚠️ 警告写入 SKILL.md 防止回退 |
| 2026-05-03 | 重构目录结构：日报 MD 读取路径改为 `日报/{YYYY}/{MM}/`；周报输出路径不变（`周报/` + `周报/assets/`）；同步 gaoyan-daily-report skill 的文件结构规范 |
