---
title: "在Windows 11上用DeepSeek驱动OpenClaw，并接入飞书"
date: 2026-02-16
draft: false
tags: 
  - "OpenClaw"
  - "DeepSeek"
  - "飞书"
  - "AI Agent"
  - "Windows"
---

最近在折腾 [OpenClaw](https://openclaw.ai/) —— 一个开源的 AI Agent 框架。它可以用浏览器聊天，也可以对接各种 IM 平台。我的需求很简单：**用 DeepSeek 的 API 作为大脑，让它在飞书里直接回复消息。**

整个过程踩了不少坑，尤其是配置文件的字段名和模型注册方式，官方文档里没完全覆盖到。这篇文章把完整流程记录下来，希望能帮到有同样需求的朋友。

## 环境

- Windows 11
- Node.js v20+
- OpenClaw 2026.2.14
- DeepSeek API（V3 / R1）
- 飞书个人版

## 第一步：安装 OpenClaw

OpenClaw 是一个 npm 包，安装非常简单：

```powershell
npm i -g openclaw
```

首次使用需要初始化：

```powershell
openclaw onboard
```

跟着引导走就行。完成后会在 `C:\Users\<用户名>\.openclaw\` 下生成配置目录。

启动也是一行命令：

```powershell
openclaw
```

然后打开 http://127.0.0.1:18789/chat 就能看到 Web 聊天界面了。

> 但这时候还不能用 —— 因为还没配模型。

## 第二步：配置 DeepSeek 作为模型 Provider

### 为什么不用 Ollama？

我一开始试过在 WSL2 里跑 Ollama + Qwen2.5:7b，但遇到了两个问题：

1. **上下文窗口太小**：OpenClaw 要求至少 16000 tokens，而 Ollama 默认只给 4096。即使在 OpenClaw 配置里改了 `contextWindow`，Ollama 那边还是会截断 prompt。
2. **需要自建 Modelfile**：要在 Ollama 侧用 `num_ctx` 参数创建自定义模型才能真正扩大上下文。

折腾了一圈，我决定直接用 DeepSeek 的云端 API —— 省事、便宜、上下文窗口 64K。

### 获取 API Key

去 [DeepSeek 开放平台](https://platform.deepseek.com/api_keys) 注册账号，创建一个 API Key（格式 `sk-xxxx`）。

### 注册 DeepSeek Provider

**重要**：DeepSeek 不是 OpenClaw 的内置模型 provider，直接写 `deepseek-chat` 会报 `Unknown model` 错误。需要把它当作 **自定义 OpenAI 兼容 provider** 来注册。

编辑 `~\.openclaw\openclaw.json`，在 `models.providers` 里加入：

```json
"deepseek": {
  "baseUrl": "https://api.deepseek.com/v1",
  "api": "openai-completions",
  "models": [
    {
      "id": "deepseek-chat",
      "name": "DeepSeek Chat (V3)",
      "reasoning": false,
      "input": ["text"],
      "cost": {
        "input": 0.27,
        "output": 1.1,
        "cacheRead": 0.07,
        "cacheWrite": 0.27
      },
      "contextWindow": 65536,
      "maxTokens": 8192
    },
    {
      "id": "deepseek-reasoner",
      "name": "DeepSeek Reasoner (R1)",
      "reasoning": true,
      "input": ["text"],
      "cost": {
        "input": 0.55,
        "output": 2.19,
        "cacheRead": 0.14,
        "cacheWrite": 0.55
      },
      "contextWindow": 65536,
      "maxTokens": 8192
    }
  ]
}
```

然后把默认模型指向它：

```json
"agents": {
  "defaults": {
    "model": {
      "primary": "deepseek/deepseek-chat"
    }
  }
}
```

注意模型名格式是 `provider/model`，写成 `deepseek/deepseek-chat`，不能只写 `deepseek-chat`。

### 配置 API Key（踩坑点）

编辑 `~\.openclaw\agents\main\agent\auth-profiles.json`：

```json
{
  "version": 1,
  "profiles": {
    "deepseek": {
      "type": "api_key",
      "provider": "deepseek",
      "key": "sk-你的API Key"
    }
  }
}
```

⚠️ **这里有个坑**：字段名必须是 **`key`**，不是 `apiKey`。我一开始写成了 `apiKey`，OpenClaw 死活找不到 Key，翻了源码才发现这个差异。

### 验证

重启 OpenClaw，在 http://127.0.0.1:18789/chat 发条消息试试。看到 DeepSeek 正常回复就说明模型配通了 🎉

## 第三步：接入飞书

现在本地聊天没问题了，下一步是让 OpenClaw 在飞书里当机器人。

### 1. 创建飞书应用

打开 [飞书开放平台](https://open.feishu.cn/app)，点击 **创建企业自建应用**。

> 飞书个人版的话，你自己就是管理员，应用审核自己批就行，不用担心。

### 2. 拿到凭证

在 **凭证与基础信息** 页面，复制 **App ID** 和 **App Secret**。

### 3. 配置权限

在 **权限管理** → **批量导入**，粘贴：

```json
{
  "scopes": {
    "tenant": [
      "aily:file:read",
      "aily:file:write",
      "application:application.app_message_stats.overview:readonly",
      "application:application:self_manage",
      "application:bot.menu:write",
      "contact:user.employee_id:readonly",
      "corehr:file:download",
      "event:ip_list",
      "im:chat.access_event.bot_p2p_chat:read",
      "im:chat.members:bot_access",
      "im:message",
      "im:message.group_at_msg:readonly",
      "im:message.p2p_msg:readonly",
      "im:message:readonly",
      "im:message:send_as_bot",
      "im:resource"
    ],
    "user": [
      "aily:file:read",
      "aily:file:write",
      "im:chat.access_event.bot_p2p_chat:read"
    ]
  }
}
```

### 4. 启用机器人 & 事件订阅

- 在 **添加应用能力** 中，启用 **机器人**
- 在 **事件与回调** → **事件配置** 中：
  - 添加事件 `im.message.receive_v1`（接收消息）
  - 选择 **长连接（WebSocket）** 模式

> 长连接模式是关键 —— 它不需要公网域名和回调地址，OpenClaw 通过 WebSocket 主动连飞书的服务器，非常适合本地开发。

### 5. 发布应用

在 **版本管理与发布** 中创建版本并提交审核。个人版管理员直接批准即可。

### 6. OpenClaw 侧配置

先启用飞书插件：

```powershell
openclaw plugins enable feishu
```

然后编辑 `openclaw.json`，添加飞书频道配置：

```json
"channels": {
  "feishu": {
    "accounts": {
      "default": {
        "appId": "cli_你的AppID",
        "appSecret": "你的AppSecret"
      }
    }
  }
},
"plugins": {
  "entries": {
    "feishu": {
      "enabled": true
    }
  }
}
```

### 7. 重启并验证

```powershell
openclaw
```

日志里看到 `[feishu] connected` 就说明连上了。

### 8. 配对用户

第一次在飞书里给机器人发消息，它会回复一个配对码（Pairing code）。在命令行里审批：

```powershell
openclaw pairing approve feishu <配对码>
```

审批通过后，就可以在飞书里愉快地跟 OpenClaw 对话了！

## 踩坑总结

| 坑 | 现象 | 解法 |
|---|---|---|
| 上下文窗口太小 | `Model context window too small (4096 tokens)` | `contextWindow` 设为 65536（或至少 16000） |
| 模型名缺 provider 前缀 | `Model "deepseek-chat" specified without provider` | 写全名 `deepseek/deepseek-chat` |
| DeepSeek 不是内置 provider | `Unknown model: deepseek/deepseek-chat` | 在 `models.providers` 中注册为自定义 OpenAI 兼容 provider |
| API Key 字段名错误 | `No API key found for provider` | `auth-profiles.json` 中用 `"key"` 而非 `"apiKey"` |
| 飞书插件安装 `spawn EINVAL` | Windows 下 npm spawn 报错 | 飞书插件是内置的，直接 `openclaw plugins enable feishu` 即可 |

## 配置文件一览

| 文件 | 用途 |
|------|------|
| `~\.openclaw\openclaw.json` | 全局配置：模型、频道、插件 |
| `~\.openclaw\agents\main\agent\auth-profiles.json` | API Key 存储（优先级最高） |
| `~\.openclaw\agents\main\agent\models.json` | Agent 级模型配置（可为空，继承全局） |

## 参考链接

- [OpenClaw 官网](https://openclaw.ai/) / [GitHub](https://github.com/openclaw/openclaw)
- [OpenClaw 飞书频道文档](https://docs.openclaw.ai/channels/feishu)
- [DeepSeek 开放平台](https://platform.deepseek.com/)
- [飞书开放平台](https://open.feishu.cn/app)

---

折腾了一下午，总算跑通了。DeepSeek V3 的响应速度和质量都不错，搭配飞书用起来比浏览器还方便 —— 毕竟飞书本来就一直开着。如果你也在找一个能自己掌控的 AI Agent 方案，OpenClaw + DeepSeek + 飞书是一个很不错的组合。
