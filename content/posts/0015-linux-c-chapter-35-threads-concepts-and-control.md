---
title: "《Linux C》第35章：线程：概念和控制"
date: 2017-02-11
draft: false
tags:
  - "Linux"
  - "C"
  - "多线程"
  - "系统编程"
---

## 1. 线程的概念

我们知道，进程在各自独立的地址空间中运行，进程之间共享数据需要通过进程间通信（IPC）机制。有些情况下，需要在一个进程中同时执行多个控制流程，此时线程就派上用场了。

main函数和信号处理函数是在同一个进程的地址空间中的多个控制流程，多线程也是如此。但是线程比信号处理函数更灵活，信号处理函数的控制流程只是在信号抵达时产生，在处理完信号之后就结束了。而多线程的控制流程是可以长期并存的，操作系统在各线程之间调度和切换，就像在多个进程之间调度和切换一样。

由于同一进程的多个线程共享一个地址空间，因此Text段、Data段都是共享的。如果定义一个函数，在各线程中都可以调用；如果定义一个全局变量，在各线程中都可以访问。除此之外，各线程还共享以下进程资源和环境：

- 文件描述符表
- 每种信号的处理方式（`SIG_IGN`、`SIG_DFL`或自定义的信号处理函数）
- 当前工作目录
- 用户id和组id

但是有些资源却是每个线程各有一份的：

- 线程id
- 上下文，包括各种寄存器的值、程序计数器和栈指针
- 栈空间
- `errno`变量
- 信号屏蔽字
- 调度优先级

## 2. 线程控制

### 2.1. 创建线程

```c
#include <pthread.h>

int pthread_create(pthread_t *restrict thread,
        const pthread_attr_t *restrict attr,
        void *(*start_routine)(void*),
        void *restrict arg);
```

返回值：成功返回0，失败返回错误号。

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>

void *thr_fn(void *arg)
{
  fprintf(stdout, "Child thread\n");
  return NULL;
}

int main(void)
{
  pthread_t tid;
  int err = pthread_create(&tid, NULL, thr_fn, NULL);
  if (err != 0) {
    fprintf(stderr, "can't create thread: %s\n", strerror(err));
    exit(1);
  }
  fprintf(stdout, "Parent thread\n");
  sleep(1);
  return 0;
}
```

结果：

```shell
Parent thread
Child thread
```

### 2.2. 终止线程

如果需要只终止某个线程而不终止整个进程，可以有三种方法：

- 从线程函数return。这种方法对主线程不适用，从main函数return相当于调用`exit`。
- 线程可以调用`pthread_cancel`终止同一进程中的另一个线程。
- 线程可以调用`pthread_exit`终止自己。

用pthread_cancel终止一个线程分同步和异步两种情况，比较复杂，暂不讨论。下面看一下`pthread_exit`和`pthread_join`的用法。

```c
#include <pthread.h>

void pthread_exit(void *value_ptr);
```

`value_ptr`和线程的返回值的用法一样，其他线程可以调用`pthread_join`获得这个指针。

需要注意，`pthread_exit`或者`return`返回的指针所指向的内存单元必须是全局的或者是用`malloc`分配的，不能在线程函数的栈上分配，因为当其他线程得到这个返回指针时线程函数已经退出了。

```c
#include <pthread.h>

int pthread_join(pthread_t thread, void **value_ptr);
```

返回值：成功返回0，失败返回错误号。

调用该函数的线程将挂起等待，直到id为thread的线程终止。thread线程以不同的方法终止，通过`pthread_join`得到的终止状态是不同的，总结如下：

- 如果thread线程通过return返回，`value_ptr`所指向的单元里存放的是thread线程函数的返回值。
- 如果thread线程被别的线程调用`pthread_cancel`异常终止掉，`value_ptr`所指向的单元里存放的是常数`PTHREAD_CANCELED`。
- 如果thread线程是自己调用`pthread_exit`终止的，`value_ptr`所指向的单元存放的是传给`pthread_exit`的参数。

如果对thread线程的终止状态不感兴趣，可以传NULL给`value_ptr`参数。

在Linux的pthread库中常数`PTHREAD_CANCELED`的值是-1。可以在头文件pthread.h中找到它的定义：

```c
#define PTHREAD_CANCELED ((void *) -1)
```

一般情况下，线程终止后，其终止状态一直保留到其他线程调用`pthread_join`获取它的状态为止。但是线程也可以被置为detach状态，这样的线程一旦终止就立刻回收它占用的所有资源，而不保留终止状态。不能对一个已经处于detach状态的线程调用`pthread_join`，这样的调用将返回`EINVAL`。对一个尚未detach的线程调用`pthread_join`或`pthread_detach`都可以把该线程置为detach状态，也就是说，不能对同一线程调用两次`pthread_join`，或者如果已经对一个线程调用了`pthread_detach`就不能再调用`pthread_join`了。
