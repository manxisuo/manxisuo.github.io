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

## 项目展示

导航的「项目」页面位于 `/projects/`，首页推荐前三个 `featured = true` 的项目。列表按 `order` 升序排列。

在 `data/projects.toml` 中维护展示名单和叙述：

- `repo`：明确选定的 GitHub `owner/repository`，不会自动添加其他仓库。
- `id`：唯一的项目锚点；`name`、`tagline`、`description`：展示文案。
- `category`、`stage`、`highlights`、`stack`：分类、阶段、亮点和技术栈。
- `featured`、`order`：首页推荐与排列顺序。
- `action_url`、`action_label`：可选的演示或下载入口。

介绍与阶段来自各项目 README 的人工整理，不会因 README 变化而自动覆盖。卡片插画是概念图，并非应用截图，可在 `layouts/partials/projects/art.html` 修改。

`data/github_projects.json` 是仓库元数据的已提交快照。每次部署前，工作流运行 `python3 scripts/sync_projects.py`，仅请求配置中的公开仓库，并同步主要语言、简介、星标、仓库链接与最近推送时间。页面展示主要语言和最近推送日期；零星标不作为项目价值评判，也不显示星标排名。

网络、限流或单个仓库获取失败时，保留该项目的已有元数据；没有快照时，仅隐藏元数据，项目介绍仍可渲染。同步不会改写展示文案。CI 使用只读 `GITHUB_TOKEN`，不会向仓库提交同步结果。构建产物包含此次同步的数据，下次失败时回退到已提交快照。

需要手动更新上线数据时，可触发现有 Pages 工作流的 `workflow_dispatch`。本地保存新的回退快照：

```sh
python3 scripts/sync_projects.py
python3 -m unittest discover -s tests
hugo --minify --environment production
```

脚本使用 Python 3.11+ 的标准库，无第三方依赖。新增项目后运行同步，检查改动并将快照一起提交即可。
