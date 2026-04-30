#Imports
import pygame, sys
from pygame.locals import *
import random, time
from persistence import save_score ,load_leaderboard,load_settings,save_settings
#Initialzing 
pygame.init()
pygame.mixer.init()
#Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()
 
#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
#Other Variables for use in the program
SCREEN_WIDTH = 551
SCREEN_HEIGHT = 1000
SPEED = 5
SCORE = 0
COIN=0
 
#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)
 
background = pygame.image.load("road.png")
bigcoin=pygame.image.load("coinBig.png")
smallcoin=pygame.image.load("coinSmall.png")
#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((603,1000))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")
def settings_menu(screen, font):
    settings = load_settings() # Загружаем текущие
    running = True
    
    # Прямоугольники кнопок
    sound_btn = pygame.Rect(200, 200, 300, 50)
    diff_btn = pygame.Rect(200, 300, 300, 50)
    back_btn = pygame.Rect(200, 500, 300, 50)

    while running:
        screen.fill((255, 255, 255))
        
        # Рисуем кнопки (меняем цвет в зависимости от состояния)
        color_sound = (0, 255, 0) if settings["sound"] else (255, 0, 0)
        pygame.draw.rect(screen, color_sound, sound_btn, 2)
        pygame.draw.rect(screen, (0, 0, 0), diff_btn, 2)
        pygame.draw.rect(screen, (0, 0, 0), back_btn, 2)
        
        # Текст
        screen.blit(font.render(f"Sound: {'ON' if settings['sound'] else 'OFF'}", True, (0,0,0)), (210, 210))
        screen.blit(font.render(f"Difficulty: {settings['difficulty']}", True, (0,0,0)), (210, 310))
        screen.blit(font.render("BACK", True, (0,0,0)), (210, 510))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if sound_btn.collidepoint(event.pos):
                    settings["sound"] = not settings["sound"] # Переключаем
                    save_settings(settings) # Сохраняем сразу
                
                if diff_btn.collidepoint(event.pos):
                    settings["difficulty"] = (settings["difficulty"] % 3) + 1 # Цикл 1 -> 2 -> 3 -> 1
                    save_settings(settings)
                    
                if back_btn.collidepoint(event.pos):
                    running = False # Выход в главное меню
                    
        pygame.display.update()
def game_over_screen(screen, font, score):
    # Кнопки
    retry_btn = pygame.Rect(150, 600, 250, 50)
    menu_btn = pygame.Rect(150, 700, 250, 50)
    
    running = True
    while running:
        screen.fill(RED)
        
        # Текст
        screen.blit(font.render("GAME OVER", True, WHITE), (130, 300))
        screen.blit(font.render(f"Score: {score}", True, WHITE), (180, 400))
        
        # Рисуем кнопки
        pygame.draw.rect(screen, WHITE, retry_btn, 2)
        pygame.draw.rect(screen, WHITE, menu_btn, 2)
        screen.blit(font.render("RETRY", True, WHITE), (retry_btn.x + 30, retry_btn.y + 5))
        screen.blit(font.render("MENU", True, WHITE), (menu_btn.x + 30, menu_btn.y + 5))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "EXIT"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_btn.collidepoint(event.pos):
                    return "PLAYING" # Перезапуск
                if menu_btn.collidepoint(event.pos):
                    return "MENU"    # Возврат в меню
                    
        pygame.display.update()
