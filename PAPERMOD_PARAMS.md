# PaperMod 主题配置参数参考

## 基础配置

```toml
[params]
  # 显示阅读时间
  ShowReadingTime = true
  
  # 代码块复制按钮
  ShowCodeCopyButtons = true
  
  # 禁用首页第一篇文章的特殊样式
  disableSpecial1stPost = false
  
  # 默认主题：auto, light, dark
  defaultTheme = "auto"
  
  # 禁用主题切换按钮
  disableThemeToggle = false
  
  # 禁用语言切换
  disableLangToggle = false
  
  # 显示完整语言名称（而非代码）
  displayFullLangName = false
  
  # 禁用滚动到顶部按钮
  disableScrollToTop = false
  
  # 环境：production 或其他
  env = "production"
  
  # 网站描述
  description = "网站描述"
  
  # 关键词
  keywords = ["关键词1", "关键词2"]
  
  # 日期格式
  DateFormat = ":date_long"
  
  # 主内容区域（用于首页文章列表）
  mainSections = ["posts"]
```

## 首页模式配置

### Home-Info Mode（首页信息模式）

```toml
[params.homeInfoParams]
  Title = "欢迎标题"
  Content = """
  欢迎内容
  支持多行
  """
  AlignSocialIconsTo = "left"  # left, center, right
```

### Profile Mode（个人资料模式）

```toml
[params.profileMode]
  enabled = false
  title = "标题"
  subtitle = "副标题"
  imageUrl = "images/avatar.jpg"
  imageTitle = "头像"
  imageWidth = 150
  imageHeight = 150
  
  # 按钮
  [[params.profileMode.buttons]]
    name = "按钮名称"
    url = "https://example.com"
```

## 资源文件配置

```toml
[params.assets]
  # Favicon
  favicon = "favicon.ico"
  favicon16x16 = "favicon-16x16.png"
  favicon32x32 = "favicon-32x32.png"
  apple_touch_icon = "apple-touch-icon.png"
  safari_pinned_tab = "safari-pinned-tab.svg"
  
  # 主题颜色
  theme_color = "#2e2e33"
  msapplication_TileColor = "#2e2e33"
  
  # 禁用指纹识别
  disableFingerprinting = false
  
  # 禁用滚动条样式
  disableScrollBarStyle = false
```

## 标签/Logo 配置

```toml
[params.label]
  text = "网站标题"
  icon = "images/logo.png"
  iconSVG = "<svg>...</svg>"
  iconHeight = 30
```

## 社交图标配置

```toml
[[params.socialIcons]]
  name = "GitHub"
  url = "https://github.com/username"
  
[[params.socialIcons]]
  name = "Twitter"
  url = "https://twitter.com/username"
```

## 分享按钮配置

```toml
[params]
  # 显示分享按钮
  ShowShareButtons = true
  
  # 自定义分享按钮（可选）
  ShareButtons = ["x", "twitter", "linkedin", "reddit", "facebook", "whatsapp", "telegram", "ycombinator"]
```

## 封面图片配置

```toml
[params.cover]
  # 响应式图片
  responsiveImages = true
  
  # 点击封面图片跳转到完整图片
  linkFullImages = false
```

## 页脚配置

```toml
[params.footer]
  # 隐藏版权信息
  hideCopyright = false
  
  # 自定义页脚文本
  text = "自定义页脚文本"
```

## 编辑文章链接

```toml
[params.editPost]
  URL = "https://github.com/username/repo/edit/main/content/"
  Text = "编辑"
  appendFilePath = true
```

## 规范链接配置

```toml
[params]
  CanonicalLinkText = "原文发布于"
```

## RSS 配置

```toml
[params]
  # RSS 中显示完整文本
  ShowFullTextinRSS = false
  
  # 图片（用于 RSS）
  images = ["images/og-image.png"]
```

## 归档页面配置

```toml
[params]
  # 在归档中显示所有页面
  ShowAllPagesInArchive = false
  
  # 在 section/term 列表页面显示 RSS 按钮
  ShowRssButtonInSectionTermList = false
```

## Schema.org 结构化数据

```toml
[params.schema]
  # 发布者类型：Organization 或 Person
  publisherType = "Organization"
  
  # 相同身份链接（用于 Person 类型）
  sameAs = ["https://github.com/username", "https://twitter.com/username"]
```

## 作者配置

```toml
[params.author]
  name = "作者名称"
  email = "author@example.com"
```

## 搜索配置（Fuse.js）

```toml
[params.fuseOpts]
  isCaseSensitive = false
  shouldSort = true
  location = 0
  distance = 1000
  threshold = 0.4
  minMatchCharLength = 0
  keys = ["title", "permalink", "summary", "content"]
```

## 分析/验证配置

```toml
[params.analytics.google]
  SiteVerificationTag = "your-verification-tag"

[params.analytics.yandex]
  SiteVerificationTag = "your-verification-tag"

[params.analytics.bing]
  SiteVerificationTag = "your-verification-tag"

[params.analytics.naver]
  SiteVerificationTag = "your-verification-tag"
```

## 社交媒体配置（Open Graph）

```toml
[params.social]
  # 社交媒体配置
```

## 文章页面参数（在文章 front matter 中使用）

```yaml
---
# 隐藏摘要
hideSummary: false

# 隐藏元数据
hideMeta: false

# 隐藏封面图片
cover:
  hidden: false
  hiddenInList: false
  hiddenInSingle: false

# 禁用分享
disableShare: false

# 显示目录
ShowToc: false

# 禁用锚点标题
disableAnchoredHeadings: false

# 隐藏首页列表
hiddenInHomeList: false

# 编辑文章
editPost:
  URL: "https://github.com/..."
  Text: "编辑"
  disabled: false

# 规范链接
CanonicalLinkText: "原文发布于"
canonicalURL: "https://original-site.com/article"

# 自定义分享按钮
ShareButtons: ["x", "twitter"]

# 不索引（SEO）
robotsNoIndex: false
---
```

