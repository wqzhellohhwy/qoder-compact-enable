# -*- coding: utf-8 -*-
"""最小复现：P-E 的 fetch 语句独立运行。"""
import subprocess, sys, os

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

wd = r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\compact"

# 从副本提取 P-E 的 fetch 部分（baseUrl 到 }); 结束）
d = open(os.path.join(wd, "_test_enhance_copy.js"), encoding="utf-8", errors="replace").read()
i = d.find("/* P-E start */")
seg = d[i : i + 1100]
# 提取 fetch 语句（从 const hr 到 const jd）
k = seg.find("const hr=await fetch")
l = seg.find("const jd=await hr.json")
fetch_stmt = seg[k:l]

src = """
async function main(){
  const mMeta = {provider:"deepseek", model:"deepseek-chat", parameters:{api_key:"sk-test"}};
  const e = "hello world";
  global.fetch = async (url, opts) => {
    console.log("URL:", url);
    console.log("MODEL:", JSON.parse(opts.body).model);
    console.log("AUTH:", (opts.headers.Authorization||"").slice(0,15)+"...");
    return { json: async () => ({ choices: [{ message: { content: "<enhanced-prompt>ok</enhanced-prompt>" } }] }) };
  };
  %FETCH%
  const jd = await hr.json();
  console.log("RESULT:", jd.choices[0].message.content);
}
main();
"""
src = src.replace("%FETCH%", fetch_stmt)
tf = os.path.join(wd, "_t_min.js")
with open(tf, "w", encoding="utf-8", newline="\n") as f:
    f.write(src)
r = subprocess.run(["node", tf], capture_output=True, text=True, timeout=60)
print("exit:", r.returncode)
print("STDOUT:", r.stdout[:400])
print("STDERR:", r.stderr[:400])