def play(DISPLAYSURF,font_small,gaming):
    class Bonus(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.type = random.choices(["nitro", "shield",'repair'])[0]  # "nitro", "shield", "repair"
            # Загрузи разные картинки для типов
            if self.type == "nitro": self.image = pygame.image.load("nitro.png")
            elif self.type == "shield": self.image = pygame.image.load("shield.png")
            else: self.image = pygame.image.load("repair.png")
            
            self.rect = self.image.get_rect()
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

        def move(self):
            self.rect.move_ip(0, SPEED)
            if self.rect.top > 1000:
                self.kill()
    class Coin(pygame.sprite.Sprite) :
        def __init__(self):
            super().__init__() 
            self.coins=random.randint(1,2)
            if self.coins==1:
                self.image=smallcoin
            else :self.image=bigcoin
            self.rect=self.image.get_rect()
            self.rect.center=(random.randint(48,SCREEN_WIDTH-48),0)
        
        def move(self):
            self.rect.move_ip(0, SPEED)
            if self.rect.top > 1000:
                self.kill()
    class Enemy(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__() 
            self.image = pygame.image.load("play.png")
            self.rect = self.image.get_rect()
            self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)  
    
        def move(self,Why=None):
            global SCORE
            self.rect.move_ip(0,SPEED)
            if (self.rect.top > 800) :
                self.rect.top = 0
                self.rect.center = (random.randint(40, SCREEN_WIDTH-40 ), 0)
            elif Why=='A':
                self.rect.top = 0
                self.rect.center = (random.randint(40, SCREEN_WIDTH-40 ), 0)
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__() 
            self.image = pygame.image.load("player.png")
            self.image1 = pygame.image.load("player2.png")
            self.image2 = pygame.image.load("player1.png")
            self.image3 = pygame.image.load("player3.png")
            self.rect = self.image.get_rect()
            self.rect.center = (270, 900)
            
        def move(self):
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -5)
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0,5)
            if pressed_keys[K_LEFT]:
                if self.rect.left > 49:
                    self.rect.move_ip(-10, 0)
            if pressed_keys[K_RIGHT]:
                if self.rect.right < SCREEN_WIDTH:
                    self.rect.move_ip(10, 0)
        def imacheim(self,type):
            if type == "nitro":
                if self.image == self.image2:
                    self.image = self.image1
                else:
                    self.image = self.image2
            elif type== "shield":
                self.image=self.image3
    #Setting up Sprites        

    SPEED = 5
    SCORE = 0
    COIN=0
    #Setting up Sprites        
    P1 = Player()
    E1 = Enemy()
    
    #Creating Sprites Groups
    coins = pygame.sprite.Group()
    Bonuses = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    enemies.add(E1)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(P1)
    all_sprites.add(E1)
    sound = pygame.mixer.Sound("sound.mp3")
    health=3
    nitr=False
    shield=False
    #Adding a new User event 
    settings = load_settings()
    ADD_COIN = pygame.USEREVENT + 2
    pygame.time.set_timer(ADD_COIN, random.randint(3,10)*1000)
    ADD_BONUS = pygame.USEREVENT +4
    pygame.time.set_timer(ADD_BONUS, 10000)
    IMAGCHAIN = pygame.USEREVENT + 3
    pygame.time.set_timer(IMAGCHAIN, 200)
    DICTANCE=pygame.USEREVENT +5
    pygame.time.set_timer(DICTANCE, 100)
    while gaming:
        if settings["sound"]:
            sound.play()
        if settings["difficulty"]==1:
            NITSPED=10
            SETSPED=5
        elif settings["difficulty"]==2:
            NITSPED=17
            SETSPED=8
        else:
            NITSPED=20
            SETSPED=10
        #Cycles through all events occurring  
        for event in pygame.event.get(): 
            if event.type == ADD_COIN:
                new_coin = Coin()
                coins.add(new_coin)
                all_sprites.add(new_coin)
            if event.type == ADD_BONUS:
                new_bonus = Bonus()
                Bonuses.add(new_bonus)
                all_sprites.add(new_bonus)
            if event.type == DICTANCE:
                SCORE+=SPEED//2
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if nitr== True:
                if event.type == IMAGCHAIN:
                    P1.imacheim(type='nitro')
    
        DISPLAYSURF.blit(background, (0,0))
        scores = font_small.render(str(SCORE)+'  Health:'+str(health), True, BLACK)
        DISPLAYSURF.blit(scores, (10,10))
        coinn = font_small.render(str(COIN), True, BLACK)
        DISPLAYSURF.blit(coinn, (10,40))
        #Moves and Re-draws all Sprites
        for entity in all_sprites:
            DISPLAYSURF.blit(entity.image, entity.rect)
            entity.move()
        
        hit_coins = pygame.sprite.spritecollide(P1, coins, True)
        for coin in hit_coins:
            if coin.coins == 1:
                COIN += 100
            else:
                COIN += 200
        if pygame.sprite.spritecollide(P1,Bonuses,True):
            if new_bonus.type =="nitro":
                nitr=True
                nitrtime=pygame.time.get_ticks()
            elif new_bonus.type == "shield":
                shield=True
                P1.imacheim('shield')
                nitrtime=pygame.time.get_ticks()
            else: 
                if health<3:health+=1
        if nitr== True:
            SPEED=SCORE//200+NITSPED
            if pygame.time.get_ticks()-nitrtime>4000:
                nitr=False
                P1.image=pygame.image.load("player.png")
        else:SPEED=SCORE//200+SETSPED
        if shield==True and pygame.time.get_ticks()-nitrtime>4000:
            shield=False
            P1.image=pygame.image.load("player.png")
        #To be run if collision occurs between Player and Enemy
        if pygame.sprite.spritecollide(P1, enemies,False):
            if shield:
                shield=False
                P1.image=pygame.image.load("player.png")
            else :health-=1
            E1.move('A')
        if health == 0:
            sound.stop()
    #         pygame.mixer.Sound('crash.wav').play()
            time.sleep(0.5)
            gaming=False
        pygame.display.update()
        FramePerSec.tick(FPS)
    return SCORE
