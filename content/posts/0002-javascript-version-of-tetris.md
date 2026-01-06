---
title: "JavaScript版俄罗斯方块"
date: 2013-03-23
draft: false
tags:
  - "JavaScript"
  - "游戏"
  - "前端"
---

用JavaScript写的俄罗斯方块，比较简单，不求用尽量少的代码，只求代码清晰条理。主要是为了练习JavaScript的面向对象编程。

<!-- more -->

![media-20130323](https://cloud.githubusercontent.com/assets/3950285/22852380/0278eb22-f076-11e6-8f5f-37836a589f91.jpg)

# 操作说明

* left: 左移
* right: 右移
* down: 加速下落
* up: 变形
* space: 直接落底

另外，考虑到触屏用户，还增加了点击屏幕进行操作的方式。
即，通过点击画布不同区域，同样可以达到控制的目的。

# Bug
在方块没有完全进入画布前，左右移动方块到边界，会导致Bug。

# 代码

<https://github.com/manxisuo/tetris>
