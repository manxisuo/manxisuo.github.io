---
title: "Qt中使用TCP接收报文"
date: 2022-11-18
draft: false
tags:
  - "Qt"
  - "网络编程"
  - "C++"
---

假设有一个TCP服务端，会向连接到它的TCP客户端周期（或随机）发送一个报文。报文由定长的报文头和不定长的报文体（数据部分）组成，报文体是一张图片，每个字节表示图片中一个像素的灰度值。我们的任务就是读取报文，解析图片内容，保存或显示图片。
报文头的格式如下：

```cpp
#define FLAG 0x12131415
struct Header
{
    quint32 flag;   // 报文标识
    quint32 length; // 报文长度
    quint32 width;  // 图片宽度
    quint32 height; // 图片高度
}
```

`flag`是报文标识，用来识别报文的开始；`length`是报文的总长度，通过它可以知道报文何时结束；`width`和`height`表示图片的高度和宽度，用来将报文体数据解析为图片。

首先构造一个QTcpScoket用于和服务端建立TCP连接，等待接收数据。

```cpp
QTcpSocket *socket = new QTcpSocket(this);
//socket->setReadBufferSize(BUF_SIZE);
connect(socket, SIGNAL(readyRead()), this, SLOT(slotReadData()));
```

测试发现，如果服务端一次发送的报文长度很长（例如10086字节），会被分割成多个包发送。下面是通过tcpdump命令抓包得到的：

```
14:47:27.438893 IP ...... length 1448
14:47:27.438916 IP ...... length 1448
14:47:27.438920 IP ...... length 1448
14:47:27.438922 IP ...... length 1448
14:47:27.438980 IP ...... length 1448
14:47:27.438983 IP ...... length 1448
14:47:27.438985 IP ...... length 1398
```

此例中，10068个字节被分割成7个包。在`QTcpSocket`接收到数据后，每个包会对应地发射一次`readyRead()`信号。也就是说，在槽函数中，只能读取整个报文的一部分。因此需要定义一些成员变量，来保存数据读取过程中的状态。

```cpp
private:
    QTcpSocket *mSocket;
    char mBuf[BUF_SIZE];     // 数据读取缓冲区
    qint64 mSize = 0;        // 已读取数据的长度
    Header mHeader;          // 报文头
    bool mHeadValid = false; // 报文头是否有效
```

接下来我们开始读取数据，有两种思路。

## 方式一

先读取报文头，再读取报文体，读完一个报文，再尝试读下一个。

```cpp
void Client::slotReadData()
{
    while (true)
    {
        qint64 readSize = mSocket->read(mBuf + mSize, getMaxDataSize());
        if (readSize == 0) break;

        mSize += readSize;

        // 读取头
        if (!mHeadValid && mSize >= sizeof(Header))
        {
            Header *header = (Header*)mBuf;
            if (header->flag == FLAG)
            {
                mHeadValid = true;
                mHeader = *header;
            }
        }

        // 处理完整数据
        if (mHeadValid && mSize == mHeader.length)
        {
            dealData();
            mHeadValid = false;
            mSize = 0;
        }
    }
}
```

代码的基本思路是，先尝试读取报文头，根据报文标识定位报文头。读到报文头后，即可得到报文总长度和其他信息，此时将报文头有效标识设为`true`。接下来继续读数据，当已读取的数据长度等于报文头中告知的报文总长度时，完成当前报文的读取，此时需要重置`mHeadValid`和`mSize`的值，为读取下一个报文做准备。其中`dealData()`函数用于处理报文数据，例如保存图片。

另外，代码中还有一个`getMaxDataSize()`函数，用来获取当前期望读取的数据的最大长度，定义如下：

```cpp
qint64 Client::getMaxDataSize()
{
    if (mHeadValid) return mHeader.length - mSize;
    else return sizeof(Header) - mSize;
}
```

## 方式二

先读取报文头，再读取报文体，每次读取尽量多的数据。代码如下：

```cpp
void Client::slotReadData()
{
    while (true)
    {
        qint64 readSize = mSocket->read(mBuf + mSize, getMaxDataSize());
        if (readSize == 0) break;

        mSize += readSize;

        // 读取头
        if (!mHeadValid && mSize >= sizeof(Header))
        {
            Header *header = (Header*)mBuf;
            if (header->flag == FLAG)
            {
                mHeadValid = true;
                mHeader = *header;
            }
        }

        // 处理完整数据
        if (mHeadValid && mSize == mHeader.length)
        {
            dealData();
            qint64 left = mSize - mHeader.length;
            if (left > 0) memmove(mBuf, mBuf + mHeader.length, left);
            mHeadValid = false;
            mSize = left;
        }
    }
}
```

在这种方式下，`getMaxDataSize()`函数的定义如下：

```cpp
qint64 Client::getMaxDataSize()
{
    return BUF_SIZE - mSize;
}
```

与第一种方式的区别在于，在读完一个报文时，当前报文后会存在下一个报文的开始部分。因此需要将这部分数据移到缓冲区的开始位置。也就是说，我们假定出现了两个报文的内容交叠在一个包中的情况。在两个报文间隔时间较长的情况下，是不应该出现这种情况的。那么什么情况下会出现呢？实验发现，在数据发送过快（TODO）或者网络断开一段时间后又连接导致服务端挤压的大量数据在段时间内发送出去时，会出现这种情况。实际上，方式一也能够处理这种情况。因此，这两种接收TCP报文的方式，都是可以的。

另外，经过测试发现：TCP服务端发出的报文数据，总是被拆分为大小为1448的包。但是——尤其在数据发送速度过快时——`readyRead()`信号的发射次数，以及每次发射时可以读取到的数据大小，与此并不一致。大致情况是，每次读到的数据大小倾向于是1448的整数倍，看起来是Qt底层把N个包合并在了一起。另外，槽函数的执行耗时也影响后续每次读取的数据大小。当前的槽函数耗时越长，下一个槽函数读到的数据越多。总之，你不能预测`readyRead()`什么时候发射，以及每次发射时能读取的数据有多少。

关于为什么是1448字节和关于TCP分段，可以参考这篇文章：[TCP分段 & IP分片](https://www.jianshu.com/p/01cde9f9b5a5)