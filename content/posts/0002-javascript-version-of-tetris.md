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

![media-20130323](https://github-production-user-asset-6210df.s3.amazonaws.com/3950285/533386797-752ccec2-701e-40b6-9317-20cebadee990.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20260108%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260108T141712Z&X-Amz-Expires=300&X-Amz-Signature=31de9e7a7a16027de95143d047ffebd7a3bd42b81dc428d4643a7183407fbfc7&X-Amz-SignedHeaders=host)

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
