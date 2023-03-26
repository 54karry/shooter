
from pygame import *
from random import randint
import time as t


# фоновая музыка
mixer.init()
mixer.music.load('background_music.ogg')
mixer.music.play()


fire = mixer.Sound('fire.ogg')


# шрифты и надписи
font.init()
font2 = font.SysFont('Arial', 36)
win = font2.render('YOU WIN', True, (255, 255, 255))
lose = font2.render('YOU LOSE', True, (180, 0, 0))
reload_text = font2.render('reload', True, (180, 0, 0))


reload = False
enable_bullets = 5
reload_time = t.time()

# нам нужны такие картинки:
img_back = "background.png"  # фон игры
img_hero = "up_player.png"  # герой
img_enemy = "down_monster.png"  # враг


score = 0  # сбито кораблей
lost = 0  # пропущено кораблей


# класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
 # конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)

        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(
            image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 # метод, отрисовывающий героя на окне

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


# класс главного игрока
class Player(GameSprite):
    # метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
 # метод "выстрел" (используем место игрока, чтобы создать там пулю)

    def fire(self):
        global reload_time
        global enable_bullets
        global reload
        enable_bullets -= 1
        print(t.time() - reload_time)

        if enable_bullets == 0 and reload == False:
            reload = True
            reload_time = t.time()

        if t.time() - reload_time >= 3:
            reload = False
            enable_bullets = 5

        if reload == False:
            bullet = Bullet('missle.png', self.rect.centerx,
                            self.rect.top, 15, 20, -15)
            bullets.add(bullet)
            fire.play()


# класс спрайта-врага
class Enemy(GameSprite):
 # движение врага
    def update(self):
        self.rect.y += self.speed
        global lost
        # исчезает, если дойдет до края экрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        # исчезает, если дойдет до края экрана
        if self.rect.y < 0:
            self.kill()


# Создаём окошко
win_width = 700
win_height = 500

max_lost = 3
max_score = 10
max_monsters = 6
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))


# создаём спрайты
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

bullets = sprite.Group()
monsters = sprite.Group()
asteroids = sprite.Group()

for i in range(3):
    asteroid = Enemy('missle.png', randint(
        80, win_width - 80), -40, 80, 50, randint(1, 5))
    asteroids.add(asteroid)

for i in range(1, max_monsters):
    monster = Enemy(img_enemy, randint(
        80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)



# переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
# Основной цикл игры:
run = True  # флаг сбрасывается кнопкой закрытия окна
while run:
    # событие нажатия на кнопку “Закрыть”
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                print(reload)
                ship.fire()
    if not finish:
        # обновляем фон
        window.blit(background, (0, 0))

        # пишем текст на экране

        # производим движения спрайтов
        ship.update()
        monsters.update()
        asteroids.update()
        bullets.update()

        # обновляем их в новом местоположении при каждой итерации цикла
        ship.reset()
        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        collides_astr = sprite.spritecollide(ship, asteroids,True )

        if len(collides_astr) != 0:
            finish = True
            window.blit(lose, (200, 200))

        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(
                80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        # ! обработать касание монстра и корабля

        if lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        if score >= max_score:
            finish = True
            window.blit(win, (200, 200))

        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

    else:
        finish = False
        score = 0
        lost = 0
        reload = False
        enable_bullets = 5

        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()

        time.delay(3000)

        for i in range(1, max_monsters):
            monster = Enemy(img_enemy, randint(
                80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        for i in range(3):
            asteroid = Enemy('missle.png', randint(
        80, win_width - 80), -40, 80, 50, randint(1, 5))
            asteroids.add(asteroid)

    display.update()
    # цикл срабатывает каждую 0.05 секунд
    time.delay(50)
