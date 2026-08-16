# -*- coding: utf-8 -*-
"""
Qoder 优化输入（promptEnhance）增强 Patch 脚本（9 处，幂等）

背景：优化输入按钮存在两处本地限制 + 一处通道缺陷：
  P-A（3 副本）：输入 <3 字符禁用按钮（z = r || trim().length<3）→ 只保留对话生成中 r
  P-B（3 副本）：输入 >1000 字符禁用按钮（$ = e.length>常量）→ 恒 false
  P-C（3 副本）：`if(Gi[Ui.SHOW_MODEL_SELECTOR])` 条件才附带模型 _meta；
                实测 cosy 下发 features 无 showModelSelector → 请求从不带 _meta
                → 增强请求走官方模型通道（消耗官方每日配额，error.code.110）。
                改为无条件调用 resolvePromptModelMeta → 附带自定义模型
                （provider/model/api_key，实测 deepseek hasApiKey=true）
                → cosy 走 BYOK 直连第三方 API，无官方配额、消耗自己的 token。

用法：1) 完全退出 Qoder
      2) 右键本 bat -> 以管理员身份运行
      3) 重启 Qoder -> 优化输入按钮任意长度可点，请求走自定义模型
回滚：rollback_qoder_enhance.bat（管理员运行）

路径探测（可移植）：
  --js <bundle路径> 或环境变量 QODER_INSTALL_DIR（安装目录）优先，
  否则自动探测 Program Files / Program Files (x86) / %LOCALAPPDATA%/Programs。
"""
import os
import sys
import shutil
import datetime

JS = r"C:\Program Files\Qoder\resources\app\out\lingma\agents-window\agents-window.desktop.main.js"

PATCHES = [
    # P-A：解除 <3 字符禁用（3 副本）
    (
        "const z=(0,wY.useMemo)(()=>!!(r||e.trim().length<3),[r,e])",
        "const z=(0,wY.useMemo)(()=>!!r,[r])",
    ),
    (
        "const z=(0,TX.useMemo)(()=>!!(r||e.trim().length<3),[r,e])",
        "const z=(0,TX.useMemo)(()=>!!r,[r])",
    ),
    (
        "const z=(0,UX.useMemo)(()=>!!(r||e.trim().length<3),[r,e])",
        "const z=(0,UX.useMemo)(()=>!!r,[r])",
    ),
    # P-B：解除 >1000 字符禁用（3 副本，常量名不同）
    (
        "$=(0,wY.useMemo)(()=>e.length>z5p,[e])",
        "$=(0,wY.useMemo)(()=>!1,[e])",
    ),
    (
        "$=(0,TX.useMemo)(()=>e.length>ohv,[e])",
        "$=(0,TX.useMemo)(()=>!1,[e])",
    ),
    (
        "$=(0,UX.useMemo)(()=>e.length>zvb,[e])",
        "$=(0,UX.useMemo)(()=>!1,[e])",
    ),
    # P-C：无条件附带模型 _meta（3 副本，replace_all）
    (
        "let G;if(Gi[Ui.SHOW_MODEL_SELECTOR]){const X=c||\"agent\"",
        "let G;{const X=c||\"agent\"",
    ),
    # P-D：extra 附带 customModel（cosy AskParams.extra.customModel 通道，普通聊天同款）
    #      —— 仅传 _meta 不够，cosy EnhancePrompt 仍走官方通道；extra.customModel 指明 BYOK 模型引用
    (
        "params:{sessionId:d,questionText:e,references:K,...G?{_meta:G}:{}}}})",
        "params:{sessionId:d,questionText:e,references:K,extra:G?.MODEL_KEY?{customModel:{name:G.MODEL_KEY,value:G.CUSTOM_MODEL?.model||G.MODEL_KEY}}:{},...G?{_meta:G}:{}}}})",
    ),
]

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

TEST_MODE = "--test" in sys.argv
if TEST_MODE:
    JS = sys.argv[sys.argv.index("--test") + 1]
else:
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

    if not os.path.exists(JS):
        print("[!] 找不到目标文件（版本可能已更新）：", JS)
        sys.exit(2)

    with open(JS, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    todo = []
    for old, new in PATCHES:
        cnt = content.count(old)
        if new in content:
            print("[*] 已 patch 跳过:", old[:50], "...")
        elif cnt == 1:
            todo.append((old, new))
        elif cnt == 3:
            todo.append((old, new))
            print("[*] 3 副本匹配:", old[:50], "...")
        elif cnt == 0:
            print("[!] 版本不匹配，未找到目标代码段:", old[:50], "...")
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_js_version.txt"), "w", encoding="utf-8") as f:
                f.write("size=%d\n" % len(content))
            sys.exit(3)
        else:
            print("[!] 目标代码段出现 %d 次（预期 1 或 3），请人工确认:" % cnt, old[:50], "...")
            sys.exit(3)

    if not todo:
        print("[*] 全部 patch 已生效，无需操作。")
        return

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = JS + ".bak_enhance_" + ts
    shutil.copy2(JS, bak)
    print("[1/3] 已备份:", os.path.basename(bak))

    for old, new in todo:
        content = content.replace(old, new)
    with open(JS, "w", encoding="utf-8", newline="") as f:
        f.write(content)
    print("[2/3] 已写入 %d 处 patch" % len(todo))

    with open(JS, "r", encoding="utf-8", errors="replace") as f:
        check = f.read()
    ok = all(new in check for _, new in PATCHES)
    if ok:
        print("[3/3] 读回验证通过。重启 Qoder 后：优化输入任意长度可点，请求携带自定义模型 _meta（走 BYOK，无官方每日配额）。")
    else:
        print("[!] 读回验证失败！请用 rollback_qoder_enhance.bat 恢复后重试。")
        sys.exit(4)


if __name__ == "__main__":
    main()
