# -*- coding: utf-8 -*-
"""从日志中提取 cosy 进程的路径信息。"""
import re, os, glob

out = []
log_dirs = sorted(glob.glob(os.path.expandvars(r"%APPDATA%\Qoder\logs\*")), reverse=True)[:3]
seen = set()
for ld in log_dirs:
    for fn in glob.glob(os.path.join(ld, "**", "*.log"), recursive=True):
        try:
            content = open(fn, "r", encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        for m in re.finditer(r"cosy", content, re.IGNORECASE):
            s = max(0, m.start() - 200)
            e = min(len(content), m.end() + 200)
            seg = content[s:e].replace("\n", " ")
            key = seg[:120]
            if key in seen:
                continue
            seen.add(key)
            out.append(f"\n--- {os.path.basename(fn)} ---")
            out.append(seg)

with open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\_cosy_log.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done, lines:", len(out))
