---
title: "JavaScript正则表达式"
date: 2016-07-10
draft: false
tags:
  - "JavaScript"
  - "正则表达式"
  - "前端"
---

## 一. 创建正则表达式

创建正则表达式有两种方式：

### 1. 字面量形式

```javascript
/pattern/flags
```

**示例**：

```javascript
var re = /^(0|([1-9][0-9]*))$/; // 自然数
```

### 2. 使用构造函数

```javascript
new RegExp(/pattern/flags)
```

**示例**：

```javascript
var re = new RegExp(/ab/i); // ab, aB, Ab, AB
```

### 3. 修饰符

- **i**：执行对大小写不敏感的匹配。
- **g**：执行全局匹配（查找所有匹配而非在找到第一个匹配后停止）。
- **m**：执行多行匹配。

## 二. 正则表达式的方法

### 1. RegExp.prototype.test()

`test()`方法执行一个检索，用来查看正则表达式与指定的字符串是否匹配。返回`true`或`false`。

**示例**：

```javascript
/.?onkey/.test('It is a monkey!'); // true
```

### 2. RegExp.prototype.exec()

`exec()`方法为指定的一段字符串执行搜索匹配操作。它的返回值是一个数组或者`null`。

**示例**：

```javascript
/.?onkey/.exec('It is a monkey!'); // ["monkey"]
```

### 3. **g模式**下的test()和exec()方法

当正则表达式带有g修饰符时，内部会维护一个位置指针。开始时位置指针指向字符串的起始位置。

每次调用test()和exec()时，如果找到匹配的子串，位置指针就会指向匹配的字串后面的位置。如果没有找到匹配的子串，位置指针依旧指向字符串的起始位置。

下次调用test()和exec()时，会从位置指针指向的位置开始搜索——即使此次搜索的字符串与上次不同。

**示例**：

```javascript
var re = /a\db/g;
var str = 'a1b, a2b, a3b';
re.exec(str); // ["a1b"]
re.exec(str); // ["a2b"]
re.exec(str); // ["a3b"]
re.exec(str); // null
re.exec(str); // ["a1b"]
re.test(str); // true
re.test(str); // true
re.test(str); // false
// ...
```

### 4. 存在分组时的exec()方法

在正则表达式中，用小括号包裹起来的部分叫做**分组**。

当正则表达式中存在n个分组时，`exec()`返回的数组将会包含n+1个元素。
其中第一个元素是匹配到的子串，后面的n个元素是子串中对应的分组的值，且与分组在正则表达式中出现的顺序一致。

**示例**：

```javascript
var linkRe = /<a name="(.+)" href="(.+)">/;
var html = '<div><a name="github" href="https://github.com">GitHub官网</a></div>';
linkRe.exec(html); // ["<a name="github" href="https://github.com">", "github", "https://github.com"]
```

## 三. 字符串中与正则表达式相关的方法

### 1. String.prototype.match()

`match()`方法会提取与指定的正则表达式匹配的子串。

**语法**：

```javascript
str.match(regexp)
```

**参数**：

`regexp`是一个正则表达式对象。如果`regexp`不是一个正则表达式对象，则内部会调用new RegExp(regexp)方法将其转换为正则表达式对象。

**示例**：

```javascript
var re1 = /a\db/;
var re2 = /a\db/g;
var str = 'a1b, a2b, a3b';
str.match(re1); // ["a1b"]
str.match(re2); // ["a1b", "a2b", "a3b"]
```

从上例中也可以看出：当正则表达式不带g修饰符时，将返回第一次匹配到的结果(与`RegExp.exec(str)`得到的结果相同)；当正则表达式带g修饰符时，将返回所有匹配到的结果。如果没有匹配项，则返回`null`。

### 2. String.prototype.split()

`split()`方法通过把字符串分割成子字符串来把一个String对象分割成一个字符串数组。

**语法**：

```javascript
str.split([separator][, limit])
```

**参数**：

