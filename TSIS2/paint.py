import pygame
from tools import flood_fill, save_canvas

# Инициализация
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Paint TSIS 2")
clock = pygame.time.Clock()

# Цвета и настройки
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CURRENT_COLOR = BLACK
BRUSH_SIZES = {pygame.K_1: 2, pygame.K_2: 5, pygame.K_3: 10}
current_size = 2

# Состояние
base_layer = pygame.Surface((800, 600))
base_layer.fill(WHITE)
drawing = False
start_pos = None
active_tool = 'pencil' # pencil, line, rect, fill, text

# Текст
font = pygame.font.SysFont("Arial", 24)
text_input = ""
text_active = False
text_pos = (0, 0)
def figure(event,where,mode):
                x_start, y_start = start_pos
                x_end, y_end = event.pos # Текущая позиция мыши
                # 1. Находим левый верхний угол (минимальные значения)
                left = min(x_start, x_end)
                top = min(y_start, y_end)
                # 2. Находим ширину и высоту (разница в пикселях)
                width = abs(x_end - x_start)
                height = abs(y_end - y_start)
                # рисование фигур при клике
                if mode == "square":
                    # 3. Рисуем[(x_start,y_start),(x_start+width//3*2,y_start),(x_end,y_end),(x_start+width//3,y_end)]
                    pygame.draw.rect(where, CURRENT_COLOR, (left, top, width, height), current_size * 2)
                elif mode == "triangle":
                    points = [(x_start,y_start),(x_start+width//3*2,y_start),(x_end,y_end),(x_start+width//3,y_end)]
                    pygame.draw.polygon(where, CURRENT_COLOR, points, current_size * 2)
                elif mode == 'paraliped':
                    points=[(x_start, y_start), (x_start-(x_end-x_start), y_end), (x_end, y_end)]
                    print('aa')
                    pygame.draw.polygon(where, CURRENT_COLOR, points, current_size * 2)
                elif mode == "rhombus":
                    # Ромб: точки — это середины сторон прямоугольника
                    points = [
                        (left + width // 2, top),       # Верх
                        (left + width, top + height // 2), # Право
                        (left + width // 2, top + height), # Низ
                        (left, top + height // 2)       # Лево
                    ]
                    pygame.draw.polygon(where, CURRENT_COLOR, points, current_size * 2)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Добавьте этот блок внутри цикла обработки событий:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:
                active_tool = 'text'
            elif event.key == pygame.K_UP:
                current_size += 1
            elif event.key == pygame.K_DOWN:
                if current_size > 1:  # Защита: чтобы размер не ушел в 0 или минус
                    current_size -= 1
            # Переключение инструментов
            elif event.key == pygame.K_p:
                active_tool = 'pencil'
            elif event.key == pygame.K_l:
                active_tool = 'line'
            elif event.key == pygame.K_f:
                active_tool = 'fill'
            elif event.key == pygame.K_d:
                active_tool = 'figure'
                print('b')
            if active_tool == 'figure':
                if event.key == pygame.K_b: mode = "brush"
                elif event.key == pygame.K_q: mode = "square"
                elif event.key == pygame.K_w: mode = "triangle"
                elif event.key == pygame.K_r: mode = "rhombus"
                elif event.key == pygame.K_i: mode = 'paraliped',print('c')
            # ... (ваша остальная логика клавиш: сохранение, размеры кисти)
        # Переключение инструментов (для простоты - логика горячих клавиш)
        if event.type == pygame.KEYDOWN:
            if event.key in BRUSH_SIZES:
                current_size = BRUSH_SIZES[event.key]
            if (event.mod & pygame.KMOD_CTRL) and event.key == pygame.K_s:
                save_canvas(base_layer)
            # Логика текста
            if text_active:
                if event.key == pygame.K_RETURN: # Зафиксировать
                    base_layer.blit(font.render(text_input, True, CURRENT_COLOR), text_pos)
                    text_input = ""
                    text_active = False
                    active_tool='pencil'
                elif event.key == pygame.K_ESCAPE: # Отмена
                    text_input = ""
                    text_active = False
                    active_tool='pencil'
                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]
                else:
                    text_input += event.unicode

        # Рисование
        if event.type == pygame.MOUSEBUTTONDOWN:
            if active_tool == 'fill':
                flood_fill(base_layer, event.pos, CURRENT_COLOR)
            elif active_tool == 'text':
                text_active = True
                text_pos = event.pos
            else:
                drawing = True
                start_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing and active_tool == 'line':
                pygame.draw.line(base_layer, CURRENT_COLOR, start_pos, event.pos, current_size)
            elif drawing and active_tool == 'figure':
                figure(event,base_layer,mode)
            drawing = False
    # Отрисовка
    screen.blit(base_layer, (0, 0))
    
    # Предварительный просмотр (Preview)
    if drawing:
        if active_tool == 'pencil':
            pygame.draw.line(base_layer, CURRENT_COLOR, start_pos, pygame.mouse.get_pos(), current_size)
            start_pos = pygame.mouse.get_pos()
        elif active_tool == 'line':
            pygame.draw.line(screen, CURRENT_COLOR, start_pos, pygame.mouse.get_pos(), current_size)
        elif active_tool == 'figure':
            figure(event,screen,mode)
            
    if text_active:
        text_surface = font.render(text_input, True, CURRENT_COLOR)
        screen.blit(text_surface, text_pos)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()