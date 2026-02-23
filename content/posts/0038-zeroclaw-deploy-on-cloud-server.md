---
title: "在2G低配云服务器上部署ZeroClaw并接入飞书和QQ"
date: 2026-02-23
draft: false
tags:
  - "Rust"
  - "Linux"
  - "云服务器"
  - "部署"
  - "飞书"
  - "QQ"
  - "聊天机器人"
  - "systemd"
---

## 前言

ZeroClaw 是一个用 Rust 编写的轻量级 AI 助手框架，支持接入 Telegram、Discord、飞书、QQ 等多种即时通讯平台。本文记录了在一台低配云服务器上从零部署 ZeroClaw，并接入飞书机器人和 QQ 机器人的完整过程，包括遇到的各种坑和解决方案。

## 环境

- **服务器**：2vCPU / 2GB 内存 / 40GB 硬盘
- **系统**：Ubuntu 24.04
- **Rust**：rustc 1.93.1 / cargo 1.93.1

配置很低，后面会看到这给编译带来了不小的麻烦。

## 一、安装 ZeroClaw

### 1.1 先尝试预编译二进制

最初通过官方的安装脚本直接装了预编译的二进制版本，一切顺利。但在准备接入飞书时发现，预编译版本没有开启 `channel-lark` feature，不支持飞书。

### 1.2 转向源码编译

克隆源码仓库：

```bash
git clone https://github.com/zeroclaw-labs/zeroclaw.git ~/zeroclaw-src
```

然后开始编译，结果服务器直接卡死，SSH 断开，只能强制重启。反复尝试了好几次，每次都是在编译过程中服务器失去响应。

### 1.3 问题排查：为什么编译总是卡死？

排查后发现了**三个关键问题**：

**问题一：`vm.swappiness = 0`（最致命）**

```bash
$ cat /proc/sys/vm/swappiness
0
```

`swappiness=0` 意味着内核几乎不会使用 swap，即使配了 6GB 的 swap 空间也形同虚设。内存耗尽后内核宁可 OOM 杀进程也不往 swap 里换页。

**问题二：Cargo.toml 中的 release profile 配置**

```toml
[profile.release]
opt-level = "z"
lto = "fat"          # 全量 LTO，链接阶段需要 4-8GB 内存
codegen-units = 1    # 单代码生成单元，峰值内存最高
```

这里的注释写着"for low-memory devices"，但指的是**运行目标设备**内存小，不是编译机器。这组配置恰恰需要**最多的编译内存**。

**问题三：swap 空间不足**

系统默认只有 2GB swap，加上 2GB 物理内存总共 4GB，对 Rust 编译来说还是不够。

### 1.4 解决方案

**第一步：增加 swap 到 6GB**

```bash
sudo fallocate -l 4G /swapfile2
sudo chmod 600 /swapfile2
sudo mkswap /swapfile2
sudo swapon /swapfile2

# 持久化到 fstab
echo '/swapfile2 none swap sw 0 0' | sudo tee -a /etc/fstab
```

**第二步：调整 swappiness**

```bash
sudo sysctl vm.swappiness=60

# 持久化
echo 'vm.swappiness=60' | sudo tee -a /etc/sysctl.conf
```

**第三步：修改编译 profile**

```toml
[profile.release]
opt-level = "z"
lto = "thin"         # thin LTO：峰值内存从 8GB 降到 2-3GB
codegen-units = 16   # 拆成 16 个编译单元，降低峰值内存
strip = true
panic = "abort"
```

**第四步：单线程编译**

```bash
CARGO_BUILD_JOBS=1 cargo build --release --features channel-lark -j1
```

最终编译全程 swap 峰值用到约 800MB，整个过程不到 7 分钟，顺利完成。

### 1.5 安装二进制

```bash
cp ~/zeroclaw-src/target/release/zeroclaw ~/.cargo/bin/zeroclaw
```

这里有个小坑：之前预编译版本安装在了 `~/.cargo/bin/zeroclaw`，而我一开始把新编译的复制到了 `/usr/local/bin/zeroclaw`。但由于 `~/.cargo/bin` 在 PATH 中排在前面，`which zeroclaw` 始终指向旧的预编译版本。需要直接替换 `~/.cargo/bin/` 中的文件。

### 1.6 还有一个隐蔽的坑：lib.rs 缓存

编译完成后运行 `zeroclaw channel list`，发现 Lark 仍然显示 "disabled"。排查发现：ZeroClaw 项目同时有 `src/lib.rs` 和 `src/main.rs`，之前 `cargo clean -p zeroclaw` + `touch src/main.rs` 只重新编译了 binary，而 library（包含 feature 检查逻辑的部分）还是旧的缓存。

解决方法：

```bash
touch src/lib.rs
cargo build --release --features channel-lark -j1
```

强制 library 也带 `--cfg 'feature="channel-lark"'` 重新编译后，问题解决。

## 二、配置 ZeroClaw

### 2.1 基础配置

ZeroClaw 的配置文件位于 `~/.zeroclaw/config.toml`。首次运行 `zeroclaw onboard` 可以通过交互式向导完成初始化，也可以直接编辑配置文件。

### 2.2 AI 模型配置

配置了两个 AI provider：

```toml
# 默认使用智谱 GLM-4.6V（支持文本+图片理解）
api_key = "智谱API密钥"
default_provider = "glm"
default_model = "glm-4.6v"
default_temperature = 0.7
```

