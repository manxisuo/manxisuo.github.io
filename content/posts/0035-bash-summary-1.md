---
title: "Bash脚本总结（一）"
date: 2026-01-20
draft: false
tags:
  - "Bash"
  - "Shell"
---

## 一. 变量与赋值

```sh
name="Alice"
count=10
echo $name
echo $((count + 5))  # 数学运算需要 $(( ))
echo "Hello, $name! You have $count new messages."
```

注意：
1. `=` 两边不能有空格
2. 变量引用时必须加`$`，除非在`[[ ]]`条件判断中使用字符串比较。

## 二. 条件与判断

Bash 有两套判断语法：`[`和`[[`。后者更现代、更安全。

```sh
if [[ $count -gt 5 ]]; then
    echo "大于5"
elif [[ $count -eq 5 ]]; then
    echo "等于5"
else
    echo "小于5"
fi
```

比较符：

+ `-eq`：等于
+ `-ne`：不等于
+ `-gt`：大于
+ `-lt`：小于
+ `-ge`：大于等于
+ `-le`：小于等于
+ 字符串比较：`==`, `!=`, `-z`, `-n`

## 三. 循环结构

Bash 有三种常见循环：

```sh
for i in {1..5}; do
    echo $i
done

while [[ $count -lt 5 ]]; do
    ((count++))
    echo $count
done

for file in *.txt; do
    echo "Found: $file"
done
```

## 四. 函数与参数

函数定义形式灵活：

```sh
greet() {
    echo "Hello $1"
}
greet "world"
```

`$1`, `$2`, … 表示参数。`$@`表示所有参数，`$#`表示参数个数。
函数的返回值是上一个命令的退出状态码（`0`表示成功）。

## 五. 退出状态与短路逻辑

Bash 的一切命令都有一个返回码：

+ **0**：成功
+ **非零**：失败

逻辑控制：

```sh
command1 && command2  # 前者成功才执行后者
command1 || command2  # 前者失败才执行后者
```

强制在出错时退出脚本：

```sh
set -e    # 只要有命令失败，整个脚本退出
```

## 六. 输入输出与管道

这是 Bash 的灵魂。

```sh
command > out.txt       # 输出重定向
command 2> err.txt      # 错误输出
command > all.txt 2>&1  # 合并输出

cat file.txt | grep "pattern" | sort
```
通过管道`|`，一个命令的输出直接成为下一个命令的输入。
这是 Linux 哲学的体现：“一切都是流（stream）”。

```sh
# 删除所偶log文件
find ./logs -name "*.log" -print0 | xargs -0 rm -f

# 另外几种方式
find ./logs -name "*.log" -exec rm -f {} \;
find ./logs -name "*.log" -exec rm -f {} +
find ./logs -name "*.log" -delete
```

## 七. 字符串与数组

```sh
str="Hello World"
echo ${str:0:5}         # Hello
echo ${str/World/Bash}  # Hello Bash

# 定义数组
arr=(apple banana cherry)
arr=([0]=apple [1]=banana [2]=cherry)

echo ${arr[1]}          # banana
for item in "${arr[@]}"; 
    do echo $item; 
done

# 添加元素
arr+=("orange")

# 删除某个元素
unset arr[1]        # 删除第二个元素

echo ${arr[@]}  # 输出数组内容
echo ${arr[*]}  # 输出数组内容
echo ${#arr[@]}  # 输出数组长度
echo ${#arr[*]}  # 输出数组长度
```

+ `"${arr[@]}"`：每个元素被当作单独的字符串处理
+ `"${arr[*]}"`：所有元素被合并成一个字符串，中间用空格分隔
+ 区别：`[@]`会保持数组元素独立，`[*]`会把所有元素拼成一个整体。

## 八. Bash的“力量来源”：Unix工具链

Bash 本身只是框架，真正的力量来自它调用的命令：

+ 文本三剑客：`grep`, `awk`, `sed`
+ 管道好伙伴：`xargs`, `cut`, `sort`, `uniq`, `tr`
+ 文件操作：`find`, `ls`, `rm`, `mv`, `cp`
+ 系统操作：`ps`, `df`, `du`, `kill`
+ 网络操作：`curl`, `scp`, `ssh`, `ping`

## 九. Bash 的运行机制

1. 交互模式（终端）：你输入一条命令，它立刻解释执行。
2. 脚本模式（文件）：执行 .sh 文件时，Bash 从上到下逐行解析。
3. 命令查找路径：执行命令时，Bash 在 `$PATH` 中依次查找。
4. 子进程模型：管道和子 Shell 都通过 `fork()` + `exec()` 机制实现。

## 十. 变量引用

