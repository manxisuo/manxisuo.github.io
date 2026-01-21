---
title: "《Spark快速大数据分析》笔记之一"
date: 2018-06-30
draft: false
tags:
  - "大数据"
  - "Spark"
  - "学习笔记"
---

## 2. Spark下载与入门

### 2.2 Spark的Shell

两种类型的Shell：

```bash
# Python Shell
bin/pyspark

# Scala Shell
bin/spark-shell
```

使用IPython：

```bash
# 下载
sudo apt-get install ipython

# 使用IPython
IPYTHON=1 ./bin/pyspark

# 下载IPython Notebook
sudo apt-get install ipython-notebook

# 使用IPython Notebook
IPYTHON_OPTS="notebook" ./bin/pyspark
```

### 2.3 Spark核心概念简介

- 驱动器（SparkContext）
- 执行器

### 2.4 独立应用

创建SparkContext：

```python
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster('local').setAppName('My App')
sc = SparkContext(conf = conf)
```

运行Python脚本：

```bash
bin/spark-submit my_script.py

# 使用Python3
PYSPARK_PYTHON=`which python3` spark-submit my_script.py
```

## 3. RDD编程

RDD - 弹性分布式数据集。是一个不可变的分布式对象集合。

### 3.2 创建RDD

创建RDD的方法：

- 读取外部数据集
- 在驱动器程序中并行化一个集合

例如：

```python
lines = sc.textFile('README.md')
nums = sc.parallelize([1, 2, 3, 4])
```

### 3.3 RDD操作

- 转化操作：例如map、filter
- 行动操作：例如count、take、collect、saveAsTextFile、saveAsSequenceFile

RDD的转换操作是惰性求值的。

注意：传递函数时，不小心可能会把函数所在的对象也序列化传出去。

1. 针对各个元素的转化操作
    - `map`
    - `flatMap`
    - `filter`
    - `distinct`
    - `sample(withReplacement, fraction, [seed])`

2. 伪集合操作
    - `RDD1.union(RDD2)`
    - `RDD1.intersection(RDD2)`
    - `RDD1.substract(RDD2)`
    - `RDD1.cartesian(RDD2)`

3. 行动操作
    - `collect()`
    - `count()`
    - `countByValue()`
    - `take(num)`
    - `top(num)`
    - `takeOrdered(num)(ordering)`
    - `takeSample(withReplacement, num, [seed])`
    - `reduce(func)`
    - `fold(zero)(func)`
    - `aggregate(zeroValue)(seqOp, combOp)`
    - `foreach(func)`

### 3.6 持久化（缓存）

`persist(storageLevel=StorageLevel(False, True, False, False, 1))`

默认级别MEMORY_ONLY_SER。等价于`cache()`。

## 4. 键值对操作

### 4.2 创建Pair RDD

方法有很多，例如用map：

```python
pairs = lines.map(lambda x : (x.split(' ')[0], x))
```

### 4.3 Pair RDD的转化操作

1. Pair RDD的转化操作
    - `reduceByKey(func)`
    - `groupByKey()`
    - `combineByKey(createCombiner, mergeValue, mergeCombiners, partitioner)`
    - `mapValues(func)`
    - `flatMapValues(func)`
    - `keys()`
    - `values()`
    - `sortByKey()`

2. 针对两个Pair RDD的转化操作
    - `substractByKey`
    - `join`
    - `rightOuterJoin`
    - `leftOuterJoin`
    - `cogroup`

#### 4.3.1 聚合操作

1. 聚合操作：

    - `reduceByKey()`：对应reduce()
    - `foldByKey()`：对应fold()
    - `combineByKey()`：对应aggregate()

2. 并行度优化：
    - `repartition()`
    - `coalesce(numPartitions, shuffle=False)`

#### 4.3.2 数据分组

`groupByKey()`

注意：`rdd.reduceByKey(func)`等价于`rdd.groupByKey().mapValues(v => v.reduce(func))`，但前者更高效。

#### 4.3.3 连接

#### 4.3.4 数据排序

`sortByKey()`

### 4.4 Pair RDD的行动操作

- `countByKey()`
- `collectAsMap()`
- `lookup(key)`

### 4.5 数据分区（进阶）

分区优化：

```python
# Python
partitionBy(numPartitions, partitionFunc=<function portable_hash at 0x7f1ac7340578>)
```

```java
// Java
public JavaPairRDD<K,V> partitionBy(Partitioner partitioner)
```

```scala
// Scala
def partitionBy(partitioner: Partitioner): JavaPairRDD[K, V]
```

分区数`numPartitions`至少应该和集群的总核心数一样。

很多操作，都会自动为结果RDD设定已知的分区方式信息。例如`sortByKey()`和`groupByKey()`，分别生成范围分区的RDD和哈希分区的RDD。另一方面，诸如`map()`这样的操作会导致新的RDD失去父RDD的分区信息。

#### 4.5.1 获取RDD的分区方式：

- Java中：`rdd.partitioner()`
- Scala中：`rdd.partitioner`
- Python中：无法获取，但是Spark内部仍然会利用已有的分区信息。

#### 4.5.3 从分区中获益的操作

- `cogroup()`
- `groupWith()`
- `join()`
- `leftOuterJoin()`
- `rightOuterJoin()`
- `groupByKey()`
- `reduceByKey()`
- `combineByKey()`
- `lookup()`

#### 4.5.4 影响分区方式的操作

所有会为结果RDD设好分区方式的操作：

- `cogroup()`
- `groupWith()`
- `join()`
- `leftOuterJoin()`
- `rightOuterJoin()`
- `groupByKey()`
- `reduceByKey()`
- `combineByKey()`
- `partitionBy()`
- `sort()`
- `mapValues()`：如果父RDD有分区方式的话
- `flatMapValues()`：如果父RDD有分区方式的话

注意：在无需改变元素的键时，尽量使用`mapValues()`或`flatMapValues()`。

#### 4.5.5 自定义分区方式

- 在Java和Scala中，扩展`Partitioner`类
- 在Python中，只需要把一个特定的哈希函数作为一个额外的参数传给`RDD.partitionBy()`函数。例如：

```python
import urlparse

def hash_domain(url):
    return hash(urlparse.urlparse(url).netloc)

rdd.partitionBy(20, hash_domain)
```

注意：如果想对多个RDD使用相同的分区方式，就应该使用同一个函数对象，比如一个全局函数，而不是为每个RDD创建一个新的函数对象。
