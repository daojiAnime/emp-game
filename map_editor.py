# -*- coding: utf-8 -*-
# @Time    : 2022/7/21 9:05
# @Author  : Daoji
# @Blog    : https://daojianime.github.io/
# @File    : map_editor.py
# @Des     :
import pickle
from os import path

import pygame

pygame.init()

tile_size = 40
cols = 20  # 列数
rows = 20  # 行数
height_margin = 100
width_margin = 300
screen_width = tile_size * cols
screen_height = tile_size * rows
screen_size = (screen_width + width_margin, screen_height + height_margin)

screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("地图编辑器")
# 加载背景图片
sky_img = pygame.image.load("img/sky.png").convert_alpha()
sky_img = pygame.transform.smoothscale(sky_img, (screen_width, screen_height))
sun_img = pygame.image.load("img/sun.png").convert_alpha()
icon_img = pygame.image.load("img/games.png").convert_alpha()
# 加载按钮图片
save_img = pygame.image.load("img/save_btn.png").convert_alpha()
load_img = pygame.image.load("img/load_btn.png").convert_alpha()
dirt_img = pygame.image.load("img/dirt.png").convert_alpha()
dirt_img = pygame.transform.smoothscale(dirt_img, (tile_size, tile_size))
grass_img = pygame.image.load("img/grass.png").convert_alpha()
grass_img = pygame.transform.smoothscale(grass_img, (tile_size, tile_size))
blob_img = pygame.image.load("img/blob.png").convert_alpha()
blob_img = pygame.transform.smoothscale(blob_img, (blob_img.get_width() * 0.8, blob_img.get_height() * 0.8))
lava_img = pygame.image.load("img/lava.png").convert_alpha()
lava_img = pygame.transform.smoothscale(lava_img, (tile_size, tile_size // 2))

exit_img = pygame.image.load("img/exit.png").convert_alpha()
exit_img = pygame.transform.smoothscale(exit_img, (tile_size, tile_size * 1.5))
coin_img = pygame.image.load("img/coin.png").convert_alpha()
coin_img = pygame.transform.smoothscale(coin_img, (tile_size // 2, tile_size // 2))

platform_x_img = pygame.image.load("img/platform_x.png").convert_alpha()
platform_x_img = pygame.transform.smoothscale(platform_x_img, (tile_size, tile_size // 2))
platform_y_img = pygame.image.load("img/platform_y.png").convert_alpha()
platform_y_img = pygame.transform.smoothscale(platform_y_img, (tile_size, tile_size // 2))
# 加载字体
font = pygame.font.SysFont('simsun', 24)
# 素材源图
big_coin_img = pygame.transform.smoothscale(coin_img, (tile_size, tile_size))
source_img_list = [dirt_img, grass_img, blob_img, platform_x_img, platform_y_img, lava_img, big_coin_img, exit_img]

LEVEL = 0
white = (255, 255, 255)
green = (144, 201, 120)

world_data = []  # 地图列表
for i in range(20):
    r = [0] * 20
    world_data.append(r)

for tile in range(0, 20):
    world_data[19][tile] = 2
    world_data[0][tile] = 1
    world_data[tile][0] = 1
    world_data[tile][19] = 1


def draw_grid():
    for col in range(0, 21):
        pygame.draw.line(screen, white, (col * tile_size, 0), (col * tile_size, screen_height), 1)
        pygame.draw.line(screen, white, (0, col * tile_size), (screen_width, col * tile_size), 1)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def world_load():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            x_pos = x * tile_size
            y_pos = y * tile_size

            # 水泥块
            if tile == 1:
                screen.blit(dirt_img, (x_pos, y_pos))
            # 草坪块
            elif tile == 2:
                screen.blit(grass_img, (x_pos, y_pos))
            # 敌人类
            elif tile == 3:
                screen.blit(blob_img, (x_pos, y_pos + 12))
            elif tile == 4:
                screen.blit(platform_x_img, (x_pos, y_pos))
            elif tile == 5:
                screen.blit(platform_y_img, (x_pos, y_pos))
            # 熔岩块
            elif tile == 6:
                screen.blit(lava_img, (x_pos, y_pos + tile_size // 2))
            # 金币
            elif tile == 7:
                screen.blit(coin_img, (x_pos + tile_size // 2, y_pos + tile_size // 2))
            # 出口
            elif tile == 8:
                screen.blit(exit_img, (x_pos, y_pos - tile_size // 2))


class Button:
    """"按钮类"""

    def __init__(self, x, y, image: pygame.Surface):
        self.image = image
        self.rect = self.image.get_rect(x=x, y=y)
        self.clicked = False

    def update(self):
        self.clicked = False
        # 判断鼠标是否点击
        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            if self.rect.collidepoint(x, y):
                self.clicked = True

        screen.blit(self.image, self.rect)
        return self.clicked


save_button = Button(screen_width // 2 - 150, screen_height + height_margin - 80, save_img)
load_button = Button(screen_width // 2 + 50, screen_height + height_margin - 80, load_img)

button_list = []
for col in range(len(source_img_list)):
    b = Button(screen_width + col % 3 * 75 + 50, col // 3 * 75 + 50, source_img_list[col])
    button_list.append(b)

clock = pygame.time.Clock()  # 定时器
current_index = 0  # 当前选择素材按钮的索引
run = True
while run:
    # 设置FPS
    clock.tick(30)
    screen.fill(green)
    # 将背景图片绑定进来
    screen.blit(sky_img, (0, 0))
    screen.blit(sun_img, (100, 100))

    if save_button.update():
        with open(f"level{LEVEL}_data", "wb") as f:
            pickle.dump(world_data, f)
            print("保存成功")

    if load_button.update():
        if path.exists(f"level{LEVEL}_data"):
            with open(f"level{LEVEL}_data", "rb") as f:
                world_data = pickle.load(f)
        else:
            print("地图不存在。")

    for index, b in enumerate(button_list):
        if b.update():
            current_index = index

    pygame.draw.rect(screen, (200, 25, 25), button_list[current_index].rect, 3)
    world_load()
    draw_grid()

    draw_text(f'地图等级: {LEVEL}', font, white, tile_size // 2, screen_height + height_margin - 80)
    draw_text('按方向键↑↓改变等级', font, white, tile_size // 2, screen_height + height_margin - 40)
    pos = pygame.mouse.get_pos()
    x = pos[0] // tile_size
    y = pos[1] // tile_size
    if x < 20 and y < 20:
        if pygame.mouse.get_pressed()[0]:
            if world_data[y][x] != current_index + 1:
                world_data[y][x] = current_index + 1
        elif pygame.mouse.get_pressed()[2]:
            if world_data[y][x] != 0:
                world_data[y][x] = 0

    # 处理点击事件
    for event in pygame.event.get():
        # 判断事件的类型
        if event.type == pygame.QUIT:
            run = False
        # 按下按键事件
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                LEVEL += 1
            elif event.key == pygame.K_DOWN and LEVEL > 0:
                LEVEL -= 1
        # 点击鼠标的事件
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     pos = pygame.mouse.get_pos()
        #     x = pos[0] // tile_size
        #     y = pos[1] // tile_size
        #     if x < 20 and y < 20:
        #         if pygame.mouse.get_pressed()[0]:
        #             world_data[y][x] += 1
        #             if world_data[y][x] > 8:
        #                 world_data[y][x] = 0
        #         elif pygame.mouse.get_pressed()[2]:
        #             world_data[y][x] -= 1
        #             if world_data[y][x] < 0:
        #                 world_data[y][x] = 8

    pygame.display.update()

pygame.quit()
