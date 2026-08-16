# -*- coding: utf-8 -*-
"""
Qoder 对话压缩无条件启用 Patch 脚本（3 处 patch，幂等）

背景：Qoder 的"压缩当前对话"（Compact Chat）按钮在上下文使用率低于 40% 时被禁用
（UI 提示"对话内容较短，暂无需压缩"）。定位到 agents-window.desktop.main.js 中
三个窗口副本的 overlay 组件，禁用条件均为 `s||t<THRESHOLD`（s=对话进行中，t=百分比）。
本脚本将条件改为 `s`（仅对话进行中禁用），百分比不再作为门槛。

用法：1) 完全退出 Qoder
      2) 右键本 bat -> 以管理员身份运行
      3) 重启 Qoder -> 任意会话打开上下文面板，压缩按钮始终可点
回滚：rollback_qoder_compact.bat（管理员运行）

路径探测（可移植）：
  --js <bundle路径> 或环境变量 QODER_INSTALL_DIR（安装目录）优先，
  否则自动探测 Program Files / Program Files (x86) / %LOCALAPPDATA%/Programs。
"""
import os
import sys
import shutil
import datetime

def detect_js():
    """探测 agents-window.desktop.main.js 路径：--js > QODER_INSTALL_DIR > 常见安装位置"""
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

JS = detect_js()

# 三个窗口副本的禁用条件：s(对话进行中) || t(百分比) < 阈值(40)
# 改为仅 s：百分比不再是压缩门槛
PATCHES = [
    # 副本1（本地 chat 面板）：iDa=40
    (
        "const c=(0,uin.useMemo)(()=>s||t<iDa,[t,s])",
        "const c=(0,uin.useMemo)(()=>s,[t,s])",
    ),
    # 副本2（quest 输入面板）：oyu=40
    (
        "const c=(0,ZBn.useMemo)(()=>s||t<oyu,[t,s])",
        "const c=(0,ZBn.useMemo)(()=>s,[t,s])",
    ),
    # 副本3（experts/agents 窗口）：kHu=40
    (
        "const c=(0,qqn.useMemo)(()=>s||t<kHu,[t,s])",
        "const c=(0,qqn.useMemo)(()=>s,[t,s])",
    ),
]

TEST_MODE = "--test" in sys.argv
if TEST_MODE:
    JS = sys.argv[sys.argv.index("--test") + 1]

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

    if not os.path.exists(JS):
        print("[!] 找不到目标文件（版本可能已更新）：", JS)
        sys.exit(2)

    with open(JS, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    todo = []
    for old, new in PATCHES:
        cnt_old = content.count(old)
        if new in content:
            print("[*] 已 patch 跳过:", old[:60], "...")
        elif cnt_old == 1:
            todo.append((old, new))
        elif cnt_old == 0:
            print("[!] 版本不匹配，未找到目标代码段:", old[:60], "...")
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_js_version.txt"), "w", encoding="utf-8") as f:
                f.write("size=%d\n" % len(content))
            sys.exit(3)
        else:
            print("[!] 目标代码段出现 %d 次（预期 1 次），请人工确认:" % cnt_old, old[:60], "...")
            sys.exit(3)

    if not todo:
        print("[*] 全部 patch 已生效，无需操作。")
        return

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = JS + ".bak_compact_" + ts
    shutil.copy2(JS, bak)
    print("[1/3] 已备份:", os.path.basename(bak))

    for old, new in todo:
        content = content.replace(old, new, 1)
    with open(JS, "w", encoding="utf-8", newline="") as f:
        f.write(content)
    print("[2/3] 已写入 %d 处 patch" % len(todo))

    with open(JS, "r", encoding="utf-8", errors="replace") as f:
        check = f.read()
    ok = all(new in check for _, new in PATCHES)
    if ok:
        print("[3/3] 读回验证通过。重启 Qoder 后，任意对话均可随时压缩（仅生成中禁用）。")
    else:
        print("[!] 读回验证失败！请用 rollback_qoder_compact.bat 恢复后重试。")
        sys.exit(4)


if __name__ == "__main__":
    main()
