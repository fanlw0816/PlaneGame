# coding=utf-8

import time
import random

import pygame
from pygame.locals import *


class Base(object):
    # 创建基类，提供x,y坐标、载入图片和显示到屏幕功能

    def __init__(self, x, y, image_type):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_type)

    def display(self):
        # 显示到窗口
        self.screen.blit(self.image, (self.x, self.y))


class Plane(Base):
    # 飞机类，继承Base类

    def __init__(self, screen_tmp, imagename):
        Base.__init__(self, 0, 0, imagename)
        self.screen = screen_tmp
        self.bullets = []  # 子弹列表

    def fire(self, x, y, bullet_type):  # 发射子弹
        self.bullets.append(Bullet(x, y, bullet_type))

    def display(self, speed, planetype):  # 重写父类display
        Base.display(self)
        tmp_list = []

        for bullet in self.bullets:  # 显示飞机同时把飞机的子弹显示出来
            bullet.display(self.screen)
            if bullet.release():  # 如果子弹超出屏幕，添加到列表，用于释放资源
                tmp_list.append(bullet)
            bullet.move(speed, planetype)  # 子弹移动

        for tmp in tmp_list:
            self.bullets.remove(tmp)  # 移除超出屏幕的子弹

        del (tmp_list)


class Hero(Plane):
    # 玩家飞机类

    def __init__(self, screen_tmp):
        Plane.__init__(self, screen_tmp, "./planeImage/hero1.png")
        self.x = 140
        self.y = 538

    def display(self):  # 继承父类
        Plane.display(self, 20, 'player')

    def fire(self):  # 继承父类
        bullet_type = "./planeImage/bullet.png"  # 子弹图片
        Plane.fire(self, self.x + 41, self.y - 23, bullet_type)

    def move_left(self):  # 向左移动
        if self.x != 0:
            self.x -= 14

    def move_right(self):  # 向右移动
        if self.x != 280:
            self.x += 14

    def move_up(self):  # 向上移动
        if self.y >= 8:
            self.y -= 14

    def move_down(self):  # 向下移动
        if self.y <= 530:
            self.y += 14

    def die(self, enemy):  # 判断玩家中弹，敌方子弹坐标与玩家飞机区域坐标重合时，玩家中弹
        for bullet in enemy.bullets:
            distance1 = bullet.x + 4 - self.x
            distance2 = bullet.y + 21 - self.y
            if 1 < distance1 <= 50:
                if 124 > distance2 >= (50 - distance1):
                    self.image = pygame.image.load("./planeImage/hero_blowup_n3.png")
                    return True


            elif 50 < distance1 <= 100:
                if 124 > distance2 >= (distance1 - 50):
                    self.image = pygame.image.load("./planeImage/hero_blowup_n3.png")
                    return True


class Enemy(Plane):
    # 敌机类, 继承Plane类

    def __init__(self, screen_tmp):
        Plane.__init__(self, screen_tmp, "./planeImage/enemy0.png")
        self.sysbol = 0

    def display(self):
        Plane.display(self, random.randint(8, 10), 'enemy')

    def fire(self):
        bullet_type = "./planeImage/bullet1.png"
        Plane.fire(self, self.x + 7, self.y + 21, bullet_type)

    def move(self):  # 敌机随机左右移动，向下移动
        firetime = random.randint(1, 30)
        self.move_row()
        self.move_col()
        if firetime == 5:  # 创建随机数，敌机随机发射子弹
            self.fire()

    def move_row(self):  # 敌机向下移动
        step = random.randint(1, 3)
        self.y += step

    def move_col(self):  # 敌机随机左右移动
        ran = ['left', 'right']
        step = random.randint(1, 10)
        select = ran[random.randint(0, 1)]
        if select == 'left':
            self.x -= step
        elif select == 'right':
            self.x += step

    def make(self, x):  # 创建敌机时设置x坐标
        self.x = x

    def release(self):  # 判定是否超出屏幕，用于释放内存
        if self.x + 50 < 0 or self.x > 380 or self.y > 673:
            return True


