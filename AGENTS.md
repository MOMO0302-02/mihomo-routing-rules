---
项目: Mihomo Routing Rules
维护方: Codex
真相源: 本文件 + manifest.json + Git
最后校准: 2026-07-29
状态源: git
状态源路径: D:\mihomo-routing-rules
---

# Mihomo Routing Rules 上手包

## 一句话

这是从订阅工作台脱敏导出的公开 Mihomo classical rule-provider 规则库，只包含分流规则，不包含代理节点、订阅地址或发布凭据。

## 当前状态

- 公开规则版本：`v2026.07.29.1GoogleAITK`（22 类、711 条；在 v2026.07.28.2 无损去冗余的基础上，`ai_custom` 新增 `DOMAIN-SUFFIX,antigravity.google`）。
- 规则文件、条目数和 SHA-256 以 `manifest.json` 为准。
- 使用方式以 `README.md`、`RULES.md` 与 `examples/all-in-one.yaml` 为准；示例是合并片段，不是完整订阅。
- `main` 是开发与文档分支，`release` 是通过验证后的稳定消费分支；公开配置地址只引用 `release`。
- GitHub 仓库：`MOMO0302-02/mihomo-routing-rules`。

## 怎么验证

```powershell
python tools\validate_rules.py
git diff --check
```

## 红线

- 禁止加入代理节点、UUID、密码、订阅地址、Cloudflare/GitHub 凭据或本机状态。
- `airport_site_custom` 与 `recmata_service_direct_custom` 属于私有工作台规则，不得发布。
- 修改规则后必须同步 `manifest.json` 中的计数与 SHA-256，并通过验证器。
- 公开发布、改可见性和删除仓库仍需用户明确授权。

## 跨工具任务接续（Beads）

项目使用本机 stealth 模式 `.beads`。新会话先运行：

```powershell
bd prime
bd ready
```

- `ai-ready/open`：AI 可直接执行的本地工作。
- `human/blocked`：需要用户选择或人工验收。
- `external-authorization/blocked`：公开发布、打 tag、推送或外部状态变更。
- `backlog/deferred`：以后再评估。
