# -*- coding: utf-8 -*-
"""提取 resolvePromptModelMeta / 次数相关 i18n / promptEnhance 后端处理。"""
import re

F = r"C:\Program Files\Qoder\resources\app\out\lingma\agents-window\agents-window.desktop.main.js"
data = open(F, encoding="utf-8", errors="replace").read()

out = []

# 1) resolvePromptModelMeta 定义与调用
ms = list(re.finditer(r"resolvePromptModelMeta", data))
out.append(f"resolvePromptModelMeta: {len(ms)} 次")
for m in ms[:6]:
    s = max(0, m.start() - 300)
    e = min(len(data), m.end() + 300)
    out.append(f"\n--- @{m.start()} ---")
    out.append(data[s:e])

# 2) limit.error 完整 i18n（中英文）
out.append("\n\n===== limit.error / 次数 i18n =====")
for m in re.finditer(r"limit\.error[^\"']*\"\s*:\s*\"[^\"]*\"", data):
    s = max(0, m.start() - 120)
    e = min(len(data), m.end() + 60)
    out.append(f"\n--- @{m.start()} ---")
    out.append(data[s:e])

# 3) 次数相关字段：remaining/left/times/quota + promptEnhance 组合
for kw in [r"enhance.*?remaining", r"remaining.*?enhance", r"promptEnhance.*?(?:count|limit|quota|remain|left|times)",
           r"(?:count|limit|quota|remain|left|times).*?promptEnhance"]:
    ms = list(re.finditer(kw, data))
    out.append(f"\n{kw}: {len(ms)} 次")
    for m in ms[:5]:
        s = max(0, m.start() - 200)
        e = min(len(data), m.end() + 200)
        out.append(f"  --- @{m.start()} ---")
        out.append("  " + data[s:e])

# 4) Gi[Ui.SHOW_MODEL_SELECTOR] 相关
for kw in ["SHOW_MODEL_SELECTOR"]:
    ms = list(re.finditer(kw, data))
    out.append(f"\n{kw}: {len(ms)} 次")
    for m in ms[:8]:
        s = max(0, m.start() - 200)
        e = min(len(data), m.end() + 200)
        out.append(f"  --- @{m.start()} ---")
        out.append("  " + data[s:e])

with open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\_pe_model.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done")
