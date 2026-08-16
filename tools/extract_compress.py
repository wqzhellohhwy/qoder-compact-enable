# -*- coding: utf-8 -*-
"""提取 compressContext 方法完整代码 + 搜索 extension 后端 compressChat。"""
import re, os

F = r"C:\Program Files\Qoder\resources\app\out\lingma\agents-window\agents-window.desktop.main.js"
data = open(F, encoding="utf-8", errors="replace").read()

out = []

# 1) compressContext 定义
m = re.search(r"async compressContext\([^)]*\)\{", data)
if m:
    out.append(f"===== compressContext @{m.start()} =====")
    out.append(data[m.start():m.start()+2500])
else:
    out.append("compressContext 未找到，尝试 compressSession:")
    m = re.search(r"async compressSession\([^)]*\)\{", data)
    if m:
        out.append(f"===== compressSession @{m.start()} =====")
        out.append(data[m.start():m.start()+2500])

# 2) 查找 extension 目录
out.append("\n\n===== extensions 目录 =====")
for root in [r"C:\Program Files\Qoder\resources\app\extensions",
             r"C:\Program Files\Qoder\resources\extensions",
             r"C:\Program Files\Qoder\resources\app\node_modules"]:
    if os.path.isdir(root):
        out.append(f"存在: {root}")
        try:
            for name in os.listdir(root)[:30]:
                out.append(f"  {name}")
        except Exception as ex:
            out.append(f"  ERROR: {ex}")
    else:
        out.append(f"不存在: {root}")

with open(r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\_compress_ctx.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done")
