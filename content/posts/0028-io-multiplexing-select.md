---
title: "IO多路复用：select"
date: 2022-08-27
draft: false
tags:
  - "系统编程"
  - "IO"
  - "Linux"
---

注：为了方便管理socket，使用了`std::set`数据结构。

```c++
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <sys/select.h>
#include <set>

#define BUF_SIZE 1024
#define SERVER_PORT 10001

int main(int argc, char *argv[])
{
    char buf[BUF_SIZE];  // 缓冲区

    // 新建Socket
    // AF_INET：IP协议族
    int listenFd = socket(AF_INET, SOCK_STREAM, 0);

    // 设置服务器地址
    struct sockaddr_in serverAddr;
    memset(&serverAddr, 0, sizeof(serverAddr));
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(SERVER_PORT);
    serverAddr.sin_addr.s_addr = htonl(INADDR_ANY);

    // 将Socket绑定到上述地址
    bind(listenFd, (struct sockaddr*)&serverAddr, sizeof(serverAddr));   
    listen(listenFd, 100);  // 开始接受连接

    // 用于保存客户端连接生成的Socket的fd
    std::set<int> clientFds;

    int maxFd = listenFd;  // 表示当前所有fd的最大值

    fd_set allSet;  // 用于保存当前所有fd
    FD_ZERO(&allSet);
    FD_SET(listenFd, &allSet);

    for (;;)
    {
        fd_set readSet = allSet;  // 用来传给内核的fd_set，之所以拷贝一份是因为内核会修改它
        int nready = select(maxFd + 1, &readSet, NULL, NULL, NULL);

        // 检查是否有客户端新建连接
        if (FD_ISSET(listenFd, &readSet))
        {
            // 获取客户端连接生成的Socket
            struct sockaddr_in clientAddr;
            socklen_t clientLen = sizeof (clientAddr);
            int connFd = accept(listenFd, (struct sockaddr*)&clientAddr, &clientLen);

            printf("Socket %d created\n", connFd);
            fflush(stdout);

            // 将客户端连接生成的Socket的fd保存起来
            clientFds.insert(connFd);

            // 将客户端连接生成的Socket的fd加入select中
            FD_SET(connFd, &allSet);

            if (connFd > maxFd) maxFd = connFd;

            nready -= 1;
            if (nready <= 0) continue;
        }

        // 检查是否存在客户端Socket有数据需要读
        for (int sockFd : clientFds)
        {
            if (FD_ISSET(sockFd, &readSet))
            {
                int n = read(sockFd, buf, BUF_SIZE);
                if (n == 0)
                {
                    close(sockFd);  // 关闭fd
                    FD_CLR(sockFd, &allSet);
                    clientFds.erase(sockFd);
                    printf("Socket %d closed\n", sockFd);
                    fflush(stdout);
                }
                else
                {
                    buf[n] = '\0';
                    write(sockFd, buf, n);
                    printf("Socket %d said : %s\n", sockFd, buf);
                    fflush(stdout);
                }
                nready -= 1;
                if (nready <= 0) break;
            }
        }
    }

    return 0;
}
```