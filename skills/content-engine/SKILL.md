# Content Engine

> Multi-platform content from source material, not generic post formulas.

## When to activate

Trigger on: repurposing articles/reports/transcripts into social posts, creating multi-platform content calendars, adapting one piece for X/LinkedIn/TikTok/YouTube/newsletters/WeChat/Xiaohongshu.

## Non-negotiables

1. **Start from source material** — articles, reports, demos, transcripts, prior posts. Never start from "write me a post about X."
2. **One post = one concrete claim** — no post tries to say three things.
3. **Adapt format for platform, not persona** — same voice, different structure.
4. **Strip corporate jargon** — "game-changer," "rapidly evolving landscape," "synergy" are banned.
5. **No engagement bait** — unless explicitly requested, skip "Agree? 👇" and "Most people don't realize…"
6. **Match author voice** — not platform stereotype. A technical founder sounds technical everywhere, just shorter on X.

## Process

### 1. Source ingestion
Identify all source material: reports, articles, daily briefs, transcripts, prior posts, data sets.

### 2. Atomic extraction
Extract 3-7 atomic ideas from the source. Each atomic idea is:
- One specific claim or insight
- Defensible with evidence from the source
- Interesting enough to stand alone

### 3. Rank by sharpness
Score each idea on:
- **Novelty** — would the audience already know this?
- **Specificity** — is there a number, name, or example attached?
- **Tension** — does it challenge a common assumption?

### 4. Platform assignment
Assign one idea per platform post. Adapt structure:

| Platform | Format | Length | Hook style |
|----------|--------|--------|------------|
| X/Twitter | Thread or single | 280 chars / 5-8 tweets | Data point or contrarian claim |
| LinkedIn | Story or insight | 150-300 words | Professional observation |
| WeChat/公众号 | Long-form | 800-2000 words | Problem statement |
| 小红书 | Visual + text | 300-500 words | Practical tip or list |
| Newsletter | Deep dive | 500-1500 words | Question or story |
| TikTok/短视频 | Script | 30-60 seconds | Pattern interrupt |

### 5. Quality check
- [ ] Each post contains exactly one idea
- [ ] No banned language
- [ ] Voice consistent with author samples
- [ ] Platform format constraints met
- [ ] Source attribution included where needed

## Brand voice integration

If multiple outputs need consistent style, use `brand-voice` skill first to establish:
- Vocabulary whitelist/blacklist
- Sentence length range
- Tone markers (humor level, formality, directness)
- Example posts rated good/bad with reasons

## Output format

Deliver as a content batch:
```
## [Platform] — [Idea label]
[Content]
---
Source: [reference]
Atomic idea: [the underlying claim]
```
