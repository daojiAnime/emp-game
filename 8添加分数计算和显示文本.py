# -*- coding: utf-8 -*-
# @Time    : 2022/6/1 11:18
# @Author  : Daoji
# @Blog    : https://daojianime.github.io/
# @File    : main.py
# @Des     :
import pickle
import sys
from os import path

import pygame

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

# TODO(Daoji) 2022/6/7 8.2定义字体变量
font_score = pygame.font.SysFont('Bauhaus 93', 30)
font = pygame.font.SysFont('Bauhaus 93', 70)

# 设置窗口图标
icon = pygame.image.load("./img/games.png").convert_alpha()
icon = pygame.transform.smoothscale(icon, (64, 64))
pygame.display.set_icon(icon)

# 加载图片
sun_img = pygame.image.load("./img/sun.png").convert_alpha()
bg_img = pygame.image.load("./img/sky.png").convert_alpha()
restart_img = pygame.image.load("img/restart_btn.png").convert_alpha()
start_img = pygame.image.load("img/start_btn.png").convert_alpha()
exit_img = pygame.image.load("img/exit_btn.png").convert_alpha()

# 定义网格大小
tile_size = 50
# 定义游戏结束的标志
game_over = 0
# 定义主菜单标志
main_menu = True
# 等级
LEVEL = 1
MAX_LEVEL = 7
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
# 定义分数统计变量
score = 0


# TODO(Daoji) 2022/6/7 8.1
def draw_text(text, font, text_color, x, y):
    """
    绘制分数
    
    :param text: 
    :param font: 
    :param text_color: 
    :param x: 
    :param y: 
    :return: 
    """
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))


