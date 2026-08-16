# -*- coding: utf-8 -*-
"""验证优化输入 patch 目标字符串的唯一性（3 副本）。"""
import re

F = r"C:\Program Files\Qoder\resources\app\out\lingma\agents-window\agents-window.desktop.main.js"
data = open(F, encoding="utf-8", errors="replace").read()

targets = {
    "P-A1 z(wY)": "const z=(0,wY.useMemo)(()=>!!(r||e.trim().length<3),[r,e])",
    "P-A2 z(TX)": "const z=(0,TX.useMemo)(()=>!!(r||e.trim().length<3),[r,e])",
    "P-A3 z(UX)": "const z=(0,UX.useMemo)(()=>!!(r||e.trim().length<3),[r,e])",
    "P-B1 $(wY)": "$=(0,wY.useMemo)(()=>e.length>z5p,[e])",
    "P-B2 $(TX)": "$=(0,TX.useMemo)(()=>e.length>ohv,[e])",
    "P-B3 $(UX)": "$=(0,UX.useMemo)(()=>e.length>zvb,[e])",
    "P-C 强制_meta": "let G;if(Gi[Ui.SHOW_MODEL_SELECTOR]){const X=c||\"agent\"",
    "P-D extra.customModel": "params:{sessionId:d,questionText:e,references:K,...G?{_meta:G}:{}}}})",
}
for name, s in targets.items():
    n = data.count(s)
    print(f"{name}: {n} 次")
    if n != 1 and name != "P-C 强制_meta":
        print("  !! 非 1 次，需人工确认")
