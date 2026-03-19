#psql postgres 
import pygame
import psycopg2
from psycopg2 import Error
import re
connect=None
connect=psycopg2.connect(
    user='aziz',
    password='1234',
    host='127.0.0.1',
    port='5432',
    database='kbtu'
)
cursor=connect.cursor()
def Voiti():
    a=input('Чтобы войти \\d или зарегистрироваться \\b или выйти \\q:')
    if a=='\\b':
        Name=None
        while not Name:
            Name=input('Имя:')
            if not re.match(r'[A-Z][a-z]+',Name):
                Name=None
                print('Напишите нормальный Имя!')
        email=None
        while not email:
            email=input('Гмайл:')
            cursor.execute('SELECT email FROM snake WHERE email=%s;',(email,))
            row = cursor.fetchone()
            if row:
                print('Такой гмайл занято!')
                email=None
            elif not re.match(r'[A-Za-z0-9]+@[A-Za-z0-9]+\.[A-Za-z]{3}$',email):
                email=None
                print('Пример:Ghost@ghost.com')
        password=None
        while not password:
            password=input('пароль:')
            if not (re.match(r'.{8,}',password) and re.search(r'[a-z]',password) and re.search(r'[A-Z]',password) and re.search(r'[0-9]',password) and re.search(r'[\W]',password)):
                password=None
                print('Поставьте надежный и больше чем 8 символов')
        cursor.execute('INSERT INTO snake (name,email,password) VALUES (%s,%s,%s);',(Name,email,password))
        cursor.execute('SELECT id FROM snake WHERE email=%s',(email,))
        id=cursor.fetchone()[0]
        cursor.execute('INSERT INTO records (snakeid) VALUES(%s)',(id,))
        connect.commit()
        return id
    elif a=='\\d':
        email=None
        realpass=None
        while not email:
            email=input('Гмайл:')
            cursor.execute('SELECT * FROM snake WHERE email=%s;',(email,))
            row = cursor.fetchone()
            if not row:
                print('Такой емайл не сушествует')
                email=None
            else:realpass=row[3]
        password=None
        poputka=4
        while (not password) and poputka!=0:
            password=input('Пароль:')
            if realpass!=password:
                poputka-=1
                print('Неправилный пароль\nУ вас осталась '+str(poputka)+' попытка!')
                password=None
        if poputka!=0 :
            cursor.execute('SELECT id FROM snake WHERE email=%s',(email,))
            id=cursor.fetchone()[0]
            return id
        else :return False
    elif a=='\\q':return 'a'
        
def Play(id):
    import random
    pygame.init()
    screen=pygame.display.set_mode((1200,900))
    Glava=True
    clock=pygame.time.Clock()
    screen.fill('gray')
    easy=pygame.Rect(300,450, 100, 50)
    normal=pygame.Rect(550,450, 100, 50)
    hard=pygame.Rect(800,450, 100, 50)
    pygame.draw.rect(screen,'green',easy)
    pygame.draw.rect(screen,'yellow',normal)
    pygame.draw.rect(screen,'red',hard)
    cursor.execute('SELECT easy,normal,hard FROM records WHERE id=%s',(id,))
    ceasy,cnormal,chard=cursor.fetchone()
    font = pygame.font.SysFont(None, 50)
    text = font.render("Scores", True, (255,255,255))
    texth = font.render(f"Hard:{str(chard)}", True, (255,255,255))
    textn = font.render(f"Normal:{str(cnormal)}", True, (255,255,255))
    texte = font.render(f"Easy:{str(ceasy)}", True, (255,255,255))
    screen.blit(text, (20, 20))
    screen.blit(texth, (20, 80))
    screen.blit(textn, (20, 140))
    screen.blit(texte, (20, 200))
    level=None
    while Glava:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Glava = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if easy.collidepoint(mouse_pos):
                    level = 'easy'
                    Glava = False
                elif hard.collidepoint(mouse_pos):
                    level = 'hard'
                    Glava = False
                elif normal.collidepoint(mouse_pos):
                    level = 'normal'
                    Glava = False
        pygame.display.update()
    Game=True
    delenie=0
    color=None
    if not level:Game=False
    elif level=='easy':
        delenie=60
        color='yellow'
        interval=500
    elif level=='normal':
        delenie=50
        interval=400
        color='purple'
    elif level=='hard':
        delenie=30
        interval=300
        color='indigo'
    apple=pygame.Rect(random.randint(1,1200//delenie-1)*delenie,random.randint(1,900//delenie-1)*delenie,delenie,delenie)
    snake=[(0,0)]
    wegde='right'
    last_move = pygame.time.get_ticks()
    win=None
    max_cells = (1200//delenie) * (900//delenie)
    while Game:
        screen.fill((53, 104, 45))
        for i in snake:
            pygame.draw.rect(screen,color,(i[0],i[1],delenie,delenie))
        pygame.draw.rect(screen,'red',(apple.x,apple.y,delenie,delenie))
        if apple.x==snake[0][0] and apple.y==snake[0][1]:
            snake.append(pygame.Rect(snake[-1][0],snake[-1][1],delenie,delenie))
            appt=True
            while appt==True:
                apple=pygame.Rect(random.randint(0,1200//delenie-1)*delenie,random.randint(0,900//delenie-1)*delenie,delenie,delenie)
                if all((i[0], i[1]) != (apple.x, apple.y) for i in snake):appt=False
        pygame.display.update()
        for i in pygame.event.get():
            if i.type==pygame.QUIT:
                Game=False
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
            for i in range(len(snake)-1,0,-1):
                snake[i] = snake[i-1]
            x, y = snake[0]
            if wegde=='right':snake[0]=(x + delenie, y)
            if wegde=='left':snake[0]=(x-delenie,y)
            if wegde=='up':snake[0]=(x,y-delenie)
            if wegde=='down':snake[0]=(x,y+delenie)
            last_move = current_time
            if snake[0][0]>1199 or snake[0][0]<0 or snake[0][1]>899 or snake[0][1]<0 or (snake[0] in snake[1:]):
                Game=False
                win=False
                break
            elif len(snake)==max_cells:
                Game=False
                win=True
                break
        clock.tick(20)
    end=True
    screen.fill('grey')
    score=len(snake)-1
    if win:
        text = font.render("Поздравляем вы выграли!", True, (255,255,255))
        screen.blit(text, (500, 400))
    else :
        text = font.render("Вы проиграли", True, (255,255,255))
        screen.blit(text, (500, 400))
        text = font.render(f"Ваш собрали:{score}", True, (255,255,255))
        screen.blit(text, (500, 500))
    from psycopg2 import sql
    if (level=='easy' and ceasy<score) or (level=='normal' and cnormal<score) or (level=='hard' and chard<score):
        query = sql.SQL("UPDATE records SET {} = %s WHERE id = %s").format(
        sql.Identifier(level)
        )
        cursor.execute(query, (score, id))
        connect.commit()
    while end:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                end=False
    return False
if connect:
    id=None
    while not id:
        id=Voiti()
        if id==False:
            print('Вход запрещен!!!')
            break
        elif id=='a':
            print('Программа завершенно!')
            id=False
            break
    while id:
        print('Вы заходили!')
        id=Play(id)