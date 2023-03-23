# -*- coding: utf-8 -*-
# @Time    : 2022/6/1 11:18
# @Author  : Daoji
# @Blog    : https://daojianime.github.io/
# @File    : main.py
# @Des     :

import pygame
from pygame.locals import *

# 初始化加载pygame模块
pygame.init()
# 定义窗口的宽度、高度为全局变量
screen_width = 1000
screen_height = 1000
# 初始化窗口
screen = pygame.display.set_mode((screen_width, screen_height))
# 设置窗口标题
pygame.display.set_caption("平台冒险游戏", "test")
# 设置窗口图标
icon = pygame.image.load("./img/games.png").convert_alpha()
icon = pygame.transform.smoothscale(icon, (64, 64))
pygame.display.set_icon(icon)

# 加载图片
sun_img = pygame.image.load("./img/sun.png").convert_alpha()
bg_img = pygame.image.load("./img/sky.png").convert_alpha()

# 定义网格大小
tile_size = 200

# 定义地图列表
world_data = [
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 2, 2, 2, 1],
]


def draw_grid():
    """
    在窗口绘制直线方格

    :return: None
    """
    for line in range(screen_width // tile_size + 1):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))


class World:
    """世界类"""

    def __init__(self, data):
        # 定义一张地图块列表
        self.tile_list = []

        # 加载泥块图片
        dirt_img = pygame.image.load('img/dirt.png').convert_alpha()
        # 加载草地块图片
        grass_img = pygame.image.load('img/grass.png').convert_alpha()

        # 遍历地图数据矩阵
        for row_index, row in enumerate(data):
            for col_index, tile in enumerate(row):
                # 如果tile为1时，将方格设为泥块
                if tile == 1:
                    # 缩放调整地图块大小，返回surface
                    img = pygame.transform.smoothscale(dirt_img, (tile_size, tile_size))
                    # 从地图块中设置一个rect对象
                    img_rect = img.get_rect(x=col_index * tile_size, y=row_index * tile_size)
                    # 添加到地图块列表
                    self.tile_list.append((img, img_rect))
                # 如果tile为2时，将方格设为草块
                elif tile == 2:
                    img = pygame.transform.smoothscale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect(x=col_index * tile_size, y=row_index * tile_size)
                    self.tile_list.append((img, img_rect))

    def draw(self):
        for tile, tile_rect in self.tile_list:
            screen.blit(tile, tile_rect)


# 初始化一个世界类对象
world = World(world_data)

# 定义游戏总开关为全局变量run
run = True
while run:
    # # TODO(Daoji) 2022/6/1 ps1：地图我要设置很多草地、滑块，我只需要把窗口划分成网格，我只要设置一个网格时草地块还是泥块就好了。

    # 绘制背景图到窗口
    screen.blit(bg_img, (0, 0))
    screen.blit(sun_img, (100, 100,))

    world.draw()
    draw_grid()

    for event in pygame.event.get():
        # 监听事件
        if event.type == pygame.QUIT:  # 当点击X按钮时
            run = False  # 退出循环

    # 刷新屏幕
    pygame.display.update()

# 卸载pygame模块
pygame.quit()
# TODO(Daoji) 2022/6/1 1.创建游戏基本框架
