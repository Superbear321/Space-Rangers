# Imports
import pygame
import random
import math

# Initialize game engine
pygame.init()


# Window
WIDTH = 1800
HEIGHT = 1000
SIZE = (WIDTH, HEIGHT)
TITLE = "Space War"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)


# Timer
clock = pygame.time.Clock()
refresh_rate = 60


# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (100, 255, 100)


# Fonts
FONT_SM = pygame.font.Font(None, 24)
FONT_MD = pygame.font.Font(None, 32)
FONT_SCORE = pygame.font.Font(None, 50)
FONT_LG = pygame.font.Font(None, 64)
FONT_XL = pygame.font.Font("assets/fonts/spacerangerboldital.ttf", 96)


# Images
ship_img = pygame.image.load('assets/images/spaceship.png').convert_alpha()
ship_img = pygame.transform.scale(ship_img, (100, 90))
laser_red_img = pygame.image.load('assets/images/laserRed.png').convert_alpha()
laser_green_img = pygame.image.load('assets/images/laserGreen.png').convert_alpha()
enemy_img = pygame.image.load('assets/images/enemyShip.png').convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (50, 40))
space_img = pygame.image.load('assets/images/space_background.png').convert_alpha()
lives_img = pygame.image.load('assets/images/life.png').convert_alpha()
doubleshot_img = pygame.image.load('assets/images/doubleshot.png').convert_alpha()
sentry_img = pygame.image.load('assets/images/laserRedShot.png').convert_alpha()
bullet_img = pygame.image.load('assets/images/bullet.png').convert_alpha()


# Sounds
EXPLOSION = pygame.mixer.Sound('assets/sounds/explosion.ogg')
SHOOT_SOUND = pygame.mixer.Sound('assets/sounds/shoot.wav')


# Stages
START = 0
PLAYING = 1
END = 2


# Game classes
class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 

        self.speed = 7

        self.shoot_clock = 0
        self.is_alive = True

        self.shoots_double = 0


    def move_left(self):
        self.rect.x -= self.speed
    
    def move_right(self):
        self.rect.x +=self.speed

    def shoot(self):
        if self.shoot_clock <= 0:
            if self.shoots_double == False:
                laser = Laser(laser_red_img)
                laser.rect.centerx = self.rect.centerx
                laser.rect.centery = self.rect.top
                lasers.add(laser)
            elif self.shoots_double == 1:
                laser = Laser(laser_red_img)
                laser.rect.centerx = self.rect.x
                laser.rect.centery = self.rect.top - 50
                lasers.add(laser)
                laser = Laser(laser_red_img)
                laser.rect.centerx = self.rect.x + self.rect.width
                laser.rect.centery = self.rect.top - 50
                lasers.add(laser)
            elif self.shoots_double == 2:
                laser = Laser(laser_red_img)
                laser.rect.centerx = self.rect.centerx
                laser.rect.centery = self.rect.top
                lasers.add(laser)
                laser = Laser(laser_red_img)
                laser.rect.centerx = self.rect.x
                laser.rect.centery = self.rect.top
                lasers.add(laser)
                laser = Laser(laser_red_img)
                laser.rect.centerx = self.rect.x + self.rect.width
                laser.rect.centery = self.rect.top
                lasers.add(laser)
                
            SHOOT_SOUND.play()

            self.shoot_clock = 20

    def process_powerups(self):
        hit_list = pygame.sprite.spritecollide(self,powerups,True,pygame.sprite.collide_mask)
        for h in hit_list:
            Powerup.apply(self, 1)
        
    def update(self):
        if self.rect.left < 0:
            self.rect.left = 0 

        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH

        hit_list = pygame.sprite.spritecollide(self,bombs,True,pygame.sprite.collide_mask)
        if len(hit_list) > 0:
            self.is_alive = False
            self.kill()

        self.shoot_clock -= 1

        self.process_powerups()


