#-------------------------------------------------------------------------------------------------------------------------
# Initialise Parameters
#-------------------------------------------------------------------------------------------------------------------------
import pygame, sys, random, time
from pygame.locals import *

# Set mixer defaults (frequency, size, channels, buffer
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()

# Load in sound files
#beep = pygame.mixer.Sound('beep.wav')
#shoot = pygame.mixer.Sound('shoot.wav')

# Load fonts
fontOne = pygame.font.Font("2015 Cruiser Bold Italic.otf", 50)

# Set caption at top of screen (can't be seen in full screen mode)
pygame.display.set_caption("Shmup")

# Set the game to a full screen display Surface
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
screenX, screenY = pygame.display.get_surface().get_size()

# Set the size of the game area so that play is consistent on different monitors
gameX = 1000
gameY = 1000

# Define Background Colour as black (R, G, B) for the screen surface outside the Play Area
backgroundColour = (0, 0, 0)


#-------------------------------------------------------------------------------------------------------------------------
# Define Images, Variables, and Class for Spaceship
#-------------------------------------------------------------------------------------------------------------------------
spaceship_image = pygame.image.load("Spaceship.png")

armour1_image = pygame.image.load("Armour1.png")
armour2_image = pygame.image.load("Armour2.png")
armour3_image = pygame.image.load("Armour3.png")

engine1_image = pygame.image.load("Engine1.png")
engine2_image = pygame.image.load("Engine2.png")
engine3_image = pygame.image.load("Engine3.png")

noseGun1_image = pygame.image.load("NoseGun1.png")
noseGun2_image = pygame.image.load("NoseGun2.png")
noseGun3_image = pygame.image.load("NoseGun3.png")

rWingGun1_image = pygame.image.load("RWingGun1.png")
rWingGun2_image = pygame.image.load("RWingGun2.png")
rWingGun3_image = pygame.image.load("RWingGun3.png")

lWingGun1_image = pygame.image.load("LWingGun1.png")
lWingGun2_image = pygame.image.load("LWingGun2.png")
lWingGun3_image = pygame.image.load("LWingGun3.png")

spaceshipX, spaceshipY = spaceship_image.get_size()
wingGunOffsetX = 56
wingGunOffsetY = 85
gunBarrelOffset = 5

lastTimePlayerFired = 0
firingDelay = 0.2
bulletDamage = 200

armour = 0
engine = 0
noseGun = 1
rWingGun = 0
lWingGun = 0

