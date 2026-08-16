# -*- coding: utf-8 -*-
"""终极验证：P-E 代码 + stub 依赖直接执行（node 运行）。"""
import subprocess, sys, os

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

wd = r"c:\Users\53518\Documents\Qoder\2026-08-14\chat-3\compact"
data = open(os.path.join(wd, "_test_enhance_copy.js"), encoding="utf-8", errors="replace").read()
i = data.find("try{/* P-E start */")
j = data.find("},[e,h,d", i)  # 不含 N 函数体闭（main 容器提供）
pe = data[i:j]  # try{...finally{...}

# 构造 stub 环境
stub = r"""
const R = { resolvePromptModelMeta: async () => ({MODEL_KEY:"custom:model_x", CUSTOM_MODEL:{provider:"deepseek", model:"deepseek-chat", parameters:{api_key:"sk-test"}}}) };
const c = "agent", o = { sessionType: "quest" }, e = "hello world", d = "session-test";
const U = () => true;
const x = { current: "old" };
const l = { current: {} };
const n = (v) => { console.log("setInputValue:", v.slice(0, 40)); };
let g, v, w, i;
g = () => {}; v = () => {}; w = () => {}; i = () => {};
// fetch stub（不真正发请求，模拟成功响应）
global.fetch = async (url, opts) => {
  console.log("fetch url:", url);
  console.log("fetch model:", JSON.parse(opts.body).model);
  console.log("fetch hasAuth:", (opts.headers.Authorization||"").startsWith("Bearer "));
  return { json: async () => ({ choices: [{ message: { content: "<enhanced-prompt>optimized: " + JSON.parse(opts.body).messages[1].content.slice(0,30) + "</enhanced-prompt>" } }] }) };
};
const K = await (async () => { return "ok"; })();
"""
stub2 = r"""
const R = { resolvePromptModelMeta: async () => ({MODEL_KEY:"custom:model_x", CUSTOM_MODEL:{provider:"deepseek", model:"deepseek-chat", parameters:{api_key:"sk-test"}}}) };
const c = "agent", o = { sessionType: "quest" }, e = "hello world", d = "session-test";
const U = () => true;
const x = { current: "old" };
const l = { current: {} };
const n = (val) => { console.log("ENHANCED_OK:", val.slice(0, 60)); };
let g = () => {}, v = () => {}, w = () => {}, i = () => {};
const p = () => {}, a = () => {};
global.fetch = async (url, opts) => {
  console.log("URL:", url);
  console.log("MODEL:", JSON.parse(opts.body).model);
  console.log("AUTH:", (opts.headers.Authorization || "").slice(0, 20) + "...");
  return { json: async () => ({ choices: [{ message: { content: "<enhanced-prompt>optimized text</enhanced-prompt>" } }] }) };
};
"""

# 组合：async main 里运行 P-E 代码（P-E 从 try{ 开始，包含完整 try/catch/finally 到 N 函数闭 }
test_src = "async function main(){\n" + stub2 + "\n" + pe + "\nconsole.log('DONE');\n}\nmain();\n"
tf = os.path.join(wd, "_t_pe_run.js")
with open(tf, "w", encoding="utf-8", newline="\n") as f:
    f.write(test_src)

r = subprocess.run(["node", tf], capture_output=True, text=True, timeout=60)
print("exit:", r.returncode)
print("STDOUT:", r.stdout[:500])
print("STDERR:", r.stderr[:500])
