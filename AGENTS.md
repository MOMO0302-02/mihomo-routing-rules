---
项目: Mihomo Routing Rules
维护方: Codex
真相源: 本文件 + manifest.json + Git
最后校准: 2026-08-16
状态源: git
状态源路径: F:\AI\Github分流规则
---

# Mihomo Routing Rules 上手包

## 一句话

这是从订阅工作台脱敏导出的公开 Mihomo classical rule-provider 规则库，只包含分流规则，不包含代理节点、订阅地址或发布凭据。

## 当前状态

- 公开规则版本：`v2026.08.16.1GoogleAITK`（22 类、779 条）。2026-08-16 在 `ai_custom` 增加 68 条（96→164），细节见 `CHANGELOG.md`；同批已同步写回上游订阅工作台规则源，两侧逐条一致。**改动目前只在本地工作区，提交、推送与打 tag 均待用户授权。**
- 2026-08-16：本次版本标记由本库先行铸造（规则先在本库和上游规则源落地，上游尚未重新生成），与「只在与上游内容等价后对齐」的常规顺序相反。上游下次生成时应确认它带出同一标记；若上游生成出别的序号，以上游为准回改本库。
- 版本标记只在与上游比对确认内容等价后对齐；条目有实际增删时必须同步 `manifest.json` 计数与 SHA-256、`RULES.md` 索引及 `CHANGELOG.md`。
- 2026-08-16 踩坑（`.google` 教训的推广）：域名迁移和产品被收购同样会让旧规则静默失效，且不会报错。实测发现 `notebooklm.google`→`notebook.google`、`lmarena.ai`→`arena.ai`、`hyperbolic.xyz`→`hyperbolic.ai`，以及 Windsurf 被 Cognition 收购后 `codeium.com`→`windsurf.com`→`devin.ai`。**只收 `api.*` 子域而不收主域**是同一类隐患（本次补了 14 家）。维护时应定期对已收录厂商做一次跳转探测，而不是只做「有没有新产品」的增量。
- 2026-08-16：国产 AI 站点收不收、进哪类，判据是**面向国内还是面向国际**，不是能否直连。实测 `deepseek.com` 直连可达（429 / 1.0s）但本库一直让它走 `ai_custom` 代理；反过来国内站直连快也不代表该收进 `ai_custom`。据此 `kimi.com`/`z.ai`/`qwen.ai`/`klingai.com`/`hailuoai.video` 等国际站进 `ai_custom`，而面向国内的 `hailuoai.com`（海螺国内站）与 `vidu.com`（`vidu.com`/`vidu.cn`/`vidu.studio` 全部 301 → `www.vidu.cn`，已无独立国际站）**刻意未收录**——本库没有网页类直连分类（只有 API 侧的 `ai_api_direct_custom`），收进 `ai_custom` 会把国内流量推上代理。要收必须新建直连分类。
- 2026-08-16 工具坑：本机 shell 设了 `HTTP_PROXY`/`HTTPS_PROXY=http://127.0.0.1:7890`，`curl` 不带 `-x` 也会走代理，直连探测会得出「直连和代理表现完全一致」的假结论。测直连必须加 `--noproxy '*'`，并且带对照组验证（`baidu.com` 应通、`google.com` 应超时）才算数。
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