class Spaceship:
    def __init__(self):
        self.x = (screenX-spaceshipX)/2
        self.y = (screenY + gameY) /2 -(spaceshipY*1.5)

    def draw(self):
        if noseGun == 1:
            screen.blit(noseGun1_image, (self.x, self.y))
        elif noseGun == 2:
            screen.blit(noseGun2_image, (self.x, self.y))
        elif noseGun == 3:
            screen.blit(noseGun3_image, (self.x, self.y))

        if rWingGun ==1:
            screen.blit(rWingGun1_image, (self.x, self.y))
        elif rWingGun == 2:
            screen.blit(rWingGun2_image, (self.x, self.y))
        elif rWingGun == 3:
            screen.blit(rWingGun3_image, (self.x, self.y))

        if lWingGun == 1:
            screen.blit(lWingGun1_image, (self.x, self.y))
        elif lWingGun == 2:
            screen.blit(lWingGun2_image, (self.x, self.y))
        elif lWingGun == 3:
            screen.blit(lWingGun3_image, (self.x, self.y))

        screen.blit(spaceship_image, (self.x, self.y))

        if engine == 1:
            screen.blit(engine1_image, (self.x, self.y))
        elif engine == 2:
            screen.blit(engine2_image, (self.x, self.y))
        elif engine == 3:
            screen.blit(engine3_image, (self.x, self.y))

        if armour == 1:
            screen.blit(armour1_image, (self.x, self.y))
        elif armour == 2:
            screen.blit(armour2_image, (self.x, self.y))
        elif armour == 3:
            screen.blit(armour3_image, (self.x, self.y))

    def move(self):
        if pressedKeys[K_w] and self.y > (screenY - gameY)/2:
            self.y -= (engine+1)**1.4*4*0.7
        if pressedKeys[K_s] and self.y < (screenY + gameY)/2 -spaceshipY:
            self.y += (engine+1)**1.4*4*1.3
        if pressedKeys[K_d] and self.x < (screenX + gameX)/2 -spaceshipX:
            self.x += (engine+1)**1.4*4
        if pressedKeys[K_a] and self.x > (screenX - gameX)/2:
            self.x -= (engine+1)**1.4*4

    def hit_by(self, enemies):
        return pygame.Rect(self.x, self.y, spaceshipX, spaceshipY).collidepoint(enemies.x+(enemy1X /2), enemies.y+(enemy1Y/2))

    def fire(self):
            if noseGun == 1:
                missiles.append(Missile(self.x + (spaceshipX / 2), self.y + 1))
            elif noseGun == 2:
                missiles.append(Missile(self.x + (spaceshipX / 2) -gunBarrelOffset, self.y))
                missiles.append(Missile(self.x + (spaceshipX / 2) +gunBarrelOffset, self.y))
            elif noseGun == 3:
                missiles.append(Missile(self.x + (spaceshipX / 2), self.y + 1))
                missiles.append(Missile(self.x + (spaceshipX / 2) -gunBarrelOffset, self.y))
                missiles.append(Missile(self.x + (spaceshipX / 2) +gunBarrelOffset, self.y))

            if rWingGun == 1:
                missiles.append(Missile(self.x + (spaceshipX / 2) +wingGunOffsetX, self.y +wingGunOffsetY+1))
            elif rWingGun == 2:
                missiles.append(Missile(self.x + (spaceshipX / 2) +wingGunOffsetX - gunBarrelOffset, self.y +wingGunOffsetY))
                missiles.append(Missile(self.x + (spaceshipX / 2) +wingGunOffsetX + gunBarrelOffset, self.y +wingGunOffsetY))
            elif rWingGun == 3:
                missiles.append(Missile(self.x + (spaceshipX / 2) +wingGunOffsetX, self.y +wingGunOffsetY+1))
                missiles.append(Missile(self.x + (spaceshipX / 2) +wingGunOffsetX - gunBarrelOffset, self.y +wingGunOffsetY))
                missiles.append(Missile(self.x + (spaceshipX / 2) +wingGunOffsetX + gunBarrelOffset, self.y +wingGunOffsetY))

            if lWingGun == 1:
                missiles.append(Missile(self.x + (spaceshipX / 2) -wingGunOffsetX, self.y +wingGunOffsetY+1))
            elif lWingGun == 2:
                missiles.append(Missile(self.x + (spaceshipX / 2) -wingGunOffsetX - gunBarrelOffset, self.y +wingGunOffsetY))
                missiles.append(Missile(self.x + (spaceshipX / 2) -wingGunOffsetX + gunBarrelOffset, self.y +wingGunOffsetY))
            elif lWingGun == 3:
                missiles.append(Missile(self.x + (spaceshipX / 2) -wingGunOffsetX, self.y +wingGunOffsetY+1))
                missiles.append(Missile(self.x + (spaceshipX / 2) -wingGunOffsetX - gunBarrelOffset, self.y +wingGunOffsetY))
                missiles.append(Missile(self.x + (spaceshipX / 2) -wingGunOffsetX + gunBarrelOffset, self.y +wingGunOffsetY))
            #shoot.play()

spaceship = Spaceship()

#-------------------------------------------------------------------------------------------------------------------------
# Define List and Class for missiles
#-------------------------------------------------------------------------------------------------------------------------
missiles = []

class Missile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.line(screen, (255,0,0), (self.x,self.y), (self.x, self.y-5), 1)

    def move(self):
        self.y -= 10


#-------------------------------------------------------------------------------------------------------------------------
#Define Images, Variables, List, and Class for Enemies
#-------------------------------------------------------------------------------------------------------------------------
enemy1_image = pygame.image.load("Invader.png").convert_alpha()
enemy1X, enemy1Y = enemy1_image.get_size()

lastTimeEnemySpawned = 0
spawnDelay = 0.8

enemies = []

class Enemies:
    def __init__(self, lvl):
        print(lvl)
        self.x = random.randint((screenX - gameX)/2,(screenX + gameX) /2 -enemy1X)
        self.y = -enemy1Y
        self.destinationY = 0
        self.destinationX = 0
        self.health = (lvl**2) *5
        print(self.health)

    def move(self):
        #Set flight patterns for enemies here
        self.destinationX += random.choice((-1,1))*self.destinationY*0.05
        self.destinationY += 0.005
        self.x += self.destinationX
        self.y += self.destinationY

    def bounce(self):
        if self.x < (screenX-gameX)/2 or self.x > (screenX + gameX) /2 -enemy1X:
            self.destinationX *= -1

    def draw(self):
        screen.blit(enemy1_image, (self.x, self.y))

    def hit_by(self, missile):
        return pygame.Rect(self.x, self.y, enemy1X, enemy1Y).collidepoint((missile.x, missile.y))

