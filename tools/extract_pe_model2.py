# -*- coding: utf-8 -*-
"""提取 resolvePromptModelMeta 定义与 SHOW_MODEL_SELECTOR 枚举。"""
import re

F = r"C:\Program Files\Qoder\resources\app\out\lingma\agents-window\agents-window.desktop.main.js"
data = open(F, encoding="utf-8", errors="replace").read()

out = []

# resolvePromptModelMeta 定义（找 "resolvePromptModelMeta(e" 或 "async resolvePromptModelMeta"）
for m in re.finditer(r"resolvePromptModelMeta", data):
    s = max(0, m.start() - 100)
    e = min(len(data), m.end() + 600)
    out.append(f"\n--- @{m.start()} ---")
    out.append(data[s:e])

# SHOW_MODEL_SELECTOR 枚举定义（Ui 枚举）
for m in list(re.finditer(r"SHOW_MODEL_SELECTOR", data))[:6]:
    s = max(0, m.start() - 250)
    e = min(len(data), m.end() + 250)
    out.append(f"\n--- SHOW_MODEL_SELECTOR @{m.start()} ---")
    out.append(data[s:e])

with open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\_pe_model2.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done")