class Powerup(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        
        self.image = image
        self.rect = self.image.get_rect()
        self.speed = 5
        
    def apply(ship, value):
        if value == 1:
            ship.shoots_double += 1
            if ship.shoots_double > 2:
                ship.shoots_double = 2

    def make_powerup(self):
        powerup_num = random.randint(1,4000)
        if powerup_num == 42:
            self = Powerup(doubleshot_img)
            self.rect.centerx = random.randint(50, WIDTH-50)
            self.rect.centery = random.randint(1,300)*-1
            powerups.add(self)

    def update(self):
        self.rect.y += self.speed
        
        if self.rect.bottom > HEIGHT:
            self.kill()
        

class Laser(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()

        self.speed = 8


    def shoot(self):
        SHOOT_SOUND.play()

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()
        

class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y        

    def drop_bomb(self):
        bomb = Bomb(laser_green_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)

        SHOOT_SOUND.play()

    def update(self):
        hit_list = pygame.sprite.spritecollide(self,lasers,True,pygame.sprite.collide_mask)
        if len(hit_list) > 0:
            player.score += 1
            self.kill() 
    

class Bomb (pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.speed = 5

    def shoot(self):
        SHOOT_SOUND.play()

    def update(self):
        self.rect.y += self.speed
        
        if self.rect.bottom > HEIGHT:
            self.kill()


class Fleet():
    def __init__(self, mobs):
        self.mobs = mobs
        self.speed = 5
        self.moving_right = True
        self.move_down_num = 7
        self.bombing_rate = 20 #Lower is faster

        self.make_aliens(WIDTH-100, HEIGHT-600, 100)

        self.wave_num = 1

    def move(self):
        hits_edge = False
        
        for m in mobs:
            if self.moving_right:
                m.rect.x += self.speed

                if m.rect.right >= WIDTH:
                    hits_edge = True
                    
            else:
                m.rect.x -= self.speed

                if m.rect.left <= 0:
                    hits_edge = True
        if hits_edge:
            self.reverse()
            self.move_down()

    def reverse(self):
        self.moving_right = not self.moving_right

    def move_down(self):
        for m in mobs:
            m.rect.y += self.move_down_num

    def choose_bomber(self):
        rand = random.randrange(self.bombing_rate)
        mob_list = mobs.sprites()

        if len(mob_list) > 0 and rand == 0:
            bomber = random.choice(mob_list)
            bomber.drop_bomb()
            

    def make_aliens(self, width, height, scale):
        for x in range(100, width, scale):
            for y in range(50, height, scale):
                mobs.add( Mob(x,y, enemy_img))

    def kill(self):
        for a in mobs():
            self.kill()
        
    def update(self):
        if len(mobs) == 0:
            self.wave_num += 1
            self.bombing_rate -= 3
            if self.bombing_rate <= 0:
                self.bombing_rate = 1

            self.move_down_num += 3
            if self.move_down_num <= 0:
                self.move_down_num = 1

            self.make_aliens(WIDTH-100, HEIGHT-600, 100)

        for m in mobs:
            if m.rect.bottom >= HEIGHT - 150:
                player.lives = 0 
            
        if player.lives <= 0:
            self.mobs.empty()
        
        self.move()
        self.choose_bomber()


class Sentry (pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.lives =  10

    def drop_bullet(self):
        bullet = Bullet(laser_green_img)
        bullet.rect.centerx = self.rect.centerx
        bullet.rect.centery = self.rect.bottom
        bullets.add(bullet)

        SHOOT_SOUND.play()

    def update(self):
        hit_list = pygame.sprite.spritecollide(self,lasers,True,pygame.sprite.collide_mask)
        temp = random.randrange(0,60)
        if len(hit_list) > 0:
            self.lives -= 1
            if self.lives == 0:
                player.score += 1
                self.kill()
        if temp == 42:
            self.drop_bullet()


class Bullet (pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.speed = 5
        self.theta = None

    def shoot(self):
        SHOOT_SOUND.play()

    def find_theta(self):
                    
        dis_x = ship.rect.centerx - self.rect.centerx
        dis_y = ship.rect.centery - self.rect.centery
        dis_dis = math.sqrt((dis_x**2 + dis_y**2))

        self.theta = math.asin(dis_x/dis_dis)
        self.find_velocity()
    
    def find_velocity(self):
        vx = math.sin(self.theta) * self.speed
        vy = math.cos(self.theta) * self.speed
        print(vx, vy)
        
    
    def update(self):
        self.find_theta()
        
        if self.rect.bottom > HEIGHT:
            self.kill()


class Fleet2():
    def __init__(self, mobs):
        self.mobs = mobs
        self.speed = 5
        self.moving_right = True
        self.move_down_num = 7
        self.bombing_rate = 20 #Lower is faster

        self.make_sentrys()

        self.wave_num = 1

    def move(self):
        hits_edge = False
        
        for m in mobs:
            if self.moving_right:
                m.rect.x += self.speed

                if m.rect.right >= WIDTH:
                    hits_edge = True
                    
            else:
                m.rect.x -= self.speed

                if m.rect.left <= 0:
                    hits_edge = True
        if hits_edge:
            self.reverse()
            self.move_down()

    def reverse(self):
        self.moving_right = not self.moving_right

    def move_down(self):
        for m in mobs:
            m.rect.y += self.move_down_num

    def choose_bomber(self):
        rand = random.randrange(self.bombing_rate)
        mob_list = mobs.sprites()

        if len(mob_list) > 0 and rand == 0:
            bomber = random.choice(mob_list)
            bomber.drop_bomb()
            

    def make_sentrys(self):
        sentrys.add(Sentry(50,400, sentry_img))
        sentrys.add(Sentry(1700,400, sentry_img))


    def kill(self):
        for a in mobs():
            self.kill()
        
    def update(self):
        if len(mobs) == 0:
            self.wave_num += 1
            self.bombing_rate -= 3
            if self.bombing_rate <= 0:
                self.bombing_rate = 1

            self.move_down_num += 3
            if self.move_down_num <= 0:
                self.move_down_num = 1

            self.make_sentrys()

        for m in mobs:
            if m.rect.bottom >= HEIGHT - 150:
                player.lives = 0 
            
        if player.lives <= 0:
            self.mobs.empty()
        
        self.move()
        self.choose_bomber()

        
# Game helper functions


def show_title_screen():
    title_text = FONT_XL.render("Space War!", 1, WHITE)
    title_txt_width = title_text.get_width()
    title_txt_height = title_text.get_height()
    screen.blit(title_text, [(1/2*WIDTH - 1/2*title_txt_width), (1/2*HEIGHT - 1/2*title_txt_height)])


def show_stats(player):
    if player.lives == 3:
        screen.blit(lives_img, (WIDTH-100, HEIGHT-50))
        screen.blit(lives_img, (WIDTH-150, HEIGHT-50))
        screen.blit(lives_img, (WIDTH-200, HEIGHT-50))
    elif player.lives == 2:
        screen.blit(lives_img, (WIDTH-100, HEIGHT-50))
        screen.blit(lives_img, (WIDTH-150, HEIGHT-50))
    elif player.lives == 1:
        screen.blit(lives_img, (WIDTH-100, HEIGHT-50))

    player_score = FONT_SCORE.render(str(player.score), 1, WHITE)
    screen.blit(player_score, [20, 20])


def setup():
    global stage, done
    global player, ship, lasers, mobs, fleet, bombs, powerups, sentrys, bullets
    
    ''' Make game objects '''
    ship = Ship(800,850,ship_img)

    ''' Make sprite groups '''
    player = pygame.sprite.GroupSingle()
    player.add(ship)
    player.lives = 3
    player.score = 0

    lasers = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    mobs = pygame.sprite.Group()
    
    fleet = Fleet(mobs)

    sentrys = pygame.sprite.Group()

    fleet2 = Fleet2(sentrys)
    
    powerups = pygame.sprite.Group()
    
    ''' set stage '''
    stage = START
    done = False


def end_game():
    screen.fill(BLACK)
    title_text = FONT_XL.render("Game Over!", 1, WHITE)
    title_txt_width = title_text.get_width()
    title_txt_height = title_text.get_height()
    screen.blit(title_text, [(1/2*WIDTH - 1/2*title_txt_width), (1/2*HEIGHT - 1/2*title_txt_height)])


def draw_wave(wave):
    wave_txt = FONT_LG.render("Wave:" + str(wave), 1, WHITE)
    screen.blit(wave_txt, [17, 925])

    
# Game loop
setup()

while not done:
    # Input handling (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if stage == START:
                if event.key == pygame.K_SPACE:
                    stage = PLAYING
        
            elif stage == PLAYING:
                if event.key == pygame.K_w:
                    ship.shoot()
                    
    ''' poll key states '''
    state = pygame.key.get_pressed()
    a = state[pygame.K_a]
    s = state[pygame.K_s]
    d = state[pygame.K_d]
    
    if stage == PLAYING:
        if a:
            ship.move_left()
        elif d:
            ship.move_right()
        else:
            block1_vx = 0
    
        if s:
            ship.shoot()

    # Game logic (Check for collisions, update points, etc.)
    if stage == PLAYING:
        player.update()
        lasers.update()
        bombs.update()
        fleet.update()
        mobs.update()
        Powerup.make_powerup(powerups)
        powerups.update()
        sentrys.update()
        bullets.update()

        if not ship.is_alive:
            player.lives -= 1
            ship = Ship(800,850,ship_img)
            bullets.add(Bullet(100,400, bullet_img))
            player.add(ship)

        


            
    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    screen.fill(BLACK)
    screen.blit(space_img, (0, 0))
    lasers.draw(screen)
    bombs.draw(screen)
    player.draw(screen)
    mobs.draw(screen)
    powerups.draw(screen)
    sentrys.draw(screen)
    bullets.draw(screen)
    draw_wave(fleet.wave_num)
    show_stats(player)

    if player.lives <= 0:
            end_game()

    if stage == START:
        show_title_screen()

        
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
