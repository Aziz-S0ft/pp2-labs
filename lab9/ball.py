import pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball Game")
WHITE = (255, 255, 255)
RED = (255, 0, 0)
radius = 25
x = WIDTH // 2  
y = HEIGHT // 2 
step = 20
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if y - step >= radius:
                    y -= step
            elif event.key == pygame.K_DOWN:
                if y + step <= HEIGHT - radius:
                    y += step
            elif event.key == pygame.K_LEFT:
                if x - step >= radius:
                    x -= step
            elif event.key == pygame.K_RIGHT:
                if x + step <= WIDTH - radius:
                    x += step
    pygame.draw.circle(screen, RED, (x, y), radius)

    pygame.display.flip()
    clock.tick(60)
pygame.quit()