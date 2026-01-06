---
title: "Ubuntu 16.04 安装Ambari和HDP：过程与经验教训"
date: 2018-07-16
draft: false
tags:
  - "大数据"
  - "Hadoop"
  - "运维"
  - "Ubuntu"
---

在个人笔记本上安装了单节点HDP集群。

参考：https://docs.hortonworks.com/HDPDocuments/Ambari-2.6.1.5/bk_ambari-installation/content/ch_Getting_Ready.html

+ 电脑：New!灵越14RD-4528冷峻灰
+ CPU：Intel(R) Core(TM) i5-4200U CPU @ 1.60GHz
+ 系统：Ubuntu 16.04 LTS
+ 内存：8G
+ 硬盘：剩余78G左右
+ 用户：su
+ 域名：cloud

注：用户和域名不是固定的，根据实际情况确定即可。

## 0. 准备工作

### (1) 域名设置

域名设置为cloud：

```bash
sudo hostname cloud
```

在/etc/hosts中，增加：

```text
127.0.1.1	cloud
```

### (2) 设置SSH免登陆

过程，略。

设置完成后，保证`ssh su@cloud`不需要密码即可登录。

### (3) 用户加入sudo组，并可免密登录

执行`su -`，然后执行`visudo`，在打开的文件最后加入新行：

```text
su ALL=(ALL) NOPASSWD: ALL
```

设置完成后，保证用户su可使用`sudo`执行命令，并且不需要输入密码。

## 1. 安装Ambari

### (1) 添加Ambari源：

```shell
wget -O /etc/apt/sources.list.d/ambari.list http://public-repo-1.hortonworks.com/ambari/ubuntu16/2.x/updates/2.6.1.5/ambari.list
apt-key adv --recv-keys --keyserver keyserver.ubuntu.com B9733A7A07513CAD
apt-get update
```

### (2) 安装Ambari：

```bash
sudo apt install ambari-server
```

### (3) 启动Ambari：

```bash
sudo ambari-server start
```

第一次启动时，会进入Ambari的设置。数据库使用内嵌的PostgreSQL即可，Java使用JDK 1.8，用户使用`su`。

## 2. 安装HDP

在浏览器中打开cloud:8080，进入集群安装向导。

### (1) Get Started

为集群设置一个名字。

### (2) Select Version

我下载的HDP版本是2.6.4.0-91，所以选择HDP-2.6.4.0。

HDP下载地址：

+ HDP: http://public-repo-1.hortonworks.com/HDP/ubuntu16/2.x/updates/2.6.4.0/HDP-2.6.4.0-ubuntu16-deb.tar.gz
+ HDP-UTILS: http://public-repo-1.hortonworks.com/HDP-UTILS-1.1.0.22/repos/ubuntu16/HDP-UTILS-1.1.0.22-ubuntu16.tar.gz
+ HDP-GPL: http://public-repo-1.hortonworks.com/HDP-GPL/ubuntu16/2.x/updates/2.6.4.0/HDP-GPL-2.6.4.0-ubuntu16-deb.tar.gz

仓库使用Public应该也是可以的，但我使用了Local仓库。

把下载的HDP等三个包解压缩后，使用Python启动一个HTTP服务：

```shell
python -m SimpleHTTPServer 8181
```

Local仓库的Base URL分别填写（URL的前半部分根据实际情况决定）：

+ HDP: http://cloud:8181/HDP/ubuntu16/2.6.4.0-91/
+ HDP-GPL: http://cloud:8181/HDP-GPL/ubuntu16/2.6.4.0-91/
+ HDP-UTILS: http://cloud:8181/HDP-UTILS/ubuntu16/1.1.0.22/

注意：一定要选中"Skip Repository Base URL validation (Advanced)"选项。

### (3) Install Options

目标主机：cloud
SSH私钥：选择文件`~/.ssh/id_rsa`文件
SSH用户账号：su

### (4) Confirm Hosts

进入此步骤后，自动对上一步中设置的主机进行检查。如果顺利，一段时间后状态变为Success。但可能会存在一些Warning。点击下面的"Click here to see the warnings."查看警告：

在弹出的面板中，会看到警告项目。上面会显示一段清理脚本，例如：

```shell
python /usr/lib/python2.6/site-packages/ambari_agent/HostCleanup.py --silent --skip=users
```

可以使用此脚本清理问题。有些问题不影响安装，例如"Package Issues"。点击Next进入下一步。

### (5) Choose Services

根据情况选中需要安装的服务。服务在后续也是可以随时安装和卸载的。我选择的服务：

### (6) Assign Masters

默认即可。由于只有一个节点，所以没得选。

### (7) Assign Slaves and Clients

根据需要选择。

### (8) Customize Services

需要注意以下几点：

- HDFS: 
  - NameNode目录: /hadoop/hdfs/namenode,/hadoop/hdfs/namenode2
  - DataNode目录: /hadoop/hdfs/data,/hadoop/hdfs/data2

- Hive:
  - 数据库选中"New MySQL Database"。
  - 密码自设。

- Ambari Metrics:
  - hbase.rootdir设为"hdfs://cloud:8020/amshbase"。
  - ~dfs.client.read.shortcircuit设为false。~

### (9) Review

查看并可打印（保存为PDF）配置。点击Deploy开始部署。







