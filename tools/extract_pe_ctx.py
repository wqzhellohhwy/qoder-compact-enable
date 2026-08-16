# -*- coding: utf-8 -*-
"""提取 setPromptEnhanceOperation / PromptEnhanceButton / enhancedPrompt 全部上下文。"""
import re

F = r"C:\Program Files\Qoder\resources\app\out\lingma\agents-window\agents-window.desktop.main.js"
data = open(F, encoding="utf-8", errors="replace").read()

out = []
for name in ["setPromptEnhanceOperation", "PromptEnhanceButton", "enhancedPrompt"]:
    ms = list(re.finditer(re.escape(name), data))
    out.append(f"\n{'='*30} {name}: {len(ms)} 次 {'='*30}")
    for m in ms:
        s = max(0, m.start() - 350)
        e = min(len(data), m.end() + 350)
        out.append(f"\n--- @{m.start()} ---")
        out.append(data[s:e])

with open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\_pe_ctx.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done")
