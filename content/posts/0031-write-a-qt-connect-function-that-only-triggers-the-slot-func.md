---
title: "写一个只触发一次槽函数的Qt connect函数"
date: 2022-09-03
draft: false
tags:
  - "Qt"
  - "C++"
  - "GUI"
---

在之前的Qt项目中，我发现经常会用到槽函数只需要执行一次的情况。也就是说，槽函数执行一次后，就需要disconnect对应的连接。然而，真正操作起来实际上挺麻烦的，或者说不优雅。因为你需要把之前connect时产生的`QMetaObject::Connection`对象保存起来，而保存它不能用局部变量，通常需要保存到类的成员变量中，或者其他生命周期足够长的地方，以防止在disconnect它的时候，它已经失效了。总之，需要使用者自己维护，因而增加了使用者的负担。

如果有一个方法能够在槽函数执行完成后自动disconnect掉连接就好了。我在网上找了一段时间，却没有找到合适的解决方案，相关讨论也比较少，可能这不是一个很常见的需求吧。不过还是在GitHub上找到了一个相关的库：<https://github.com/misje/once>，但是看它的源码，感觉比较复杂。它针对`QObject::connect`函数的每种情况，写了对应的实现，总感觉太复杂了，应该存在一种更通用的方法。

最近在阅读了《C++ Primer》模板相关的章节后，我突然想到也许用完美转发相关的东西可以简化实现。于是试着写了一下，貌似真得可以，代码如下：

ConnectionUtil.h：

```c++
#pragma once

#include <QObject>
#include <functional>

namespace ConnectionUtil
{
    typedef QMetaObject::Connection Conn;

    class ReceiverObj : public QObject
    {
        Q_OBJECT

    public:
        explicit ReceiverObj(Conn *conn1, Conn *conn2) : mConn1(conn1), mConn2(conn2)  {}

    public slots:
        void slot()
        {
            QObject::disconnect(*mConn1);
            QObject::disconnect(*mConn2);
            delete mConn1;
            delete mConn2;
            deleteLater();
        }

    private:
        Conn *mConn1, *mConn2;
    };

    // 处理信号为SIGNAL(...)的情况
    template <typename Sender, typename ...Args>
    void connectOnce(Sender &&sender, const char *signal, Args &&...args)
    {
        Conn *conn1 = new Conn;
        Conn *conn2 = new Conn;
        *conn1 = QObject::connect(std::forward<Sender>(sender), signal, std::forward<Args>(args)...);
        *conn2 = QObject::connect(std::forward<Sender>(sender), signal, new ReceiverObj(conn1, conn2), SLOT(slot()));
    }

    // 处理其他情况
    template <typename Sender, typename Signal, typename ...Args>
    void connectOnce(Sender &&sender, Signal &&signal, Args &&...args)
    {
        Conn *conn1 = new Conn;
        Conn *conn2 = new Conn;
        *conn1 = QObject::connect(std::forward<Sender>(sender), std::forward<Signal>(signal), std::forward<Args>(args)...);
        *conn2 = QObject::connect(std::forward<Sender>(sender), std::forward<Signal>(signal), std::bind(&ReceiverObj::slot, new ReceiverObj(conn1, conn2)));
    }
}
```

这个实现假定`QObject::connect`的所有重载函数前两个参数分别是Sender和Signal，事实上确实是这样。关键点就是，额外建立一个连接，在收到信号后，disconnect用户的连接。不过，我总感觉这个实现在多线程的情况下可能有bug，但在经过简单的测试后，暂时没有发现。使用示例如下：

```c++
ConnectionUtil::connectOnce(this, SIGNAL(bong(int)), obj, SLOT(slotBong(int)), Qt::QueuedConnection);

ConnectionUtil::connectOnce(this, &MainWindow::bong, obj, &SomeObject::slotBong, Qt::QueuedConnection);

ConnectionUtil::connectOnce(this, &MainWindow::bong, this, []() {
    qDebug() << "bingo";
});
```

请大家批评指正。