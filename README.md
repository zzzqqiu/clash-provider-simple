# clash-provider-simple

[中文](#中文说明) | [English](#english)

## 中文说明

`clash-provider-simple` 是一个面向 Clash Mi / iOS 使用场景的精简 rule-provider 聚合仓库。

规则来源于优秀的开源项目 [Loyalsoldier/clash-rules](https://github.com/Loyalsoldier/clash-rules)。原项目提供了完整、细分的 Clash Premium `RULE-SET` 规则集，兼容 ClashX Pro、Clash for Windows 等基于 Clash Premium 内核的客户端。

本仓库不原创规则内容，只做一件事：把多个上游规则文件定时拉取、合并、去重，并发布成 3 个更少的 provider 文件，方便 Clash Mi 在 iOS 上加载。

### 为什么要做这个？

在 iOS 上使用 Clash Mi 时，如果配置里有 10+ 个 `rule-providers`，VPN 启动阶段可能需要同步加载多个 provider。这个过程会产生多次 HTTP 请求和 DNS 解析，如果网络环境不稳定，可能阻塞 iOS Network Extension 启动流程，导致 VPN 启动失败。

所以这个仓库把“规则自动更新”从 Clash Mi 客户端转移到 GitHub Actions：

- GitHub Actions 监控上游更新，并保留每 6 小时强制刷新兜底
- 自动合并成 3 个文件
- Clash Mi 只加载 3 个 provider
- 保留自动更新能力
- 降低 VPN 启动阶段的网络阻塞风险

### 合并结果

- `merged_proxy.txt`: `proxy.txt` + `gfw.txt` + `tld-not-cn.txt` + `google.txt`
- `merged_direct.txt`: `direct.txt` + `cncidr.txt` + `lancidr.txt` + `apple.txt` + `icloud.txt`
- `merged_reject.txt`: `reject.txt` + `private.txt`

### Raw URLs

```text
https://raw.githubusercontent.com/ranjugao/clash-provider-simple/main/merged_proxy.txt
https://raw.githubusercontent.com/ranjugao/clash-provider-simple/main/merged_direct.txt
https://raw.githubusercontent.com/ranjugao/clash-provider-simple/main/merged_reject.txt
```

### Clash Mi 使用示例

把原来多个上游 `rule-providers` 简化成下面 3 个：

```yaml
rule-providers:
  proxy:
    type: http
    behavior: domain
    url: https://raw.githubusercontent.com/ranjugao/clash-provider-simple/main/merged_proxy.txt
    interval: 21600

  direct:
    type: http
    behavior: domain
    url: https://raw.githubusercontent.com/ranjugao/clash-provider-simple/main/merged_direct.txt
    interval: 21600

  reject:
    type: http
    behavior: domain
    url: https://raw.githubusercontent.com/ranjugao/clash-provider-simple/main/merged_reject.txt
    interval: 21600

rules:
  - RULE-SET,reject,REJECT
  - RULE-SET,direct,DIRECT
  - RULE-SET,proxy,PROXY
```

如果你的代理策略组不叫 `PROXY`，请把 `RULE-SET,proxy,PROXY` 里的 `PROXY` 改成你的实际策略组名称。

### 自动更新

GitHub Actions 支持两种更新触发方式：

- 每小时 `:15` 和 `:45` 检查一次上游 `Loyalsoldier/clash-rules` 的 `release` 分支。
- 如果发现上游 SHA 变化，会等待 10 分钟再合并，避免刚发布时文件还没完全同步。
- 每 6 小时强制刷新一次，作为兜底机制。
- 也支持在 Actions 页面手动触发。

更新流程：

1. 从 `Loyalsoldier/clash-rules` 下载上游规则文件。
2. 合并成 3 个 provider 文件。
3. 删除空行。
4. 使用 `sort -u` 去重。
5. 仅在文件有变化时提交，避免空 commit 报错。

### 致谢与许可

规则内容来自 [Loyalsoldier/clash-rules](https://github.com/Loyalsoldier/clash-rules)，原项目使用 GNU General Public License v3.0。

本仓库只是对上游规则进行自动化合并与发布。使用前请自行确认你的 Clash 客户端、规则格式和策略组名称是否匹配。

---

## English

`clash-provider-simple` is a small rule-provider aggregation repository for Clash Mi on iOS.

The rule content comes from the excellent open-source project [Loyalsoldier/clash-rules](https://github.com/Loyalsoldier/clash-rules), which provides complete Clash Premium `RULE-SET` files for clients such as ClashX Pro, Clash for Windows, and other Clash Premium-core clients.

This repository does not create original rule content. It only fetches upstream rule files on a schedule, merges them, removes empty lines, deduplicates entries, and publishes 3 simplified provider files for Clash Mi.

### Why

On iOS, loading 10+ `rule-providers` during VPN startup can trigger many HTTP requests and DNS lookups. If those requests block, iOS Network Extension may time out and Clash Mi may fail to start the VPN.

This repository moves rule-provider updates from the iOS client to GitHub Actions:

- GitHub Actions monitors upstream changes and keeps a forced 6-hour refresh as a fallback
- Rules are merged into 3 files
- Clash Mi only loads 3 providers
- Automatic updates are preserved
- VPN startup has fewer network requests to block on

### Output Files

- `merged_proxy.txt`: `proxy.txt` + `gfw.txt` + `tld-not-cn.txt` + `google.txt`
- `merged_direct.txt`: `direct.txt` + `cncidr.txt` + `lancidr.txt` + `apple.txt` + `icloud.txt`
- `merged_reject.txt`: `reject.txt` + `private.txt`

### Raw URLs

```text
https://raw.githubusercontent.com/ranjugao/clash-provider-simple/main/merged_proxy.txt
https://raw.githubusercontent.com/ranjugao/clash-provider-simple/main/merged_direct.txt
https://raw.githubusercontent.com/ranjugao/clash-provider-simple/main/merged_reject.txt
```

### Usage

Replace many upstream rule providers in Clash Mi with these three merged providers:

```yaml
rule-providers:
  proxy:
    type: http
    behavior: domain
    url: https://raw.githubusercontent.com/ranjugao/clash-provider-simple/main/merged_proxy.txt
    interval: 21600

  direct:
    type: http
    behavior: domain
    url: https://raw.githubusercontent.com/ranjugao/clash-provider-simple/main/merged_direct.txt
    interval: 21600

  reject:
    type: http
    behavior: domain
    url: https://raw.githubusercontent.com/ranjugao/clash-provider-simple/main/merged_reject.txt
    interval: 21600

rules:
  - RULE-SET,reject,REJECT
  - RULE-SET,direct,DIRECT
  - RULE-SET,proxy,PROXY
```

If your proxy policy group is not named `PROXY`, replace `PROXY` with the actual policy group name in your Clash Mi profile.

### Update Schedule

GitHub Actions supports multiple update triggers:

- Checks the upstream `Loyalsoldier/clash-rules` `release` branch at minute `:15` and `:45` every hour.
- If the upstream SHA changed, waits 10 minutes before merging, so freshly published upstream files have time to settle.
- Runs a forced refresh every 6 hours as a safety fallback.
- Can also be triggered manually from the Actions tab.

The update workflow:

1. Downloads upstream rule files from `Loyalsoldier/clash-rules`.
2. Merges them into three provider files.
3. Removes empty lines.
4. Deduplicates entries with `sort -u`.
5. Commits and pushes only when the merged files changed.

### Credits and License

Rule content comes from [Loyalsoldier/clash-rules](https://github.com/Loyalsoldier/clash-rules), licensed under GNU General Public License v3.0.

This repository only automates merging and publishing upstream rules. Please verify that your Clash client, rule syntax, and policy group names match your own profile before use.
