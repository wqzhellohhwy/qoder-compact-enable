# -*- coding: utf-8 -*-
"""搜索 Qoder bundle 中压缩(compact/summarize)相关关键词，统计出现次数并提取上下文片段。"""
import os, re, sys

FILES = [
    r"C:\Program Files\Qoder\resources\app\out\lingma\agents-window\agents-window.desktop.main.js",
    r"C:\Program Files\Qoder\resources\app\out\lingma\agents-window\electron-browser\agents-window.js",
    r"C:\Program Files\Qoder\resources\app\out\vs\code\electron-browser\workbench\workbench.js",
]

KEYWORDS = [
    r"compact",
    r"compress",
    r"summariz",
    r"condens",
    r"trimContext",
    r"contextPercent",
    r"usagePercent",
    r"percent",
]

def count_occurrences(data, pattern):
    return len(re.findall(pattern, data, re.IGNORECASE))

for f in FILES:
    if not os.path.exists(f):
        print(f"MISSING: {f}")
        continue
    size_mb = os.path.getsize(f) / 1024 / 1024
    with open(f, "r", encoding="utf-8", errors="replace") as fp:
        data = fp.read()
    print(f"=== {f} ({size_mb:.1f} MB) ===")
    for kw in KEYWORDS:
        n = count_occurrences(data, kw)
        if n:
            print(f"  {kw!r}: {n}")
    print()
