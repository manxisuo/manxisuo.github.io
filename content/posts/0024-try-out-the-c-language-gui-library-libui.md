---
title: "试用C语言GUI库：libui"
date: 2018-11-22
draft: false
tags:
  - "C"
  - "GUI"
  - "编程语言"
---

libui是一个简单易用的C语言GUI库。

# 1. 编译libui

(1) 从官网下载libui的源码

下载地址：<https://github.com/andlabs/libui>

(2) 根据README的说明进行构建

```bash
$ # you must be in the top-level libui directory, otherwise this won't work
$ mkdir build
$ cd build
$ cmake ..
$ make
$ make tester         # for the test program
$ make examples       # for examples
```

执行cmake时报错，相关信息如下：

```text
-- No package 'gtk+-3.0' found
CMake Error at /usr/share/cmake-3.5/Modules/FindPkgConfig.cmake:367 (message):
A required package was not found
Call Stack (most recent call first):
/usr/share/cmake-3.5/Modules/FindPkgConfig.cmake:532 (_pkg_check_modules_internal)
unix/CMakeLists.txt:4 (pkg_check_modules)
```

解决方法为安装libgtk，即：

```bash
sudo apt-get install libgtk-3-dev
```

编译完成后，生成的共享库位于`build/out`目录。

```text
libui.so
libui.so.0
```

# 2. 编写测试代码

代码如下：

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ui.h>

int onClosing(uiWindow *w, void *data)
{
    uiQuit();
    return 1;
}

void onClicked(uiButton *b, void *data)
{
    char msg[32] = "Button is clicked!";
    uiLabelSetText(uiLabel(data), msg);
    puts(msg);
}

int main(void)
{
    uiInitOptions o;
    const char *err;
    uiWindow *w;
    uiGrid *g;
    uiLabel *l;
    uiButton *b;

    memset(&o, 0, sizeof(uiInitOptions));
    err = uiInit(&o);
    if (err != NULL) {
        puts(err);
        uiFreeInitError(err);
        return 1;
    }

    // 创建Window
    w = uiNewWindow("libui测试", 320, 240, 0);
    uiWindowSetMargined(w, 1);

    // 创建Grid
    g = uiNewGrid();
    uiGridSetPadded(g, 1);
    uiWindowSetChild(w, uiControl(g));

    // 创建Label
    l = uiNewLabel("I am a label.");
    uiGridAppend(g, uiControl(l),
        0, 2, 2, 1,
        1, uiAlignCenter, 1, uiAlignFill);

    // 创建Button，注册按钮点击时的回调函数
    b = uiNewButton("Click me!");
    uiButtonOnClicked(b, onClicked, l);
    uiGridAppend(g, uiControl(b),
        0, 2, 2, 1,
        1, uiAlignCenter, 1, uiAlignEnd);

    // 注册窗口关闭时的回调函数
    uiWindowOnClosing(w, onClosing, NULL);

    // 显示窗口
    uiControlShow(uiControl(w));

    // 启动主循环
    uiMain();

    return 0;
}
```

编译、运行：

```bash
# 注意将libui.so加入共享库搜索路径
gcc main.c -l ui -L . -I ~/dev/C/libui-master -o main
./main
```

效果如下：

![libui测试](https://user-images.githubusercontent.com/3950285/48910793-d0851100-eeab-11e8-8198-09f0ebeffcca.png)
