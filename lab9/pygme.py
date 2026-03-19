import pygame
import random
pygame.init()
screen=pygame.display.set_mode((900,900))
pygame.display.set_caption('Pygame Project')
running=True
icon=pygame.image.load('images/3426132.png')
clock = pygame.time.Clock()
my_snake=[pygame.Rect(0,0,30,30)]
pygame.draw.rect(screen, (0, 255, 0), my_snake[0])
interval = 400 
last_move = pygame.time.get_ticks()
pygame.display.set_icon(icon)
apple=[random.randint(0,29),random.randint(0,29)]
apple[0]*=30
apple[1]*=30
appt=False
clock=pygame.time.Clock()
wegde='right'
while running:
    screen.fill((0, 173, 32))
    pygame.draw.rect(screen,'red',(apple[0],apple[1],30,30))
    for i in my_snake:
        pygame.draw.rect(screen,'black',i)
    if apple[0]==my_snake[0].x and apple[1]==my_snake[0].y:
        my_snake.append(pygame.Rect(my_snake[-1].x,my_snake[-1].y,30,30))
        appt=True
        while appt==True:
            apple=[random.randint(0,29),random.randint(0,29)]
            apple[0]*=30
            apple[1]*=30
            if (all( i.x!=apple[0] and i.y!=apple[1] for i in my_snake)):appt=False
    pygame.display.update()
    for i in pygame.event.get():
        if i.type==pygame.QUIT:
            running=False
        if i.type==pygame.KEYDOWN:
            if i.key==pygame.K_a or i.key==pygame.K_d:
                if wegde=='up' or wegde=='down':
                    if i.key==pygame.K_a:wegde='left'
                    else:wegde='right'
            if i.key==pygame.K_w or i.key==pygame.K_s:
                if wegde=='right' or wegde=='left':
                    if i.key==pygame.K_w:wegde='up'
                    else:wegde='down'
    current_time = pygame.time.get_ticks()
    if current_time - last_move >= interval:
        for i in range(len(my_snake)-1,0,-1):
            my_snake[i] = my_snake[i-1].copy()
        if wegde=='right':my_snake[0].x+=30
        if wegde=='left':my_snake[0].x-=30
        if wegde=='up':my_snake[0].y-=30
        if wegde=='down':my_snake[0].y+=30
        last_move = current_time
    clock.tick(20)