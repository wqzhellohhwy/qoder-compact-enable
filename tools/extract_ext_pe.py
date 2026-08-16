# -*- coding: utf-8 -*-
"""提取 extension.js 中 promptEnhance 完整实现。"""
import re

F = r"C:\Program Files\Qoder\resources\app\extensions\aicoding-agent\dist\extension.js"
data = open(F, encoding="utf-8", errors="replace").read()

out = []
m = re.search(r"async promptEnhance\(e\)\{", data)
if m:
    out.append(f"===== promptEnhance @{m.start()} =====")
    out.append(data[m.start():m.start()+2500])

with open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\_ext_pe.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done")
