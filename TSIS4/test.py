import pygame
import psycopg2
import random
import os
import json
# --- Настройка БД ---
try:
    connect = psycopg2.connect(
        user='aziz', password='1234', host='127.0.0.1', port='5432', database='kbtu'
    )
    cursor = connect.cursor()
except Exception as e:
    print(f"Ошибка БД: {e}"); exit()

pygame.init()
WIDTH, HEIGHT = 1200, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 60)
clock = pygame.time.Clock()
show_grid = True
snake_colors = ['yellow', 'blue', 'white', 'green']
current_color_idx = 0
# Инициализация при запуске программы

# Загрузка настроек при старте программы
if os.path.exists('settings.json'):
    try:
        with open('settings.json', 'r') as f:
            loaded_settings = json.load(f)
            # Применяем загруженные данные
            show_grid = loaded_settings.get("show_grid", True)
            current_color_idx = loaded_settings.get("current_color_idx", 0)
    except:
        pass # Если файл битый, просто оставим дефолтные значения
def Settings_Menu(player_id):
    global show_grid, current_color_idx
    running = True
    while running:
        screen.fill((30, 30, 30))
        # Кнопки
        btn_grid = pygame.Rect(50, 100, 300, 50)
        btn_color = pygame.Rect(50, 170, 300, 50)
        btn_save = pygame.Rect(50, 300, 300, 50)
        
        pygame.draw.rect(screen, 'gray', btn_grid); pygame.draw.rect(screen, 'gray', btn_color)
        pygame.draw.rect(screen, 'green', btn_save)
        
        screen.blit(font.render(f"Сетка: {'Вкл' if show_grid else 'Выкл'}", True, (255,255,255)), (60, 110))
        screen.blit(font.render(f"Цвет змейки: {snake_colors[current_color_idx]}", True, (255,255,255)), (60, 180))
        screen.blit(font.render("Сохранить и вернуться", True, (0,0,0)), (60, 310))
        
        for event in pygame.event.get():
                    if event.type == pygame.QUIT: return
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        if btn_grid.collidepoint(pos): 
                            show_grid = not show_grid
                        elif btn_color.collidepoint(pos): 
                            current_color_idx = (current_color_idx + 1) % len(snake_colors)
                        
                        elif btn_save.collidepoint(pos): 
                            # СОХРАНЕНИЕ НАСТРОЕК
                            settings_data = {
                                "show_grid": show_grid,
                                "current_color_idx": current_color_idx
                            }
                            with open('settings.json', 'w') as f:
                                json.dump(settings_data, f)
                            return # Выход в главное меню
        pygame.display.update()
        
def get_text_input(prompt):
    user_text = ""; active = True
    while active:
        screen.fill((50, 50, 50))
        screen.blit(font.render(prompt + user_text, True, (255, 255, 255)), (100, 400))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: active = False
                elif event.key == pygame.K_BACKSPACE: user_text = user_text[:-1]
                else: user_text += event.unicode
    return user_text

def Voiti():
    email = get_text_input('Введите email: ')
    if email:
        cursor.execute('SELECT id FROM snake WHERE email=%s;', (email,))
        row = cursor.fetchone()
        return row[0] if row else None
    return None
def Game_Over(player_id, score, level):
    # Получаем личный рекорд из базы
    cursor.execute("SELECT MAX(score) FROM game_sessions WHERE player_id = %s", (player_id,))
    record = cursor.fetchone()[0] or 0
    
    while True:
        screen.fill((30, 30, 30))
        # Текст статистики
        screen.blit(big_font.render("GAME OVER", True, (200, 0, 0)), (450, 100))
        screen.blit(font.render(f"Итоговый счет: {score}", True, (255, 255, 255)), (500, 250))
        screen.blit(font.render(f"Уровень: {level}", True, (255, 255, 255)), (500, 300))
        screen.blit(font.render(f"Личный рекорд: {record}", True, (255, 215, 0)), (500, 350))
        
        # Кнопки
        btn_retry = pygame.Rect(450, 500, 300, 60)
        btn_menu = pygame.Rect(450, 600, 300, 60)
        
        pygame.draw.rect(screen, 'green', btn_retry)
        pygame.draw.rect(screen, 'blue', btn_menu)
        
        screen.blit(font.render("Повторить", True, (0,0,0)), (530, 515))
        screen.blit(font.render("Главное меню", True, (255,255,255)), (500, 615))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return 'quit'
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if btn_retry.collidepoint(pos): return 'retry'
                if btn_menu.collidepoint(pos): return 'menu'
