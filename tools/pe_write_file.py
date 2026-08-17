# -*- coding: utf-8 -*-
"""P-E catch 写文件调试：更新 patch 脚本 + 真实文件（3 处）。"""
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

old = 'catch(err){console.warn("[P-E] local enhance failed, fallback:",err);L?.error("[P-E] "+(err?.message||err))}}'
new = ('catch(err){console.warn("[P-E] local enhance failed, fallback:",err);'
       'try{var peMsg="[P-E] "+new Date().toISOString()+" "+(err&&err.message||err)+"\\n"+(err&&err.stack||"")+"\\n";'
       'var peOk=!1;'
       'try{if(typeof require==="function"){require("fs").appendFileSync("C:\\\\Users\\\\53518\\\\Desktop\\\\pe_error.log",peMsg);peOk=!0}}catch(peE){}'
       'peOk||(document.title="[P-E] "+(err&&err.message||err))}catch(peE2){}'
       'L?.error("[P-E] "+(err?.message||err))}}')

# 1) 更新 patch 脚本（P-E NEW 字符串）
P = r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\compact\patch_qoder_enhance.py"
d = open(P, encoding="utf-8").read()
print("脚本旧片段出现:", d.count(old))
if d.count(old) == 1:
    d = d.replace(old, new, 1)
    open(P, "w", encoding="utf-8", newline="\n").write(d)
    print("脚本已更新")
else:
    print("脚本片段数量异常，跳过")

# 2) 真实文件替换（3 处）
JS = r"C:\Program Files\Qoder\resources\app\out\lingma\agents-window\agents-window.desktop.main.js"
data = open(JS, encoding="utf-8", errors="replace").read()
print("真实文件旧片段出现:", data.count(old))
if data.count(old) == 3:
    data = data.replace(old, new)
    open(JS, "w", encoding="utf-8", newline="").write(data)
    print("真实文件已更新")
else:
    print("真实文件片段数量异常，跳过")
