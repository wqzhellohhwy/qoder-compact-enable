# -*- coding: utf-8 -*-
"""搜索 promptEnhance（优化输入）相关代码：次数限制/模型入口/计费。"""
import re
from collections import Counter

F = r"C:\Program Files\Qoder\resources\app\out\lingma\agents-window\agents-window.desktop.main.js"
data = open(F, encoding="utf-8", errors="replace").read()

out = []

# 1) promptEnhance 相关词频
for kw in ["promptEnhance", "prompt_enhance", "enhancePrompt", "enhance", "PromptEnhance"]:
    n = len(re.findall(kw, data))
    out.append(f"{kw}: {n}")

# 2) promptEnhance 驼峰组合统计
words = Counter(re.findall(r"[A-Za-z_$]*[Pp]romptEnhance[A-Za-z_$]*|[A-Za-z_$]*enhance[A-Za-z_$]*", data))
out.append("\n词频 Top40:")
for w, n in words.most_common(40):
    out.append(f"  {w}: {n}")

with open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\_pe_scan.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done")
