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
clock = pygame.time.Clock()
# 定义窗口的宽度、高度为全局变量
screen_width = 1000
screen_height = 1000
# 初始化窗口
screen = pygame.display.set_mode((screen_width, screen_height))
# 设置窗口标题
pygame.display.set_caption("平台冒险游戏")
# 设置窗口图标
icon = pygame.image.load("./img/games.png").convert_alpha()
icon = pygame.transform.smoothscale(icon, (64, 64))
pygame.display.set_icon(icon)

# 加载图片
sun_img = pygame.image.load("./img/sun.png").convert_alpha()
bg_img = pygame.image.load("./img/sky.png").convert_alpha()

# 定义网格大小
tile_size = 50
# 定义游戏结束的标志
game_over = False

# 定义地图列表
world_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1],
    [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1],
    [1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1],
    [1, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1],
    [1, 0, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
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

    def __init__(self, data, blob_group):
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
                elif tile == 3:
                    enemy = Enemy(col_index * tile_size, row_index * tile_size + 15)
                    blob_group.add(enemy)
                # TODO(Daoji) 2022/6/2 5.1绘制熔岩块
                elif tile == 6:
                    lava = Lava(col_index * tile_size, row_index * tile_size + tile_size // 2)
                    lara_group.add(lava)

    def draw(self):
        for tile, tile_rect in self.tile_list:
            screen.blit(tile, tile_rect)


class Player(pygame.sprite.Sprite):
    """玩家类"""

    def __init__(self, x, y):
        super(Player, self).__init__()
        # 定义一个图片列表
        self.image_right = []
        self.image_left = []
        self.index = 0
        self.counter = 0

        # 加载玩家图片
        for num in range(1, 5):
            player_img = pygame.image.load(f"img/guy{num}.png").convert_alpha()
            player_img = pygame.transform.smoothscale(player_img, (40, 80))
            player_img_flip = pygame.transform.flip(player_img, True, False)
            self.image_right.append(player_img)
            self.image_left.append(player_img_flip)

        # self.image = pygame.transform.smoothscale(player_img, (40, 80)) #初始
        self.image = self.image_right[self.index]
        self.rect = self.image.get_rect(x=x, y=y)

        # TODO:加载鬼魂图片
        self.dead_img = pygame.image.load("img/ghost.png").convert_alpha()

        # 竖直方向速度y
        self.vy = 0
        # 跳跃控制
        self.jumped = False
        # 玩家方向
        self.direction = 0

    def update(self, _world: World, enemy: pygame.sprite.Group, lara: pygame.sprite.Group, _game_over: bool) -> bool:
        dx = 0
        dy = 0
        # 步行冷却时间
        walk_cooldown = 5

        if not _game_over:
            # 获知按键按下
            _keys = pygame.key.get_pressed()
            if _keys[pygame.K_LEFT] or _keys[pygame.K_a]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if _keys[pygame.K_RIGHT] or _keys[pygame.K_d]:
                dx += 5
                self.counter += 1
                self.direction = 1
            if _keys[pygame.K_SPACE] and not self.jumped:
                self.vy = -15
                self.jumped = True
            if not _keys[pygame.K_SPACE]:
                self.jumped = False
            if not (_keys[pygame.K_LEFT] or _keys[pygame.K_RIGHT] or _keys[pygame.K_a] or _keys[pygame.K_d]):
                self.index = 0
                self.counter = 0
                if self.direction == 1:
                    self.image = self.image_right[self.index]
                if self.direction == -1:
                    self.image = self.image_left[self.index]
                # print(f"left:{_keys[pygame.K_LEFT]},right:{_keys[pygame.K_RIGHT]}")

            # 处理动画
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                # 重置玩家图片索引
                if self.index >= len(self.image_right):
                    self.index = 0
                # 更新玩家图片
                if self.direction == 1:
                    self.image = self.image_right[self.index]
                if self.direction == -1:
                    self.image = self.image_left[self.index]

            # 添加重力模拟
            self.vy += 1
            if self.vy > 10:
                self.vy = 10
            dy += self.vy

            # 侦测碰撞
            for tile in _world.tile_list:
                # if tile[1].colliderect(self.rect.move(0, dy)):
                # 检查X方向的碰撞
                if tile[1].colliderect(self.rect.move(dx, 0)):
                    dx = 0
                # 检查Y方向的碰撞
                if tile[1].colliderect(self.rect.move(0, dy)):
                    # 检查是否在空中，例如 跳跃
                    if self.vy < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vy = 0  # 避免吸顶
                    # 检查下坠的情况
                    elif self.vy >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vy = 0  # 避免吸顶

            # 侦测与敌人碰撞
            if pygame.sprite.spritecollide(self, enemy, False) or pygame.sprite.spritecollide(self, lara, False):
                _game_over = True

            # 更新玩家坐标
            self.rect.x += dx
            self.rect.y += dy
            # self.rect.move_ip(dx, dy)

        # TODO:如果游戏结束，显示鬼魂图片
        elif game_over:
            self.image = self.dead_img
            if self.rect.y > 200:
                self.rect.y -= 5

        # 将玩家图片绘制到屏幕上
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, width=1)

        return _game_over


class Enemy(pygame.sprite.Sprite):
    """敌人类"""

    def __init__(self, x, y):
        super(Enemy, self).__init__()
        self.image = pygame.image.load("img/blob.png").convert_alpha()
        self.rect = self.image.get_rect(x=x, y=y)
        # 定义史莱姆移动方向
        self.move_direction = 1
        # 定义移动计数器
        self.move_counter = 0

    def update(self):
        # 左右移动
        self.rect.move_ip(self.move_direction, 0)
        # 限制史莱姆位移距离
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1  # 将move_counter从50变为-50，可以使史莱姆在原位置左右各移动50px


class Lava(pygame.sprite.Sprite):
    """熔岩类"""

    def __init__(self, x, y):
        super(Lava, self).__init__()
        self.image = pygame.image.load("img/lava.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect(x=x, y=y)
        # 定义史莱姆移动方向
        self.move_direction = 1
        # 定义移动计数器
        self.move_counter = 0


# 创建一个史莱姆精灵组
blob_group = pygame.sprite.Group()
# 创建一个熔岩精灵组
lara_group = pygame.sprite.Group()

# 初始化一个世界类对象
world = World(world_data, blob_group)
# 初始化一个玩家对象
player = Player(100, screen_height - 130)

# 定义游戏总开关为全局变量run
run = True
while run:
    clock.tick(60)

    # 绘制背景图到窗口
    screen.blit(bg_img, (0, 0))
    screen.blit(sun_img, (100, 100,))

    # 绘制精灵
    world.draw()

    blob_group.draw(screen)
    if not game_over:
        blob_group.update()
    lara_group.draw(screen)

    game_over = player.update(world, blob_group, lara_group, game_over)  # 更新玩家动作

    for event in pygame.event.get():
        # 监听事件
        if event.type == pygame.QUIT:  # 当点击X按钮时
            run = False  # 退出循环

    # 判断按键按下
    keys = pygame.key.get_pressed()
    # 当Esc键按下为True时
    if keys[pygame.K_ESCAPE]:
        run = False

    # 刷新屏幕
    pygame.display.update()

# 卸载pygame模块
pygame.quit()
# TODO(Daoji) 2022/6/1 1.创建平台横板游戏基本框架
# TODO(Daoji) 2022/6/1 2.添加玩家的代码逻辑
# TODO(Daoji) 2022/6/1 3.碰撞
# TODO(Daoji) 2022/6/1 4.添加敌人
# TODO(Daoji) 2022/6/2 5.添加熔岩和死亡
