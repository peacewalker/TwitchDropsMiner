# Twitch Drops Miner WebUI Lite

本版本保留 fireph 的 NiceGUI WebUI，参考 fireph/docker-twitch-drops-miner 的端口、配置挂载和启动方式，改为直接从源码构建，不等待 fireph 发布打包程序。

## 行为

- 只使用已有的 `config/cookies.jar` 登录，沿用原来的配置和缓存目录。
- 不提供 Twitch 登录按钮，不收集密码或令牌。
- 镜像不包含 Chromium、Xvfb、VNC、noVNC、zendriver，也不包含浏览器登录模块。
- Cookie 缺失或失效时，等待你放入有效文件并重启容器，不启动浏览器、不循环重启。
- 每 30 分钟检查 DevilXD/TwitchDropsMiner 的 `master`，直接合并更新。
- 测试通过后构建并检查 amd64、arm64 镜像，全部成功才更新 `latest`。
- 合并冲突、测试失败或构建失败时保留已发布镜像；需要处理冲突后重跑 Actions。
- 已发布的同一源码版本在定时任务中跳过构建。构建失败的版本会在后续定时任务中重试。

GitHub 的定时任务可能延迟，检查周期不等于更新时限。公开仓库长期没有活动时，GitHub 也可能暂停定时任务；可在 Actions 页面重新启用。上游改变 WebUI 依赖接口时，仍可能需要人工适配。

## 首次发布

1. Fork `https://github.com/fireph/TwitchDropsMiner`，保留默认 `webui` 分支。
2. 将本次修改及上游合并提交写入你自己的 `webui` 分支。
3. 在 Actions 页面启用工作流。新文件为 `.github/workflows/lite.yml`。
4. 运行 **Sync upstream and publish browser-free image**。
5. 镜像发布到 `ghcr.io/<你的GitHub用户名>/twitch-drops-miner:latest`。

工作流使用自带 `GITHUB_TOKEN`，不需要 Docker Hub 密码或 PAT_TOKEN。仓库必须允许 Actions 写入仓库和 Packages。如果首次 GHCR 镜像是私有的，可以在 GitHub Packages 的包设置里改成 Public，或者在拉取机器上使用有读取包权限的凭据登录 GHCR。

## 部署

已配置 `peacewalker` 的示例：

```bash
docker compose -f compose.lite.yml up -d
```

先将现有有效 `cookies.jar` 放入 `./config/`。这必须是原矿工使用的 Cookie 文件格式，不是任意浏览器导出的文本文件。保留现有 `settings.json` 即可沿用设置。WebUI 地址为 `http://服务器地址:5800`。

宿主机目录位置、端口和 `USER_ID` / `GROUP_ID` 可以按现有部署修改。默认以 root 启动入口脚本设置目录权限，随后以 UID/GID 1000 运行应用。

更新：

```bash
docker compose -f compose.lite.yml pull
docker compose -f compose.lite.yml up -d
```

Cookie 更新后重启：

```bash
docker compose -f compose.lite.yml restart
```

镜像发布不会自动更新你服务器上已运行的容器。原版本的 WebUI HTTPS 与鉴权配置仍可使用。

## 本地构建

```bash
docker build -f Dockerfile.lite -t twitch-drops-miner:lite .
```

采用 Python slim 多阶段构建，安装 Python 依赖后复制运行环境，运行镜像不包含构建工具。实际体积以构建结果为准，不能把内存占用与镜像磁盘体积混为一谈。

## 验证与来源

已合并 DevilXD 上游提交 `f693b0ca41301ac2282f3978713479efebe0490e`，其中包括最新的 playlist HEAD 掉宝逻辑。

基于 fireph WebUI 提交 `10706072459ce1125b6747e685bf5c5b3d1a69c6`。

本地及 GitHub Actions 已通过 321 项测试，2 项需要 Chromium 的集成测试跳过。amd64 和 arm64 镜像均已构建并通过实际容器启动检查，WebUI 与健康检查可用，浏览器登录路由不存在。首次发布的源码为 `af2743e6d3e15f6f90fa3327f518d8589c5d9f7a`，公开镜像可以免登录拉取。

来源：

- https://github.com/DevilXD/TwitchDropsMiner
- https://github.com/fireph/TwitchDropsMiner
- https://github.com/fireph/docker-twitch-drops-miner

原项目许可证保持不变。
