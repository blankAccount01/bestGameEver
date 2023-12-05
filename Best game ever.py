import pygame
import math
import pygame.key as key
import time
import random as r
# activate the pygame library .
pygame.init()
X = 1000
Y = 600

# create the display surface object
# of specific dimension..e(X, Y).
screen = pygame.display.set_mode((X, Y))

# set the pygame window name
pygame.display.set_caption('THIS IS THE BEST GAME EVER')
icon = pygame.image.load("assets/enemy.png")
pygame.display.set_icon(icon)

def blitRotate(surf, image, pos, originPos, angle):
    image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
    rotated_offset = offset_center_to_pivot.rotate(-angle)
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
    surf.blit(rotated_image, rotated_image_rect)
    
a = 50000
class Player():
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.location = [450,250]
        self.health = 3
        self.shield = False
        self.imp = pygame.image.load("assets/player.png").convert()
        self.imp3 = pygame.image.load("assets/playerRed.png").convert()
        self.imp4 = pygame.image.load("assets/playerShield.png").convert()
        self.imp2 = self.imp 
        self.gun = pygame.image.load("assets/gun.png").convert()
        self.gun2 = self.gun
        self.rect = pygame.Rect(self.location[0]+25,self.location[1]+50,50,100)
    def update(self,screen):
        if self.shield == True:
            self.imp = self.imp4
        screen.blit(self.imp, (self.location[0], self.location[1]))
        #screen.blit(self.gun, (self.location[0]+44, self.location[1]+36))
        self.rect = pygame.Rect(self.location[0]+10,self.location[1],30,100)
bulletGroup = pygame.sprite.Group()
enemyGroup = pygame.sprite.Group()
bulletGroupFreeze = pygame.sprite.Group()
class Bullet(pygame.sprite.Sprite):
    def __init__(self, location, x, y, Btype, time, length, speed):
        pygame.sprite.Sprite.__init__(self)
        self.location = location
        self.speed = speed
        self.velx = x
        self.rectSize = 20
        self.vely = y
        self.type = Btype
        self.time = time+400*length
        self.imp = pygame.image.load("assets/bullet.png").convert()
        self.imp2 = pygame.image.load("assets/bulletFreeze.png").convert()
        self.rect = pygame.Rect(self.location[0],self.location[1],20,20)
        if Btype == "flame":
            self.imp = pygame.image.load("assets/flame.png").convert()
            self.rectSize = 30
    def update(self,screen):
        if self.type == "freeze":
            screen.blit(self.imp2, (self.location[0], self.location[1]))
        else:
            screen.blit(self.imp, (self.location[0], self.location[1]))
        self.location[0] += self.velx*self.speed
        self.location[1] += self.vely*self.speed
        self.rect = pygame.Rect(self.location[0],self.location[1],self.rectSize,self.rectSize)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, location, Etype):
        pygame.sprite.Sprite.__init__(self)
        self.location = location
        self.rect = pygame.Rect(self.location[0],self.location[1],50,50)
        self.freeze = 0
        self.type = Etype
        self.rectSize = 50
        self.move = [0,0]
        if self.type == 1:
            self.health = 1
            self.imp = pygame.image.load("assets/enemy.png").convert()
            self.speed = 1
        elif self.type == 2:
            self.health = 3
            self.imp = pygame.image.load("assets/enemy2.png").convert()
            self.speed = 1
        elif self.type == 3:
            self.health = 0.5
            self.imp = pygame.image.load("assets/enemy3.png").convert()
            self.speed = 2
        elif self.type == 10:
            self.health = 40
            self.imp = pygame.image.load("assets/enemyBoss.png").convert()
            self.rectSize = 100
            self.speed = 1
        self.timer = -1
        self.hitCooldown = 0
    def update(self,screen,player, a):
        screen.blit(self.imp, (self.location[0], self.location[1]))
        self.rect = pygame.Rect(self.location[0],self.location[1],self.rectSize,self.rectSize)
        if self.freeze == 0:
            if a % 4 == 0:
                self.rel_x, self.rel_y = player.location[0]+25 - self.location[0] , player.location[1]+50 - self.location[1]
                self.angle = ((180 / math.pi) * -math.atan2(self.rel_y, self.rel_x))+90
                self.location[0] += math.sin(math.radians(self.angle)) *self.speed
                self.location[1] += math.cos(math.radians(self.angle)) *self.speed
                self.move[0] = math.sin(math.radians(self.angle)) *self.speed
                self.move[1] = math.cos(math.radians(self.angle)) *self.speed

