# -*- coding: utf-8 -*-
"""
Qoder 压缩/优化输入 patch 统一回滚脚本（自包含版）

精确逆向还原 compact（P1-P3）与 enhance（P-A~P-E）的全部 patch，
使 agents-window.desktop.main.js 回到本仓库修改前的状态。
**不影响专家团项目（experts/）的 patch**。

用法：1) 完全退出 Qoder
      2) 右键本 bat -> 以管理员身份运行
      3) 重启 Qoder

路径探测（可移植）：--js <bundle路径> 或环境变量 QODER_INSTALL_DIR 优先，
      否则自动探测常见安装位置。
"""
import os
import sys
import shutil
import datetime

JS = r"C:\Program Files\Qoder\resources\app\out\lingma\agents-window\agents-window.desktop.main.js"


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

# 反转表：[(当前patch后文本, 原始文本)] —— compact(P1-P3) + enhance(P-A~P-E)
REVERSES = [
    ('const c=(0,uin.useMemo)(()=>s,[t,s])', 'const c=(0,uin.useMemo)(()=>s||t<iDa,[t,s])'),
    ('const c=(0,ZBn.useMemo)(()=>s,[t,s])', 'const c=(0,ZBn.useMemo)(()=>s||t<oyu,[t,s])'),
    ('const c=(0,qqn.useMemo)(()=>s,[t,s])', 'const c=(0,qqn.useMemo)(()=>s||t<kHu,[t,s])'),
    ('const z=(0,wY.useMemo)(()=>!!r,[r])', 'const z=(0,wY.useMemo)(()=>!!(r||e.trim().length<3),[r,e])'),
    ('const z=(0,TX.useMemo)(()=>!!r,[r])', 'const z=(0,TX.useMemo)(()=>!!(r||e.trim().length<3),[r,e])'),
    ('const z=(0,UX.useMemo)(()=>!!r,[r])', 'const z=(0,UX.useMemo)(()=>!!(r||e.trim().length<3),[r,e])'),
    ('$=(0,wY.useMemo)(()=>!1,[e])', '$=(0,wY.useMemo)(()=>e.length>z5p,[e])'),
    ('$=(0,TX.useMemo)(()=>!1,[e])', '$=(0,TX.useMemo)(()=>e.length>ohv,[e])'),
    ('$=(0,UX.useMemo)(()=>!1,[e])', '$=(0,UX.useMemo)(()=>e.length>zvb,[e])'),
    ('let G;{const X=c||"agent"', 'let G;if(Gi[Ui.SHOW_MODEL_SELECTOR]){const X=c||"agent"'),
    ('params:{sessionId:d,questionText:e,references:K,extra:G?.MODEL_KEY?{customModel:{name:G.MODEL_KEY,value:G.CUSTOM_MODEL?.model||G.MODEL_KEY}}:{},...G?{_meta:G}:{}}}})', 'params:{sessionId:d,questionText:e,references:K,...G?{_meta:G}:{}}}})'),
    ('try{/* P-E start */const G2=await R.resolvePromptModelMeta(c||"agent",o?.sessionType,d);const mMeta=G2?.CUSTOM_MODEL,mKey=G2?.MODEL_KEY;if(mKey&&mMeta?.parameters?.api_key){try{const apiKey=mMeta.parameters.api_key;const baseUrl=mMeta.provider==="deepseek"?"https://api.deepseek.com":(mMeta.base_url||"");if(baseUrl){const hr=await fetch(baseUrl.replace(/\\/+$/,"")+"/chat/completions",{method:"POST",headers:{"Content-Type":"application/json",Authorization:"Bearer "+apiKey},body:JSON.stringify({model:mMeta.model,messages:[{role:"system",content:"You are a professional prompt optimization assistant. Output only the optimized instruction wrapped in <enhanced-prompt> tags."},{role:"user",content:"Here is an instruction that I\'d like to give you, but it needs to be improved. Rewrite and enhance this instruction to make it clearer, more specific, less ambiguous, and correct any mistakes. Do not use any tools: reply immediately with your answer, even if you\'re not sure.\\n\\n<instruction>\\n"+e+"\\n</instruction>"}],stream:!1,temperature:.3})});const jd=await hr.json();const txt=jd?.choices?.[0]?.message?.content||"";const m2=txt.match(/<enhanced-prompt>([\\s\\S]*?)<\\/enhanced-prompt>/);const out=(m2?m2[1]:txt).trim();if(out&&U()){x.current=out;l?.current&&"setPromptEnhanceOperation"in l.current&&l.current.setPromptEnhanceOperation(e);n(out);g(!0);v(e);w([]);i();return}}}catch(err){console.warn("[P-E] local enhance failed, fallback:",err)}}/* P-E end */const K=await', 'try{const K=await'),
]

# 专家团 patch 标记（回滚后必须仍存在，防止误伤）
EXPERTS_MARKERS = [
    "_isCustomModelExists(e){return!!uie(e)}",          # P1
    "r===pn.EXPERTS?(this._availableModelConfigs.get(r)||[]).concat(",  # P2
    "re=(0,yl.useMemo)(()=>!1,[Q.userPlan,Q.userInfo,c])",  # P4
]


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
    already = []
    for new, old in REVERSES:
        cnt_new = content.count(new)
        if cnt_new == 0:
            already.append(new)
            continue
        if old in content:
            print("[!] 原始代码段已存在（可能已回滚）:", old[:60], "...")
            already.append(new)
            continue
        if cnt_new in (1, 3):
            todo.append((new, old))
        else:
            print("[!] patch 文本出现 %d 次（预期 1 或 3），请人工确认:" % cnt_new, new[:60], "...")
            sys.exit(3)

    if already:
        print("[*] %d 项无需回滚（未找到 patch 或已还原）" % len(already))
    if not todo:
        print("[*] 全部 patch 已回滚，无需操作。")
    else:
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        bak = JS + ".bak_allrollback_" + ts
        shutil.copy2(JS, bak)
        print("[1/3] 已备份当前(patch)状态:", os.path.basename(bak))

        for new, old in todo:
            content = content.replace(new, old)
        with open(JS, "w", encoding="utf-8", newline="") as f:
            f.write(content)
        print("[2/3] 已还原 %d 处 patch" % len(todo))

    # 读回验证
    with open(JS, "r", encoding="utf-8", errors="replace") as f:
        check = f.read()
    miss = [old for _, old in REVERSES if old not in check]
    leftover = [new for new, _ in REVERSES if new in check]
    experts_ok = all(m in check for m in EXPERTS_MARKERS)
    print("[3/3] 原始代码段缺失:", len(miss), "| patch 残留:", len(leftover), "| 专家团 patch 保留:", experts_ok)
    if not miss and not leftover and experts_ok:
        print("      回滚验证通过。重启 Qoder 后压缩/优化输入恢复原始行为。")
    else:
        print("[!] 验证未全通过！请从备份恢复。")
        sys.exit(4)


if __name__ == "__main__":
    main()