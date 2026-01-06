---
title: "IO多路复用：poll"
date: 2022-08-27
draft: false
tags:
  - "系统编程"
  - "IO"
  - "Linux"
---

```c++
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <netinet/in.h>
#include <sys/poll.h>

#define BUF_SIZE 1024
#define OPEN_MAX 1024
#define SERVER_PORT 10001
#define INFTIM -1

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

    struct pollfd fds[OPEN_MAX];
    fds[0].fd = listenFd;
    fds[0].events = POLLRDNORM;

    for (int i = 1; i < OPEN_MAX; i++) fds[i].fd = -1;

    int maxIndex = 0;

    for (;;)
    {
        int nready = poll(fds, maxIndex + 1, INFTIM);

        if (fds[0].revents & POLLRDNORM)
        {
            // 获取客户端连接生成的Socket
            struct sockaddr_in clientAddr;
            socklen_t clientLen = sizeof (clientAddr);
            int connFd = accept(listenFd, (struct sockaddr*)&clientAddr, &clientLen);

            printf("Socket %d created\n", connFd);
            fflush(stdout);

            int i;
            for (i = 1; i < OPEN_MAX; i++)
            {
                if (fds[i].fd < 0)
                {
                    fds[i].fd = connFd;
                    fds[i].events = POLLRDNORM;
                    break;
                }
            }

            if (i == OPEN_MAX)
            {
                printf("too many clients!\n");
            }

            if (i > maxIndex) maxIndex = i;

            nready -= 1;
            if (nready <= 0) continue;
        }

        for (int i = 1; i <= maxIndex; i++)
        {
            if (fds[i].fd < 0) continue;
            int sockFd = fds[i].fd;
            if (fds[i].revents & (POLLRDNORM | POLLERR))
            {
                int n = read(sockFd, buf, BUF_SIZE);
                if (n == 0)
                {
                    close(sockFd);
                    fds[i].fd = -1;
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