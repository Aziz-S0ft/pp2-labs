import pygame
import datetime
import math
pygame.init()
screen=pygame.display.set_mode((1400,1050))
a=pygame.image.load("images/mickeyclock.jpeg").convert_alpha()
b=pygame.image.load('images/right.png').convert_alpha()
c=pygame.image.load('images/left.png').convert_alpha()
clock = pygame.time.Clock()
running=True
def draw_rotated_hand(surface, image, angle, center):
    rotated_image = pygame.transform.rotozoom(image, angle, 1)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=center).center)
    surface.blit(rotated_image, new_rect)
while running:
    pygame.display.update()
    for i in pygame.event.get():
        if i.type==pygame.QUIT :
            running=False
    now = datetime.datetime.now()
    minutes = now.minute
    seconds = now.second
    
    angle_sec = 90 - (seconds * 6) 
    angle_min = 90 - (minutes * 6)

    screen.fill((255, 255, 255)) 
    screen.blit(a, (0,0))

    draw_rotated_hand(screen, b, angle_sec, (700,525))
    draw_rotated_hand(screen, c, angle_min, (700,525))

    pygame.display.flip()
    clock.tick(120) 
pygame.quit()
    