status = True
clock = pygame.time.Clock()
player = Player()
bullets =[]
enemies = []
angle = 0
rel_y, rel_x = 0,0
cooldownFreeze = 0
cooldown = 0
healthCooldown = 0
damageCooldown = -1
weapon = "gun"
points = 0
while (status):
    #time.sleep(0.001)
    clock.tick(400)
    a+=1
    screen.fill((255,255,255))
    player.update(screen)
    if a%1 == 0:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - player.location[0], mouse_y - player.location[1]
        angle = ((180 / math.pi) * -math.atan2(rel_y, rel_x))+90
        #player.gun = pygame.transform.rotate(player.gun2, int(angle))
        #rect = player.gun.get_rect(center=(player.location[0],player.location[1]+1000))
        blitRotate(screen, player.gun, (player.location[0]+44, player.location[1]+36), (1,1),angle)
    
    keys = key.get_pressed()
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and player.location[1] >= 0:
        for q in enemies:
            q.location[1]+=1
        for w in bullets:
            w.location[1]+=1
    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player.location[1] <= 500:
        for q in enemies:
            q.location[1]-=1
        for w in bullets:
            w.location[1]-=1
    if player.location[0] >= 0 and (keys[pygame.K_LEFT] or keys[pygame.K_a]):
        for q in enemies:
            q.location[0]+=1
        for w in bullets:
            w.location[0]+=1
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.location[0] <= 900:
        for q in enemies:
            q.location[0]-=1
        for w in bullets:
            w.location[0]-=1
    if (keys[pygame.K_p]):
        for e in enemies:
            enemies.remove(e)
            enemyGroup.remove(e)
            points+=1
    if (keys[pygame.K_c]):
        if player.shield == False:
            player.health+=10
            player.shield = True
    if keys[pygame.K_1]:
        weapon = "gun"
    if keys[pygame.K_2]:
        weapon = "shotgun"
    if keys[pygame.K_3]:
        weapon = "minigun"
    if keys[pygame.K_4]:
        weapon = "beam"
    if keys[pygame.K_5]:
        weapon = "flamethrower"
    if pygame.mouse.get_pressed()[0] and cooldown < a:
        if weapon == "gun":
            l = Bullet([player.location[0]+44, player.location[1]+36], math.sin(math.radians(angle)), math.cos(math.radians(angle)), "normal",a,4,1)
            bullets.append(l)
            bulletGroup.add(l)
            cooldown = a + 150
        elif weapon == "shotgun":
            for i in range(-2,3):
                l = Bullet([player.location[0]+44, player.location[1]+36], math.sin(math.radians(angle+i*5)), math.cos(math.radians(angle+i*5)), "normal",a,1,1)
                bullets.append(l)
                bulletGroup.add(l)
                cooldown = a + 400
        elif weapon == "minigun":
            l = Bullet([player.location[0]+44, player.location[1]+36], math.sin(math.radians(angle)), math.cos(math.radians(angle)), "normal",a,1,1.5)
            bullets.append(l)
            bulletGroup.add(l)
            cooldown = a + 20
        elif weapon == "beam":
            l = Bullet([player.location[0]+44, player.location[1]+36], math.sin(math.radians(angle)), math.cos(math.radians(angle)), "normal",a,1,100)
            bullets.append(l)
            bulletGroup.add(l)
            cooldown = a +10
        elif weapon == "flamethrower":
            for i in range(-1,2):
                l = Bullet([player.location[0]+44, player.location[1]+36], math.sin(math.radians(angle+i*10)), math.cos(math.radians(angle+i*10)), "flame",a,0.8,0.5)
                bullets.append(l)
                bulletGroup.add(l)
                cooldown = a +60
    if keys[pygame.K_l] and cooldownFreeze < a:
        for i in range(-10,9):
            l = Bullet([player.location[0]+44, player.location[1]+36], math.sin(math.radians(i*30)), math.cos(math.radians(i*30)), "freeze",a,4,2)
            bullets.append(l)
            bulletGroupFreeze.add(l)
        cooldownFreeze = a + 800
    # iterate over the list of Event objects
    # that was returned by pygame.event.get() method.
    if a % 50 == 0 and (a< 12000 or (a >36000 and a< 55000)):
        SpawnEnemy(1)
    elif a % 25 == 0 and ((a< 24000 and a > 12000) or (a >36000 and a< 55000)):
        SpawnEnemy(2)
    if a % 50 == 0 and ((a< 36000 and a > 24000)or (a >36000 and a< 55000)):
        SpawnEnemy(3)
    if a % 5000 == 0 or (a>55000 and a%200 == 0):
        SpawnEnemy(10)
    def SpawnEnemy(lvl):
        if len(enemies) < 80:
            Sx = r.randint(player.location[1]-800,player.location[0]+1000)
            Sy = r.randint(player.location[1]-500,player.location[1]+500)
            if Sx > player.location[0]+500 or Sx < player.location[0]-800 or Sy > player.location[1]+300 or Sy < player.location[0]-500:
                g = Enemy([Sx,Sy],lvl)
                enemies.append(g)
                enemyGroup.add(g)
    if player.health == 3:
        player.shield = False
        player.imp = player.imp2
    if pygame.sprite.spritecollideany(player, enemyGroup) and healthCooldown < a:
        player.health-=1
        healthCooldown = a + 200
        player.imp = player.imp3
        damageCooldown = a + 200
        if player.health == 0:
            status = False
    if damageCooldown < a and damageCooldown != -1:
        player.imp = player.imp2
        damageCooldown = -1
    for e in enemies:
        if e.timer != -1 and e.timer < a:
            e.freeze = 0
            e.timer = -1
        if pygame.sprite.spritecollideany(e, bulletGroup) and e.hitCooldown <= a:
            if weapon == "shotgun":
                e.health -= 3
            elif weapon == "minigun":
                e.health -=0.3
            elif weapon == "beam":
                e.health -=3
            elif weapon == "flamethrower":
                e.health -=10
            else:
                e.health -=1
            e.hitCooldown = a + 80
            e.freeze = 1
            e.timer = a+20
        elif pygame.sprite.spritecollideany(e, bulletGroupFreeze):
            e.freeze = 1
            e.timer = a+400
        else:
            e.update(screen, player, a)
        enemyGroup.remove(e)
        if pygame.sprite.spritecollideany(e, enemyGroup) and a % 50 ==0:
            d = pygame.sprite.spritecollide(e, enemyGroup,False)
            for m in d:
                m.location[0]-= r.randint(-10,10)/10
                m.location[1]-= r.randint(-10,10)/10
            e.location[0]+=1
            m.location[1]+=1
        enemyGroup.add(e)
            
        if e.health <= 0:
            enemies.remove(e)
            enemyGroup.remove(e)
            points+=1
        if math.hypot(player.location[0] - e.location[0], player.location[1] - e.location[1]) > 1000:
            enemies.remove(e)
            enemyGroup.remove(e)
    for i in bullets:
        if a> i.time:
            bullets.remove(i)
            if i.type == "freeze":
                bulletGroupFreeze.remove(i)
            else:
                bulletGroup.remove(i)
            
        else:
            i.update(screen)
    font = pygame.font.SysFont("Comic Sans MS", 40)
    screen.blit(font.render(str(points), False, (0,60,20)), (0,0))
    for event in pygame.event.get():

        # if event object type is QUIT
        # then quitting the pygame
        # and program both.
        if event.type == pygame.QUIT:
            status = False
    pygame.display.flip()
# deactivates the pygame library
pygame.quit()