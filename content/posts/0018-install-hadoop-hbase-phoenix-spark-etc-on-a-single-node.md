---
title: "单节点安装Hadoop、HBase、Phoenix和Spark等"
date: 2017-08-20
draft: false
tags:
  - "大数据"
  - "Hadoop"
  - "Spark"
  - "运维"
---

# 1. 准备

## 1.1 下载安装包

- Hadoop：[2.7.1](https://archive.apache.org/dist/hadoop/common/hadoop-2.7.1/hadoop-2.7.1.tar.gz)
- HBase：[1.1.2](https://archive.apache.org/dist/hbase/1.1.2/hbase-1.1.2-bin.tar.gz)
- Phoenix：[4.4.0](https://archive.apache.org/dist/phoenix/phoenix-4.4.0-HBase-1.1/bin/phoenix-4.4.0-HBase-1.1-bin.tar.gz)
- Spark：[1.6.1](https://archive.apache.org/dist/spark/spark-1.6.1/spark-1.6.1-bin-without-hadoop.tgz)
- JDK：[jdk-7u1-linux-x64.tar.gz](http://www.oracle.com/technetwork/java/javase/downloads/java-archive-downloads-javase7-521261.html)

将大数据相关安装包解压在~/bd目录下，JDK解压在/usr/local目录下。

## 1.2 设置环境变量

在.bashrc中设置：

```sh
export JAVA_HOME=/usr/local/jdk1.7.0_01
export PATH=$JAVA_HOME/bin:$PATH
```

## 1.3 设置域名

在/etc/hosts中增加master域名

## 1.4 设置SSH免密登录

过程参考[这里](http://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/SingleCluster.html#Setup_passphraseless_ssh)。

注：需要将公钥拷贝到root用户下，即

```ssh
sudo cp id_rsa.pub /root/.ssh
```

# 2. 部署Hadoop

为了方便使用，在.bashrc中设置：

```sh
export HADOOP_HOME=~/bd/hadoop-2.7.1
export PATH=$HADOOP_HOME/bin:$PATH
```

## 2.1 配置JAVA路径
在etc/hadoop/hadoop-env.sh中设置：

```sh
export JAVA_HOME=/usr/local/jdk1.7.0_01
```

注：如果设置了JAVA_HOME变量，这一步不是必须的。

## 2.2 配置HDFS

在etc/hadoop/core-site.xml中增加：

```xml
<property>
    <name>fs.defaultFS</name>
    <value>hdfs://master:9000</value>
</property>
```

另外，hadoop.tmp.dir默认值为`/tmp/{hadoop-${user.name}`。而/tmp目录中的文件在系统重启后可能会删除，导致NameNode启动失败，所以要设置成其他目录（这个目录会自动创建），例如：

```xml
<property>
    <name>hadoop.tmp.dir</name>
    <value>/home/admin/bd-data/hadoop-admin</value>
</property>
```

在etc/hadoop/hdfs-site.xml中增加：

```xml
<property>
    <name>dfs.replication</name>
    <value>1</value>
</property>
```

格式化文件系统：

```sh
bin/hdfs namenode -format
```

## 2.3 配置Yarn

如果使用MapReduce，则进行以下配置。

在etc/hadoop/mapred-site.xml中：

```xml
<property>
    <name>mapreduce.framework.name</name>
    <value>yarn</value>
</property>
```

在etc/hadoop/yarn-site.xml中：

```xml
<property>
    <name>yarn.nodemanager.aux-services</name>
    <value>mapreduce_shuffle</value>
</property>
```

## 2.4 启动Hadoop

### (1) 启动NameNode和DataNode守护进程：

```sh
sbin/start-dfs.sh
```

NameNode的Web UI是<http://localhost:50070>

### (2) 启动ResourceManager和NodeManager守护进程：

```sh
sbin/start-yarn.sh
```

ResourceManager的Web UI是<http://localhost:8088>

# 3. 部署HBase

为了方便使用，在.bashrc中设置：

```sh
export HBASE_HOME=~/bd/hbase-1.1.2
export PATH=$HBASE_HOME/bin:$PATH
```

## 3.1 配置JAVA路径
在conf/hbase-env.sh中设置：

```sh
export JAVA_HOME=/usr/local/jdk1.7.0_01
```

注：如果设置了JAVA_HOME变量，这一步不是必须的。

## 3.2 设置hbase和zookeeper数据的存储位置

在conf/hbase-site.xml中：

```xml
<property>
    <name>hbase.rootdir</name>
    <value>file:///home/admin/bd-data/hbase</value>
</property>
<property>
    <name>hbase.zookeeper.property.dataDir</name>
    <value>/home/admin/bd-data/zookeeper</value>
</property>
```

在伪分布式模式下，需要增加：

```xml
<property>
    <name>hbase.cluster.distributed</name>
    <value>true</value>
</property>
```

并且修改数据存储位置到HDFS：

```xml
<property>
  <name>hbase.rootdir</name>
  <value>hdfs://master:9000/hbase</value>
</property>
```

## 3.3 启动HBase

```sh
bin/start-hbase.sh
```

启动后jps能看到HMaster。

# 4. 部署Phoenix

为了方便使用，在.bashrc中设置：

```sh
export PHOENIX_HOME=~/bd/phoenix-4.4.0-HBase-1.1-bin
export PATH=$PHOENIX_HOME/bin:$PATH
```

将Phoenix目录下的jar包复制到$HBASE_HOME/lib目录下。

将phoenix-[version]-client.jar添加到$CLASSPATH：

```sh
export CLASSPATH=$CLASSPATH:~/bd/phoenix-4.4.0-HBase-1.1-bin/phoenix-4.4.0-HBase-1.1-client.jar
```

TODO：不确定此步骤是否必须。

重启HBase，执行：

```sh
sqlline.py master
```

查看是否正常进入。

# 5. 部署Spark

为了方便使用，在.bashrc中设置：

```sh
export SPARK_HOME=~/bd/spark-1.6.1-bin-without-hadoop
export PATH=$SPARK_HOME/bin:$PATH
```

## 5.1 Standalone模式

### (1) 告诉Spark使用哪个Hadoop

Spark会使用Hadoop client库，用来访问HDFS和YARN。我下载的是即不带Hadoop的版本，好处是比较灵活，可以自己选择连接哪一个版本的Hadoop。但是要在环境变量中配置路径，即在conf/spark-env.sh中增加：

```sh
export SPARK_DIST_CLASSPATH=$(hadoop classpath)
```

### (2) 手动启动Spark集群 TODO

```sh
sbin/start-master.sh -h 192.168.229.128
sbin/start-slave.sh spark://192.168.229.128:7077
```

启动后jps可以看到：Master和Worker。
使用Spark Shell连接到集群：

```sh
bin/spark-shell --master spark://192.168.229.128:7077
```

## 5.2 Yarn模式

Yarn模式下，不需要手动启动Spark。由Yarn来调用。

# 6. 部署Hive

TODO TODO

```sh
export HIVE_HOME=~/bd/apache-hive-1.2.2-bin
export PATH=$HIVE_HOME/bin:$PATH
```

## 6.1 TODO

## 6.2 TODOd

## 6.3 TODO

## 6.4 在Spark中使用HiveContext

```python
from pyspark import SparkConf, SparkContext
from pyspark.sql import HiveContext, Row

conf =  SparkConf().setMaster('local').setAppName('My App')
sc = SparkContext(conf = conf)
sqlContext = HiveContext(sc)
```

# To Be Continued...
