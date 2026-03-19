import pygame
pygame.init()
screen=pygame.display.set_mode((1000,900))
time=pygame.time.Clock()
running=True
color='black'
screen.fill("white")
colors=['white','black','red','blue','green','yellow','aqua','brown','orange']
prev_pos=None
size=2
for i,j in enumerate(colors):
    pygame.draw.rect(screen,j,rect=(900,i*100,100,100))
while running:
    x, y = pygame.mouse.get_pos()
    pygame.display.update()
    for i in pygame.event.get():
        if i.type==pygame.QUIT:
            running=False
        elif i.type==pygame.KEYDOWN:
            if i.key==pygame.K_c:
                screen.fill("white")
                for i,j in enumerate(colors):
                    pygame.draw.rect(screen,j,rect=(900,i*100,100,100))
            elif i.key == pygame.K_1:size = 1
            elif i.key == pygame.K_2:size = 2
            elif i.key == pygame.K_3:size = 3
            elif i.key == pygame.K_4:size = 4
            elif i.key == pygame.K_5:size = 5
        elif i.type == pygame.MOUSEBUTTONDOWN:
            if x >= 900:
                index = y // 100
                if index < len(colors):
                    color = colors[index]
    buttons = pygame.mouse.get_pressed()
    if buttons[0] and x<900:
        if prev_pos is not None:
            pygame.draw.line(screen,color,prev_pos,(x,y),size*2)
        prev_pos=(x,y)
    else:
        prev_pos=None
    time.tick(60)