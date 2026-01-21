---
title: "trap：Bash信号处理器"
date: 2026-01-20
draft: false
tags:
  - "Bash"
  - "Shell"
  - "信号处理"
  - "进程控制"
  - "错误处理"
---

`trap` 是 **Bash 信号处理器**，用于在脚本接收到信号时执行特定操作。下面详细介绍其用法：

## 一. 基本语法

```bash
trap [命令] [信号]
```

## 二. 常用信号

| 信号 | 值 | 说明 | 常见触发方式 |
|------|----|------|------------|
| **EXIT** | 0 | 脚本退出时（非真实信号） | 脚本正常结束或调用 exit |
| **ERR** | - | 命令失败时（非真实信号） | 命令返回非零状态 |
| **INT** | 2 | 中断信号 | Ctrl+C |
| **TERM** | 15 | 终止信号 | `kill` 命令默认信号 |
| **HUP** | 1 | 挂起信号 | 终端断开连接 |
| **QUIT** | 3 | 退出信号 | Ctrl+\ |
| **KILL** | 9 | 强制终止 | `kill -9`（**不可捕获**） |
| **DEBUG** | - | 每条命令后执行（非真实信号） | 调试用途 |

## 三. 基础用法示例

### 1. **捕获 Ctrl+C（INT 信号）**
```bash
#!/bin/bash
# trap1.sh

echo "脚本开始，按 Ctrl+C 试试"
trap 'echo "捕获到 Ctrl+C，但脚本继续运行"' INT

sleep 10
echo "脚本正常结束"
```

### 2. **清理临时文件**
```bash
#!/bin/bash
# trap2.sh

temp_file="/tmp/my_temp_$$"  # $$ 是当前进程ID

# 创建临时文件
echo "创建临时文件: $temp_file"
touch "$temp_file"

# 设置退出时清理
trap 'echo "清理临时文件..."; rm -f "$temp_file"' EXIT

# 脚本逻辑
echo "处理数据..."
sleep 2
echo "处理完成"
# 退出时会自动执行清理
```

### 3. **捕获多个信号**
```bash
#!/bin/bash
# trap3.sh

cleanup() {
    echo "执行清理操作..."
    # 清理代码
    echo "清理完成"
}

# 捕获多个信号
trap cleanup EXIT INT TERM HUP

echo "脚本运行中，PID: $$"
echo "试试："
echo "1. 按 Ctrl+C"
echo "2. 在其他终端执行: kill $$"
echo "3. 等待10秒自动结束"

sleep 10
```

## 四. 高级用法

### 1. **忽略信号**
```bash
#!/bin/bash
# 忽略 Ctrl+C
trap '' INT

echo "按 Ctrl+C 无效！"
sleep 5
echo "结束"
```

### 2. **重置信号处理**
```bash
#!/bin/bash
# 第一次捕获
trap 'echo "第一次捕获"' INT
echo "第一次：按 Ctrl+C"
sleep 2

# 重置为默认行为
trap - INT
echo "现在 Ctrl+C 会终止脚本"
sleep 2

# 再次设置
trap 'echo "重新捕获"' INT
echo "再次捕获 Ctrl+C"
sleep 2
```

### 3. **ERR 信号（错误处理）**
```bash
#!/bin/bash
# trap-err.sh

# 任何命令失败时执行
trap 'echo "错误发生在第 $LINENO 行: $BASH_COMMAND"' ERR

set -e  # 遇到错误退出

echo "第6行"
ls /nonexistent  # 这个命令会失败
echo "这行不会执行"  # 因为 set -e
```

### 4. **DEBUG 信号（调试）**
```bash
#!/bin/bash
# trap-debug.sh

# 每条命令执行前执行
trap 'echo "执行命令: $BASH_COMMAND"' DEBUG

x=1
y=2
z=$((x + y))
echo "结果: $z"
```

### 5. **获取退出状态**
```bash
#!/bin/bash
# trap-exit-status.sh

trap 'echo "退出状态: $?"' EXIT

# 不同退出状态
if [ "$1" = "error" ]; then
    exit 1
else
    exit 0
fi
```

