"""统计 UTF-8 文本中的词频，仅使用 Python 标准库。"""

import argparse
from collections import Counter
from pathlib import Path
import re


def count_words(text):
    """忽略大小写，以连续 Unicode 字母（包括汉字）为统计单位。"""
    words = re.findall(r"[^\W\d_]+", text.casefold())
    return Counter(words)


def main():
    parser = argparse.ArgumentParser(description="统计 UTF-8 文本文件中的词频")
    parser.add_argument("file", type=Path, help="要统计的 UTF-8 文本文件路径")
    args = parser.parse_args()

    try:
        # utf-8-sig 同时兼容普通 UTF-8 和带 BOM 的 UTF-8 文件。
        text = args.file.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        parser.exit(1, "错误：文件不是有效的 UTF-8 文本，请转换编码后重试。\n")
    except OSError as error:
        parser.exit(1, f"错误：无法读取文件 {args.file}（{error}）。\n")

    counts = count_words(text)
    print(f"总词数：{sum(counts.values())}")
    print(f"不同词数：{len(counts)}")
    if not counts:
        print("未找到可统计的词语。")
        return

    print("词语\t次数")
    for word, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
        print(f"{word}\t{count}")


if __name__ == "__main__":
    main()
