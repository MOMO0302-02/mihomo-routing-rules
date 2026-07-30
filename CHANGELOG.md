# Changelog

## v2026.07.29.1GoogleAITK

### Rules

- `ai_custom` 增加 `DOMAIN-SUFFIX,antigravity.google`，覆盖 Google Antigravity 的授权与产品域名；分类保持 22 个，规则由 710 条增至 711 条。
- 该域名此前无任何规则命中，会落到用户配置的兜底策略，与同一登录链路上的 `*.googleapis.com` 分处不同策略组。`.google` gTLD 不被 `geosite:google` 覆盖，同类域名需逐条显式加入。

## v2026.07.28.2GoogleAITK

### Rule quality

- 无损移除 102 条已被同组 `DOMAIN-SUFFIX` 完全覆盖的 `DOMAIN` 规则。
- 公开分类保持 22 个，规则由 812 条精简为 710 条，实际匹配范围不变。
- 验证器新增同类语义冗余门禁，防止重复写法回流。

### Distribution

- 增加稳定 `release` 消费分支，`main` 保留为开发与文档分支。
- 所有示例切换到 `release` 地址。
- 增加 22 类规则索引、GitHub Raw 与 jsDelivr 双下载地址。
- 增加贡献、隐私和发布流程说明。
- 扩展验证器，锁定稳定地址、规则索引和示例完整性。

## v2026.07.28.1GoogleAITK

### Public rule set

- 首次公开 22 个通用分类，共 812 条 Mihomo classical 规则。
- 排除机场站点、本地专用服务、订阅、节点和凭据。
