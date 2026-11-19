#!/usr/bin/env python3
"""中文开发者技术文档规范确定性检查工具（零第三方依赖）。

用于辅助审校 Markdown 技术文档中的机械性规范违例：
- 盘古之白（中英文/数字/行内代码留白、全角标点旁多余空格）
- 计量单位与百分号间距
- 标点与样式（感叹号、中文斜体、反引号外套引号、半角标点混用）
- 标题结构（多 H1、标题跳级、标题末尾句号）
- 高频禁用词、错别字、模糊链接锚文本、占位符前缀

示例用法：
  python3 scripts/lint_doc.py README.md
  python3 scripts/lint_doc.py docs/ --format markdown
  python3 scripts/lint_doc.py guide.md --format json --ignore P001,P002
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


SEVERITY_ORDER = {"P0": 0, "P1": 1, "P2": 2}

CJK_CHAR = r"\u4e00-\u9fff"
CJK_PUNCT = r"，。、：；！？（）【】《》“”‘’—"

# 常见英文计量单位（区分大小写，避免误匹配普通词或型号如 H1/v2/3D）
UNIT_PATTERN = (
    r"(?:KiB|MiB|GiB|TiB|PiB|KB|kB|MB|GB|TB|PB|B|bps|kbps|Kbps|Mbps|Gbps|"
    r"ms|us|ns|Hz|kHz|MHz|GHz|mm|cm|km|kg|mg|mL|dB)"
)

# 预编译正则
RE_FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
RE_HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
RE_INLINE_CODE = re.compile(r"(`+)([^`]+?)\1")
RE_MD_LINK = re.compile(r"(!?)\[([^\]]*)\]\(([^)]*)\)")
RE_URL = re.compile(r"https?://[^\s<>)\]]+")
RE_HTML_TAG = re.compile(r"</?[A-Za-z][A-Za-z0-9-]*(?:\s[^>]*)?/?>")

RE_BAD_ANCHOR = re.compile(
    r"^(?:点击这里|点这里|这里|此处|点击此处|本文档|这篇文档|这篇博客|查看详情|了解更多|click here|here)$",
    re.IGNORECASE,
)
RE_QUOTED_CODE = re.compile(r"“(`+[^`]+`+)”")
RE_CJK_SINGLE = re.compile(rf"[{CJK_CHAR}]")
RE_PANGU_CJK_ALNUM = re.compile(rf"([{CJK_CHAR}])([A-Za-z0-9])")
RE_PANGU_ALNUM_CJK = re.compile(rf"([A-Za-z0-9])([{CJK_CHAR}])")
RE_SPACE_BEFORE_CJK_PUNCT = re.compile(rf"[^\s/→\-]\s+[{CJK_PUNCT}]")
RE_SPACE_AFTER_CJK_PUNCT = re.compile(rf"[{CJK_PUNCT}]\s+[^\s/→\-]")
RE_NUMBER_UNIT = re.compile(rf"(?<![A-Za-z0-9_/-])(\d+(?:\.\d+)?)({UNIT_PATTERN})\b")
RE_NUMBER_PERCENT_SPACE = re.compile(r"(\d+(?:\.\d+)?)\s+%")
RE_CJK_ITALIC = re.compile(
    rf"(?<!\*)\*(?!\*)([^*\n]*[{CJK_CHAR}][^*\n]*)(?<!\*)\*(?!\*)"
)
RE_HALFWIDTH_PUNCT_IN_CJK = re.compile(
    rf"[{CJK_CHAR}][,;?!:]|[,;?!][{CJK_CHAR}]"
)
RE_PLACEHOLDER_PREFIX = re.compile(r"\b(?:YOUR|MY)_[A-Z0-9_]+\b")
RE_LATIN_ABBR = re.compile(r"(?<![A-Za-z0-9_])(?:e\.g\.|i\.e\.|etc\.|vs\.|aka\b)", re.IGNORECASE)
RE_AND_OR = re.compile(r"和/或")
RE_SUBJECTIVE_WORDS = re.compile(
    r"(?:简单地|只需|轻松地?|显然|毫无疑问|显而易见|轻而易举|让我们)"
)
RE_TEMPORAL_PHRASES = re.compile(
    r"(?:截至本文撰写时|目前尚不支持|现阶段暂不支持|未来将会支持|后续版本会)"
)
RE_TYPO_FAZHI = re.compile(r"阀值")
RE_TYPO_DENGLU = re.compile(r"登陆")


@dataclass
class Issue:
    file: str
    line: int
    rule: str
    severity: str
    message: str
    excerpt: str


def _mask_span(text: str, pattern: re.Pattern[str], token: str = " ") -> str:
    """将匹配区间替换为等长安全占位符，避免误触发后续正则。"""
    return pattern.sub(lambda m: token * len(m.group(0)), text)


def _extract_prose_for_checks(line: str) -> str:
    """去除 URL、HTML 标签、行内代码与链接目标，仅保留正文用于文本与标点检查。"""
    # 先把 markdown 链接 [text](url) 替换为 text + 等长空白，保留锚文本检查
    def _replace_link(match: re.Match[str]) -> str:
        is_img, label, _url = match.group(1), match.group(2), match.group(3)
        if is_img:
            return " " * len(match.group(0))
        return label

    cleaned = RE_MD_LINK.sub(_replace_link, line)
    cleaned = RE_INLINE_CODE.sub(lambda m: " " * len(m.group(0)), cleaned)
    cleaned = RE_URL.sub(lambda m: " " * len(m.group(0)), cleaned)
    cleaned = RE_HTML_TAG.sub(lambda m: " " * len(m.group(0)), cleaned)
    return cleaned


def lint_lines(
    lines: list[str],
    file_label: str,
    ignored_rules: set[str] | None = None,
) -> list[Issue]:
    ignored = ignored_rules or set()
    issues: list[Issue] = []

    def add(line_no: int, rule: str, severity: str, message: str, raw_line: str) -> None:
        if rule in ignored:
            return
        excerpt = raw_line.strip()
        if len(excerpt) > 100:
            excerpt = excerpt[:97] + "..."
        issues.append(
            Issue(
                file=file_label,
                line=line_no,
                rule=rule,
                severity=severity,
                message=message,
                excerpt=excerpt,
            )
        )

    in_frontmatter = False
    in_code_block = False
    fence_char = ""
    fence_len = 0
    in_html_comment = False

    h1_count = 0
    prev_heading_level = 0

    for idx, raw_line in enumerate(lines, start=1):
        line = raw_line.rstrip("\r\n")

        # 处理文件开头的 YAML frontmatter
        if idx == 1 and line.strip() == "---":
            in_frontmatter = True
            continue
        if in_frontmatter:
            if line.strip() in ("---", "..."):
                in_frontmatter = False
            continue

        # 处理围栏代码块
        fence_match = RE_FENCE.match(line)
        if fence_match:
            marker = fence_match.group(1)
            if not in_code_block:
                in_code_block = True
                fence_char = marker[0]
                fence_len = len(marker)
            elif marker[0] == fence_char and len(marker) >= fence_len and line.strip() == marker:
                in_code_block = False
                fence_char = ""
                fence_len = 0
            continue

        if in_code_block:
            # 代码块内仅检查明显违规的 YOUR_/MY_ 占位符前缀
            m_ph = RE_PLACEHOLDER_PREFIX.search(line)
            if m_ph:
                add(
                    idx,
                    "W006",
                    "P1",
                    f"占位符“{m_ph.group(0)}”包含物主代词前缀，建议去掉 YOUR_/MY_ 前缀。",
                    line,
                )
            continue

        # 处理 HTML 注释
        if in_html_comment:
            if "-->" in line:
                in_html_comment = False
            continue
        if "<!--" in line:
            if "-->" not in line:
                in_html_comment = True
            line = re.sub(r"<!--.*?-->", "", line)
            if not line.strip():
                continue

        # 跳过表格分隔行
        if re.match(r"^\s*\|?[\s:-]+\|[\s|:-]*$", line):
            continue

        # 1. 标题结构检查
        h_match = RE_HEADING.match(line)
        if h_match:
            level = len(h_match.group(1))
            title_text = h_match.group(2)
            if level == 1:
                h1_count += 1
                if h1_count > 1:
                    add(idx, "H003", "P1", "同一页面出现多个一级标题（#），每个页面应仅有一个一级标题。", line)
            if prev_heading_level > 0 and level > prev_heading_level + 1:
                add(
                    idx,
                    "H002",
                    "P1",
                    f"标题层级跳级（从 H{prev_heading_level} 跳至 H{level}），应逐级递进。",
                    line,
                )
            prev_heading_level = level
            if title_text.endswith(("。", ".")):
                add(idx, "H001", "P1", "标题末尾不应加句号。", line)

        # 2. Markdown 链接与锚文本检查
        for m_link in RE_MD_LINK.finditer(line):
            is_img, label, _url = m_link.group(1), m_link.group(2).strip(), m_link.group(3)
            if not is_img and RE_BAD_ANCHOR.match(label):
                add(
                    idx,
                    "L001",
                    "P0",
                    f"链接锚文本“{label}”缺乏独立语义，请改为具体的目标页面或主题名称。",
                    line,
                )

        # 3. 依赖反引号原样的检查（需在遮罩行内代码前执行）
        if RE_QUOTED_CODE.search(line):
            add(idx, "P008", "P2", "行内代码（反引号）外部不应额外套中文双引号。", line)

        # 检查中文与行内代码之间缺半角空格（基于真实 inline code span 边界，避免跨段误匹配）
        line_no_urls = RE_MD_LINK.sub(lambda m: m.group(2) if not m.group(1) else " ", line)
        missing_code_space = False
        for m_code in RE_INLINE_CODE.finditer(line_no_urls):
            left_ch = line_no_urls[m_code.start() - 1] if m_code.start() > 0 else ""
            right_ch = line_no_urls[m_code.end()] if m_code.end() < len(line_no_urls) else ""
            if (left_ch and RE_CJK_SINGLE.match(left_ch)) or (
                right_ch and RE_CJK_SINGLE.match(right_ch)
            ):
                missing_code_space = True
                break
        if missing_code_space:
            add(idx, "P002", "P2", "中文字符与行内代码（反引号）之间应保留一个半角空格。", line)

        # 检查行内占位符前缀
        m_ph_inline = RE_PLACEHOLDER_PREFIX.search(line)
        if m_ph_inline:
            add(
                idx,
                "W006",
                "P1",
                f"占位符“{m_ph_inline.group(0)}”包含物主代词前缀，建议去掉 YOUR_/MY_ 前缀。",
                line,
            )

        # 4. 正文提取（遮罩代码、URL、HTML 标签与链接目标）
        prose = _extract_prose_for_checks(line)

        # 4.1 盘古之白：中文与英文/数字之间缺空格
        if RE_PANGU_CJK_ALNUM.search(prose) or RE_PANGU_ALNUM_CJK.search(prose):
            add(idx, "P001", "P2", "中文字符与英文字母或阿拉伯数字之间应保留一个半角空格。", line)

        # 4.2 全角标点旁误加空格（排除行首列表/引用符后紧跟左引号/左括号，以及表格竖线旁）
        prose_no_pipe = prose.replace("|", "")
        prose_trimmed = re.sub(r"^\s*(?:[-*+]|\d+\.|>+)?\s*", "", prose_no_pipe)
        # 去除破折号/中文标点后接 Markdown 粗体/行内代码已被遮罩成的空格（若原行是全角标点紧跟 ** 或 `）
        raw_trimmed = re.sub(r"^\s*(?:[-*+]|\d+\.|>+)?\s*", "", line)
        raw_trimmed = RE_MD_LINK.sub(lambda m: m.group(2) if not m.group(1) else "", raw_trimmed)
        raw_trimmed = RE_URL.sub("", raw_trimmed)
        # 排除表格单元格分隔 `| ` 后紧跟左引号/书名号，以及 `/` 和 `→` 流程分隔符
        for seg in raw_trimmed.split("|"):
            seg_clean = seg.strip()
            if RE_SPACE_BEFORE_CJK_PUNCT.search(seg_clean) or RE_SPACE_AFTER_CJK_PUNCT.search(seg_clean):
                add(idx, "P003", "P2", "中文全角标点符号两侧不应添加空格。", line)
                break

        # 4.3 数字与英文计量单位连写（如 64GB、100ms）
        m_unit = RE_NUMBER_UNIT.search(prose)
        if m_unit:
            add(
                idx,
                "P004",
                "P2",
                f"数字与单位缩写“{m_unit.group(1)}{m_unit.group(2)}”之间应保留一个半角空格（写为 {m_unit.group(1)} {m_unit.group(2)}）。",
                line,
            )

        # 4.4 数字与百分号间误加空格
        if RE_NUMBER_PERCENT_SPACE.search(prose):
            add(idx, "P005", "P2", "数字与百分号（%）之间不应加空格。", line)

        # 4.5 感叹号检查
        if "！" in prose:
            add(idx, "P006", "P1", "技术文档正文中应避免使用感叹号（！），保持冷静客观的语气。", line)

        # 4.6 中文正文斜体检查
        # 忽略粗体 **...** 后检查单星号斜体
        prose_no_bold = re.sub(r"\*\*[^*\n]+\*\*", "", prose)
        if RE_CJK_ITALIC.search(prose_no_bold):
            add(idx, "P007", "P1", "中文正文禁用斜体，强调请改用粗体、引号或书名号。", line)

        # 4.7 中文语境混用半角标点（跳过 GitHub Alert 标签行如 > [!NOTE]）
        if not re.match(r"^\s*>\s*\[!(?:NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]", line):
            if RE_HALFWIDTH_PUNCT_IN_CJK.search(prose):
                add(idx, "P009", "P2", "中文正文中疑似混用英文半角标点（, ; ? ! :），请使用全角中文标点。", line)

        # 4.8 错别字与高频禁用词
        if RE_TYPO_FAZHI.search(prose):
            add(idx, "W001", "P0", "疑似错别字“阀值”，技术术语应写作“阈值”。", line)
        if RE_TYPO_DENGLU.search(prose):
            add(idx, "W001", "P1", "出现“登陆”，若指账号验证进入系统，应写作“登录”。", line)

        m_latin = RE_LATIN_ABBR.search(prose)
        if m_latin:
            add(
                idx,
                "W002",
                "P1",
                f"正文中出现拉丁缩写“{m_latin.group(0)}”，建议改用规范中文（例如/即/等/对比/又称）。",
                line,
            )

        if RE_AND_OR.search(prose):
            add(idx, "W003", "P1", "避免使用“和/或”，请改为“A、B 或两者兼具”或“A 或 B”。", line)

        m_subj = RE_SUBJECTIVE_WORDS.search(prose)
        if m_subj:
            add(
                idx,
                "W004",
                "P1",
                f"避免使用主观评价或口语引导词“{m_subj.group(0)}”，请客观直接陈述步骤或事实。",
                line,
            )

        m_temp = RE_TEMPORAL_PHRASES.search(prose)
        if m_temp:
            add(
                idx,
                "W005",
                "P1",
                f"出现易过时或预告未来的表述“{m_temp.group(0)}”，参考文档应保持无时间依赖或锚定具体版本号。",
                line,
            )

    return issues


def collect_markdown_files(paths: Iterable[str]) -> list[Path]:
    result: list[Path] = []
    for raw in paths:
        p = Path(raw)
        if p.is_file():
            result.append(p)
        elif p.is_dir():
            result.extend(sorted(p.rglob("*.md")))
        else:
            print(f"警告：路径不存在，已跳过：{raw}", file=sys.stderr)
    return result


def format_text(issues: list[Issue]) -> str:
    if not issues:
        return "检查通过：未发现规范违例。"
    lines = []
    for item in issues:
        lines.append(
            f"[{item.severity}][{item.rule}] {item.file}:{item.line} - {item.message}\n"
            f"    原行：{item.excerpt}"
        )
    summary = _build_summary(issues)
    lines.append("")
    lines.append(summary)
    return "\n".join(lines)


def format_markdown(issues: list[Issue]) -> str:
    if not issues:
        return "检查通过：未发现规范违例。"
    out = [
        "| 级别 | 规则 | 位置 | 说明 | 原行片段 |",
        "|---|---|---|---|---|",
    ]
    for item in issues:
        safe_excerpt = item.excerpt.replace("|", "\\|")
        out.append(
            f"| {item.severity} | `{item.rule}` | `{item.file}:{item.line}` | {item.message} | `{safe_excerpt}` |"
        )
    out.append("")
    out.append(_build_summary(issues))
    return "\n".join(out)


def _build_summary(issues: list[Issue]) -> str:
    counts = {"P0": 0, "P1": 0, "P2": 0}
    for item in issues:
        counts[item.severity] = counts.get(item.severity, 0) + 1
    return (
        f"汇总：共发现 {len(issues)} 处问题"
        f"（P0 必改：{counts['P0']}，P1 建议：{counts['P1']}，P2 润色：{counts['P2']}）。"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="中文开发者技术文档规范确定性检查工具（零依赖）"
    )
    parser.add_argument("paths", nargs="+", help="待检查的 Markdown 文件或目录路径")
    parser.add_argument(
        "--format",
        choices=("text", "markdown", "json"),
        default="text",
        help="输出格式（默认：text）",
    )
    parser.add_argument(
        "--ignore",
        default="",
        help="忽略的规则编号列表，使用逗号分隔（例如：P001,W005）",
    )
    parser.add_argument(
        "--min-severity",
        choices=("P0", "P1", "P2"),
        default="P2",
        help="最低报告严重度（默认：P2，即输出全部级别）",
    )
    parser.add_argument(
        "--fail-on",
        choices=("P0", "P1", "P2", "none"),
        default="P2",
        help="达到该严重度及以上时返回退出码 1（默认：P2；设为 none 始终返回 0）",
    )
    args = parser.parse_args(argv)

    ignored_rules = {r.strip().upper() for r in args.ignore.split(",") if r.strip()}
    files = collect_markdown_files(args.paths)
    if not files:
        print("未找到可检查的 Markdown 文件。", file=sys.stderr)
        return 2

    all_issues: list[Issue] = []
    min_rank = SEVERITY_ORDER[args.min_severity]
    for path in files:
        content = path.read_text(encoding="utf-8").splitlines()
        file_issues = lint_lines(content, str(path), ignored_rules=ignored_rules)
        all_issues.extend(i for i in file_issues if SEVERITY_ORDER[i.severity] <= min_rank)

    if args.format == "json":
        print(json.dumps([asdict(i) for i in all_issues], ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(format_markdown(all_issues))
    else:
        print(format_text(all_issues))

    if args.fail_on == "none":
        return 0
    fail_rank = SEVERITY_ORDER[args.fail_on]
    has_failure = any(SEVERITY_ORDER[i.severity] <= fail_rank for i in all_issues)
    return 1 if has_failure else 0


if __name__ == "__main__":
    raise SystemExit(main())
