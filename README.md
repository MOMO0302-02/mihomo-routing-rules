# Mihomo Routing Rules

一组面向 Mihomo/Clash Meta 的公开分流规则，重点覆盖 AI 服务、GitHub、TikTok、支付、流媒体、Microsoft、Adobe 和常用移动应用。

[![Validate rules](https://github.com/MOMO0302-02/mihomo-routing-rules/actions/workflows/validate.yml/badge.svg)](https://github.com/MOMO0302-02/mihomo-routing-rules/actions/workflows/validate.yml)
[![Latest release](https://img.shields.io/github/v/release/MOMO0302-02/mihomo-routing-rules)](https://github.com/MOMO0302-02/mihomo-routing-rules/releases/latest)

## 先说明

本仓库提供的是**规则片段**，不是完整订阅。它不包含代理节点、DNS、端口或策略组，不能直接替代你的订阅配置。

使用时需要把 `rule-providers` 和 `rules` 合并进现有 Mihomo 配置，或者放进 Clash Party、FlClash 等客户端的覆写/扩展配置中。23 个分类的用途、条目数和独立下载地址见 [`RULES.md`](RULES.md)。

## 稳定更新通道

- `main`：文档、示例、验证器和下一版规则的开发分支。
- `release`：通过验证后才更新的稳定消费分支，配置文件应固定引用它。
- [GitHub Releases](https://github.com/MOMO0302-02/mihomo-routing-rules/releases)：按规则版本保存可下载归档和 manifest。

规则地址优先使用 GitHub Raw：

```text
https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/<分类名>.yaml
```

网络环境无法稳定访问 Raw 时，可改用 jsDelivr：

```text
https://cdn.jsdelivr.net/gh/MOMO0302-02/mihomo-routing-rules@release/rules/<分类名>.yaml
```

jsDelivr 可能存在缓存延迟，不保证与 `release` 分支瞬时同步；需要立即获得最新版时优先使用 Raw 或 GitHub Release。

## 最快用法：添加一个分类

下面以 AI 规则为例。

### 1. 添加远程规则源

把这一段放到配置根级的 `rule-providers:` 中：

```yaml
rule-providers:
  ai_custom:
    type: http
    behavior: classical
    format: yaml
    url: https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/ai_custom.yaml
    path: ./ruleset/ai_custom.yaml
    interval: 86400
```

如果原配置已经有 `rule-providers:`，只复制其中的 `ai_custom:` 部分，不要再创建第二个同名根字段。

### 2. 添加分流规则

把这行插入配置根级的 `rules:` 中，并放在 `GEOSITE`、`GEOIP`、`MATCH` 等兜底规则之前：

```yaml
rules:
  - RULE-SET,ai_custom,AI
```

`AI` 必须是你配置里已经存在的策略组。没有这个策略组时，可改成你现有的组名，例如 `节点选择`、`其他代理`，或者按需求改成 `DIRECT`。

### 3. 验证配置

```bash
mihomo -t -f config.yaml
```

通过后重新加载配置。首次命中时，Mihomo 会自动下载对应规则文件。

## 全量使用 23 个分类

仓库提供三种组合文件：

- [`examples/all-in-one.yaml`](examples/all-in-one.yaml)：完整合并片段，包含 `rule-providers` 和建议的 `rules` 顺序。
- [`examples/rule-providers.yaml`](examples/rule-providers.yaml)：只有全部 provider 定义。
- [`examples/rules.yaml`](examples/rules.yaml)：只有建议的规则顺序和策略名。

推荐操作：

1. 打开 [`examples/all-in-one.yaml`](examples/all-in-one.yaml)。
2. 将其中 `rule-providers` 的子项合并到现有配置的同名根字段。
3. 将其中的 `RULE-SET` 行插入现有 `rules` 列表前部。
4. 按下表把示例策略名替换成你配置中真实存在的策略组。
5. 保证这些自定义规则位于 `MATCH` 等兜底规则之前。
6. 运行 `mihomo -t -f config.yaml`，通过后再让客户端重新加载。

不要把 `all-in-one.yaml` 当作完整订阅直接导入；它没有代理节点和完整运行参数。

## 和原有规则怎么排序

这 22 类是高优先级的服务专项规则，不负责替代你原配置的 LAN、广告、国内/国外大类或最终兜底策略。推荐顺序：

1. 本地网络、私有地址和必须优先的安全规则；
2. 本仓库的专项 `RULE-SET`；
3. 原配置的其他服务、`GEOSITE`、`GEOIP`；
4. 最后的 `MATCH`。

你原配置采用“默认直连”还是“默认代理”，仍由最后的兜底规则决定；接入本仓库不应擅自改变 `MATCH`。`openai_login_custom` 是 `ai_custom` 的专项子集，必须排在它前面。

## 示例策略名怎么对应

| 示例策略 | 对应分类 | 建议 |
|---|---|---|
| `DIRECT` | 抖音、腾讯文档、国内移动应用、国内手游、Microsoft 连通性、Adobe 下载、指定直连 AI API | 保持直连 |
| `AI` | OpenAI 登录、Google Drive、AI API、综合 AI 服务 | 换成你的 AI 或稳定代理组 |
| `GitHub` | GitHub | 换成你的开发服务代理组 |
| `TikTok` | TikTok/CapCut | 换成适合目标地区的节点组 |
| `Crypto` | 加密货币服务 | 换成稳定、地区一致的代理组 |
| `Payment` | 支付服务 | 换成固定地区或稳定节点组 |
| `Streaming` | 流媒体、YouTube | 换成流媒体策略组 |
| `Microsoft` | Microsoft Store、更新和其他服务 | 按你的网络情况选择代理组 |
| `Adobe` | Adobe 服务 | 换成 Adobe 或通用代理组 |
| `OtherProxy` | 海外移动应用 | 换成通用代理组 |

## Clash Party / FlClash 等订阅客户端

如果你使用远程订阅，不建议直接修改客户端缓存下来的订阅文件，因为更新订阅后通常会被覆盖。

应使用客户端提供的“覆写、扩展配置、Merge、Mixin”一类功能：

1. 把 [`examples/rule-providers.yaml`](examples/rule-providers.yaml) 的内容合并到根级 `rule-providers`。
2. 把 [`examples/rules.yaml`](examples/rules.yaml) 中需要的行插入根级 `rules` 前部。
3. 将示例策略名替换成订阅中实际存在的策略组名称。
4. 保存覆写并重新加载订阅。

不同客户端的菜单名称会变化，但合并目标始终是配置根级的 `rule-providers` 和 `rules`，不是 `proxies` 或 `proxy-groups`。

## 只用某个规则文件

所有分类都在 [`rules/`](rules/) 下；完整索引见 [`RULES.md`](RULES.md)。稳定远程地址格式为：

```text
https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/<分类名>.yaml
```

例如：

```text
https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/release/rules/tiktok_custom.yaml
```

全部分类、建议策略、条目数、Raw 与 CDN 地址见 [`RULES.md`](RULES.md)，精确 SHA-256 见 [`manifest.json`](manifest.json)。

## 更新方式

provider 示例使用 `interval: 86400`，Mihomo 会每 24 小时检查一次更新。需要立即更新时，可在客户端的规则集/provider 页面手动刷新，或重载配置。

## 仓库自检

克隆仓库后可运行：

```bash
python tools/validate_rules.py
```

验证器会检查分类数量、规则数量、重复项、manifest 哈希和敏感信息。GitHub Actions 会在每次推送时执行同样的检查。

## 目录

- `rules/`：可由 Mihomo 直接加载的 classical rule-provider。
- `examples/`：单独片段与全量合并示例。
- `RULES.md`：全部分类、建议策略和下载地址索引。
- `manifest.json`：版本、条目数和文件哈希。
- `tools/validate_rules.py`：无第三方依赖的本地验证器。

## 维护与来源

- 贡献或修正规则前先读 [`CONTRIBUTING.md`](CONTRIBUTING.md)。
- 版本变化见 [`CHANGELOG.md`](CHANGELOG.md)。
- 仓库的发布结构参考了 [Loyalsoldier/clash-rules](https://github.com/Loyalsoldier/clash-rules) 的稳定分支、逐文件地址和发布归档做法；没有复制其规则数据或代码。

## 隐私边界

此仓库只公开通用规则。机场站点、本地专用服务、订阅链接、代理节点、UUID、密码、Token、KV 状态和客户端数据均不会进入仓库。

## 许可

[MIT](LICENSE)