六种变量引用形式：

```sh
$a
${a}
'$a'
'${a}'
"$a"
"${a}"
```

六种写法看似相似，其实完全不等价，它们在 **变量展开（variable expansion）** 和 **引号处理（quoting）** 上有本质区别。

我们逐个分析。假设：

```bash
a="hello world"
```

### 1. `$a`

**效果：变量展开，空格分隔。**

```bash
echo $a
```

输出：

```txt
hello world
```

> 这里 `$a` 被替换成变量内容，然后由 shell 按空格再次分词。
> 所以如果 `a` 中有多个词（比如文件名），它们会被拆成多个参数。

### 2. `${a}`

**完全等价于 `$a`，只是语法更安全。**

```bash
echo ${a}
```

输出：

```txt
hello world
```

区别在于：

* `${a}` 明确界定了变量名边界。
* 在复杂场景（如 `${a}_suffix`）时可以避免歧义。

例：

```bash
echo "$a_suffix"     # 试图引用变量 a_suffix
echo "${a}_suffix"   # 正确：引用 a，再加 _suffix
```

### 3. `'$a'`

**单引号禁止变量展开。**

```bash
echo '$a'
```

输出：

```txt
$a
```

单引号内的内容是**完全字面值（literal）**，不做任何解释。
也就是说 `$`、`*`、`\` 都失去特殊含义。

### 4. `'${a}'`

**仍然是字面值，不会展开。**

```bash
echo '${a}'
```

输出：

```txt
${a}
```

单引号的作用范围比 `${}` 还强。它告诉 Bash：“不要动里面的内容”。
所以这一种和 `'$a'` 在本质上等价。

### 5. `"$a"`

**双引号允许变量展开，但禁止分词。**

```bash
echo "$a"
```

输出：

```txt
hello world
```

区别于 `$a` 的地方在于：
即使 `a` 含有空格，也会作为**一个整体参数**传入。

示例：

```bash
a="file 1.txt"
echo $a     # 等价于 echo file 1.txt  -> 两个参数
echo "$a"   # 等价于 echo "file 1.txt" -> 一个参数
```

因此，**双引号是 Bash 编程中保护字符串的最佳实践。**

### 6. `"${a}"`

**与 `"$a"` 等价。**

```bash
echo "${a}"
```

输出：

```txt
hello world
```

两者差别仅在于是否明确了变量边界（与 `${a}` vs `$a` 的区别相同）。
推荐始终写 `"${a}"`，这是最安全、最通用的引用方式。

### ✅ 总结对比表：

| 写法       | 是否展开变量 | 是否保留空格    | 说明           |
| -------- | ------ | --------- | ------------ |
| `$a`     | ✅ 是    | ❌ 否（会被分词） | 简单展开，易出错     |
| `${a}`   | ✅ 是    | ❌ 否       | 同上，安全些       |
| `'$a'`   | ❌ 否    | ✅ 是       | 字面值，不展开      |
| `'${a}'` | ❌ 否    | ✅ 是       | 字面值，不展开      |
| `"$a"`   | ✅ 是    | ✅ 是       | 展开但保留整体（推荐）  |
| `"${a}"` | ✅ 是    | ✅ 是       | 展开但保留整体（最推荐） |

一句话总结：

> 在 Bash 中，`双引号包裹 + ${}展开`是安全、通用的写法。
> 即：始终用`"${var}"`。

## 十一. `$*`、`$@`、`"$*"`、`"$@"`的区别

| 形式     | 是否展开所有参数 | 参数是否独立     | 实际行为          |
| ------ | -------- | ---------- | ------------- |
| `$*`   | ✅ 是      | ❌ 否（拆散）    | 所有参数拼成一个词串    |
| `"$*"` | ✅ 是      | ❌ 否（合并成一个） | 所有参数拼成一个整体字符串 |
| `$@`   | ✅ 是      | ❌ 否（拆散）    | 同 `$*`        |
| `"$@"` | ✅ 是      | ✅ 是（逐个独立）  | 正确逐个参数展开      |

### 推荐记忆方法

> * 想逐个传参数，用：`"$@"`
> * 想拼成一句话，用：`"$*"`

### 实际应用例子

假设我们写一个简单的转发脚本：

```bash
#!/bin/bash
echo "Forwarding all args to another command:"
echo "$@"

# 推荐的写法
another_command "$@"
```

如果你用错写成 `"$*"`，参数中带空格的内容就会被破坏，可能引发灾难性错误。

总结一句：

> Bash 的 `"${@}"` 是**参数安全展开**的黄金标准。几乎所有脚本都应使用它，而避免裸 `$*` 或 `$@`。

