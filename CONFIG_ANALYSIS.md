# Hugo 配置分析：通用 vs 主题特定

## ✅ Hugo 核心配置（所有主题通用）

这些配置是 Hugo 框架本身的，**所有主题都支持**：

```toml
# 基础配置
baseURL = "https://manxisuo.github.io/"      # ✅ Hugo 核心
languageCode = "zh-cn"                        # ✅ Hugo 核心
title = "Manxisuo的博客"                      # ✅ Hugo 核心
theme = "PaperMod"                            # ✅ Hugo 核心（指定使用哪个主题）

# 输出格式配置
[outputs]
  home = ["HTML", "RSS", "JSON"]              # ✅ Hugo 核心

# 菜单配置（Hugo 核心，但不同主题渲染方式可能不同）
[menu]
  [[menu.main]]
    name = "博文"
    url = "/posts/"
    weight = 10                               # ✅ Hugo 核心
```

## ⚠️ PaperMod 主题特定配置

所有 `[params]` 下的配置都是**主题特定的**，只有 PaperMod 主题会使用：

### 完全 PaperMod 特定的：

```toml
[params]
  # PaperMod 功能开关
  ShowReadingTime = true                       # ⚠️ PaperMod 特定
  ShowCodeCopyButtons = true                   # ⚠️ PaperMod 特定
  ShowShareButtons = true                      # ⚠️ PaperMod 特定
  disableSpecial1stPost = true                 # ⚠️ PaperMod 特定
  
  # PaperMod 首页模式
  [params.homeInfoParams]                      # ⚠️ PaperMod 特定
    Title = "欢迎来到我的博客"
    Content = "..."
    AlignSocialIconsTo = "left"
  
  # PaperMod 封面图片配置
  [params.cover]                               # ⚠️ PaperMod 特定
    responsiveImages = true
    linkFullImages = false
  
  # PaperMod 社交图标
  [[params.socialIcons]]                       # ⚠️ PaperMod 特定
    name = "GitHub"
    url = "https://github.com/manxisuo"
  
  # PaperMod 页脚配置
  [params.footer]                              # ⚠️ PaperMod 特定
    hideCopyright = false
    text = ""
  
  # PaperMod Schema.org 配置
  [params.schema]                              # ⚠️ PaperMod 特定
    publisherType = "Person"
    sameAs = ["..."]
```

### 部分通用但实现方式不同：

```toml
[params]
  # SEO 元数据（很多主题都支持，但参数名可能不同）
  description = "..."                          # ⚠️ 主题特定（虽然很多主题都支持）
  keywords = [...]                             # ⚠️ 主题特定
  
  # 作者信息（很多主题都支持，但结构可能不同）
  [params.author]                              # ⚠️ 主题特定
    name = "Manxisuo"
```

## 📊 配置分类总结

| 配置项 | 类型 | 切换主题时 |
|--------|------|-----------|
| `baseURL`, `languageCode`, `title` | ✅ Hugo 核心 | ✅ 保留 |
| `theme` | ✅ Hugo 核心 | ⚠️ 需要修改 |
| `[outputs]` | ✅ Hugo 核心 | ✅ 保留 |
| `[menu]` | ✅ Hugo 核心 | ✅ 保留（但渲染可能不同）|
| `[params]` 下的所有配置 | ⚠️ 主题特定 | ❌ 需要重新配置 |

## 🔄 切换主题时的建议

### 1. 保留的配置（Hugo 核心）
```toml
baseURL = "https://manxisuo.github.io/"
languageCode = "zh-cn"
title = "Manxisuo的博客"

[outputs]
  home = ["HTML", "RSS", "JSON"]

[menu]
  [[menu.main]]
    name = "博文"
    url = "/posts/"
    weight = 10
  # ... 其他菜单项
```

### 2. 需要重新配置的（主题特定）
- 所有 `[params]` 下的配置
- 需要查看新主题的文档，了解支持的参数
- 可能需要调整菜单的显示方式

### 3. 可能需要调整的
- 内容文件的结构（如 `archives.md`, `search.md` 的 layout）
- 静态资源的位置
- 自定义 CSS/JS

## 💡 最佳实践

1. **分离配置**：可以考虑将主题特定配置单独放在一个文件中
2. **文档记录**：记录哪些配置是主题特定的
3. **版本控制**：切换主题时，可以创建一个新的配置分支

## 📝 示例：分离配置

可以创建两个配置文件：

**`hugo.toml`**（Hugo 核心配置）：
```toml
baseURL = "https://manxisuo.github.io/"
languageCode = "zh-cn"
title = "Manxisuo的博客"
theme = "PaperMod"

[outputs]
  home = ["HTML", "RSS", "JSON"]

[menu]
  # ... 菜单配置
```

**`config/papermode.toml`**（PaperMod 特定配置）：
```toml
[params]
  ShowReadingTime = true
  # ... 其他 PaperMod 配置
```

然后在 `hugo.toml` 中引用：
```toml
[module]
  [[module.imports]]
    path = "config/papermode.toml"
```

