---
title: "《Linux C》第35章：线程：同步"
date: 2017-02-11
draft: false
tags:
  - "Linux"
  - "C"
  - "多线程"
  - "系统编程"
---

# 3. 线程间同步

## 3.1. Mutex（互斥锁）

对于多线程的程序，访问冲突的问题是很普遍的，解决的办法是引入互斥锁（Mutex，Mutual Exclusive Lock），获得锁的线程可以完成“读-修改-写”的操作，然后释放锁给其他线程，没有获得锁的线程只能等待而不能访问共享数据，这样“读-修改-写”三步操作组成一个原子操作，要么都执行，要么都不执行，不会执行到中间被打断，也不会在其他处理器上并行做这个操作。

Mutex用`pthread_mutex_t`类型的变量表示，可以这样初始化和销毁：

```c
#include <pthread.h>

int pthread_mutex_destroy(pthread_mutex_t *mutex);
int pthread_mutex_init(pthread_mutex_t *mutex,
        const pthread_mutexattr_t *restrict attr);
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
```

返回值：成功返回0，失败返回错误号。

如果Mutex变量是静态分配的（全局变量或static变量），也可以用宏定义`PTHREAD_MUTEX_INITIALIZER`来初始化，相当于用`pthread_mutex_init`初始化并且`attr`参数为`NULL`。Mutex的加锁和解锁操作可以用下列函数：

```c
#include <pthread.h>

int pthread_mutex_lock(pthread_mutex_t *mutex);
int pthread_mutex_trylock(pthread_mutex_t *mutex);
int pthread_mutex_unlock(pthread_mutex_t *mutex);
```

返回值：成功返回0，失败返回错误号。

一个线程可以调用`pthread_mutex_lock`获得Mutex，如果这时另一个线程已经调用`pthread_mutex_lock`获得了该Mutex，则当前线程需要挂起等待，直到另一个线程调用`pthread_mutex_unlock`释放Mutex，当前线程被唤醒，才能获得该Mutex并继续执行。

如果一个线程既想获得锁，又不想挂起等待，可以调用`pthread_mutex_trylock`，如果Mutex已经被另一个线程获得，这个函数会失败返回`EBUSY`，而不会使线程挂起等待。

“挂起等待”和“唤醒等待线程”的操作如何实现？每个Mutex有一个等待队列，一个线程要在Mutex上挂起等待，首先在把自己加入等待队列中，然后置线程状态为睡眠，然后调用调度器函数切换到别的线程。一个线程要唤醒等待队列中的其他线程，只需从等待队列中取出一项，把它的状态从睡眠改为就绪，加入就绪队列，那么下次调度器函数执行时就有可能切换到被唤醒的线程。

## 3.2. Condition Variable（条件变量）

线程间的同步还有这样一种情况：线程A需要等某个条件成立才能继续往下执行，现在这个条件不成立，线程A就阻塞等待，而线程B在执行过程中使这个条件成立了，就唤醒线程A继续执行。在pthread库中通过条件变量（Condition Variable）来阻塞等待一个条件，或者唤醒等待这个条件的线程。条件变量用`pthread_cond_t`类型的变量表示，可以这样初始化和销毁：

```c
#include <pthread.h>

int pthread_cond_destroy(pthread_cond_t *cond);
int pthread_cond_init(pthread_cond_t *restrict cond,
        const pthread_condattr_t *restrict attr);
pthread_cond_t cond = PTHREAD_COND_INITIALIZER;
```

返回值：成功返回0，失败返回错误号。

和Mutex的初始化和销毁类似，pthread_cond_init函数初始化一个Condition Variable，attr参数为NULL则表示缺省属性，pthread_cond_destroy函数销毁一个Condition Variable。如果Condition Variable是静态分配的，也可以用宏定义PTHEAD_COND_INITIALIZER初始化，相当于用pthread_cond_init函数初始化并且attr参数为NULL。Condition Variable的操作可以用下列函数：

```c
#include <pthread.h>

int pthread_cond_timedwait(pthread_cond_t *restrict cond,
        pthread_mutex_t *restrict mutex,
        const struct timespec *restrict abstime);
int pthread_cond_wait(pthread_cond_t *restrict cond,
        pthread_mutex_t *restrict mutex);
int pthread_cond_broadcast(pthread_cond_t *cond);
int pthread_cond_signal(pthread_cond_t *cond);
```

返回值：成功返回0，失败返回错误号。

可见，一个条件变量总是和一个Mutex搭配使用的。一个线程可以调用`pthread_cond_wait`在一个条件变量上阻塞等待，这个函数做以下三步操作：

1. 释放Mutex
2. 阻塞等待
3. 当被唤醒时，重新获得Mutex并返回

`pthread_cond_timedwait`函数还有一个额外的参数可以设定等待超时，如果到达了`abstime`所指定的时刻仍然没有别的线程来唤醒当前线程，就返回`ETIMEDOUT`。一个线程可以调用`pthread_cond_signal`唤醒在某个条件变量上等待的另一个线程，也可以调用`pthread_cond_broadcast`唤醒在这个条件变量上等待的所有线程。

## 3.3. Semaphore（信号量）

Mutex变量是非0即1的，可看作一种资源的可用数量，初始化时Mutex是1，表示有一个可用资源，加锁时获得该资源，将Mutex减到0，表示不再有可用资源，解锁时释放该资源，将Mutex重新加到1，表示又有了一个可用资源。

信号量和Mutex类似，表示可用资源的数量，和Mutex不同的是这个数量可以大于1。

以下介绍的是POSIX semaphore库函数，详见sem_overview(7)，这种信号量不仅可用于同一进程的线程间同步，也可用于不同进程间的同步。

```c
#include <semaphore.h>

int sem_init(sem_t *sem, int pshared, unsigned int value);
int sem_wait(sem_t *sem);
int sem_trywait(sem_t *sem);
int sem_post(sem_t * sem);
int sem_destroy(sem_t * sem);
```

semaphore变量的类型为sem_t，sem_init()初始化一个semaphore变量，value参数表示可用资源的数量，pshared参数为0表示信号量用于同一进程的线程间同步。在用完semaphore变量之后应该调用sem_destroy()释放与semaphore相关的资源。

调用sem_wait()可以获得资源，使semaphore的值减1，如果调用sem_wait()时semaphore的值已经是0，则挂起等待。如果不希望挂起等待，可以调用sem_trywait()。调用sem_post()可以释放资源，使semaphore的值加1，同时唤醒挂起等待的线程。

## 3.4. 其他线程间同步机制

如果共享数据是只读的，那么各线程读到的数据应该总是一致的，不会出现访问冲突。只要有一个线程可以改写数据，就必须考虑线程间同步的问题。由此引出了读写锁（Read-Write Lock）的概念，Reader之间并不互斥，可以同时读共享数据，而Writer是独占的（exclusive），在Writer修改数据时其他Reader或Writer不能访问数据，可见Reader-Writer Lock比Mutex具有更好的并发性。

用挂起等待的方式解决访问冲突不见得是最好的办法，因为这样毕竟会影响系统的并发性，在某些情况下解决访问冲突的问题可以尽量避免挂起某个线程，例如Linux内核的Seqlock、RCU（read-copy-update）等机制。
