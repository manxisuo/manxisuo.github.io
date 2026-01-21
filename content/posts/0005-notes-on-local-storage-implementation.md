---
title: "本地存储(local storage)实现的便笺"
date: 2013-08-28
draft: false
tags:
  - "前端"
  - "存储"
  - "JavaScript"
---

使用HTML LocalStorage(本地存储)实现的便笺。可以添加任意多个便笺，可以移动位置、改变大小、折叠、修改标题。

输入的内容、便笺的标题、位置、尺寸大小会自动保存到本地存储，支持导出功能。

<!-- more -->

![便笺](https://cloud.githubusercontent.com/assets/3950285/22852505/871b78de-f078-11e6-8017-784b0f12e16a.png)


## 演示地址：

[点击打开](http://manxisuo.github.io/notepaper/)

## 注意事项：

所有内容是保存在本地的，如果清理了网站在本地的数据(例如在chrome中选择 **删除 Cookie 以及其他网站数据和插件数据** )，则**数据将全部丢失**。
