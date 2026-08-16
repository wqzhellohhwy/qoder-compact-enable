# -*- coding: utf-8 -*-
"""提取 PromptEnhance 完整代码（第一副本 @8716000-@8723000）+ enhance i18n 文案。"""
import re

F = r"C:\Program Files\Qoder\resources\app\out\lingma\agents-window\agents-window.desktop.main.js"
data = open(F, encoding="utf-8", errors="replace").read()

out = []

# 1) 第一副本完整区域
out.append("===== 第一副本 @8716000-@8724000 =====")
out.append(data[8716000:8724000])

# 2) chat.input.enhance 相关 i18n 键（中英文）
out.append("\n\n===== chat.input.enhance i18n =====")
for m in re.finditer(r"chat\.input\.enhance\.prompt[^\"']*", data):
    s = max(0, m.start() - 60)
    e = min(len(data), m.end() + 260)
    seg = data[s:e]
    if seg not in out:
        out.append(f"\n--- @{m.start()} ---")
        out.append(seg)

with open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\_pe_full.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done")
