---
title: "C++笔记一：默认构造函数、拷贝构造函数、（拷贝）赋值运算符"
date: 2022-08-20
draft: false
tags:
  - "C++"
  - "编程语言"
  - "学习笔记"
---

首先我们写一个类`Product`，代码如下：

Product.h

```c++
#pragma once
#include <QString>

class Product
{
public:
    Product();
    Product(const QString &name);
    Product(const Product &other);
    Product& operator=(const Product &other);
    ~Product();
    inline QString name() const { return mName; }

private:
    QString mName;
    int mId;
    static int getId();
};
````

Product.cpp

```c++
#include "Product.h"
#include <QDebug>

Product::Product()
{
    mId = getId();
    qInfo() << "无参构造函数" << mId << mName;
}

Product::Product(const QString &name) : mName(name)
{
    mId = getId();
    qInfo() << "有参构造函数" << mId << mName;
}

Product::Product(const Product &other)
{
    mId = getId();
    mName = other.mName;
    qInfo() << "拷贝构造函数" << mId << mName;
}

Product &Product::operator=(const Product &other)
{
    mName = other.mName;
    qInfo() << "赋值运算符";
    return *this;
}

Product::~Product()
{
    qInfo() << "析构函数" << mId << mName;
}

int Product::getId()
{
    static int id = 0;
    return ++id;
}
```

## 1. 无参构造函数

无参构造函数，也就是默认构造函数，有以下几种调用方式：

```c++
qInfo() << "栈对象：";
Product s1;
Product s12();  // 函数声明
Product s2{};
Product s3 = {};

qInfo() << "堆对象：";
Product *h1 = new Product;
Product *h2 = new Product();
Product *h3 = new Product{};
```

在栈和堆上使用无参构造函数实例化Product的对象时，各有三种方式。其中的` Product s12()`实际上是一个函数声明。上述代码运行结果如下：

>栈对象：
>无参构造函数 1 ""
>无参构造函数 2 ""
>无参构造函数 3 ""
>堆对象：
>无参构造函数 4 ""
>无参构造函数 5 ""
>无参构造函数 6 ""
>析构函数 3 ""
>析构函数 2 ""
>析构函数 1 ""

从中可见，栈上的对象的析构顺序与其构造顺序相反，这应该是栈的特点导致的（存疑）。

## 2. 有参构造函数

有参构造函数，也就是带有参数的构造函数，有以下几种调用方式：

```c++
qInfo() << "栈对象：";
Product s1("Appple");
Product s2{"Banana"};
Product s3 = {"Grape"};
Product s4 = Product(QString("Orange"));

qInfo() << "堆对象：";
Product *h1 = new Product("Peach");
Product *h2 = new Product{"Watermelon"};
```

在栈和堆上使用有参构造函数实例化Product的对象时，分别有三种和两种方式。上述代码运行结果如下：

>栈对象：
>有参构造函数 1 "Appple"
>有参构造函数 2 "Banana"
>有参构造函数 3 "Grape"
>有参构造函数 4 "Orange"
>堆对象：
>有参构造函数 5 "Peach"
>有参构造函数 6 "Watermelon"
>析构函数 4 "Orange"
>析构函数 3 "Grape"
>析构函数 2 "Banana"
>析构函数 1 "Appple"

## 3. 拷贝构造函数

拷贝构造函数，有以下几种调用方式：

```c++
Product p("Apple");

qInfo() << "栈对象：";
Product s1(p);
Product s2 = p;
Product s3 {p};
Product s4 = {p};
Product s5 = Product(p);  // 注意：只调了一次拷贝构造函数

qInfo() << "堆对象：";
Product *h1 = new Product(p);
Product *h2 = new Product{p};
```

在栈和堆上使用拷贝构造函数实例化Product的对象时，分别有五种和两种方式。上述代码运行结果如下：

>有参构造函数 1 "Apple"
>栈对象：
>拷贝构造函数 2 "Apple"
>拷贝构造函数 3 "Apple"
>拷贝构造函数 4 "Apple"
>拷贝构造函数 5 "Apple"
>拷贝构造函数 6 "Apple"
>堆对象：
>拷贝构造函数 7 "Apple"
>拷贝构造函数 8 "Apple"
>析构函数 6 "Apple"
>析构函数 5 "Apple"
>析构函数 4 "Apple"
>析构函数 3 "Apple"
>析构函数 2 "Apple"
>析构函数 1 "Apple"

## 4. （拷贝）赋值运算符

赋值运算符只是将一个对象的状态赋值给另一个同类型的对象，本身不会产生新的`Product`对象。调用方式如下：

```c++
Product p1("Apple");
Product p2("Banana");
p2 = p1;
```

上述代码运行结果如下：

>有参构造函数 1 "Apple"
>有参构造函数 2 "Banana"
>赋值运算符
>析构函数 2 "Apple"
>析构函数 1 "Apple"

## 5. 对象作为函数的参数

构造以下四个函数：

```c++
void fn1(Product p) {}
void fn2(const Product p) {}
void fn3(Product &p) {}
void fn4(const Product &p) {}
```

测试代码如下：

```c++
Product p("Apple");
qInfo() << "call fn1()";
fn1(p);
qInfo() << "call fn2()";
fn2(p);
qInfo() << "call fn3()";
fn3(p);
qInfo() << "call fn4()";
fn4(p);
```

运行结果如下：

>有参构造函数 1 "Apple"
>call fn1()
>拷贝构造函数 2 "Apple"
>析构函数 2 "Apple"
>call fn2()
>拷贝构造函数 3 "Apple"
>析构函数 3 "Apple"
>call fn3()
>call fn4()
>析构函数 1 "Apple"

可见，应尽量使用引用（尤其是const引用）作为函数的参数。

## 6. 对象作为函数的返回值

假设存在一个返回`Product`对象的函数，如下：

```c++
Product makeProduct(const QString &name)
{
    Product p(name);
    return p;
}
```

测试代码如下：

```c++
Product p1 = makeProduct("Apple");
const Product p2 = makeProduct("Banana");
const Product &p3 = makeProduct("Grape");
```

运行结果如下：

>有参构造函数 1 "Apple"
>有参构造函数 2 "Banana"
>有参构造函数 3 "Grape"
>析构函数 3 "Grape"
>析构函数 2 "Banana"
>析构函数 1 "Apple"

可见，三个语句都只是在函数内部调用了一次`Product`的有参构造函数。按道理前两个应该调用拷贝构造函数，但实际上并没有，这是编译器优化的结果。在前面讲拷贝构造函数时，代码`Product s5 = Product(p);`也只调用了一次拷贝构造函数，道理是一样的。详细地说，这叫做返回值优化（**RVO**或**NRVO**），即为了避免多余的对象拷贝，编译器将本应该在被调用函数内部生成的对象，直接生成到了调用者的栈上，从而减少了一次拷贝构造函数的调用，提高了效率。
