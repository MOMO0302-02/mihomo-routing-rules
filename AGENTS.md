---
项目: Mihomo Routing Rules
维护方: Codex
真相源: 本文件 + manifest.json + Git
最后校准: 2026-07-28
状态源: git
状态源路径: D:\mihomo-routing-rules
---

# Mihomo Routing Rules 上手包

## 一句话

这是从订阅工作台脱敏导出的公开 Mihomo classical rule-provider 规则库，只包含分流规则，不包含代理节点、订阅地址或发布凭据。

## 当前状态

- 公开规则版本：`v2026.07.28.1GoogleAITK`。
- 规则文件、条目数和 SHA-256 以 `manifest.json` 为准。
- 使用方式以 `README.md` 与 `examples/all-in-one.yaml` 为准；示例是合并片段，不是完整订阅。
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
