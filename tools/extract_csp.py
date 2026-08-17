# -*- coding: utf-8 -*-
"""搜 Qoder bundle 中的 CSP（Content-Security-Policy / connect-src）。"""
import re

F = r"C:\Program Files\Qoder\resources\app\out\lingma\agents-window\agents-window.desktop.main.js"
data = open(F, encoding="utf-8", errors="replace").read()

out = []
for pat in [r"Content-Security-Policy", r"connect-src", r"default-src", r"webRequest\.onHeadersReceived",
            r"onHeadersReceived", r"webSecurity"]:
    ms = list(re.finditer(pat, data))
    out.append(f"{pat}: {len(ms)} 次")
    for m in ms[:5]:
        s = max(0, m.start() - 150)
        e = min(len(data), m.end() + 250)
        out.append(f"\n--- @{m.start()} ---")
        out.append(data[s:e])

with open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\_csp.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done")
