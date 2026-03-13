import ctypes
import pygame
import random
import math
import time

ctypes.windll.user32.SetProcessDPIAware()

pygame.init()

info = pygame.display.Info()
WIDTH = info.current_w
HEIGHT = info.current_h

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("视觉训练系统")

clock = pygame.time.Clock()

font = pygame.font.SysFont("SimHei", int(HEIGHT*0.04))
icon_font = pygame.font.SysFont("Segoe UI Symbol", int(HEIGHT*0.035))
title_font = pygame.font.SysFont("SimHei", int(HEIGHT*0.07))

mode = "menu"

TRAIN_TIME = 10
training_start = None
show_over = False
over_time = 0

ball_radius = int(HEIGHT*0.035)

dark_mode = True


def get_theme():
    if dark_mode:
        return (18,18,18),(235,235,235)
    else:
        return (240,240,240),(30,30,30)


class CapsuleButton:

    def __init__(self,text,x,y,w,h,font_obj):
        self.text=text
        self.rect=pygame.Rect(x,y,w,h)
        self.font=font_obj

    def draw(self):

        mouse=pygame.mouse.get_pos()
        hover=self.rect.collidepoint(mouse)

        # 光晕
        if hover:

            for i in range(6):

                expand=8+i*10
                glow_rect=self.rect.inflate(expand,expand)

                glow_surface=pygame.Surface(
                    (glow_rect.width,glow_rect.height),
                    pygame.SRCALPHA
                )

                alpha=max(0,25-i*4)

                pygame.draw.rect(
                    glow_surface,
                    (255,255,255,alpha),
                    glow_surface.get_rect(),
                    border_radius=glow_rect.height//2
                )

                screen.blit(glow_surface,(glow_rect.x,glow_rect.y))

        base_color=(250,245,160)
        hover_color=(255,250,180)

        color=hover_color if hover else base_color

        pygame.draw.rect(
            screen,
            color,
            self.rect,
            border_radius=self.rect.height//2
        )

        label=self.font.render(self.text,True,(40,40,40))

        screen.blit(
            label,
            (
                self.rect.centerx-label.get_width()/2,
                self.rect.centery-label.get_height()/2
            )
        )

    def clicked(self,pos):
        return self.rect.collidepoint(pos)


button_width=WIDTH*0.25
button_height=HEIGHT*0.07

btn1=CapsuleButton("追踪训练",WIDTH/2-button_width/2,HEIGHT*0.35,button_width,button_height,font)
btn2=CapsuleButton("跳点训练",WIDTH/2-button_width/2,HEIGHT*0.45,button_width,button_height,font)
btn3=CapsuleButton("圆周训练",WIDTH/2-button_width/2,HEIGHT*0.55,button_width,button_height,font)
btn4=CapsuleButton("随机目标",WIDTH/2-button_width/2,HEIGHT*0.65,button_width,button_height,font)

theme_w=80
theme_h=50

btn_theme=CapsuleButton(
    "☀",
    WIDTH-theme_w-30,
    30,
    theme_w,
    theme_h,
    icon_font
)

buttons=[btn1,btn2,btn3,btn4]


while True:

    BG_COLOR,TEXT_COLOR=get_theme()

    for event in pygame.event.get():

        if event.type==pygame.QUIT:
            pygame.quit()
            exit()

        if event.type==pygame.KEYDOWN:

            if event.key==pygame.K_ESCAPE:

                if mode=="menu":
                    pygame.quit()
                    exit()
                else:
                    mode="menu"

        if event.type==pygame.MOUSEBUTTONDOWN:

            pos=pygame.mouse.get_pos()

            if mode=="menu":

                if btn1.clicked(pos):
                    mode="pursuit"
                    training_start=time.time()

                if btn2.clicked(pos):
                    mode="saccade"
                    training_start=time.time()

                if btn3.clicked(pos):
                    mode="circle"
                    training_start=time.time()

                if btn4.clicked(pos):
                    mode="random"
                    training_start=time.time()

                if btn_theme.clicked(pos):

                    dark_mode = not dark_mode

                    if dark_mode:
                        btn_theme.text="☀"
                    else:
                        btn_theme.text="🌙"


    screen.fill(BG_COLOR)

    if mode=="menu":

        title=title_font.render("视觉训练系统",True,TEXT_COLOR)

        screen.blit(title,(WIDTH/2-title.get_width()/2,HEIGHT*0.2))

        for b in buttons:
            b.draw()

        btn_theme.draw()

    else:

        if not show_over and time.time()-training_start>TRAIN_TIME:

            show_over=True
            over_time=time.time()

        if show_over:

            text=title_font.render("OVER",True,TEXT_COLOR)

            screen.blit(text,(WIDTH/2-text.get_width()/2,HEIGHT/2))

            if time.time()-over_time>2:

                show_over=False
                mode="menu"

        else:

            if mode=="pursuit":

                x=int(WIDTH/2+math.sin(time.time()*2)*WIDTH*0.35)
                y=HEIGHT//2

                pygame.draw.circle(screen,(255,80,80),(x,y),ball_radius)

            elif mode=="saccade":

                if int(time.time()*2)%2==0:
                    pos=(WIDTH*0.2,HEIGHT/2)
                else:
                    pos=(WIDTH*0.8,HEIGHT/2)

                pygame.draw.circle(screen,(80,160,255),(int(pos[0]),int(pos[1])),ball_radius)

            elif mode=="circle":

                angle=time.time()*2

                x=int(WIDTH/2+math.cos(angle)*WIDTH*0.2)
                y=int(HEIGHT/2+math.sin(angle)*HEIGHT*0.2)

                pygame.draw.circle(screen,(120,255,120),(x,y),ball_radius)

            elif mode=="random":

                if int(time.time()*2)%2==0:

                    x=random.randint(int(WIDTH*0.1),int(WIDTH*0.9))
                    y=random.randint(int(HEIGHT*0.1),int(HEIGHT*0.9))

                pygame.draw.circle(screen,(200,120,255),(x,y),ball_radius)

    pygame.display.update()
    clock.tick(60)