def show_leaderboard(screen, font):
    running = True # Условие для while
    
    while running:
        screen.fill(WHITE)
        # Рисуем таблицу (загружаем данные через твой persistence)
        scores = load_leaderboard() 
        
        for i, entry in enumerate(scores):
            score_text = font.render(f"{i+1}. {entry['name']} - {entry['score']}", True, BLACK)
            screen.blit(score_text, (50, 100 + i * 50))
            
        # Кнопка "Назад"
        back_btn = pygame.Rect(200, 800, 200, 50)
        pygame.draw.rect(screen, BLACK, back_btn, 2)
        screen.blit(font.render("НАЗАД", True, BLACK), (250, 810))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(event.pos):
                    running = False # Выход из этого while цикла возвращает в меню
        
        pygame.display.update()
def get_user_name(screen, font):
    name = ""
    running = True # Условие для нашего while
    
    while running:
        screen.fill(WHITE)
        # Рисуем подсказку
        text = font.render(f"Введите имя: {name}", True, BLACK)
        screen.blit(text, (50, 450))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: # Нажали Enter
                    return name # Возвращаем имя и выходим из цикла
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1] # Удаляем последний символ
                else:
                    if len(name) < 10: # Ограничение длины имени
                        name += event.unicode
        
        pygame.display.update()
def main_menu(screen, font):
    # Цвета и текст
    menu_active = True
    
    # Создаем прямоугольники для кнопок (x, y, width, height)
    play_btn = pygame.Rect(200, 300, 200, 50)
    leaderboard_btn = pygame.Rect(200, 400, 200, 50)
    settings_btn = pygame.Rect(200, 500, 200, 50)
    exit_btn = pygame.Rect(200, 600, 200, 50)

    while menu_active:
        screen.fill((255, 255, 255)) # Фон
        
        # Рисуем кнопки (просто как прямоугольники)
        pygame.draw.rect(screen, (0, 0, 0), play_btn, 2)
        pygame.draw.rect(screen, (0, 0, 0), leaderboard_btn, 2)
        pygame.draw.rect(screen, (0, 0, 0), settings_btn, 2)
        pygame.draw.rect(screen, (0, 0, 0), exit_btn, 2)
        
        # Рисуем текст кнопок
        screen.blit(font.render("PLAY", True, (0,0,0)), (play_btn.x + 50, play_btn.y + 10))
        screen.blit(font.render("LEADERS", True, (0,0,0)), (leaderboard_btn.x + 30, leaderboard_btn.y + 10))
        screen.blit(font.render("SETTINGS", True, (0,0,0)), (settings_btn.x + 30, settings_btn.y + 10))
        screen.blit(font.render("EXIT", True, (0,0,0)), (exit_btn.x + 50, exit_btn.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "EXIT"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if play_btn.collidepoint(mouse_pos):
                    return "PLAYING"
                if leaderboard_btn.collidepoint(mouse_pos):
                    return "LEADERBOARD"
                if settings_btn.collidepoint(mouse_pos):
                    return "SETTINGS"
                if exit_btn.collidepoint(mouse_pos):
                    return "EXIT"
                    
        pygame.display.update()
runnig=True
name=get_user_name(DISPLAYSURF,font_small)   
off=True               
while runnig:
    #Game Loop
    gaming=True
    if off:
        menu=main_menu(DISPLAYSURF,font_small)
        if menu== 'EXIT':
            gaming=False
            runnig=False
        elif menu=='LEADERBOARD':
            leadbord=show_leaderboard(DISPLAYSURF,font_small)
            gaming=False
        elif menu=='PLAYING':
            gaming=True
        else:
            settings=settings_menu(DISPLAYSURF,font_small)
            gaming=False
    SCORE=play(DISPLAYSURF,font_small,gaming)
    if menu == 'PLAYING':
        off=game_over_screen(DISPLAYSURF,font_small,SCORE)
    if off =='EXIT':
        runnig=False
    elif off == 'PLAYING' :
        off=False
    save_score(name,SCORE)

pygame.quit()
sys.exit()