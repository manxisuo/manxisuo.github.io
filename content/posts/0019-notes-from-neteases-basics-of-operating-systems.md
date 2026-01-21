---
title: "网易《操作系统之基础》笔记"
date: 2017-08-20
draft: false
tags:
  - "操作系统"
  - "学习笔记"
---

## 一. 操作系统概述

### L1. 什么是操作系统

操作系统是计算机硬件与应用之间的一层软件，它方便我们使用并高效地使用硬件。它的硬件管理功能包括：

- CPU管理
- 内存管理
- 终端管理
- 磁盘管理
- 文件管理
- 网络管理
- 电源管理
- 多核管理

学习操作系统的3个层次：

1. 从应用程序出发探到操作系统
    - 使用操作系统的接口
    - 显示器(printf)、CPU(fork)、文件(open、read)等
2. 从应用程序出发进入操作系统
    - 一段文字是如何写到磁盘上的
3. 从硬件出发设计并实现操作系统
    - 给一个板子，能够配出操作系统

## 二. 操作系统引导

### L2. 揭开操作系统的面纱

图灵机模拟人在白纸上读写和思考的过程，是一种可以完成特定任务的抽象机器。将任务的步骤作为数据输入给图灵机，图灵机可以根据不同的步骤完成不同的任务，这样就得到了通用图灵机。计算机就是通用图灵机的一种具体实现。

冯诺依曼提出了**存储程序**思想，即将程序和数据保存到内存中，计算机在在程序的控制下一步步进行处理。

计算机的五大组成部件：输入设备、输出设备、存储器、运算器和控制器。

计算机工作的过程简单说就是“取址执行”。

计算机刚打开时，IP是什么？

对于X86 PC，开机时CPU处于实模式，此模式下CPU寻址空间为1MB。此时`CS=0xFFFF`，`IP=0x0000`，物理地址为`0xFFFF0`，即ROM BIOS映射区的起始地址，于是进入BIOS中。

BIOS负责RAM、键盘、显示器、软硬盘等，并将磁盘的0磁道0扇区（即引导扇区）处的512个字节读到`0x7C00`处，并设置`CS=0x07C0`，`IP=0x0000`。于是接下来开始执行引导扇区的512KB的代码。

引导扇区存放着开机后第一段我们可以控制的代码，即**bootsect.s**。

```as
// BOOTSEG  = 0x07c0
// INITSEG  = 0x9000
// SETUPSEG = 0x9020

start:
    mov ax, #BOOTSEG
    mov ds, ax          // ds = 0x07c0
    mov ax, #INITSEG
    mov es, ax          // ds = 0x9000
    mov cx, #256
    sub si, si
    sub di, di
    rep movw

// 以上代码，将`0x7C00`处的256个字移动到`0x90000`处，即将bootsect.s移动到了`0x90000`处。

    jmpi go, INITSEG // 实际就是跳到go，不过是移动后的go处
    // 执行完毕后，CS=INITSEG, ip=go

go:
    mov ax, cs // cs = 0x9000
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov sp, #0xff00

load_setup:
    mov dx, #0x0000
    mov cx, #0x0002
    mov bx, #0x0200
    mov ax, #0x0200+SETUPLEN // SETUPLEN = 4
    int 0x13 // BIOS读磁盘扇区终端

// 以上代码，将磁盘第2、3、4、5共四个扇区(即setup)的内容，读到90200处，即紧挨着引导程序的位置。  

    jnc ok_load_setup
    mov dx, #0x0000
    mov ax, #0x0000 // 复位
    int 0x13
    j   load_setup // 重读

ok_load_setup:
    
    // 略去在屏幕上显示Loading...

    mov ax, #SYSSEG // SYSSEG = 0x1000
    mov es, ax
    call read_it // 读入system模块
    jmpi 0, SETUPSEG // 转入90200，执行setup.s

read_it:
    mov ax, es
    cmp ax, #ENDSEG
    jb ok1_read
    ret

ok1_read:
    mov ax, sectors
    sub ax, sread
    call read_track // 读磁道...
```

在引导扇区的末尾，BIOS用以识别引导扇区：
```as
.org 510
    .word 0xAA55 // 扇区的最后两个字节
```

总结：boot的工作包括读setup、打印启动画面、读system，然后将执行权交给setup。

### L3. 操作系统启动

setup.s用以完成OS启动前的设置。
