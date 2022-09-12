#!/usr/bin/python3
# -*- coding utf-8 -*-
#@Time     :2022/5/15 9:45
#@aUTHOR   :
#@File     :bao_snake.py
#@Software :PyCham

#导入所需的库
import sys
import random
import pygame

# 全局定义
SCREEN_X = 800
SCREEN_Y = 800
seven_color = [(255,0,0),(255,165,0),(255,255,0),(0,255,0),(0,127,255),(0,0,255),(139,0,255)]

# 蛇

# 属性 1.初始化长度
#      2.头 方向
# 方法 1.吃
#      2.死亡
#      3.移动
#      4.方向
class Snake(object):
    def __init__(self):
        self.dirction = pygame.K_RIGHT
        self.body = []
        #设置初始长度
        for x in range(2):
            self.addnode()




    #吃到食物后改变长度
    def addnode(self):
        left,top = (0,0)
        if self.body:
            left,top = (self.body[0].left,self.body[0].top)
        node = pygame.Rect(left,top,25,25)
        if self.dirction == pygame.K_LEFT:
            node.left -= 25
        elif self.dirction == pygame.K_RIGHT:
            node.left += 25
        elif self.dirction == pygame.K_UP:
            node.top -= 25
        elif self.dirction == pygame.K_DOWN:
            node.top += 25
        self.body.insert(0,node)
    def delnode(self):
        self.body.pop()

    #死亡判断
    def isdead(self):
        #撞墙死亡
        if self.body[0].x not in range(SCREEN_X):
            return True
        if self.body[0].y not in range(SCREEN_Y):
            return True
        #撞自己死亡
        if self.body[0] in self.body[1:]:
            return True
        return  False
    #移动
    def move(self):
        self.addnode()
        self.delnode()

    #改变方向
    def changedirection(self,curkey):
        LR = [pygame.K_LEFT,pygame.K_RIGHT]
        UD = [pygame.K_UP, pygame.K_DOWN]
        if curkey in LR + UD:
            if (curkey in LR) and (self.dirction in LR):
                return
            if (curkey in UD) and (self.dirction in UD):
                return
            self.dirction = curkey


# 食物
class Food:
    def __init__(self):
        self.rect = pygame.Rect(-25,0,25,25)
    def remove(self):
        self.rect.x = -25
    def set(self):
        if self.rect.x == -25:
            allpos = []
            #不靠墙太近 25 ~ SCREEN_X-25之间
            for pos in range(25,SCREEN_X - 25,25):
                allpos.append(pos)
            self.rect.left = random.choice(allpos)
            self.rect.top = random.choice(allpos)
            print(self.rect)
            

#音乐
class Music:
    def __init__(self):
        #载入背景音乐
        background_music = pygame.mixer.music.load('background_music.mp4')
        #吃到食物的载入音效
        eat_music = pygame.mixer.Sound('eat_music.mp4')
        self.background_music = background_music
        self.eat_music = eat_music
    #播放背景音乐
    def music_play(self):
        pygame.mixer.music.set_volume(1)#设置音量
        pygame.mixer.music.play(-1)
    #停止背景音乐
    def music_stop(self):
        pygame.mixer.music.stop()
    #播放吃的食物后的音效
    def eat_music_play(self):
        self.eat_music.set_volume(1.5)#设置音量
        self.eat_music.play()
        
#文本显示        
def show_text(screen,pos,text,color,font_bold=False,font_size=60,font_italic=False):
    cur_font = pygame.font.SysFont('宋体',font_size)
    cur_font.set_bold(font_bold)
    cur_font.set_italic(font_italic)
    text_fmt = cur_font.render(text,1,color)
    screen.blit(text_fmt,pos)

#主函数
def main():
    #初始化
    pygame.mixer.init()
    pygame.init()
    screen_size = (SCREEN_X,SCREEN_Y)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('宝哥的彩虹蛇')   #窗口标题
    clock = pygame.time.Clock()
    scores = 0
    isdead = False
    music = Music()
    music.music_play()
    snake = Snake()
    
    food1 = Food()
    food2 = Food()
    food3 = Food()
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                snake.changedirection(event.key)
                if event.key == pygame.K_SPACE and isdead:
                    return main()
        screen.fill((255,255,255))
        
        #画蛇身
        if not isdead:
            snake.move()
        for rect in snake.body:
            pygame.draw.rect(screen,seven_color[random.randint(0,6)],rect,0)

        #显示死亡文字
        isdead = snake.isdead()
        if isdead:
            music.music_stop()
            show_text(screen,(180,200),'YOU DEAD!!!',(227,29,18),False,100)
            show_text(screen, (140, 300), 'press space key to play again...', (0, 0, 22), False, 50)

        #食物的处理 吃到+50   食物与蛇头   蛇 长度+1方块
        if food1.rect == snake.body[0]:
            music.eat_music_play()
            scores += 50
            food1.remove()
            snake.addnode()

        food1.set()
        pygame.draw.rect(screen,(0,0,255),food1.rect,0)
        if food2.rect == snake.body[0]:
            music.eat_music_play()
            scores += 50
            food2.remove()
            snake.addnode()

        food2.set()
        pygame.draw.rect(screen,(0,255,0),food2.rect,0)
        
        if food3.rect == snake.body[0]:
            music.eat_music_play()
            scores += 50
            food3.remove()
            snake.addnode()

        food3.set()
        pygame.draw.rect(screen,(255,0,0),food3.rect,0)
        show_text(screen, (120,0), 'press (up,down,left,right) key to control the snake\'s direction', (0, 0, 22), False, 25)
        
        #显示文字分数
        show_text(screen, (50, 700), 'scores:'+str(scores), (255, 192, 203))
        pygame.display.update()  #更新
        clock.tick(10)

#调用主函数
main()
