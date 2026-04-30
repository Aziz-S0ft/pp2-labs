import pygame
import datetime

def flood_fill(surface, start_pos, fill_color):
    """
    Итеративный алгоритм заливки (BFS).
    Использует get_at/set_at как требовалось в задании.
    """
    width, height = surface.get_size()
    x, y = start_pos
    
    # Получаем целевой цвет, который нужно заменить
    target_color = surface.get_at((x, y))
    
    # Если цвет тот же самый, ничего не делаем
    if target_color == fill_color:
        return

    # Очередь для BFS
    queue = [(x, y)]
    surface.set_at((x, y), fill_color)

    while queue:
        curr_x, curr_y = queue.pop(0)

        # Проверяем 4 направления
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = curr_x + dx, curr_y + dy
            
            if 0 <= nx < width and 0 <= ny < height:
                # Если цвет совпадает с целевым, закрашиваем и добавляем в очередь
                if surface.get_at((nx, ny)) == target_color:
                    surface.set_at((nx, ny), fill_color)
                    queue.append((nx, ny))

def save_canvas(surface):
    """Сохраняет холст с временной меткой в формате PNG."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"canvas_{timestamp}.png"
    pygame.image.save(surface, filename)
    print(f"Файл сохранен: {filename}")