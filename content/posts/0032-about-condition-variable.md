---
title: "关于条件变量（Condition Variable）"
date: 2022-09-03
draft: false
tags:
  - "多线程"
  - "系统编程"
  - "C++"
---

条件变量的特点是它需要与一个锁联合使用。

## 一. pthread中的条件变量

曾在#17 中讲过pthread中的条件变量，对应的API是`pthread_cond_xxx`形式的函数，在这里给出一个示例。如下：

```c++
#include <iostream>
#include "pthread.h"
#include "unistd.h"

pthread_mutex_t lock;
pthread_cond_t cond;

int num = 0;

void *produce_fn(void *arg)
{
    while (true)
    {
        pthread_mutex_lock(&lock);

        num += 1;
        std::cout << "produce:" << num << std::endl;

        if (num >= 10) pthread_cond_signal(&cond);

        pthread_mutex_unlock(&lock);
        usleep(300e3);
    }

    return NULL;
}

void *consume_fn(void *arg)
{
    while (true)
    {
        pthread_mutex_lock(&lock);

        while (num < 10) pthread_cond_wait(&cond, &lock);

        std::cout << "consume:" << num << std::endl;
        num = 0;

        pthread_mutex_unlock(&lock);
    }

    return NULL;
}

int main(void)
{
    pthread_mutex_init(&lock, NULL);
    pthread_cond_init(&cond, NULL);

    pthread_t t_produce, t_consume;
    pthread_create(&t_produce, NULL, produce_fn, NULL);
    pthread_create(&t_consume, NULL, consume_fn, NULL);

    pthread_join(t_produce, NULL);
    pthread_join(t_consume, NULL);

    pthread_cond_destroy(&cond);
    pthread_mutex_destroy(&lock);
}
```

## 二. Python中的条件变量

Python中的条件变量，似乎本身已经包含了锁。示例如下：

```python3
# encoding: utf-8
import threading
import time

cond = threading.Condition()
num = 0

class Producer(threading.Thread):
    def run(self):
        global num
        while True:
            cond.acquire()

            num += 1
            print(f"produce: {num}")

            if num >= 10: cond.notify()

            cond.release()
            time.sleep(0.3)

class Consumer(threading.Thread):
    def run(self):
        global num
        while True:
            cond.acquire()

            while num < 10: cond.wait()

            print(f"consume: {num}")
            num = 0

            cond.release()

if __name__ == '__main__':
    p = Producer()
    c = Consumer()
    p.start()
    c.start()
    p.join()
    c.join()
```

## 三. Java中的条件变量

Java中的条件变量，最简单的就是`Object::wait()`和`Object.notify()`。示例如下：

```java
package com.company;
import java.util.concurrent.TimeUnit;

class Resource
{
    public static int num = 0;
}

class Producer implements Runnable {
    @Override
    public void run() {
        while (true) {
            synchronized (Resource.class) {
                Resource.num += 1;
                System.out.println("produce: " + Resource.num);

                if (Resource.num >= 10) notify();
            }
            try {
                TimeUnit.MILLISECONDS.sleep(300);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}

class Consumer implements Runnable {
    @Override
    public void run() {
        while (true) {
            synchronized (Resource.class) {
                if (Resource.num < 10) {
                    try {
                        wait();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }

                System.out.println("consume: " + Resource.num);
                Resource.num = 0;
            }
        }
    }
}

public class Main {
    public static void main (String[] args) throws InterruptedException {
        Thread p = new Thread(new Producer());
        Thread c = new Thread(new Consumer());

        p.start();
        c.start();

        p.join();
        c.join();
    }
}
```