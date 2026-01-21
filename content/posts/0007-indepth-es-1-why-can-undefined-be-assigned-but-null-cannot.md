---
title: "深入ES(一)：为什么undefined可以被赋值，而null不可以？"
date: 2015-12-28
draft: false
tags:
  - "JavaScript"
  - "ES"
  - "前端"
---

## 提出问题

如下代码：

```javascript
undefined = 123; // 不报错，但是赋值操作无效
null = 123; // 报错：Uncaught Reference Error
```

第一条语句可以执行，尽管赋值并没有成功；第二条语句报错。这是为什么呢？`undefined`和`null`有什么区别？

## 解决问题

读过ES规范后，发现原来是这样的：

- `undefined`、`NaN`和`Infinity`都是全局对象`window`的属性。既然是属性，当然可以赋值。然而这三个属性又是不可写的属性，即它们的的内部特性`[[writable]]`为`false`，所以赋值无效。

- `null`是一个字面量(literal)，准确地说叫做**Null字面量**。与`true`和`false`类似。它们都属于JavaScript的保留字。换句话说它们都是**值**，与数字值`123`、字符串值`"foobar"`一样，当然不能被赋值了。

## 再多说些

1. 既然`undefined`只是一个属性，并不是语言的保留字，那么它是否可以用来作为变量的名字？当然可以，你完全可以自定义一个叫做`undefined`的变量或者函数，但是注意不要把它放到全局作用域。例如：

```javascript
function foo() {
     var undefined = 10;
     console.log(undefined);
}
foo(); // 打印10
```

2. 通过ES5新增的方法`Object.getOwnPropertyDescriptor`方法，可证明`undefined`是`window`对象的只读属性：

```javascript
Object.getOwnPropertyDescriptor(window, 'undefined');

/*
  输出：
  Object {value: undefined, writable: false,
  enumerable: false, configurable: false}
*/
```

3. 在严格模式下，给`undefined`赋值会报错。因为严格模式下，禁止给对象的只读属性赋值。

4. `null`虽然号称是`Null`这种原始类型可以取的唯一值，然而：

```javascript
typeof null; // 输出"object"
```

## 参考文档

1. [15.1.1.3 undefined][1]
2. [7.6.1 Reserved Words][2]

  [1]: http://es5.github.io/#x15.1.1.3
  [2]: http://es5.github.io/#x7.6.1