`separator`指定分割字符串的分隔符，它可以是一个字符串或者正则表达式。如果忽略`separator`，则返回整个字符串的数组形式。如果`separator`是一个空字符串，则`str`将会把原字符串中每个字符的数组形式返回。

`limit`是一个整数，限定返回的分割片段数量。`split`方法仍然分割每一个匹配的`separator`，但是返回的数组只会截取最多`limit`个元素。

**示例**：

```javascript
'Hi, JS'.split() // ["Hi, JS"]
'Hi, JS'.split('') // ["H", "i", ",", " ", "J", "S"]
'Hi, JS'.split(',') // ["Hi", " JS"]
'foo, bar & baz'.split(/,|&/) // ["foo", " bar ", " baz"]
'foo, bar & baz'.split(/,|&/, 2) // ["foo", " bar "]
```

如果 separator 是一个正则表达式，且包含捕获括号（capturing parentheses），则每次匹配到 separator 时，捕获括号匹配的结果将会插入到返回的数组中。然而，不是所有浏览器都支持该特性。

**示例**：

```javascript
'A123B345C567D'.split(/\d(\d)\d/) // ["A", "2", "B", "4", "C", "6", "D"]
```

### 3. String.prototype.search()

`search()`方法执行一个查找，看该字符串对象与一个正则表达式是否匹配。

**语法**：

```javascript
str.search(regexp)
```

**参数**：

`regexp`是一个正则表达式对象。如果`regexp`不是一个正则表达式对象，则内部会调用new RegExp(regexp)方法将其转换为正则表达式对象。

如果匹配成功，则返回正则表达式在字符串中首次匹配项的索引。否则，返回 -1。

当你想要知道字符串中是否存在某个模式（pattern）时可使用`search`，类似于正则表达式的`test`方法。当要了解更多匹配信息时，可使用`test`（会更慢），该方法类似于正则表达式的`exec`方法。

**示例**：

```javascript
'There are cat, hat and bat!'.search(/\wat/); // 10
'Java and JavaScript'.search('Python'); // -1
```

### 4. String.prototype.replace()

`replace()`方法使用一个替换值（replacement）替换掉一个匹配模式（pattern）在原字符串中某些或所有的匹配项，并返回替换后的新的字符串。这个替换模式可以是一个字符串或者一个`RegExp`，替换值可以是一个字符串或者一个函数。

**语法**：

```javascript
str.replace(regexp|substr, newSubStr|function)
```

**参数**：

- 参数`regexp`是一个`RegExp`对象。该正则所匹配的内容会被第二个参数的返回值替换掉。
- `substr`是一个要被newSubStr`替换的字符串。
- `newSubStr`用于替换掉第一个参数在原字符串中的匹配部分的`String`。该字符串中可以内插一些**特殊的变量名**。
- `function`一个用来创建新子字符串的函数，该函数的返回值将替换掉第一个参数匹配到的结果。

`newSubStr`中可以使用的特殊的变量名：

- $$：插入一个 "$"。
- $&：插入匹配的子串。
- $`：插入当前匹配的子串左边的内容。
- $'：插入当前匹配的子串右边的内容。
- $n：假如第一个参数是 RegExp对象，并且 n 是个小于100的非负整数，那么插入第 n 个括号匹配的字符串。

指定一个函数作为参数：

- `match`：匹配的子串。（对应于上述的$&。）
- `p1, p2, ...`：假如`replace()``方法的第一个参数是一个`RegExp`对象，则代表第n个括号匹配的字符串。（对应于上述的$1，$2等。）
- `offset`：匹配到的子字符串在原字符串中的偏移量。（比如，如果原字符串是“abcd”，匹配到的子字符串时“bc”，那么这个参数将时1）
- `string`：被匹配的原字符串。

**示例**：

```javascript
// 交换字符串中的两个单词
var re = /(\w+)\s(\w+)/;
var str = "John Smith";
var newstr = str.replace(re, "$2, $1"); // "Smith, John"
```

在 `replace()`中使用global和ignore时，会执行全局替换和忽略大小写的替换。
