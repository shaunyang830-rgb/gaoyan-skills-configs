# -*- coding: utf-8 -*-
"""
从「高岩全文入库 MD」中拆分：
- *_原文.md：自「## 逐页抽取」起的 OOXML + 逐页 Slide 底稿（含 tsv / chart 解析）
- *_重点页全文.md：每页统一「重点页」版式（核心观点 / 要点摘要 / 表格 / 数据来源 / 技术附录指向）
- *_摘要.md：报告级摘要 + 逐页一句话速览表

输入：单一大文件，须含「## 逐页内容」与「### Slide N」结构（由 _pptx_full_extract 等生成）。
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple

# 母版噪声：非本报告英文占位
_NOISE_EN = re.compile(
    r"mRNA|RNA assets|therapy|pipeline|cancer|As of 2022|Novel cancer|BRCA|Anti-aging|Treatments addressing",
    re.I,
)
_ZH = re.compile(r"[\u4e00-\u9fff]")


def strip_english_template_blocks(body: str) -> str:
    """剔除 PPT 母版误入的整段英文（如 Slide 4 医疗占位），保留后续中文论述。"""
    lines = body.splitlines()
    out: List[str] = []
    skipping = False
    for line in lines:
        s = line.strip()
        if not skipping and _NOISE_EN.search(s) and not _has_chinese(s):
            skipping = True
            continue
        if skipping:
            if _has_chinese(s) and len(re.sub(r"\s+", "", s)) >= 6:
                skipping = False
                out.append(line)
            continue
        out.append(line)
    return "\n".join(out)


def _has_chinese(s: str) -> bool:
    return bool(_ZH.search(s))


def _is_noise_line(line: str) -> bool:
    s = line.strip()
    if not s:
        return True
    if s in ("**要点与正文**", "**表格（从 PPT 结构提取）**"):
        return True
    if re.fullmatch(r"\d{1,3}", s):
        return True
    if s.startswith("**关联图表**") or s.startswith("**图表数据"):
        return True
    if s.startswith("**图表 XML"):
        return True
    if s.startswith("**数值序列**"):
        return True
    if s.startswith("**类别序列**"):
        return True
    if s.startswith("```"):
        return True
    if s.startswith("|") and "---" in s:  # md separator inside table block
        return False
    if s.startswith("数据来源"):
        return True
    if _NOISE_EN.search(s) and not _has_chinese(s):
        return True
    if len(s) < 3:
        return True
    return False


def _title_display(raw: str) -> str:
    """PPT 艺术字「驱 动 因 素」→「驱动因素」。"""
    s = raw.strip()
    if _has_chinese(s) and not re.search(r"[a-zA-Z]{4,}", s):
        s = re.sub(r"\s+", "", s)
    else:
        s = re.sub(r"\s{2,}", " ", s).strip()
    if len(s) > 72:
        s = s[:69] + "…"
    return s


def infer_title(slide_num: int, body: str) -> str:
    """取版式上**第一条**像样的中文标题，避免长文段落被误作标题。"""
    body = strip_english_template_blocks(body)
    lines = body.splitlines()
    for line in lines:
        raw = line.strip()
        if _is_noise_line(raw):
            continue
        if raw.startswith("**") and raw.endswith("**") and len(raw) < 40:
            continue
        if raw.startswith("|"):
            continue
        if not _has_chinese(raw):
            continue
        compact = re.sub(r"\s+", "", raw)
        if len(compact) < 4:
            continue
        # 纯数字+量级作标题过弱，跳过
        if re.fullmatch(r"[\d\.\s,%亿万千\+\-↑↓]+", compact):
            continue
        # 长段更像正文：多逗号且超长
        if raw.count("，") >= 3 and len(raw) > 100:
            continue
        show = _title_display(raw)
        if len(show) > 72:
            show = show[:69] + "…"
        if slide_num == 1 and len(show) < 6:
            continue
        return show
    return f"Slide {slide_num}"


def _is_cv_noise(s: str) -> bool:
    if re.match(r"^(前|曾任|曾于)", s) and ("总经理" in s or "商务官" in s or "麦肯锡" in s or "评委" in s):
        return True
    if re.match(r"^\d+年\+", s):
        return True
    if "FOODAILY" in s or "iSEE" in s:
        return True
    return False


def infer_thesis(body: str) -> str:
    """优先取第一条「长句型」中文论述行（含逗号或足够长），避免拼接简历与脚注。"""
    body = strip_english_template_blocks(body)
    lines = []
    for line in body.splitlines():
        s = line.strip()
        if not s or s.startswith("|") or s.startswith("```"):
            continue
        if s.startswith("**关联") or s.startswith("**图表"):
            break
        if s.startswith("数据来源"):
            break
        if s == "**要点与正文**":
            continue
        if re.fullmatch(r"\d{1,3}", s):
            continue
        if _is_noise_line(s) and not _has_chinese(s):
            continue
        if not _has_chinese(s):
            continue
        if _is_cv_noise(s):
            continue
        if len(s) < 8:
            continue
        lines.append(s)

    for s in lines:
        compact = re.sub(r"\s+", "", s)
        if len(compact) < 10:
            continue
        if "，" in s or "。" in s or "：" in s:
            if len(compact) >= 14:
                if "。" in s:
                    return s[: s.index("。") + 1][:400]
                return s[:220] + ("…" if len(s) > 220 else "")
        if len(compact) >= 22:
            return s[:220] + ("…" if len(s) > 220 else "")

    if lines:
        blob = re.sub(r"\s+", " ", lines[0]).strip()
        return blob[:220] + ("…" if len(blob) > 220 else "")
    return "（本页以版式、图示或短标题为主，结论见要点摘要与表格。）"


def bullet_points(body: str, max_items: int = 6) -> List[str]:
    """从正文中抽短句作要点（非表格、非代码）。"""
    body = strip_english_template_blocks(body)
    items: List[str] = []
    for line in body.splitlines():
        s = line.strip()
        if not s or s.startswith("|") or s.startswith("```"):
            continue
        if s.startswith("**关联") or s.startswith("**图表"):
            break
        if s.startswith("数据来源"):
            break
        if s == "**要点与正文**":
            continue
        if re.fullmatch(r"\d{1,3}", s):
            continue
        if _NOISE_EN.search(s) and not _has_chinese(s):
            continue
        if 15 <= len(s) <= 160 and _has_chinese(s):
            if s.endswith("：") or len(s) < 25:
                continue
            items.append(s)
        if len(items) >= max_items:
            break
    # 去重保序
    seen = set()
    out = []
    for x in items:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out[:max_items]


def extract_markdown_tables(body: str) -> List[str]:
    lines = body.splitlines()
    blocks: List[str] = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("|") and line.count("|") >= 2:
            j = i
            buf: List[str] = []
            while j < len(lines) and lines[j].strip().startswith("|"):
                buf.append(lines[j].rstrip())
                j += 1
            if len(buf) >= 2:
                blocks.append("\n".join(buf))
            i = j
            continue
        i += 1
    return blocks


def extract_data_source(body: str) -> str | None:
    for line in body.splitlines():
        if "数据来源" in line and ":" in line:
            return line.strip()
    return None


def strip_tech_blocks(body: str) -> str:
    """去掉图表 xml/tsv 块，仅保留叙述与表格（用于要点摘要区不重複大段）。"""
    out: List[str] = []
    skip = False
    for line in body.splitlines():
        if line.strip().startswith("```"):
            skip = not skip
            continue
        if skip:
            continue
        if line.startswith("**关联图表**"):
            break
        out.append(line)
    return "\n".join(out).strip()


def parse_slides(逐页内容: str) -> List[Tuple[int, str]]:
    parts = re.split(r"^### Slide (\d+)\s*$", 逐页内容, flags=re.MULTILINE)
    # parts[0] is preamble (often whitespace)
    slides: List[Tuple[int, str]] = []
    i = 1
    while i + 1 < len(parts):
        num = int(parts[i])
        body = parts[i + 1]
        slides.append((num, body))
        i += 2
    slides.sort(key=lambda x: x[0])
    return slides


def build_structured_md(
    report_title: str,
    出品: str,
    数据截止: str,
    页码说明: str,
    koujing_bullets: List[str],
    slides: List[Tuple[int, str]],
    原文_link: str,
) -> str:
    lines: List[str] = [
        "---",
        f'title: "{report_title}（重点页全文）"',
        "tags: [高岩科技, 高岩文件库, 重点页全文, 专业入库]",
        'summary: "逐页「重点页」版式：核心观点、要点摘要、表格与数据来源；数值底稿见联动原文笔记。"',
        "links: [高岩, 重点页, 蓝皮书, 全文入库]",
        "date_processed: auto",
        "---",
        "",
        f"# {report_title}",
        "",
        f"出品：{出品}",
        f"数据截止：{数据截止}",
        f"页码：{页码说明}",
        "",
        "> 数值与图表 XML、xlsb 导出全文见："
        + f" [[{原文_link}]]（原文·底稿）。",
        "",
        "## 口径说明",
        "",
    ]
    for b in koujing_bullets:
        lines.append(f"- {b}")
    lines.append("")
    for num, body in slides:
        title = infer_title(num, body)
        thesis = infer_thesis(strip_tech_blocks(body))
        bullets = bullet_points(strip_tech_blocks(body))
        tables = extract_markdown_tables(body)
        ds = extract_data_source(body)

        lines.append(f"## 重点页：Slide {num}｜{title}")
        lines.append("")
        lines.append(f"**核心观点**：{thesis}")
        lines.append("")
        lines.append("**要点摘要**")
        lines.append("")
        if bullets:
            for b in bullets:
                lines.append(f"- {b}")
        else:
            lines.append("- （见核心观点与下表。）")
        lines.append("")
        if tables:
            for ti, tbl in enumerate(tables, 1):
                if len(tables) > 1:
                    lines.append(f"### 表 {ti}")
                    lines.append("")
                lines.append(tbl)
                lines.append("")
        if ds:
            lines.append(ds)
            lines.append("")
        lines.append(
            f"**技术附录**：图表 `c:f`、xlsb `tsv` 见原文 [[{原文_link}]]（检索 `### Slide {num}`）。"
        )
        lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def build_summary_md(
    report_title: str,
    slides: List[Tuple[int, str]],
    重点页_link: str,
    原文_link: str,
) -> str:
    # 报告级摘要：优先取前言/定位页（Slide 2）+ 数据总览（Slide 9）各一句，避免堆叠封面免责声明
    pick_idx = [i for i in (1, 8) if i < len(slides)]
    global_lines: List[str] = []
    for i in pick_idx:
        _, body = slides[i]
        t = infer_thesis(strip_tech_blocks(body))
        if len(t) > 25 and "（本页" not in t:
            global_lines.append(t)
    if not global_lines:
        for _, body in slides[1:5]:
            t = infer_thesis(strip_tech_blocks(body))
            if len(t) > 25 and "（本页" not in t:
                global_lines.append(t)
                if len(global_lines) >= 2:
                    break
    exec_blob = " ".join(global_lines)
    if len(exec_blob) > 520:
        exec_blob = exec_blob[:517] + "…"

    rows = ["| Slide | 页题 | 一句话 |", "| --- | --- | --- |"]
    for num, body in slides:
        tit = infer_title(num, body)
        one = infer_thesis(strip_tech_blocks(body)).replace("|", "\\|")
        if len(one) > 100:
            one = one[:97] + "…"
        rows.append(f"| {num} | {tit.replace('|', '\\|')} | {one} |")

    return (
        "---\n"
        f'title: "{report_title}（摘要）"\n'
        "tags: [高岩科技, 摘要, 速览]\n"
        'summary: "报告级短摘要 + 58 页一句话速览表；细节见重点页全文与原文底稿。"\n'
        "---\n\n"
        f"# {report_title} · 摘要\n\n"
        f"**完整重点页版**：[[{重点页_link}]] ｜ **数据底稿原文**：[[{原文_link}]]\n\n"
        "## 报告级摘要\n\n"
        f"{exec_blob or '（见各页一句话速览。）'}\n\n"
        "## 逐页一句话速览\n\n"
        + "\n".join(rows)
        + "\n"
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input_md", type=Path, help="合并入库 MD（含 ## 逐页内容）")
    ap.add_argument("--title", default="", help="报告主标题（默认从 frontmatter 或文件名推断）")
    args = ap.parse_args()
    inp: Path = args.input_md.resolve()
    if not inp.exists():
        print("File not found:", inp, file=sys.stderr)
        return 1
    text = inp.read_text(encoding="utf-8")

    fm_title_m = re.search(r"^title:\s*\"([^\"]+)\"", text, re.MULTILINE)
    report_title = args.title or (fm_title_m.group(1) if fm_title_m else inp.stem)
    # 去掉括号后缀 cleaner
    report_title = re.sub(r"（[^）]+）$", "", report_title).strip()

    idx_extract = text.find("## 逐页抽取")
    idx_content = text.find("## 逐页内容")
    idx_footer = text.find("\n## 高岩关联洞察")
    if idx_content < 0:
        print("Missing ## 逐页内容", file=sys.stderr)
        return 1
    if idx_extract < 0:
        print("Missing ## 逐页抽取", file=sys.stderr)
        return 1

    end_slides = idx_footer if idx_footer > 0 else len(text)
    逐页内容 = text[idx_content : end_slides]
    原文_segment = text[idx_extract:]
    if idx_footer > 0:
        原文_segment = text[idx_extract:end_slides] + text[idx_footer:]

    slides = parse_slides(逐页内容)
    if not slides:
        print("No slides parsed", file=sys.stderr)
        return 1

    stem = inp.stem
    if stem.endswith("_20260426"):
        base = stem
    else:
        base = stem

    path_原文 = inp.with_name(f"{base}_原文.md")
    path_重点 = inp.with_name(f"{base}_重点页全文.md")
    path_摘要 = inp.with_name(f"{base}_摘要.md")

    obs_原文 = path_原文.stem
    obs_重点 = path_重点.stem
    obs_摘要 = path_摘要.stem

    原文_md = (
        "---\n"
        f'title: "{report_title}（原文·OOXML 与图表底稿）"\n'
        "tags: [高岩科技, 原文, 图表底稿, xlsb]\n"
        'summary: "逐页抽取：正文、Markdown 表、xlsb TSV、chart XML 解析；供审计与数值核对。"\n'
        "---\n\n"
        f"# {report_title} · 原文底稿\n\n"
        f"**重点页可读版**：[[{obs_重点}]] ｜ **摘要**：[[{obs_摘要}]]\n\n"
        + 原文_segment.lstrip()
    )
    path_原文.write_text(原文_md, encoding="utf-8")

    口径 = [
        "数据来源以各页脚注为准；「—」表示原图未标同比或无法对齐项。",
        "图表 `tsv` 为 xlsb 导出，与幻灯片视觉不一致时以 **PPT 配图** 为准。",
    ]

    重点_body = build_structured_md(
        report_title=report_title,
        出品="高岩科技 · 高岩餐饮研究院（按原稿）",
        数据截止="见各页标注；行业数据以 **2025 年** 为主、部分展望 **2026**（与原稿一致）。",
        页码说明=f"Slide 1–{slides[-1][0]}，与 PPT 页序一致。",
        koujing_bullets=口径,
        slides=slides,
        原文_link=obs_原文,
    )
    path_重点.write_text(重点_body, encoding="utf-8")

    摘要_body = build_summary_md(report_title, slides, obs_重点, obs_原文)
    path_摘要.write_text(摘要_body, encoding="utf-8")

    path_index = inp.with_name(f"{base}_入库索引.md")
    index_md = (
        "---\n"
        f'title: "{report_title}（入库索引）"\n'
        "tags: [高岩科技, 入库索引, 现制饮品]\n"
        'summary: "本主题三份笔记：重点页全文 / 摘要 / 原文底稿；从此页跳转。"\n'
        "---\n\n"
        f"# {report_title}\n\n"
        "本报告已拆分为专业入库三件套（由 `gaoyan-ingest-full-version` 流程生成）：\n\n"
        f"1. **[[{obs_重点}]]** — 逐页「重点页」版式（核心观点、要点、表、数据来源）。\n"
        f"2. **[[{obs_摘要}]]** — 报告摘要 + 逐页一句话速览表。\n"
        f"3. **[[{obs_原文}]]** — OOXML 抽取 + xlsb/chart XML 数值底稿。\n\n"
        "合并抽取母文件（若仍保留）：\n"
        f"`[[{inp.stem}]]`\n\n"
        "更新母文件后重新生成三件套：\n\n"
        "```bash\n"
        "python .claude/skills/gaoyan-ingest-full-version/scripts/slide_appendix_to_structured.py "
        f'"{inp.as_posix()}"\n'
        "```\n"
    )
    path_index.write_text(index_md, encoding="utf-8")

    print("Wrote:", path_原文)
    print("Wrote:", path_重点)
    print("Wrote:", path_摘要)
    print("Wrote:", path_index)
    return 0


if __name__ == "__main__":
    sys.exit(main())
