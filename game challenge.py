import pygame, random, time, sys
from pygame.locals import *

running = True
platforms = pygame.sprite.Group()
plats = []
previous_Plat = pygame.Vector3(0,0,0)
all_sprites = pygame.sprite.Group()
pygame.font.init()
f = pygame.font.SysFont("Verdana", 50)

currentPlat = []

pygame.init()
WIDTH = 1920
HIEGHT = 1080
screen = pygame.display.set_mode([WIDTH,HIEGHT])


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface((50,50))
        self.surface.fill((255,255,255))
        self.rect = self.surface.get_rect()
        self.rect.center = (int(WIDTH/2),int(HIEGHT/2))

        self.pos = pygame.Vector2(self.rect.x, self.rect.y)        
        self.vel = pygame.Vector2(0,0)
        self.accel = pygame.Vector2(0,0)

        self.score = 0
    def gravity(self):
        self.accel = pygame.Vector2(0,0.1)

        self.vel += self.accel
        self.pos += self.vel + 0.5 * self.accel

        self.rect.midbottom = self.pos

    def update(self):
        global running
        collisions = pygame.sprite.spritecollide(player, platforms, False)
        if player.vel.y > 0:
            if collisions:
                self.pos.y = collisions[0].rect.top+1
                self.vel.y = 0
                if self.pos.y < collisions[0].rect.bottom:
                    if collisions in currentPlat:
                        pass
                    else:
                        currentPlat.append(collisions)
                        self.score += 1


        if self.rect.y > HIEGHT:
            running = False
            
    def jump(self):
        collisions = pygame.sprite.spritecollide(player, platforms, False)
        if collisions:
            self.vel.y = -10
    def addPlat(self):
        collision = pygame.sprite.collide_rect(player, plats[len(plats)-3])
        if collision:
            createPlat()
            #plats.pop(0)
            for plat in all_sprites:
                if plat.rect.x < -1000:
                    all_sprites.remove(plat)
                    plats.remove(plat)
                    try:
                        currentPlats.remove(plat)
                    except:
                        print("Not in array")  
                    plat.kill
                

class Platform(pygame.sprite.Sprite):
    def __init__(self, width):
        super().__init__()
        global previous_Plat
        self.surface = pygame.Surface((width,25))
        gap = pygame.Vector2(random.randint(10,150), random.randint(-previous_Plat.y, HIEGHT- previous_Plat.y))
        if gap.y > 500 or gap.y < -500:
            gap.y = random.randint(-500,500)
        self.surface.fill((0,150,0))
        self.rect = self.surface.get_rect(center = (previous_Plat.x + (previous_Plat.z/2) + gap.x + width, previous_Plat.y + gap.y))
        previous_Plat = pygame.Vector3(self.rect.x, self.rect.y, width)
        platforms.add(self)
        all_sprites.add(self)
        plats.append(self)

        self.pos = self.rect.x
        self.vel = 0
        self.accel = 0
    def move(self, direction):
        if direction == 'r':
            self.accel += 5 
        else:
            self.accel -= 5

        self.accel += self.vel * -0.5
        self.vel += self.accel
        self.pos += self.vel + 0.5 * self.accel 

        self.rect.x = self.pos
player = Player()

plat1 = Platform(1000)
plat1.surface = pygame.Surface((1000, 20))
plat1.surface.fill((150,150,0))
plat1.rect = plat1.surface.get_rect(center = (WIDTH/2, HIEGHT/2))


all_sprites.add(player)
all_sprites.add(plat1)

def createPlat():
    plat = Platform(random.randint(200,1000))
    print("created Planet", plat.rect.x, plat.rect.y)
for i in range(3):
    createPlat()
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running = False
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                running = False
    
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        for plat in plats:
            plat.move('r')
    if key[pygame.K_RIGHT]:
        for plat in plats:
            plat.move('l')
    if key[pygame.K_SPACE]:
        player.jump()


    all_sprites.update()
    screen.fill((0,0,0))
    g = f.render(str(player.score), True, (123, 255, 0))
    screen.blit(g, (WIDTH/2, 10))

    for entity in all_sprites:
        screen.blit(entity.surface, entity.rect)
    #pygame.display.update()    
    pygame.display.flip()

    player.gravity()
    player.update()
    player.addPlat()
    
    
for entity in all_sprites:
    entity.kill()
    screen.fill((155,0,0))
    f = pygame.font.SysFont("Verdana", 100)
    g = f.render("GAME OVER", True, (0, 255,0))
    screen.blit(g, (WIDTH/3, HIEGHT/3))
    pygame.display.update()
    time.sleep(1)


pygame.quit
sys.exit