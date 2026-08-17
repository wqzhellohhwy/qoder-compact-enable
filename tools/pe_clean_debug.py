# -*- coding: utf-8 -*-
"""移除 P-E 调试代码（写文件/document.title/L?.error），还原为仅 console.warn。"""
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

dbg = ('catch(err){console.warn("[P-E] local enhance failed, fallback:",err);'
       'try{var peMsg="[P-E] "+new Date().toISOString()+" "+(err&&err.message||err)+"\\n"+(err&&err.stack||"")+"\\n";'
       'var peOk=!1;'
       'try{if(typeof require==="function"){require("fs").appendFileSync("C:\\\\Users\\\\53518\\\\Desktop\\\\pe_error.log",peMsg);peOk=!0}}catch(peE){}'
       'peOk||(document.title="[P-E] "+(err&&err.message||err))}catch(peE2){}'
       'L?.error("[P-E] "+(err?.message||err))}}')
clean = 'catch(err){console.warn("[P-E] local enhance failed, fallback:",err)}}'

# 1) patch 脚本
P = r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\compact\patch_qoder_enhance.py"
d = open(P, encoding="utf-8").read()
print("脚本调试片段出现:", d.count(dbg))
if d.count(dbg) == 1:
    d = d.replace(dbg, clean, 1)
    open(P, "w", encoding="utf-8", newline="\n").write(d)
    print("脚本已还原")

# 2) 真实文件（3 处）
JS = r"C:\Program Files\Qoder\resources\app\out\lingma\agents-window\agents-window.desktop.main.js"
data = open(JS, encoding="utf-8", errors="replace").read()
print("真实文件调试片段出现:", data.count(dbg))
if data.count(dbg) == 3:
    data = data.replace(dbg, clean)
    open(JS, "w", encoding="utf-8", newline="").write(data)
    print("真实文件已还原")
