---
title: "IO多路复用：epoll"
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
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/epoll.h>

#define BUF_SIZE 1024
#define EVENTS_SIZE 64
#define SERVER_PORT 10001

void epollCtl(int epfd, int fd, int op, uint32_t events)
{
    struct epoll_event event;
    event.data.fd = fd;
    event.events = events;
    epoll_ctl(epfd, op, fd, &event);
}

int main(void)
{
    char buf[BUF_SIZE];  // 缓冲区

    // 新建Socket
    int listenFd = socket(AF_INET, SOCK_STREAM, 0);

    // 设置服务器地址
    struct sockaddr_in serverAddr;
    memset(&serverAddr, 0, sizeof(serverAddr));
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(SERVER_PORT);
    //serverAddr.sin_addr.s_addr = htonl(INADDR_ANY);
    serverAddr.sin_addr.s_addr = inet_addr("0.0.0");

    // 将Socket绑定到上述地址
    bind(listenFd, (struct sockaddr*)&serverAddr, sizeof(serverAddr));   
    listen(listenFd, 100);  // 开始接受连接

    int epfd = epoll_create(256);
    epollCtl(epfd, listenFd, EPOLL_CTL_ADD, EPOLLIN | EPOLLET);

    // 保存epoll_wait返回的触发的事件
    struct epoll_event events[EVENTS_SIZE];

    for (;;)
    {
        int nfds = epoll_wait(epfd, events, EVENTS_SIZE, -1);
        int sockFd;

        for (int i = 0; i < nfds; i++)
        {
            sockFd = events[i].data.fd;
            if (listenFd == sockFd)  // 客户端新建连接
            {
                struct sockaddr_in clientAddr;
                socklen_t clientLen = sizeof (clientAddr);
                int connFd = accept(listenFd, (struct sockaddr*)&clientAddr, &clientLen);
                epollCtl(epfd, connFd, EPOLL_CTL_ADD, EPOLLIN | EPOLLET);
                printf("Socket %d created\n", connFd);
                fflush(stdout);
            }
            else if (events[i].events & EPOLLIN)  // 客户端可读（包括关闭）
            {
                if (sockFd < 0) continue;
                int n = recv(sockFd, buf, BUF_SIZE, 0);
                if (n <= 0)
                {
                    close(sockFd);
                    events[i].data.fd = -1;
                    printf("Socket %d closed\n", sockFd);
                    fflush(stdout);
                }
                else
                {
                    buf[n] = '\0';
                    epollCtl(epfd, sockFd, EPOLL_CTL_MOD, EPOLLOUT | EPOLLET);
                    printf("Socket %d said : %s\n", sockFd, buf);
                    fflush(stdout);
                }
            }
            else if (events[i].events & EPOLLOUT)  // 客户端可写
            {
                send(sockFd, "Hello!\n", 8, 0);
                epollCtl(epfd, sockFd, EPOLL_CTL_MOD, EPOLLIN | EPOLLET);
            }
            else
            {
                printf("This is not avaible!");
            }
        }
    }

    return 0;
}
```