def draw_grid():
    """
    在窗口绘制直线方格

    :return: None
    """
    for line in range(screen_width // tile_size + 1):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))


def reset_level(level):
    """
    重置关卡

    :param level:
    :return:
    """
    player.reset(100, screen_height - 120)
    blob_group.empty()
    lara_group.empty()
    exit_group.empty()

    if path.exists(f"level{level}_data"):
        with open(f"level{level}_data", "rb") as _f:
            return World(pickle.load(_f))
    else:
        return None


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
                elif tile == 3:
                    enemy = Enemy(col_index * tile_size, row_index * tile_size + 15)
                    blob_group.add(enemy)
                elif tile == 6:
                    lava = Lava(col_index * tile_size, row_index * tile_size + tile_size // 2)
                    lara_group.add(lava)
                # TODO(Daoji) 2022/6/7 8.1.2显示硬币
                elif tile == 7:
                    coin = Coin(col_index * tile_size + (tile_size // 2), row_index * tile_size + (tile_size // 2))
                    coin_group.add(coin)
                elif tile == 8:
                    exit = Exit(col_index * tile_size, row_index * tile_size - tile_size * 0.5)
                    exit_group.add(exit)

    def draw(self):
        for tile, tile_rect in self.tile_list:
            screen.blit(tile, tile_rect)


class Player(pygame.sprite.Sprite):
    """玩家类"""

    def __init__(self, x, y):
        super(Player, self).__init__()
        self.reset(x, y)

    def update(self, _world: World, _enemy_group: pygame.sprite.Group, _lara_group: pygame.sprite.Group,
               _exit_group: pygame.sprite.Group, _game_over: bool) -> bool:
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
            if _keys[pygame.K_SPACE] and not self.jumped and not self.in_air:
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
            self.in_air = True
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
                        self.in_air = False

            # 侦测与敌人碰撞
            if pygame.sprite.spritecollide(self, _enemy_group, False) or pygame.sprite.spritecollide(self, _lara_group,
                                                                                                     False):
                _game_over = -1

            # 与出口碰撞
            if pygame.sprite.spritecollide(self, _exit_group, False):
                _game_over = 1

            # 更新玩家坐标
            self.rect.x += dx
            self.rect.y += dy
            # self.rect.move_ip(dx, dy)

        # 如果游戏结束，显示鬼魂图片
        elif _game_over == -1:
            self.image = self.dead_img
            if self.rect.y > 200:
                self.rect.y -= 5

        # 将玩家图片绘制到屏幕上
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, width=1)

        return _game_over

    def reset(self, x, y):
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

        # 加载鬼魂图片
        self.dead_img = pygame.image.load("img/ghost.png").convert_alpha()

        # 竖直方向速度y
        self.vy = 0
        # 跳跃控制
        self.jumped = False
        # 玩家方向
        self.direction = 0
        self.in_air = True


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


# TODO(Daoji) 2022/6/7 8.1硬币类
class Coin(pygame.sprite.Sprite):
    """硬币类"""

    def __init__(self, x, y):
        super(Coin, self).__init__()
        self.image = pygame.image.load("img/coin.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (tile_size // 2, tile_size // 2))
        # # TODO(Daoji) 2022/6/7 8.1.1根据中心点定位
        self.rect = self.image.get_rect(center=(x, y))
        # 定义史莱姆移动方向
        self.move_direction = 1
        # 定义移动计数器
        self.move_counter = 0


class Button:
    """按钮类"""

    def __init__(self, x, y, image: pygame.Surface):
        self.image = image
        self.rect = self.image.get_rect(x=x, y=y)
        # 定义点击事件的标志
        self.clicked = False

    def draw(self):
        # 定义一个布尔值反馈
        action = False
        pos = pygame.mouse.get_pos()

        # 检查鼠标点击
        if self.rect.collidepoint(pos):
            # print("鼠标点击到了！")
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                action = True
                self.clicked = True
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        screen.blit(self.image, self.rect)
        return action


class Exit(pygame.sprite.Sprite):
    """出口类"""

    def __init__(self, x, y):
        super(Exit, self).__init__()
        self.image = pygame.image.load("img/exit.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (tile_size, tile_size * 1.5))
        self.rect = self.image.get_rect(x=x, y=y)


# 创建一个史莱姆精灵组
blob_group = pygame.sprite.Group()
# 创建一个熔岩精灵组
lara_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
# 初始化硬币显示分数
score_coin = Coin(tile_size // 2, tile_size // 2)
coin_group.add(score_coin)
# 加载不到地图数据就退出程序
if path.exists(f"level{LEVEL}_data"):
    with open(f"level{LEVEL}_data", "rb") as f:
        world_data = pickle.load(f)
else:
    print("找不到地图文件：" + f"level{LEVEL}_dada")
    pygame.quit()
    sys.exit()

# 初始化一个世界类对象
world = World(world_data)
# 初始化按钮
restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, restart_img)
start_button = Button(screen_width // 2 - 350, screen_height // 2, start_img)
exit_button = Button(screen_width // 2 + 150, screen_height // 2, exit_img)

# 初始化一个玩家对象
player = Player(100, screen_height - 130)

# 定义游戏总开关为全局变量run
run = True

while run:
    clock.tick(60)

    # 绘制背景图到窗口
    screen.blit(bg_img, (0, 0))
    screen.blit(sun_img, (100, 100,))
    # 显示主菜单
    if main_menu:
        if start_button.draw():
            main_menu = False
        if exit_button.draw():
            run = False
    else:
        # 绘制精灵
        world.draw()
        exit_group.draw(screen)
        blob_group.draw(screen)
        lara_group.draw(screen)
        exit_group.draw(screen)
        coin_group.draw(screen)

        # 游戏进行中
        if game_over == 0:
            blob_group.update()
            # TODO(Daoji) 2022/6/7 8.2硬币碰撞
            if pygame.sprite.spritecollide(player, coin_group, True):
                score += 1
            draw_text(f'X {score}', font_score, (255, 255, 255), tile_size - 10, 10)

        game_over = player.update(world, blob_group, lara_group, exit_group, game_over)  # 更新玩家动作

        # 游戏结束时
        if game_over == -1:
            # TODO(Daoji) 2022/6/7 8.2
            draw_text("GAME OVER!", font, (128, 125, 243), (screen_width // 2) - 200, screen_height // 2)
            if restart_button.draw():
                world_data.clear()
                world = reset_level(LEVEL)
                game_over = 0
                score = 0
        # 闯关成功
        elif game_over == 1:
            LEVEL += 1
            if LEVEL <= MAX_LEVEL:
                world_data.clear()
                world = reset_level(LEVEL)
                game_over = 0
            # 完成所有关卡时
            else:
                # TODO(Daoji) 2022/6/7 8.2
                draw_text("YOU WIN!", font, (128, 125, 243), (screen_width // 2) - 140, screen_height // 2)
                if restart_button.draw():
                    LEVEL = 1
                    world_data.clear()
                    world = reset_level(LEVEL)
                    game_over = 0

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
# TODO(Daoji) 2022/6/2 6.添加退出和重置按钮
# TODO(Daoji) 2022/6/2 7.添加开始退出按钮和多个关卡加载
# TODO(Daoji) 2022/6/7 8.添加分数计算和显示文本
# TODO(Daoji) 2022/6/7 9.添加声音特效
# TODO(Daoji) 2022/6/7 10.添加移动平台和其碰撞
