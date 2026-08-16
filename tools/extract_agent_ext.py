# -*- coding: utf-8 -*-
"""在 aicoding-agent extension 中搜索 compressChat 相关代码。"""
import re, os

DIR = r"C:\Program Files\Qoder\resources\app\extensions\aicoding-agent\dist"
out = []

for fn in os.listdir(DIR):
    if not fn.endswith(".js"):
        continue
    path = os.path.join(DIR, fn)
    data = open(path, encoding="utf-8", errors="replace").read()
    hits = []
    for pat in [r"compressChat", r"compress", r"compaction"]:
        for m in re.finditer(pat, data):
            hits.append(m)
    if hits:
        out.append(f"\n===== {fn}: {len(hits)} hits =====")
        for m in hits[:5]:
            s = max(0, m.start() - 250)
            e = min(len(data), m.end() + 250)
            out.append(f"\n--- @{m.start()} ---")
            out.append(data[s:e])

with open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\_agent_ext.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done")
