# 注意事项

- 每次改动完成后，都必须创建一个对应的 Git commit，以便后续追踪和回滚。
- 每次改动后，都必须编写或更新相关测试，并在交付给用户前，确保所有测试和验证全部通过。

## 部署（重要）

本仓库已配置 **GitHub Pages + Actions 自动部署**，不需要任何手动部署步骤。

- 仓库：`https://github.com/xxc-rgb/zhongqiu`
- 正式访问地址：`https://xxc-rgb.github.io/zhongqiu/`（长期有效，可直接分享给别人）
- 推送凭证和代理已在本机配置好，`git push` 可直接用

**交付流程：改动 → 测试通过 → commit → 执行 `git push origin main`。**

push 之后 Actions 会自动构建并发布到上面的地址，约 1 分钟内生效，无需再做任何事。

**禁止**用以下方式代替真正部署：
- 启动临时隧道（cloudflared / ngrok / localhost.run 等）拿一个临时链接
- 起本地静态服务器（`python -m http.server` 之类）让用户自己访问
- 只说"已部署"但线上内容并没有变

判断是否真的部署成功，以 `https://xxc-rgb.github.io/zhongqiu/` 的实际内容与本地 `web/index.html` 一致为准。
