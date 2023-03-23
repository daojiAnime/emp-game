# -*- coding: utf-8 -*-
# @Time    : 2022/7/22 9:32
# @Author  : Daoji
# @Blog    : https://daojianime.github.io/
# @File    : net.py
# @Des     :

import socket
import threading

addr_set = set()
is_server = True
position = ''
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr = ("", 8080)
s.bind(addr)
reload = False


# 接收消息
def recv_msg(udp_socket):
    global position, reload
    while True:
        data = udp_socket.recvfrom(2048)  # 接收数据最大为（1024 字节）
        addr_set.add(data[1])  # 保存客户端IP
        # print(f"已接收：{data[1]}" + data[0].decode("utf8"))
        if is_server:
            for address in addr_set:
                if address != data[1]:
                    send_msg(address, data[0].decode("utf8"))
        else:
            if data[0].decode("utf8") != "reload":
                position = data[0].decode("utf8")
            else:
                reload = True

        if reload:
            for address in addr_set:
                send_msg(address, "reload")


# 发送消息
def send_msg(address, data):
    s.sendto(data.encode('utf8'), address)


# 开启客户端
def start_client():
    global is_server
    is_server = False
    # 后台接收数据
    t = threading.Thread(target=recv_msg, args=(s,))
    t.start()


# 开启服务端
def start_server():
    global is_server
    is_server = True
    # 后台接收数据
    t = threading.Thread(target=recv_msg, args=(s,))
    t.start()


if __name__ == '__main__':
    start_server()
