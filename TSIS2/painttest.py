import pygame

pygame.init()

W, H = 800, 500
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Text on Canvas")

font = pygame.font.SysFont("Arial", 28)

clock = pygame.time.Clock()

# ---------------- state ----------------
texts = []  # зафиксированный текст

typing = False
current_text = ""
cursor_pos = (0, 0)

running = True

while running:
    screen.fill((30, 30, 30))

    # -------- events --------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # mouse click → set cursor
        if event.type == pygame.MOUSEBUTTONDOWN:
            cursor_pos = event.pos
            typing = True
            current_text = ""

        # keyboard input
        if event.type == pygame.KEYDOWN and typing:

            if event.key == pygame.K_RETURN:
                # confirm text
                texts.append((current_text, cursor_pos))
                typing = False
                current_text = ""

            elif event.key == pygame.K_ESCAPE:
                # cancel
                typing = False
                current_text = ""

            elif event.key == pygame.K_BACKSPACE:
                current_text = current_text[:-1]

            else:
                current_text += event.unicode

    # -------- draw fixed texts --------
    for txt, pos in texts:
        render = font.render(txt, True, (255, 255, 255))
        screen.blit(render, pos)

    # -------- draw typing text (live) --------
    if typing:
        render = font.render(current_text, True, (0, 255, 0))
        screen.blit(render, cursor_pos)

        # cursor line
        pygame.draw.line(
            screen,
            (0, 255, 0),
            cursor_pos,
            (cursor_pos[0], cursor_pos[1] + 30),
            2
        )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()