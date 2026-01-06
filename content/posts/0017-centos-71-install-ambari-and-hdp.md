---
title: "CentOS 7.1 安装Ambari和HDP"
date: 2017-08-19
draft: false
tags:
  - "大数据"
  - "Hadoop"
  - "运维"
---

# 0. 硬件

共三台联想System X服务器。每台配置硬盘14个，记为0\~13号，容量均为1T。其中0号和1号做成RAID 1，作为系统盘；2\~13号分别做成RAID 0，作为数据盘，主要用于HDFS。

# 1. 安装操作系统

系统镜像为CentOS-7-x86_64-DVD-1611.iso。

分区方案如下：

TODO

建立用户admin。

## 1.1 分区方案

# 2. 配置

## 2.1 将用户添加到sudoers文件

执行`su -`，然后执行`visudo`，在打开的文件最后加入新行：

```
admin ALL=(ALL) ALL
```

## 2.2 使用光盘作为软件源

## 2.3 配置网络

### 2.3.1 禁用NetworkManager

### 2.3.2 配置网络

### 2.3.3 配置路由



