# -*- coding: utf-8 -*-
"""验证 enhance 测试副本的 patch 结果。"""
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

d = open(r"C:\Program Files\Qoder\resources\app\out\lingma\agents-window\agents-window.desktop.main.js", encoding="utf-8", errors="replace").read()

old_pc = 'let G;if(Gi[Ui.SHOW_MODEL_SELECTOR]){const X=c||"agent"'
new_pc = 'let G;{const X=c||"agent"'
print("OLD if(Gi) 残留:", d.count(old_pc))
print("NEW 无条件块:", d.count(new_pc))
print("z 新版本(!!r):", d.count("useMemo)(()=>!!r,[r])"))
print("z 旧版本(<3):", d.count("trim().length<3"))
print("$ 新版本(!1):", d.count("useMemo)(()=>!1,[e])"))