DeepSeek 作为降级备选：

```toml
[reliability]
fallback_providers = ["deepseek"]
```

DeepSeek 的 API Key 通过 systemd 服务的环境变量传入：

```ini
[Service]
Environment=DEEPSEEK_API_KEY=sk-xxx
```

### 2.3 设置 systemd 开机自启

ZeroClaw 自带服务管理功能：

```bash
zeroclaw service install
zeroclaw service start
```

关键一步：启用 `loginctl linger`，否则用户注销后 user 级 systemd 服务会被停止：

```bash
sudo loginctl enable-linger $USER
```

常用管理命令：

```bash
zeroclaw service status          # 查看状态
zeroclaw service restart         # 重启
journalctl --user -u zeroclaw -f # 实时查看日志
```

## 三、接入飞书机器人

### 3.1 ZeroClaw 侧配置

在 `~/.zeroclaw/config.toml` 中添加：

```toml
[channels_config.lark]
app_id = "cli_xxx"
app_secret = "xxx"
use_feishu = true              # 使用飞书中国端点
receive_mode = "websocket"     # WebSocket 长连接，无需公网域名
allowed_users = ["*"]
```

### 3.2 飞书开放平台配置

1. **启用机器人能力**：应用详情 → 添加应用能力 → 启用「机器人」
2. **配置权限**：权限管理 → 搜索 `im:message`，开通发消息和读消息相关权限
3. **配置事件订阅**：事件与回调 → 订阅方式选择「长连接」→ 添加 `im.message.receive_v1` 事件
4. **发布应用**：版本管理与发布 → 创建版本 → 提交审核

### 3.3 验证

```bash
$ zeroclaw channel doctor
🩺 ZeroClaw Channel Doctor
  ✅ Lark      healthy
```

日志中出现 `Lark: WS connected` 即表示连接成功。

### 3.4 已知限制

目前 ZeroClaw 的飞书频道只支持文本消息，不支持图片消息。发送图片给机器人会被静默丢弃。我已在 GitHub 上提交了 Feature Request（参考 QQ 频道的 #1252 图片支持实现）。

## 四、接入 QQ 机器人

### 4.1 ZeroClaw 侧配置

QQ 频道是默认编译的，不需要额外的 feature flag：

```toml
[channels_config.qq]
app_id = "xxx"
app_secret = "xxx"
allowed_users = ["*"]
```

### 4.2 QQ 开放平台配置

1. 在 [QQ 机器人管理端](https://q.qq.com) 创建应用
2. 开发 → 回调配置 → **不要填 HTTPS 回调地址**（ZeroClaw 使用 WebSocket，填了会导致 WebSocket 失效）→ 添加事件 `C2C_MESSAGE_CREATE` 和 `GROUP_AT_MESSAGE_CREATE`
3. 开发 → 沙箱配置 → 添加测试成员（你自己的 QQ 号）

### 4.3 沙箱模式下如何找到机器人

沙箱模式下机器人**无法通过搜索 QQ 号或名称找到**，需要通过以下方式：

- 浏览器打开 `https://qun.qq.com/qunpro/robot/qunshare?robot_appid={AppID}`
- 用手机 QQ 扫码打开机器人资料卡
- 点「发消息」开始测试

### 4.4 遇到的问题

连接成功（日志显示 `QQ: connected and identified`），但发送消息后机器人不回复。日志报错：

```
❌ Failed to reply on qq: QQ send message failed (400 Bad Request):
{"message":"主动消息失败, 无权限","code":40034102}
```

原因是 QQ 机器人在**沙箱模式下没有主动消息权限**。需要完成「发布上架」流程（填写自测报告、提交审核）后才能正常回复消息。QQ 的发布流程相对繁琐，暂时搁置。

## 五、定时任务

ZeroClaw 支持通过飞书对话创建定时任务，底层使用 cron 调度器。需要注意的是，默认时区是 UTC，需要手动指定时区：

```bash
zeroclaw cron update <task-id> --tz Asia/Shanghai
```

## 六、总结

### 踩过的坑

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 编译反复卡死 | `vm.swappiness=0`，内核不用 swap | 改为 60 |
| 有 swap 也 OOM | `lto="fat"` + `codegen-units=1` 峰值内存 8GB+ | 改为 `thin` + `16` |
| 编译成功但 feature 不生效 | 只重编了 main.rs，lib.rs 用了旧缓存 | `touch src/lib.rs` |
| 新二进制不生效 | `~/.cargo/bin` 中的旧版本优先 | 替换正确路径的文件 |
| 飞书图片不识别 | ZeroClaw 暂不支持 Lark 图片消息 | 已提 GitHub issue |
| QQ 机器人不回复 | 沙箱模式无主动消息权限 | 需完成发布上架 |

### 最终架构

```
飞书用户 ←→ 飞书开放平台 ←WSS→ ZeroClaw Daemon ←→ 智谱 GLM-4.6V
                                     ↓ (fallback)
                                  DeepSeek
```

### 对低配服务器的建议

如果你也在低配机器上编译 Rust 项目：

1. **先检查 `vm.swappiness`**，为 0 的话一定要改
2. **多加 swap**，磁盘空间换内存，编译完可以删掉
3. **用 `-j1` 限制并行编译**
4. **避免 `lto="fat"` + `codegen-units=1`** 的组合，这是内存杀手
5. **编译完记得确认 `which` 指向的是新版本**