#-------------------------------------------------------------------------------------------------------------------------
# Set other game variables
#-------------------------------------------------------------------------------------------------------------------------
clock = pygame.time.Clock()

score = 0
totalScore = 0
level = 1
levelTimer = 0
levelDelay = 60 #Counts in seconds
menu = False
menuButton = 1

#-------------------------------------------------------------------------------------------------------------------------
#/////////////////////////////////////////////////////////////////////////////////////////////////////
# Main Game Loop - Start of loop
#-------------------------------------------------------------------------------------------------------------------------
while 1:
    # Set Framerate
    clock.tick(60)

    if menu == False:
        pygame.mixer.fadeout(300)
        pygame.mixer.music.load('music_track00.wav')
        pygame.mixer.music.play(-1)
        menu = True

    # Exit game process
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.quit()
            pygame.display.quit()
            sys.exit()

    # Start Rendering to screen
    screen.fill(backgroundColour)
    # Draws the game surface area: pygame.draw.rect(Surface, (r, g, b, transparency), (left, top, boxSize, boxSize), outlineThickness)
    pygame.draw.rect(screen, (150,50,150), ( (screenX-gameX)/2, (screenY-gameY)/2, gameX, gameY ), 0)

    pressedKeys = pygame.key.get_pressed()
    if pressedKeys[K_w]:
        menuButton = 1  # Start Game
    if pressedKeys[K_a]:
        menuButton = 2  # Credits
    if pressedKeys[K_s]:
        menuButton = 3  # Upgrades
    if pressedKeys[K_d]:
        menuButton = 4  # Options

    pygame.display.update()

#-------------------------------------------------------------------------------------------------------------------------
#/////////////////////////////////////////////////////////////////////////////////////////////////////
    # Game Mode - Start of loop
#-------------------------------------------------------------------------------------------------------------------------
    if pressedKeys[K_RETURN] and menuButton ==1:
        pygame.mixer.fadeout(300)
        pygame.mixer.music.load('music_track01.wav')
        pygame.mixer.music.play(-1)
        menu = False

        level = 1
        levelTimer = time.time()

        maxHealth = 75 * (1.6**(armour+1))
        health = maxHealth
        while health > 0:
        #Set Framerate
            clock.tick(60)

            # Exit game process
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.quit()
                    pygame.display.quit()
                    sys.exit()

            pressedKeys = pygame.key.get_pressed()

            if time.time() - levelTimer > levelDelay:
                level += 1
                levelTimer = time.time()

            # Start Rendering to screen
            screen.fill(backgroundColour)
            #Draws the game surface area: pygame.draw.rect(Surface, (r, g, b, transparency), (left, top, boxSize, boxSize), outlineThickness)
            pygame.draw.rect(screen, (0,50,150), ( (screenX-gameX)/2, (screenY-gameY)/2, gameX, gameY ), 0)

            # Spawns new enemies if the timer has elapsed
            if time.time() - lastTimeEnemySpawned > spawnDelay-(level*0.02): # Spawn timer goes into negative at 40 levels
                enemies.append(Enemies(level))
                lastTimeEnemySpawned = time.time()

            # Calls the Spaceship Class to perform functions
            spaceship.move()
            spaceship.draw()
            if pressedKeys[K_RETURN] and time.time() - lastTimePlayerFired > firingDelay:
                spaceship.fire()
                lastTimePlayerFired = time.time()

            # Loop to move and draw all missiles
            j=0
            while j < len(missiles):
                missiles[j].move()
                missiles[j].draw()
                if missiles[j].y < (screenY - gameY)/2 -10:
                    del missiles[j]
                    j -= 1
                j += 1

            # Loop to move and draw all enemies
            i = 0
            while i < len(enemies):
                enemies[i].move()
                enemies[i].bounce()
                enemies[i].draw()
                # Deletes enemies if they reach the bottom of the screen
                if enemies[i].y > (screenY + gameY)/2:
                    del enemies[i]
                    i -= 1
                i += 1

            # Nested to loop to check collisions between missiles and enemies
            i = 0
            while i < len(enemies):
                j=0
                while j < len(missiles):
                    if enemies[i].hit_by(missiles[j]):
                        del missiles[j]
                        # Sound effect for hitting enemies
                        #enemyHit.play()
                        # Reduces health of enemies and then destroys them if health is gone
                        enemies[i].health-=bulletDamage
                        if enemies[i].health <= 0:
                            del enemies[i]
                            score += level *10 +90
                            i -= 1
                            # Sound effect for enemies dying
                            #enemyKill.play()
                        break
                    j +=1
                i += 1

            i = 0
            while i < len(enemies):
                if spaceship.hit_by(enemies[i]):
                    del enemies[i]
                    health -= level *5 +10
                    # Sound effect for losing health
                    i -= 1
                i += 1

            pygame.draw.rect (screen, (200,0,50), ( (screenX-gameX)/2+10, (screenY-gameY)/2+10, health/maxHealth*300, 50 ) )
            screen.blit (fontOne.render("Level: " + str(level), True, (200,0,50)), ( (screenX)/2, (screenY-gameY)/2+10 ) )
            screen.blit (fontOne.render("Timer: " + str(round(levelDelay-time.time() + levelTimer,1)), True, (200,0,50)), ( (screenX)/2-30, (screenY-gameY)/2+75 ) )
            screen.blit (fontOne.render("Score: " + str(score), True, (200,0,50)), ( (screenX-gameX)/2+10, (screenY-gameY)/2+75 ) )
            pygame.display.update()

