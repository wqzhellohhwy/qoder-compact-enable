# -*- coding: utf-8 -*-
"""提取 customModelService.resolveModelConfig 定义与返回结构。"""
import re

F = r"C:\Program Files\Qoder\resources\app\out\lingma\agents-window\agents-window.desktop.main.js"
data = open(F, encoding="utf-8", errors="replace").read()

out = []

# resolveModelConfig 定义
m = re.search(r"resolveModelConfig\([^)]*\)\{", data)
if m:
    out.append(f"===== resolveModelConfig @{m.start()} =====")
    out.append(data[m.start():m.start()+3000])

# resolveModelConfig 所有出现
ms = list(re.finditer(r"resolveModelConfig", data))
out.append(f"\n\nresolveModelConfig 出现: {len(ms)} 次")

with open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\_rmc.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done")
