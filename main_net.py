# -*- coding: utf-8 -*-
# @Time    : 2022/7/18 9:11
# @Author  : Daoji
# @Blog    : https://daojianime.github.io/
# @File    : main.py
# @Des     :
import pickle
from os import path

import pygame

import net

address = ("192.168.50.10", 8080)  # 服务器地址
# pygame初始化
pygame.init()
# 定义窗口宽度和高度
screen_width = 1000
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("大胖闯天涯")

# 加载背景图片
sky_img = pygame.image.load("img/sky.png").convert_alpha()
sun_img = pygame.image.load("img/sun.png").convert_alpha()
icon_img = pygame.image.load("img/games.png").convert_alpha()
# 加载按钮图片
reset_img = pygame.image.load("img/restart_btn.png").convert_alpha()
start_img = pygame.image.load("img/start_btn.png").convert_alpha()
exit_img = pygame.image.load("img/exit_btn.png").convert_alpha()
# 加载字体
font_score = pygame.font.SysFont('Bauhaus 93', 30)
font = pygame.font.SysFont('Bauhaus 93', 70)
# 加载声音
jump_fx = pygame.mixer.Sound("img/jump.wav")
jump_fx.set_volume(0.5)
coin_fx = pygame.mixer.Sound("img/coin.wav")
coin_fx.set_volume(0.5)
game_over_fx = pygame.mixer.Sound("img/game_over.wav")
game_over_fx.set_volume(0.5)
pygame.mixer.music.load("img/music.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0, 5000)  # （循环次数 开始时间 到最大音量时间ms）

# 缩小icon图片尺寸，并设置到窗口
icon_img = pygame.transform.smoothscale(icon_img, (64, 64))
pygame.display.set_icon(icon_img)
# 定义一个网格尺寸
tile_size = 50
# 主菜单显示开关
main_menu = True
# 定义世界地图列表
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
# 等级
LEVEL = 4
MAX_LEVEL = 8
run = True  # 定义全局变量作为游戏总开关
score = 0  # 分数
if path.exists(f"level{LEVEL}_data"):
    with open(f"level{LEVEL}_data", "rb") as f:
        world_data = pickle.load(f)
else:
    run = False
    print("找不到地图" + f"level{LEVEL}_data")


def reset_level(l):
    """
    重置地图

    :param l: 地图等级
    :return: None
    """

    if path.exists(f"level{l}_data"):
        with open(f"level{l}_data", "rb") as f:
            return pickle.load(f)
    else:
        return False


def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))


