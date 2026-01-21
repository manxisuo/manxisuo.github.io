---
title: "图解JavaScript闭包"
date: 2016-04-06
draft: false
tags:
  - "JavaScript"
  - "前端"
  - "闭包"
---

代码：

```javascript
function Foo() {
    var i=0;
    return function() {
        console.log(i++);
    }
}

var f1 = Foo();
var f2 = Foo()
f1();
f1();
f2();
```

## 1. 刚定义完函数Foo时：

![closure-1](https://cloud.githubusercontent.com/assets/3950285/22853559/a33f1202-f094-11e6-89ab-27b362d8bcbb.png)

## 2. 所有代码执行完时：

![closure-2](https://cloud.githubusercontent.com/assets/3950285/22853561/a9147f6e-f094-11e6-8a93-798234c9e493.png)

## 3. 说明一下：

问题的关键是：

(1) 函数在执行期间会产生一个执行上下文(EC)，作为函数的运行时表示，函数返回时此上下文销毁。所以很函数`Foo`被调用了两次必然产生两个不同的执行上下文。

(2) 执行上下文中有个叫做词法环境(LE)的东西，用来存放函数执行时产生的局部变量、this等东西。函数`Foo`里面的局部变量`i`就放在词法环境LE里面。

(3) 函数返回后，执行上下文销毁了，但是词法环境还是可以存在的，所以你要问`i`存放在哪里？不错，就在词法环境里面。

(4) 函数里面定义的**内部函数**总是有一个内部指针(即图中的[[scope]])指向外部词法环境。所以f1和f2可以引用它们的外部词法环境中的各自的`i`变量，并对它们进行操作。 如果还有什么不明白的，可以留言。 注：为了方便理解，图中某些地方进行了简化，但是本质没有变化。
