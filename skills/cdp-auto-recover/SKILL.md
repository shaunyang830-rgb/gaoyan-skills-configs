---
name: cdp-auto-recover
description: 自动诊断并修复 Chrome CDP 连接，执行 check-deps、拉起调试 Chrome、校验 proxy 与 targets。用户提到“CDP 挂了/打不开/连不上/恢复 CDP”或出现 chrome not connected、proxy not ready 时必须优先使用。
---

# CDP Auto Recover

## Purpose
在继续任何 CDP 任务前，先把 CDP 恢复到可用状态并返回可验证证据。

## Execution Rules (Hard Gate)
- 发现 CDP 不可用时，**先恢复、后继续**。
- 禁止在恢复前改走其他方案（WebSearch/WebFetch/curl）规避问题。
- 禁止先问用户“要不要重试/要不要改方案”；默认直接自愈。
- 仅当恢复脚本执行后仍失败，才向用户汇报失败证据并请求下一步。

## Run
`powershell -ExecutionPolicy Bypass -File c:\Users\杨顺\Documents\Obsidian Vault\.claude\skills\cdp-auto-recover\scripts\recover-cdp.ps1`

## Success Criteria
- 输出包含 `node: ok`
- 输出包含 `chrome: ok (port 9222)`
- 输出包含 `proxy: ready`
- `http://127.0.0.1:3456/targets` 返回正常 JSON

## Trigger phrases
- CDP 又挂了
- CDP 打不开
- 帮我恢复 CDP
- chrome not connected
- proxy not ready
