# 博客视觉设计与维护

这版设计在 Hugo Stack 上增加独立的首页模板和一套共享的视觉变量，保持原有文章 URL、Markdown 内容、搜索、归档、标签、RSS 和 Giscus 评论配置。

## 修改首页

编辑 `data/home.toml`：

- `eyebrow`、`title`、`titleAccent`、`description`、`note`：首页文案。
- `topics`：主题入口。`tag` 填已有标签的名称，链接由 Hugo 自动解析。
- `featured`：精选文章。`path` 填内容路径，不包含 `.md`；`label` 和 `description` 是首页的推荐文案。

最近文章与文章/标签统计自动生成；默认每页 8 篇。首页第二页起仅显示文章列表。

## 修改样式

`assets/scss/custom.scss` 顶部定义浅色与深色变量。首页插画在 `layouts/partials/home/landscape.html`，是本地 SVG，没有远程图片或字体依赖。正文沿用 Stack，统一调整中文排版、代码块、引用、链接与卡片。

桌面保留可折叠侧栏，折叠偏好不会隐藏手机导航。深色模式支持鼠标、Enter 和空格操作，并沿用 Stack 的系统主题与偏好持久化。

## 本地预览与发布

```sh
git submodule update --init themes/Stack
hugo server --disableFastRender
```

使用与 CI 一致的 Hugo **0.146.0 extended**。生产验证命令：

```sh
hugo --minify --environment production
```

合并到 `main` 后，现有 `.github/workflows` 会构建并部署到 GitHub Pages。无需增加 Node 依赖或修改写作流程。