## 五. 实际应用场景

### 场景1：**数据库备份脚本**
```bash
#!/bin/bash
# backup.sh

set -euo pipefail

# 定义清理函数
cleanup() {
    local exit_code=$?
    echo "备份脚本结束，退出码: $exit_code"
    
    # 释放锁文件
    rm -f /tmp/backup.lock
    
    # 发送通知
    if [ $exit_code -eq 0 ]; then
        echo "备份成功" | mail -s "备份完成" admin@example.com
    else
        echo "备份失败" | mail -s "备份错误" admin@example.com
    fi
    
    # 记录日志
    echo "$(date): 备份脚本退出，代码: $exit_code" >> /var/log/backup.log
}

# 设置信号处理
trap cleanup EXIT INT TERM ERR

# 创建锁文件
lockfile="/tmp/backup.lock"
if [ -f "$lockfile" ]; then
    echo "备份正在运行，退出..."
    exit 1
fi
touch "$lockfile"

# 备份逻辑
echo "开始备份..."
mysqldump -u root database > backup.sql
gzip backup.sql
scp backup.sql.gz backup@server:/backups/

echo "备份完成"
```

### 场景2：**长时间运行进程**
```bash
#!/bin/bash
# long-running.sh

# 优雅关闭处理
graceful_shutdown() {
    echo "收到关闭信号，正在优雅停止..."
    
    # 停止子进程
    kill -TERM "$child_pid" 2>/dev/null
    wait "$child_pid" 2>/dev/null
    
    # 清理资源
    echo "释放资源..."
    
    exit 0
}

# 注册信号
trap graceful_shutdown TERM INT QUIT

# 主业务逻辑
echo "启动服务..."
sleep infinity &
child_pid=$!

# 等待子进程
wait "$child_pid"
```

### 场景3：**确保目录恢复**
```bash
#!/bin/bash
# ensure-cd-back.sh

original_dir=$(pwd)
cd /tmp/some_directory

# 确保返回原目录
trap 'cd "$original_dir"' EXIT

# 执行操作
echo "当前目录: $(pwd)"
# ... 其他操作
# 无论正常退出还是异常退出，都会返回原目录
```

## 六. 嵌套和局部处理

```bash
#!/bin/bash
# nested-trap.sh

global_cleanup() {
    echo "全局清理"
}

local_cleanup() {
    echo "局部清理"
}

# 全局处理
trap global_cleanup EXIT

echo "=== 区块1 ==="
trap local_cleanup EXIT  # 覆盖全局处理
# 这个区块退出时会执行 local_cleanup

echo "=== 区块2 ==="
trap - EXIT  # 移除局部处理，恢复全局
# 这个区块退出时会执行 global_cleanup
```

## 七. 最佳实践

1. **使用函数**：将清理代码放在函数中，提高可读性
   ```bash
   cleanup() { ... }
   trap cleanup EXIT
   ```

2. **按需清理**：明确清理什么资源
   ```bash
   trap 'rm -f "$lock_file"' EXIT
   ```

3. **避免多次触发**：对于耗时清理，防止重复执行
   ```bash
   cleanup() {
       if [ "$cleaned" != "true" ]; then
           cleaned="true"
           # 清理代码
       fi
   }
   ```

4. **记录信号**：调试时记录接收到的信号
   ```bash
   trap 'echo "收到信号: $?" >> /var/log/signals.log' INT TERM HUP
   ```

5. **考虑并发**：清理操作要考虑多进程情况

## 八. 注意事项

1. **KILL 信号不可捕获**：`kill -9` 无法被拦截
2. **EXIT 总是执行**：无论脚本如何结束（除非被 KILL）
3. **信号链式调用**：小心在处理器中触发其他信号
4. **子进程继承**：子进程可能继承信号处理，使用 `trap -` 重置

`trap` 是编写健壮 Shell 脚本的关键工具，能确保资源正确释放，实现优雅关闭。
