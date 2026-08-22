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
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/select.h>
#include <sys/socket.h>

constexpr int SERVER_PORT = 10001;
constexpr int BUF_SIZE = 1024;

int main()
{
    // 1. 创建监听 socket
    int listenFd = socket(AF_INET, SOCK_STREAM, 0);
    if (listenFd < 0) {
        perror("socket");
        return 1;
    }

    // 2. 绑定地址并开始监听
    sockaddr_in serverAddr{};
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(SERVER_PORT);
    serverAddr.sin_addr.s_addr = htonl(INADDR_ANY);

    if (bind(listenFd,
             reinterpret_cast<sockaddr *>(&serverAddr),
             sizeof(serverAddr)) < 0) {
        perror("bind");
        close(listenFd);
        return 1;
    }

    if (listen(listenFd, 10) < 0) {
        perror("listen");
        close(listenFd);
        return 1;
    }

    printf("server is listening on port %d\n", SERVER_PORT);

    // masterSet 保存所有需要监听的 fd。
    // select() 会修改传入的 fd_set，所以每次循环都要复制一份。
    fd_set masterSet;
    FD_ZERO(&masterSet);
    FD_SET(listenFd, &masterSet);

    int maxFd = listenFd;
    char buffer[BUF_SIZE];

    for (;;) {
        fd_set readSet = masterSet;

        // 阻塞，直到至少有一个 fd 可读
        int ready = select(maxFd + 1, &readSet, nullptr, nullptr, nullptr);
        if (ready < 0) {
            perror("select");
            break;
        }

        // 监听 fd 可读，表示有新的客户端连接到来
        if (FD_ISSET(listenFd, &readSet)) {
            int clientFd = accept(listenFd, nullptr, nullptr);
            if (clientFd >= 0) {
                FD_SET(clientFd, &masterSet);
                if (clientFd > maxFd)
                    maxFd = clientFd;

                printf("client %d connected\n", clientFd);
            }
        }

        // 检查已有客户端 fd 是否有数据可读
        for (int fd = 0; fd <= maxFd; ++fd) {
            if (fd == listenFd || !FD_ISSET(fd, &readSet))
                continue;

            int n = read(fd, buffer, sizeof(buffer));

            if (n == 0) {
                // read 返回 0，表示客户端关闭了连接
                close(fd);
                FD_CLR(fd, &masterSet);
                printf("client %d disconnected\n", fd);
                continue;
            }

            if (n < 0)
                continue;

            // 简单 echo：把收到的数据发回客户端。
            // 这里按字节数输出，不把网络数据当作 C 字符串。
            write(fd, buffer, n);

            printf("client %d says: %.*s\n", fd, n, buffer);
        }
    }

    close(listenFd);
    return 0;
}
```