class Bullet(Base):
    # 子弹类，继承Base类

    def display(self, screen_tmp):
        screen_tmp.blit(self.image, (self.x, self.y))

    def move(self, speed, type_plane):  # 子弹的移动，判断是敌机子弹还是玩家子弹
        if type_plane == 'player':
            self.y -= speed
        elif type_plane == 'enemy':
            self.y += speed

    def release(self):  # 判定子弹是否超出屏幕，用于释放内存
        if self.x < 0 or self.x > 380 or self.y < 0 or self.y > 673:
            return True


class Enemys(object):
    # 用于创建敌机

    def __init__(self, screen_tmp):
        self.all_enemy = []
        self.y = 0
        self.x = random.randint(0, 280)
        self.screen = screen_tmp
        self.remove_list = []

    def make_enemy(self):  # 随机创建敌机
        if random.randint(1, 70) == 50:  # 敌机出现的x随机
            enemy = Enemy(self.screen)
            enemy.make(self.x)
            self.all_enemy.append(enemy)

    def display(self):  # 显示敌机
        tmp_list = []
        for enemy in self.all_enemy:
            enemy.display()
            if enemy.release():  # 判断超出屏幕，添加列表，释放内存资源
                tmp_list.append(enemy)
            enemy.move()

        for tmp in tmp_list:  # 释放内存资源
            self.all_enemy.remove(tmp)

        del (tmp_list)

    def hurted_list(self, hero):  # 被玩家击中判定
        for enemy in self.all_enemy:
            for bullet in hero.bullets:
                distance1 = bullet.y - enemy.y - 14
                distance2 = bullet.x - enemy.x + 11

                if 0 < distance2 <= 25:
                    if 0 < distance1 < distance2:
                        self.remove_list.append((bullet, enemy))

                elif 25 <= distance2 < 50:
                    if 0 < distance1 < (50 - distance2):
                        self.remove_list.append((bullet, enemy))

    def wipe_out(self, hero):  # 若被击中，移除玩家子弹和飞机
        self.hurted_list(hero)
        for rm_tuple in self.remove_list:
            hero.bullets.remove(rm_tuple[0])
            self.all_enemy.remove(rm_tuple[1])

        self.remove_list = []

    def kill_hero(self, hero):  # 击中玩家判定
        isdie = False
        for enemy in self.all_enemy:
            if hero.die(enemy):
                isdie = True
        return isdie


def control(hero):  # 玩家飞机键盘控制

    # pygame.init()

    for event in pygame.event.get():

        # 判断是否是点击了退出按钮
        if event.type == QUIT:
            print("exit")
            exit()
        # 判断是否是按下了键

        elif event.type == KEYDOWN:
            # 检测按键是否是a或者left
            if event.key == K_a or event.key == K_LEFT:
                print('left')
                hero.move_left()

            # 检测按键是否是d或者right
            elif event.key == K_d or event.key == K_RIGHT:
                print('right')
                hero.move_right()

            # 检测按键是否是w或者up
            elif event.key == K_w or event.key == K_UP:
                print('up')
                hero.move_up()

            # 检测按键是否是s或者down
            elif event.key == K_s or event.key == K_DOWN:
                print('down')
                hero.move_down()

            # 检测按键是否是空格键
            elif event.key == K_SPACE:
                print('space')
                hero.fire()

                # pygame.key.set_repeat(old_k_delay, old_k_interval)


def main():
    # 1. 创建窗口
    screen = pygame.display.set_mode((380, 673), 0, 32)

    # 2. 创建背景图片
    background = pygame.image.load("./planeImage/background.png")

    # 3.创建一个飞机图片
    hero = Hero(screen)

    # 创建一个敌人
    # enemy = Enemy(screen)

    pygame.key.set_repeat(100, 20)
    enemys = Enemys(screen)

    isdie = False
    while True:
        screen.blit(background, (0, 0))

        hero.display()
        enemys.make_enemy()
        enemys.display()
        enemys.wipe_out(hero)
        enemys.kill_hero(hero)
        pygame.display.update()

        if isdie:  # 如果玩家飞机被击中，程序睡眠3秒后退出
            time.sleep(3)
            exit()

        isdie = enemys.kill_hero(hero)
        control(hero)

        time.sleep(0.02)


if __name__ == "__main__":
    main()
