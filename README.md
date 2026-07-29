# Mihomo Routing Rules

一组面向 Mihomo/Clash Meta 的公开分流规则，重点覆盖 AI 服务、GitHub、TikTok、支付、流媒体、Microsoft、Adobe 和常用移动应用。

## 特点

- 每个分类都是 Mihomo `behavior: classical` 可用的独立 YAML rule-provider。
- 规则数据只包含域名、关键词和进程名，不包含任何代理节点。
- 每次发布都由 `manifest.json` 绑定文件条目数与 SHA-256。
- GitHub Actions 自动检查格式、重复项、清单哈希和敏感信息。

## 使用

以 AI 规则为例：

```yaml
rule-providers:
  ai_custom:
    type: http
    behavior: classical
    format: yaml
    url: https://raw.githubusercontent.com/MOMO0302-02/mihomo-routing-rules/main/rules/ai_custom.yaml
    path: ./ruleset/ai_custom.yaml
    interval: 86400

rules:
  - RULE-SET,ai_custom,AI
```

`examples/rule-providers.yaml` 包含全部公开分类的 provider 定义，`examples/rules.yaml` 给出建议顺序与策略名称。策略组名称只是示例，需要与你自己的配置保持一致。

## 目录

- `rules/`：可直接由 Mihomo 加载的规则文件。
- `examples/`：provider 和规则顺序示例。
- `manifest.json`：版本、条目数和文件哈希。
- `tools/validate_rules.py`：无第三方依赖的本地验证器。

## 隐私边界

此仓库只公开通用规则。机场站点、本地专用服务、订阅链接、代理节点、UUID、密码、Token、KV 状态和客户端数据均不会进入仓库。

## 验证

```bash
python tools/validate_rules.py
```

## 许可

[MIT](LICENSE)
