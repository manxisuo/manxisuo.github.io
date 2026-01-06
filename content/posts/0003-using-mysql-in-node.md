---
title: "在Node中使用MySQL"
date: 2013-03-24
draft: false
tags:
  - "Node.js"
  - "数据库"
  - "MySQL"
---

本文介绍了如何在Node中使用MySQL进行简单的数据库操作。

<!-- more -->

# 1. 安装

在终端执行：

```shell
npm install mysql
```

# 2. 简单的查询

```javascript
var mysql = require('mysql');

var conn = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'root',
    database: 'test'
});

conn.connect();

var queryString = 'SELECT * FROM Person';

conn.query(queryString, function(err, rows, fields) {
    if (err) throw err;

    for (var i in rows) {
        console.log(i, rows[i]);
    }

    for (var i in fields) {
        // console.log(i, fields[i]);
    }
});

conn.end();
```

结果如下：

![a5d4224f-74d4-3cb3-a189-322b26a3e03b](https://cloud.githubusercontent.com/assets/3950285/22852415/bdd9fc26-f076-11e6-9c75-c43ada801dae.png)

当然, Connection的选项也可以这样写：

```javascript
var conn = mysql.createConnection('mysql://root:root@localhost/test');
```

上面这种方式, 是等到查询得到所有行之后, 才回调的. 如果表的行数很大, 你想每查到一行就执行相应的动作时, 可以这样写：

```javascript
var mysql = require('mysql');

var conn = mysql.createConnection('mysql://root:root@localhost/test');

conn.connect();

var query = conn.query('SELECT * FROM Person');

query.on('error', function(err) {
    throw err;
});

query.on('fields', function(fields) {
    console.log(fields);
});

query.on('result', function(row) {
    console.log(row);
});

conn.end();
```

需要注意的是, 只要某一行数据到来时, 就会相应的调用回调函数. 如果由于某种原因, 你想在处理完某一行之前不希望得到下一行, 那么你需要暂停查询, 等到处理完这一行后再恢复查询. 但是要小心, 由于某些错误, 可能会导致结果的不一致性.

```javascript
query.on('result', function(row) {
    conn.pause();
    console.log(row);
    conn.resume();
});
```
