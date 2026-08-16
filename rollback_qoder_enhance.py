# -*- coding: utf-8 -*-
"""
Qoder 优化输入 patch 回滚脚本
从最近一次 .bak_enhance_* 备份恢复 agents-window.desktop.main.js。
用法：右键本 bat -> 以管理员身份运行
路径探测（可移植）：--js <bundle路径> 或环境变量 QODER_INSTALL_DIR 优先，
      否则自动探测常见安装位置。
"""
import os
import sys
import glob
import shutil

JS = r"C:\Program Files\Qoder\resources\app\out\lingma\agents-window\agents-window.desktop.main.js"

TEST_MODE = "--test" in sys.argv
if TEST_MODE:
    JS = sys.argv[sys.argv.index("--test") + 1]

KEY = ".bak_enhance_"


def detect_js():
    if "--js" in sys.argv:
        return sys.argv[sys.argv.index("--js") + 1]
    env = os.environ.get("QODER_INSTALL_DIR")
    rel = os.path.join("resources", "app", "out", "lingma", "agents-window", "agents-window.desktop.main.js")
    if env:
        return os.path.join(env, rel)
    for root in (r"C:\Program Files\Qoder", r"C:\Program Files (x86)\Qoder",
                 os.path.expandvars(r"%LOCALAPPDATA%\Programs\Qoder")):
        p = os.path.join(root, rel)
        if os.path.exists(p):
            return p
    return os.path.join(r"C:\Program Files\Qoder", rel)


if not TEST_MODE:
    JS = detect_js()

# 控制台 UTF-8 输出（避免 GBK 乱码）
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def main():
    if not TEST_MODE:
        tasklist = os.popen('tasklist /FO CSV /NH 2>nul').read().lower()
        if "qoder" in tasklist:
            print("[!] Qoder 仍在运行，请先完全退出（含托盘）再执行。")
            sys.exit(1)

    baks = sorted(glob.glob(JS + KEY + "*"))
    if not baks:
        print("[*] 未找到 enhance 备份，无需回滚（或备份已被清理）。")
        return

    bak = baks[-1]
    print("[1/3] 使用备份:", os.path.basename(bak))

    with open(JS, "r", encoding="utf-8", errors="replace") as f:
        current = f.read()
    markers = ["const z=(0,wY.useMemo)(()=>!!r,[r])",
               "const z=(0,TX.useMemo)(()=>!!r,[r])",
               "const z=(0,UX.useMemo)(()=>!!r,[r])"]
    if not any(m in current for m in markers):
        print("[*] 当前文件已无 enhance patch 标记，无需回滚。")
        return

    ts = os.path.basename(bak).replace(KEY, "")
    pre = JS + ".bak_enhance_reverted_" + ts
    shutil.copy2(JS, pre)
    print("[2/3] 已备份当前状态:", os.path.basename(pre))

    shutil.copy2(bak, JS)
    print("[3/3] 已从备份恢复。重启 Qoder 后优化输入恢复原样（长度限制 + 官方通道）。")


if __name__ == "__main__":
    main()