def Play_Game(player_id, level):
    # 1. НАСТРОЙКИ ПЕРЕД ЦИКЛОМ
    delenie = {'easy': 60, 'normal': 50, 'hard': 30}[level]
    base_interval = {'easy': 500, 'normal': 400, 'hard': 300}[level]
    snake = [(0, 0)]; direction = 'right'; last_move = pygame.time.get_ticks(); food_list = []
    
    # Состояние бонусов
    has_shield = False
    speed_boost_end = 0
    slow_motion_end = 0
    
    lifespan_map = {1: 15000, 3: 13000, 5: 9000, 0: 7000}

    def spawn_food():
            while True: # Бесконечный цикл, который прервется, когда найдем свободное место
                rand = random.random()
                
                # 1. Выбор типа (как было раньше)
                if rand < 0.7:
                    weight = random.choices([1, 3, 5], weights=[0.8, 0.25, 0.05])[0]
                    color = 'red' if weight == 1 else 'orange' if weight == 3 else 'gold'
                    type_ = 'food'
                elif rand < 0.8:
                    weight, color, type_ = 0, (139, 0, 0), 'poison' # Яд
                else:
                    bonus = random.choice(['speed', 'slow', 'shield'])
                    type_, weight = bonus, 0
                    color = {'speed': 'cyan', 'slow': 'purple', 'shield': 'white'}[bonus]

                # 2. Генерируем координаты
                rect = pygame.Rect(random.randint(0, WIDTH//delenie-1)*delenie, 
                                random.randint(0, HEIGHT//delenie-1)*delenie, delenie, delenie)
                
                # 3. Проверка: не попали ли мы в стену?
                # any(...) вернет True, если прямоугольник rect пересекается хотя бы с одной стеной из wall_list
                if not any(rect.colliderect(w) for w in wall_list):
                    # Если столкновений нет (not True = False), добавляем еду и выходим из цикла
                    food_list.append({'rect': rect, 'weight': weight, 'color': color, 'spawn_time': pygame.time.get_ticks(), 'type': type_})
                    break
    wall_list = [] # Список прямоугольников стен
    current_level = 1 # Счётчик уровней (увеличивай его при наборе очков)
    
    def generate_walls():
        nonlocal wall_list
        wall_list = []
        # Количество стен зависит от уровня: например, 3 + (уровень - 3)
        num_walls = 3 + (current_level - 3)
        for _ in range(num_walls):
            while True:
                w_rect = pygame.Rect(random.randint(0, WIDTH//delenie-1)*delenie, 
                                     random.randint(0, HEIGHT//delenie-1)*delenie, delenie, delenie)
                # Проверяем, чтобы стена не попала на змею
                if w_rect.colliderect(pygame.Rect(snake[0][0], snake[0][1], delenie, delenie)):
                    continue
                wall_list.append(w_rect)
                break
    # 3. ОСНОВНОЙ ЦИКЛ ИГРЫ
    Game = True
    while Game:
        screen.fill((53, 104, 45))
        clock.tick(60)
        current_time = pygame.time.get_ticks()

        # А) Считаем параметры
        current_score = len(snake) - 1
        base_int = max(50, base_interval - (current_score * 5))
        
        # Применяем бонусы к скорости
        if current_time < speed_boost_end: current_interval = base_int // 2
        elif current_time < slow_motion_end: current_interval = base_int * 2
        else: current_interval = base_int
        # 1. Логика смены уровня (например, каждые 5 очков)
        new_level = (len(snake) - 1) // 5 + 1
        if new_level != current_level and new_level >= 3:
            current_level = new_level
            generate_walls() # Генерируем новые стены
        # Б) Отрисовка интерфейса и сетки
        if show_grid:
            for x in range(0, WIDTH, delenie): pygame.draw.line(screen, (70, 70, 70), (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, delenie): pygame.draw.line(screen, (70, 70, 70), (0, y), (WIDTH, y))
        screen.blit(font.render(f"Score: {current_score}", True, (255, 255, 255)), (10, 10))

        # В) Логика еды (удаление и спавн)
        for f in food_list[:]:
            if current_time - f['spawn_time'] > lifespan_map[f.get('weight', 1)]: food_list.remove(f)
        if len(food_list) < 3: spawn_food()
        
        # Г) Отрисовка объектов
        for f in food_list: pygame.draw.rect(screen, f['color'], f['rect'])
        for s in snake: pygame.draw.rect(screen, snake_colors[current_color_idx], (s[0], s[1], delenie, delenie))
        if has_shield: pygame.draw.rect(screen, 'white', (snake[0][0], snake[0][1], delenie, delenie), 3)
        # 2. Отрисовка стен
        for w in wall_list:
            pygame.draw.rect(screen, (100, 100, 100), w) # Серые стены
        # Д) События (клавиатура)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: Game = False
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_a, pygame.K_d] and direction in ['up', 'down']: direction = 'left' if event.key == pygame.K_a else 'right'
                elif event.key in [pygame.K_w, pygame.K_s] and direction in ['right', 'left']: direction = 'up' if event.key == pygame.K_w else 'down'
        
        # Е) Движение и коллизии
        if pygame.time.get_ticks() - last_move >= current_interval:
            x, y = snake[0]
            new_head = {'right': (x+delenie, y), 'left': (x-delenie, y), 'up': (x, y-delenie), 'down': (x, y+delenie)}[direction]
            
            # 3. Проверка столкновения со стеной (в блоке движения)
            if any(head_rect.colliderect(w) for w in wall_list):
                if has_shield:
                    has_shield = False # Щит поглощает удар
                else:
                    Game = False
            x, y = snake[0]
            new_head = {'right': (x+delenie, y), 'left': (x-delenie, y), 'up': (x, y-delenie), 'down': (x, y+delenie)}[direction]
            
            # --- БЛОК ПРОВЕРКИ СТОЛКНОВЕНИЙ ---
            # Создаем Rect для головы, чтобы проверить столкновение со стенами и едой
            new_head_rect = pygame.Rect(new_head[0], new_head[1], delenie, delenie)
            
            # Проверка границ, хвоста и статических стен
            is_out_of_bounds = not (0 <= new_head[0] < WIDTH and 0 <= new_head[1] < HEIGHT)
            is_self_collision = new_head in snake[1:]
            is_wall_collision = any(new_head_rect.colliderect(w) for w in wall_list)

            if is_out_of_bounds or is_self_collision or is_wall_collision:
                if has_shield:
                    has_shield = False # Щит "ломается", но игра продолжается
                else:
                    Game = False
            if Game:
                ate = False
                head_rect = pygame.Rect(new_head[0], new_head[1], delenie, delenie)
                for f in food_list[:]:
                    if head_rect.colliderect(f['rect']):
                        # Обработка типов
                        if f['type'] == 'food':
                            for i in range(f['weight'] -1 ): snake.append(snake[-1])
                        elif f['type'] == 'poison':
                            if len(snake) <= 3: Game = False
                            else: snake = snake[:-2]
                        elif f['type'] == 'speed': speed_boost_end = current_time + 5000
                        elif f['type'] == 'slow': slow_motion_end = current_time + 5000
                        elif f['type'] == 'shield': has_shield = True
                        food_list.remove(f); ate = True; break
                
                if not ate: snake.pop()
                snake.insert(0, new_head)
                last_move = pygame.time.get_ticks()
        
        pygame.display.update()

    # 4. ВЫХОД ИЗ ЦИКЛА
    score = len(snake) - 1
    cursor.execute("INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)", 
                   (player_id, score, {'easy': 1, 'normal': 2, 'hard': 3}[level]))
    connect.commit()
    
    action = Game_Over(player_id, score, level)
    if action == 'menu': return True
    elif action == 'retry': return Play_Game(player_id, level)
    return False

def Main_Menu(player_id):
    screen_state = 'menu'
    running = True
    while running:
        screen.fill((30, 30, 30))
        
        if screen_state == 'menu':
            # Кнопки меню
            btn_easy = pygame.Rect(50, 100, 200, 50); btn_norm = pygame.Rect(50, 160, 200, 50); btn_hard = pygame.Rect(50, 220, 200, 50)
            btn_lead = pygame.Rect(50, 350, 250, 50); btn_my = pygame.Rect(50, 410, 250, 50)
            btn_sett = pygame.Rect(50, 470, 250, 50) # Новая кнопка
            
            pygame.draw.rect(screen, 'green', btn_easy); pygame.draw.rect(screen, 'yellow', btn_norm); pygame.draw.rect(screen, 'red', btn_hard)
            pygame.draw.rect(screen, 'blue', btn_lead); pygame.draw.rect(screen, 'purple', btn_my)
            pygame.draw.rect(screen, 'orange', btn_sett) # Отрисовка кнопки настроек
            
            screen.blit(font.render("Easy", True, (0,0,0)), (60, 110)); screen.blit(font.render("Normal", True, (0,0,0)), (60, 170)); screen.blit(font.render("Hard", True, (0,0,0)), (60, 230))
            screen.blit(font.render("Leaderboard", True, (255,255,255)), (60, 360)); screen.blit(font.render("My Stats", True, (255,255,255)), (60, 420))
            screen.blit(font.render("Settings", True, (255,255,255)), (60, 480)) # Текст кнопки

        else:
            # Отображение таблиц (Leaderboard или My Stats)
            btn_back = pygame.Rect(50, 800, 150, 50)
            pygame.draw.rect(screen, 'gray', btn_back)
            screen.blit(font.render("Назад", True, (0,0,0)), (65, 810))
            
            header = "№    Имя          Счет     Ур-нь     Дата"
            screen.blit(font.render(header, True, (200, 200, 200)), (100, 50))
            
            if screen_state == 'leaderboard':
                cursor.execute("SELECT s.name, gs.score, gs.level_reached, gs.played_at FROM game_sessions gs JOIN snake s ON gs.player_id = s.id ORDER BY gs.score DESC LIMIT 10")
            elif screen_state == 'my_stats':
                cursor.execute("SELECT s.name, gs.score, gs.level_reached, gs.played_at FROM game_sessions gs JOIN snake s ON gs.player_id = s.id WHERE gs.player_id = %s ORDER BY gs.played_at DESC LIMIT 10", (player_id,))
            
            for i, row in enumerate(cursor.fetchall()):
                date_str = str(row[3])[:10]
                text = f"{i+1:<5} {row[0]:<12} {row[1]:<8} {row[2]:<8} {date_str}"
                print(text)
                screen.blit(font.render(text, True, (255,255,255)), (100, 100 + i*40))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                a = None
                pos = pygame.mouse.get_pos()
                if screen_state == 'menu':
                    if btn_easy.collidepoint(pos): a = Play_Game(player_id, 'easy')
                    elif btn_norm.collidepoint(pos): a = Play_Game(player_id, 'normal')
                    elif btn_hard.collidepoint(pos): a = Play_Game(player_id, 'hard')
                    elif btn_lead.collidepoint(pos): screen_state = 'leaderboard'
                    elif btn_my.collidepoint(pos): screen_state = 'my_stats'
                    elif btn_sett.collidepoint(pos): Settings_Menu(player_id) # Вызов меню настроек
                else:
                    if btn_back.collidepoint(pos): screen_state = 'menu'
                if a == 'quit': running = False

if __name__ == "__main__":
    pid = Voiti()
    if pid: Main_Menu(pid)
    else: print("Пользователь не найден")
    pygame.quit(); cursor.close(); connect.close()