from pygame import *
from random import randint
from time import sleep
 
 
#фоновая музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
 
 
#шрифты и надписи
font.init()
font2 = font.SysFont('Arial', 36)
font1 = font.SysFont('Arial' , 80)
win = font1.render('ТЫ ПОБEДИЛ', True , (255 , 255 , 255))
lose = font1.render('ТЫ ПРОИГРАЛ' , True , (180 , 0 , 0))

max_lost = 3
 
#нам нужны такие картинки:
img_back = "fon.jpg" # фон игры
img_hero = "da1.png" # герой
img_enemy = "ufo.png" # враг
img_bullet = 'bullet.png'
 
score = 0 #сбито кораблей
lost = 0 #пропущено кораблей
 
 
#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
 #конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       #Вызываем конструктор класса (Sprite):
       sprite.Sprite.__init__(self)
 
 
       #каждый спрайт должен хранить свойство image - изображение
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed
 
 
       #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
 #метод, отрисовывающий героя на окне
    def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))
 
 
#класс главного игрока
class Player(GameSprite):
   #метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
 #метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self):
        bullet = Bullet(img_bullet , self.rect.centerx, self.rect.top , 15 ,20 , -15)
        bullets.add(bullet)
 
 
#класс спрайта-врага  
class Enemy(GameSprite):
   #движение врага
    def update(self):
       self.rect.y += self.speed
       global lost
       #исчезает, если дойдет до края экрана
       if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)
           self.rect.y = 0
           lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

 
 
#Создаём окошко
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

coll = 0
bullets = sprite.Group()
 
#создаём спрайты
ship = Player(img_hero, 5, win_height - 100, 180, 100, 10)
 
 
monsters = sprite.Group()
for i in range(1, 6):
   monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
   monsters.add(monster)
 
 
#переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
#Основной цикл игры:
run = True #флаг сбрасывается кнопкой закрытия окна
while run:
   #событие нажатия на кнопку “Закрыть”
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
             if e.key == K_SPACE:
                 fire_sound.play()
                 ship.fire()
 
 
    if not finish:
        #обновляем фон
        window.blit(background,(0,0))

        colides = sprite.groupcollide(bullets , monsters , True, True)
        for c in colides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,6))
            monsters.add(monster)

        if sprite.spritecollide(ship , monsters , False) or lost >= 3:
            finish = True
            window.blit(lose , (180 , 200))
        
        if score >= 10:
            finish = True
            window.blit(win , (180 , 200))


        #пишем текст на экране
        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))


        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))


        #производим движения спрайтов
        ship.update()
        monsters.update()
        bullets.update()


        #обновляем их в новом местоположении при каждой итерации цикла
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
    

        display.update()
    #цикл срабатывает каждую 0.05 секунд
    time.delay(30)