class World:
    """世界类"""

    def __init__(self, data):
        # 定义瓷砖列表
        self.tile_list = []

        # 加载图片
        dirt_img = pygame.image.load("img/dirt.png").convert_alpha()
        dirt_img = pygame.transform.smoothscale(dirt_img, (tile_size, tile_size))
        grass_img = pygame.image.load("img/grass.png").convert_alpha()
        grass_img = pygame.transform.smoothscale(grass_img, (tile_size, tile_size))

        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                x_pos = x * tile_size
                y_pos = y * tile_size

                # 水泥块
                if tile == 1:
                    rect = dirt_img.get_rect(x=x_pos, y=y_pos)
                    # 将图片和位置添加到列表里面
                    self.tile_list.append((dirt_img, rect))
                # 草坪块
                elif tile == 2:
                    rect = grass_img.get_rect(x=x_pos, y=y_pos)
                    self.tile_list.append((grass_img, rect))
                # 敌人类
                elif tile == 3:
                    # 生成一个敌人
                    enemy = Enemy(x_pos, y_pos + 15)
                    # 把敌人加入敌人精灵组
                    enemy_group.add(enemy)
                # TODO(Daoji) 2022/7/20 水平平台
                elif tile == 4:
                    platform = Platform(x_pos, y_pos, False)
                    platform_group.add(platform)
                # TODO(Daoji) 2022/7/20 垂直平台
                elif tile == 5:
                    platform = Platform(x_pos, y_pos, True)
                    platform_group.add(platform)
                # 熔岩块
                elif tile == 6:
                    lava = Lava(x_pos, y_pos + tile_size // 2)
                    enemy_group.add(lava)
                # 金币
                elif tile == 7:
                    coin = Coin(x_pos + tile_size // 2, y_pos + tile_size // 2)
                    coin_group.add(coin)
                # 出口
                elif tile == 8:
                    exit = Exit(x_pos, y_pos - tile_size // 2)
                    exit_group.add(exit)

    def draw(self):
        for tile, size in self.tile_list:
            screen.blit(tile, size)


class Player(pygame.sprite.Sprite):
    """玩家类"""

    def __init__(self, x, y, p1=True):
        # 调用精灵类的初始化函数
        super(Player, self).__init__()
        # 右走图片列表
        self.image_right = []
        # 左走图片列表
        self.image_left = []
        # 当前图片索引
        self.index = 0
        # 计数器
        self.counter = 0
        # 左右的方向 左：0 右：1
        self.direction = 0
        self.vy = 0  # y方向速度
        self.jumped = False  # 跳跃
        self.p1 = p1
        self.dead = False  # 是否死亡
        self.passed = False  # 是否通关
        self.reloaded = False  # 是否已重置

        # 遍历加载图片
        for i in range(1, 5):
            player_img = pygame.image.load(f"img/guy{i}.png").convert_alpha()
            player_img = pygame.transform.smoothscale(player_img, (40, 80))
            player_img_flip = pygame.transform.flip(player_img, True, False)
            self.image_right.append(player_img)
            self.image_left.append(player_img_flip)

        self.image = self.image_left[self.index]
        self.rect = self.image.get_rect(x=x, y=y)
        # 加载死亡图片
        self.dead_img = pygame.image.load("img/ghost.png").convert_alpha()

    def update(self):
        global game_over, LEVEL, world, run, world_data
        """
        更新玩家动作

        :return:
        """
        walk_cooldown = 5  # 冷却时间
        dx = 0  # x轴移动距离
        dy = 0  # y轴移动距离
        collide_threshold = 20  # 碰撞阈值 20px

        if not self.dead:
            if self.p1:
                # 获取按键事件
                keys = pygame.key.get_pressed()
                # 判断按下方向键右
                if keys[pygame.K_RIGHT]:
                    dx = 5
                    self.direction = 1
                    self.counter += 1

                elif keys[pygame.K_LEFT]:
                    dx = -5
                    self.direction = 0
                    self.counter += 1

                elif not keys[pygame.K_LEFT] or not keys[pygame.K_RIGHT]:
                    self.counter = 0
                    self.index = 0
                # 按下空格键
                if keys[pygame.K_SPACE] and not self.jumped:
                    jump_fx.play()
                    self.vy = -15
                    self.jumped = True

                # 行走计数
                if self.counter > walk_cooldown:
                    self.counter = 0
                    self.index += 1
                    if self.index >= len(self.image_right):
                        self.index = 0
                # 模拟重力
                if self.vy < 10:
                    self.vy += 1
                dy += self.vy

                # 侦测死亡
                if pygame.sprite.spritecollide(self, enemy_group, False):
                    game_over_fx.play()
                    self.dead = True
                # 侦测是否碰到出口
                if pygame.sprite.spritecollide(self, exit_group, False):
                    self.passed = True
                # 发送数据
                data = (
                    self.rect.x, self.rect.y, self.direction, self.counter, self.index, self.vy, self.jumped, self.dead,
                    self.passed, world_data, self.reloaded)
                net.send_msg(address, str(data))
            else:
                if len(net.position) > 0:
                    data = eval(net.position)  # 将 str 转换为 python代码
                    self.rect.x, self.rect.y = data[0], data[1]
                    self.direction = data[2]
                    self.counter, self.index = data[3], data[4]
                    self.vy, self.jumped = data[5], data[6]
                    self.dead, self.passed = data[7], data[8]
                    self.reloaded = data[10]
                    if len(data[9]) > 0 and world_data != data[9]:
                        world_data = data[9]
                        self.load()

            # 根据玩家方向，设置图片造型
            if self.direction == 1:
                self.image = self.image_right[self.index]
            else:
                self.image = self.image_left[self.index]
            # ----------------------------------------------
            # 侦测碰撞
            for tile, tile_rect in world.tile_list:
                # 检查x方向的碰撞
                if tile_rect.colliderect(self.rect.move(dx, 0)):
                    dx = 0
                # 检查y方向的碰撞
                if tile_rect.colliderect(self.rect.move(0, dy)):
                    # 下降
                    if self.vy >= 0:
                        dy = tile_rect.top - self.rect.bottom
                        self.jumped = False
                    # 在空中(跳跃)
                    elif self.vy < 0:
                        dy = tile_rect.bottom - self.rect.top
                    self.vy = 0

            # 平台碰撞
            for platform in platform_group:
                # x方向碰撞
                if platform.rect.colliderect(self.rect.move(dx, 0)):
                    dx = 0
                # y方向碰撞
                if platform.rect.colliderect(self.rect.move(0, dy)):
                    # TODO(Daoji) 2022/7/20 低于平台
                    if abs((self.rect.top + dy) - platform.rect.bottom) < collide_threshold:
                        self.vy = 0
                        dy = platform.rect.bottom - self.rect.top
                    # TODO(Daoji) 2022/7/20 高于平台
                    elif abs((self.rect.bottom + dy) - platform.rect.top) < collide_threshold:
                        dy = platform.rect.top - self.rect.bottom - 1
                        self.jumped = False
                    # TODO(Daoji) 2022/7/20 跟着平台移动
                    if not platform.vertical:
                        dx += platform.direction
        else:
            self.image = self.dead_img
            self.rect.y -= 5
            if self.rect.y < 200:
                self.kill()

        self.rect.x += dx
        self.rect.y += dy
        if not self.p1:
            pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)

    def reset(self, x, y):
        """
        重置玩家状态

        :return: None
        """
        self.index = 0
        self.vy = 0
        self.jumped = False
        self.counter = 0
        self.image = self.image_left[self.index]
        self.rect = self.image.get_rect(x=x, y=y)

    def load(self):
        global world
        # 清空精灵组
        enemy_group.empty()
        exit_group.empty()
        coin_group.empty()
        platform_group.empty()

        world = World(world_data)
        player.passed = False
        player.reset(100, screen_height - 130)


class Enemy(pygame.sprite.Sprite):
    """敌人类"""

    def __init__(self, x, y):
        super(Enemy, self).__init__()
        self.image = pygame.image.load("img/blob.png").convert_alpha()
        self.rect = self.image.get_rect(x=x, y=y)
        self.direction = 1
        self.counter = 0

    def update(self):
        self.rect.x += self.direction

        self.counter += 1
        if self.counter > 50:
            self.direction *= -1
            self.counter *= -1


class Lava(pygame.sprite.Sprite):
    """熔岩类"""

    def __init__(self, x, y):
        super(Lava, self).__init__()
        self.image = pygame.image.load("img/lava.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect(x=x, y=y)


class Exit(pygame.sprite.Sprite):
    """出口类"""

    def __init__(self, x, y):
        super(Exit, self).__init__()
        self.image = pygame.image.load("img/exit.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (tile_size, tile_size * 1.5))
        self.rect = self.image.get_rect(x=x, y=y)


class Coin(pygame.sprite.Sprite):
    """金币类"""

    def __init__(self, x, y):
        super(Coin, self).__init__()
        self.image = pygame.image.load("img/coin.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Platform(pygame.sprite.Sprite):
    """平台类"""

    def __init__(self, x, y, vertical: bool):
        super(Platform, self).__init__()
        self.image = pygame.image.load("img/platform.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect(x=x, y=y)
        self.direction = 1
        self.counter = 0
        self.vertical = vertical  # 是否垂直移动

    def update(self):
        if self.vertical:
            self.rect.y += self.direction  # 垂直移动
        else:
            self.rect.x += self.direction  # 水平移动

        self.counter += 1
        if self.counter > 50:
            self.direction *= -1
            self.counter *= -1


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


# 创建一个玩家的精灵组
player_group = pygame.sprite.Group()
# 敌人精灵组
enemy_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
# 初始化地图
world = World(world_data)
# 实例化玩家
player = Player(100, screen_height - 130)
p2 = Player(130, screen_height - 130, False)
player_group.add(player)
player_group.add(p2)
# 创建按钮
reset_button = Button(screen_width // 2 - 60, screen_height // 2 - 21, reset_img)
start_button = Button(screen_width // 2 - 350, screen_height // 2, start_img)
exit_button = Button(screen_width // 2 + 150, screen_height // 2, exit_img)
# 显示分数金币
display_group = pygame.sprite.Group()
score_coin = Coin(tile_size // 2, tile_size // 2)
display_group.add(score_coin)

clock = pygame.time.Clock()  # 定时器
game_over = False  # 定义游戏结束的标志

while run:
    # 设置FPS
    clock.tick(60)
    # 将背景图片绑定进来
    screen.blit(sky_img, (0, 0))
    screen.blit(sun_img, (100, 100))
    if main_menu:  # 显示主菜单
        if start_button.update():
            main_menu = False
            net.start_client()  # 开启客户端联网
        if exit_button.update():
            run = False
    else:  # 进入主菜单
        # 绘制地图 / 显示
        world.draw()
        platform_group.draw(screen)
        exit_group.draw(screen)
        coin_group.draw(screen)
        display_group.draw(screen)
        enemy_group.draw(screen)
        player_group.draw(screen)
        # 更新动作 / 更新
        player_group.update()
        platform_group.update()

        # 获取按下的按键（dict）
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            run = False

        if game_over:  # 游戏结束
            draw_text("GAME OVER!", font, (128, 125, 243), (screen_width // 2) - 200, screen_height // 2 + 50)
            if reset_button.update():  # 当按钮被点击重置游戏
                player = Player(100, screen_height - 130)
                player.reloaded = True
                player.update()
                data = eval(net.position)
                if data[10]:
                    game_over = False
                    score = 0  # 重置分数
                    enemy_group.empty()
                    exit_group.empty()
                    coin_group.empty()
                    platform_group.empty()

                    world = World(world_data)
                    player = Player(100, screen_height - 130)
                    p2 = Player(130, screen_height - 130, False)
                    player_group.add(player)
                    player_group.add(p2)

                    net.reload = True
                elif net.reload:
                    game_over = False
                    score = 0  # 重置分数
                    enemy_group.empty()
                    exit_group.empty()
                    coin_group.empty()
                    platform_group.empty()

                    world = World(world_data)
                    player = Player(100, screen_height - 130)
                    p2 = Player(130, screen_height - 130, False)
                    player_group.add(player)
                    player_group.add(p2)

                    net.reload = False

        if not game_over:  # 游戏未结束
            enemy_group.update()
            # p1 p2全死亡
            if not player.alive() and not p2.alive():
                game_over = True
            elif (player.dead and p2.passed) or (p2.dead and player.passed) or (player.passed and p2.passed):
                # 进入下一关
                if LEVEL < MAX_LEVEL:
                    LEVEL += 1
                else:
                    LEVEL = 0
                world_data = reset_level(LEVEL)
                if world_data:
                    player.load()
                else:
                    run = False

            # 侦测吃到金币
            if pygame.sprite.spritecollide(player, coin_group, True):
                coin_fx.play()
                score += 1

        # 显示分数
        draw_text(f"X{score}", font_score, (255, 255, 255), tile_size - 10, 10)

    # 处理点击事件
    for event in pygame.event.get():
        # 判断是不是退出事件
        if event.type == pygame.QUIT:
            run = False
            net.s.close()
    # 刷新屏幕
    pygame.display.update()

# 卸载pygame模块
pygame.quit()
# (Daoji) 2022/7/18 1.创建一个基础游戏框架
# (Daoji) 2022/7/18 2.添加一个玩家并且能操控
# (Daoji) 2022/6/1 3.碰撞
# (Daoji) 2022/6/1 4.添加敌人
# (Daoji) 2022/6/2 5.添加熔岩和死亡
# (Daoji) 2022/6/2 6.添加退出和重置按钮
# (Daoji) 2022/6/2 7.添加开始退出按钮和多个关卡加载
# (Daoji) 2022/6/7 8.添加分数计算和显示文本
# (Daoji) 2022/6/7 9.添加声音特效
# TODO(Daoji) 2022/6/7 10.添加移动平台和其碰撞
