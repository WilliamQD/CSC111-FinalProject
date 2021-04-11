import pygame
import sys
from load_image import load_card_image_part1

pygame.init()  # 初始化pygame
size = (640, 480)  # 设置窗口
screen = pygame.display.set_mode(size)  # 显示窗口
color = (0, 0, 0)  # 设置颜色

width, height = screen.get_size()  # 获取屏幕大小
square_size = (width / 12, height / 9)  # 获取单个方块大小
load_card_image_part1(square_size)

card = pygame.image.load("Resources/1.jpg")  # 加载图片
cardrect = card.get_rect()  # 获取可编辑矩形区域（type == Surface）
speed = [5, 5]  # 设置移速（x， y）
clock = pygame.time.Clock()  # 设置时钟

while True:
    clock.tick(60)  # 每秒执行60次
    for event in pygame.event.get():  # 获取事件
        if event.type == pygame.QUIT:  # 如果点击退出（右上角X）
            sys.exit()  # 系统退出

    cardrect = cardrect.move(speed)  # 移动
    if cardrect.left < 0 or cardrect.right > width:  # 如果横向碰撞
        speed[0] = - speed[0]  # 反弹

    if cardrect.top < 0 or cardrect.bottom > height:  # 如果纵向碰撞
        speed[1] = - speed[1]  # 反弹

    screen.fill(color)  # 填充颜色
    screen.blit(card, cardrect)  # 把图片画到窗口上
    pygame.display.flip()  # 刷新显示
