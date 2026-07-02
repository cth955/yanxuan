#!/usr/bin/env python3
"""统计盐选故事 Markdown 正文字数（汉字口径）。"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# CJK 统一表意文字 + 常用中文标点
CHAR_PATTERN = re.compile(
    r"[\u4e00-\u9fff\u3400-\u4dbf"
    r"\u3000-\u303f\uff00-\uffef"
    r"，。！？；：、""''（）《》【】—…]"
)


def strip_markdown(text: str) -> str:
    """去掉常见 Markdown 标记，保留叙事正文。"""
    text = re.sub(r"```[\s\S]*?```", "", text)
    text = re.sub(r"`[^`]+`", "", text)
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*\d+\.\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"^---+\s*$", "", text, flags=re.MULTILINE)
    return text


def count_chars(text: str) -> int:
    return len(CHAR_PATTERN.findall(strip_markdown(text)))


def check_file(path: Path, target: int, threshold: float) -> tuple[int, bool]:
    content = path.read_text(encoding="utf-8")
    actual = count_chars(content)
    minimum = int(target * threshold)
    ok = actual >= minimum
    return actual, ok


def main() -> int:
    parser = argparse.ArgumentParser(description="统计故事 Markdown 字数")
    parser.add_argument("path", type=Path, help="章节文件或故事目录")
    parser.add_argument("--target", type=int, default=1500, help="单章目标字数")
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.8,
        help="达标阈值（相对目标字数，默认 0.8）",
    )
    parser.add_argument(
        "--min-total", type=int, default=0, help="全文最低字数（检查目录时生效）"
    )
    args = parser.parse_args()
    path: Path = args.path

    if not path.exists():
        print(f"错误：路径不存在 {path}", file=sys.stderr)
        return 2

    failed = False
    total = 0
    minimum = int(args.target * args.threshold)

    if path.is_file():
        actual, ok = check_file(path, args.target, args.threshold)
        status = "OK" if ok else "FAIL"
        print(f"{path.name}: {actual} 字 (目标 {args.target}, 下限 {minimum}) — {status}")
        return 0 if ok else 1

    chapters = sorted(path.glob("chapter-*.md"))
    if not chapters:
        print(f"错误：目录下未找到 chapter-*.md — {path}", file=sys.stderr)
        return 2

    print(f"{'文件':<20} {'字数':>6}  {'状态'}")
    print("-" * 40)
    for ch in chapters:
        actual, ok = check_file(ch, args.target, args.threshold)
        total += actual
        status = "OK" if ok else "FAIL"
        print(f"{ch.name:<20} {actual:>6}  {status}")
        if not ok:
            failed = True

    print("-" * 40)
    print(f"{'合计':<20} {total:>6}")

    min_total = args.min_total or 0
    if min_total and total < min_total:
        print(f"全文未达标：{total} < {min_total}", file=sys.stderr)
        failed = True
    elif min_total:
        print(f"全文字数达标：{total} ≥ {min_total}")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
