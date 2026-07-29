# 贡献指南

欢迎提交公开、可复核的通用分流修正。本仓库不接受代理节点、订阅地址、账号凭据或个人网络状态。

## 修改规则

1. 在对应的 `rules/<provider>.yaml` 中修改 `payload`。
2. 只使用当前验证器支持的 classical 类型：`DOMAIN`、`DOMAIN-SUFFIX`、`DOMAIN-KEYWORD`、`PROCESS-NAME`。
3. 避免重复规则；能够使用精确域名或后缀时，不要用过宽的关键词。
4. 说明规则来源、服务用途和预期策略；不要仅以“在我的设备上能用”作为依据。
5. 同步 `manifest.json` 中对应文件的条目数、SHA-256、总条目数和分类数。
6. 如增删分类，同步 `examples/`、`RULES.md` 和 README。

## 本地验证

```bash
python tools/validate_rules.py
git diff --check
```

将片段合并到一份没有私密节点的测试配置后，再运行：

```bash
mihomo -t -f config.yaml
```

## 隐私与安全

禁止提交：

- `vless://`、`vmess://`、`trojan://`、`ss://` 等代理 URI；
- UUID、密码、Token、API Key；
- 机场订阅、机场域名、本地专用服务；
- Cloudflare KV、客户端日志、外部控制器密钥或真实设备状态。

`airport_site_custom` 与 `recmata_service_direct_custom` 永远只属于私有工作台，不进入公开仓库。

## 发布流程

`main` 用于审核下一版内容；验证通过后才把同一提交推进到 `release`，再创建与 `manifest.json` 规则版本一致的 GitHub Release。配置示例只引用 `release`，避免开发中的规则直接影响使用者。