#-------------------------------------------------------------------------------------------------------------------------
# Game Mode - Debug
#-------------------------------------------------------------------------------------------------------------------------
            if pressedKeys[K_KP_PLUS] and time.time() > levelTimer+0.2:
                level += 1
                levelTimer = time.time()

#-------------------------------------------------------------------------------------------------------------------------
# Game Mode - Reset after death
#-------------------------------------------------------------------------------------------------------------------------
        totalScore += score
        score = 0

        spaceship.x = (screenX-spaceshipX)/2
        spaceship.y = (screenY + gameY) /2 -(spaceshipY*1.5)
        
        armour = 0
        engine = 0
        noseGun = 1
        rWingGun = 0
        lWingGun = 0

        enemies = []
        missiles = []
#-------------------------------------------------------------------------------------------------------------------------
# Game Mode - End of loop
#/////////////////////////////////////////////////////////////////////////////////////////////////////
#-------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------------
#/////////////////////////////////////////////////////////////////////////////////////////////////////
# Upgrade Mode - Start of loop
#-------------------------------------------------------------------------------------------------------------------------
    if pressedKeys[K_RETURN] and menuButton ==3:
        pygame.mixer.fadeout(300)
        pygame.mixer.music.load('music_track02.wav')
        pygame.mixer.music.play(-1)
        menu = False

        while True:
        #Set Framerate
            clock.tick(60)

            # Exit game process
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.quit()
                    pygame.display.quit()
                    sys.exit()

            pressedKeys = pygame.key.get_pressed()
            if pressedKeys[K_ESCAPE]:
                break
#-------------------------------------------------------------------------------------------------------------------------
# Upgrade Mode - Debug
#-------------------------------------------------------------------------------------------------------------------------
            if pressedKeys[K_F1]:
                lWingGun = 0
            if pressedKeys[K_F2]:
                lWingGun = 1
            if pressedKeys[K_F3]:
                lWingGun = 2
            if pressedKeys[K_F4]:
                lWingGun = 3

            if pressedKeys[K_F5]:
                noseGun = 0
            if pressedKeys[K_F6]:
                noseGun = 1
            if pressedKeys[K_F7]:
                noseGun = 2
            if pressedKeys[K_F8]:
                noseGun = 3

            if pressedKeys[K_F9]:
                rWingGun = 0
            if pressedKeys[K_F10]:
                rWingGun = 1
            if pressedKeys[K_F11]:
                rWingGun = 2
            if pressedKeys[K_F12]:
                rWingGun = 3

            if pressedKeys[K_u]:
                armour = 0
            if pressedKeys[K_i]:
                armour = 1
            if pressedKeys[K_o]:
                armour = 2
            if pressedKeys[K_p]:
                armour = 3

            if pressedKeys[K_h]:
                engine = 0
            if pressedKeys[K_j]:
                engine = 1
            if pressedKeys[K_k]:
                engine = 2
            if pressedKeys[K_l]:
                engine = 3

#-------------------------------------------------------------------------------------------------------------------------
# Upgrade Mode - End of loop
#/////////////////////////////////////////////////////////////////////////////////////////////////////
#-------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------------
# Main Game Loop - End of loop
#/////////////////////////////////////////////////////////////////////////////////////////////////////
#-------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------------
# End of Code
#/////////////////////////////////////////////////////////////////////////////////////////////////////
#-------------------------------------------------------------------------------------------------------------------------
