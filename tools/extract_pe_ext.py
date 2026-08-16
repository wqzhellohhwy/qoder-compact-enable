# -*- coding: utf-8 -*-
"""在 aicoding-agent extension 中搜索 promptEnhance 处理。"""
import re, os

DIR = r"C:\Program Files\Qoder\resources\app\extensions\aicoding-agent\dist"
out = []

for fn in os.listdir(DIR):
    if not fn.endswith(".js"):
        continue
    path = os.path.join(DIR, fn)
    data = open(path, encoding="utf-8", errors="replace").read()
    hits = []
    for pat in [r"promptEnhance", r"prompt_enhance", r"enhancePrompt"]:
        for m in re.finditer(pat, data):
            hits.append(m)
    if hits:
        out.append(f"\n===== {fn}: {len(hits)} hits =====")
        for m in hits[:8]:
            s = max(0, m.start() - 300)
            e = min(len(data), m.end() + 300)
            out.append(f"\n--- @{m.start()} ---")
            out.append(data[s:e])

with open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\_pe_ext.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done")
