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
fontTwo = pygame.font.Font("2015 Cruiser Bold Italic.otf", 20)
fontHelp = pygame.font.Font("2015 Cruiser Bold Italic.otf", 30)

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
# Load in background images
menuBackground_image = pygame.image.load("GameBackground.png")
gameBackground_image = pygame.image.load("GameBackground.png")
backgroundX, backgroundY = gameBackground_image.get_size()
backgroundScroll = 0

#-------------------------------------------------------------------------------------------------------------------------
# Define Images, Variables, and Class for Spaceship
#-------------------------------------------------------------------------------------------------------------------------
spaceship_image = pygame.image.load("Spaceship.png")
spaceshipX, spaceshipY = spaceship_image.get_size()

armour_image = ["",
pygame.image.load("Armour1.png"),
pygame.image.load("Armour2.png"),
pygame.image.load("Armour3.png")
]

engine_image = ["",
pygame.image.load("Engine1.png"),
pygame.image.load("Engine2.png"),
pygame.image.load("Engine3.png")
]

noseGun_image = ["",
pygame.image.load("NoseGun1.png"),
pygame.image.load("NoseGun2.png"),
pygame.image.load("NoseGun3.png")
]

rWingGun_image = ["",
pygame.image.load("RWingGun1.png"),
pygame.image.load("RWingGun2.png"),
pygame.image.load("RWingGun3.png")
]

lWingGun_image = ["",
pygame.image.load("LWingGun1.png"),
pygame.image.load("LWingGun2.png"),
pygame.image.load("LWingGun3.png")
]

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

#     1100    approx for clearing L1
#     9000    approx for clearing L5
#   30k        approx for clearing L10
#   75k        approx for clearing L15
# 170k        approx for clearing L20
# 350k        approx for clearing L25
armourCost =[100, 300, 500]
engineCost =[100, 300, 500]
nGunCost =[0, 300, 500]
rGunCost =[30000, 300, 500]
lGunCost =[30000, 300, 500]

class Spaceship:
    def __init__(self):
        self.x = (screenX-spaceshipX)/2
        self.y = (screenY + gameY) /2 -(spaceshipY*1.5)

    def draw(self):
        if noseGun > 0:
            screen.blit(noseGun_image[noseGun], (self.x, self.y))
        if rWingGun > 0:
            screen.blit(rWingGun_image[rWingGun], (self.x, self.y))
        if lWingGun > 0:
            screen.blit(lWingGun_image[lWingGun], (self.x, self.y))
        screen.blit(spaceship_image, (self.x, self.y))
        if engine > 0:
            screen.blit(engine_image[engine], (self.x, self.y))
        if armour > 0:
            screen.blit(armour_image[armour], (self.x, self.y))

    def move(self):
        if pressedKeys[K_w] and self.y > (screenY - gameY)/2 + ((engine+1)**1.4*4*1.3):
            self.y -= (engine+1)**1.4*4*0.7
        elif pressedKeys[K_w]:
            self.y = (screenY - gameY)/2

        if pressedKeys[K_s] and self.y < (screenY + gameY)/2 -spaceshipY-((engine+1)**1.4*4*1.3):
            self.y += (engine+1)**1.4*4*1.3
        elif pressedKeys[K_s]:
            self.y = (screenY + gameY)/2 - spaceshipY

        if pressedKeys[K_d] and self.x < (screenX + gameX)/2 -spaceshipX-((engine+1)**1.4*4):
            self.x += (engine+1)**1.4*4
        elif pressedKeys[K_d]:
            self.x = (screenX + gameX)/2 -spaceshipX

        if pressedKeys[K_a] and self.x > (screenX - gameX)/2 + ((engine+1)**1.4*4):
            self.x -= (engine+1)**1.4*4
        elif pressedKeys[K_a]:
            self.x = (screenX - gameX)/2

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
        self.y -= 20

#-------------------------------------------------------------------------------------------------------------------------
# Define Images List and Class for Explosions
#-------------------------------------------------------------------------------------------------------------------------
explosion = [
    pygame.image.load("Explosion1.png"),
    pygame.image.load("Explosion2.png"),
    pygame.image.load("Explosion3.png"),
    pygame.image.load("Explosion4.png"),
    pygame.image.load("Explosion5.png"),
    pygame.image.load("Explosion6.png"),
    pygame.image.load("Explosion7.png"),
    pygame.image.load("Explosion8.png"),
    pygame.image.load("Explosion9.png"),
    pygame.image.load("Explosion10.png"),
    pygame.image.load("Explosion11.png"),
    pygame.image.load("Explosion12.png")
    ]

explosions = []

class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rot = random.randint(1,360)
        self.animation = 0

    def draw(self):
        explode = pygame.transform.rotate(explosion[self.animation], self.rot)
        explodeX, explodeY = explosion[0].get_size()
        screen.blit(explode, (self.x - (explodeX /2), self.y - (explodeY /2)))

#-------------------------------------------------------------------------------------------------------------------------
#Define Images, Variables, List, and Class for Enemies
#-------------------------------------------------------------------------------------------------------------------------
enemy1 = [
    pygame.image.load("AlienDrone1a.png"),
    pygame.image.load("AlienDrone1b.png"),
    pygame.image.load("AlienDrone1c.png"),
    pygame.image.load("AlienDrone1d.png")
    ]
enemy1X, enemy1Y = enemy1[0].get_size()

enemy2a = [
    pygame.image.load("AlienDrone2a.png"),
    pygame.image.load("AlienDrone2b.png"),
    pygame.image.load("AlienDrone2c.png"),
    pygame.image.load("AlienDrone2d.png")
    ]
enemy2b = [
    pygame.image.load("AlienDrone2e.png"),
    pygame.image.load("AlienDrone2f.png"),
    pygame.image.load("AlienDrone2g.png"),
    pygame.image.load("AlienDrone2h.png")
    ]
enemy2aX, enemy2aY = enemy2a[0].get_size()
enemy2bX, enemy2bY = enemy2b[0].get_size()

lastTimeEnemySpawned = 0
spawnDelay = 2.0

fireDelay = 4.0

enemies = []

class Enemies:
    def __init__(self, lvl):
        enemyType = random.randint(1,5)
        if enemyType != 1:
            self.type = 1
            self.health = (lvl**2) *5
            self.x = random.randint(  (screenX - gameX)/2+(enemy1X/2), (screenX + gameX) /2 - (enemy1X /2))
            self.y = -enemy1Y
        else:
            self.type = 2
            self.mode = 0
            self.health = (lvl**2) *5
            self.x = random.randint(  (screenX - gameX)/2+(enemy2aX/2), (screenX + gameX) /2 - (enemy2aX /2))
            self.y = -enemy2aY
            self.fireTimer = 0

        self.destinationY = 0
        self.destinationX = 0

        self.animation = 0

    def move(self):
        #Set flight patterns for enemies here
        self.destinationX += random.choice((-1,1))*self.destinationY*0.05
        self.destinationY += 0.005
        self.x += self.destinationX
        if self.type == 1 or (self.type == 2 and self.mode == 0):
            self.y += self.destinationY

        if self.type == 2 and self.mode == 0 and self.y> random.randint(200,600):
            self.mode = 1
            self.fireTimer = time.time()

    def bounce(self):
        # Change the direction of travel across the screen when an enemy hits the edge of the play area
        if self.type == 1:
            if (self.x < (screenX-gameX)/2+(enemy1X /2) and self.destinationX < 0) or (self.x > (screenX + gameX) /2 -(enemy1X /2) and self.destinationX >0):
                self.destinationX *= -1

        if self.type == 2:
            if self.mode == 0:
                if (self.x < (screenX-gameX)/2 + (enemy2aX /2) and self.destinationX <0) or (self.x > (screenX + gameX) /2 - (enemy2aX /2) and self.destinationX >0):
                    self.destinationX *= -1
            if self.mode == 1:
                if (self.x < (screenX-gameX)/2 + (enemy2bX /2) and self.destinationX <0) or (self.x > (screenX + gameX) /2 - (enemy2bX /2) and self.destinationX >0):
                    self.destinationX *= -1

    def draw(self):
        # renders the image to the screen
        if self.type == 1:
            screen.blit(enemy1[self.animation], (self.x-(enemy1X /2), self.y-(enemy1Y /2)))
            
        if self.type == 2:
            if self.mode == 0:
                screen.blit(enemy2a[self.animation], (self.x-(enemy2aX /2), self.y-(enemy2aY /2)))
            if self.mode == 1:
                screen.blit(enemy2b[self.animation], (self.x-(enemy2bX /2), self.y-(enemy2bY /2)))

    def hit_by(self, missile):
        if self.type == 1:
            return pygame.Rect(self.x - (enemy1X /2), self.y - (enemy1Y /2), enemy1X, enemy1Y).collidepoint((missile.x, missile.y))

        if self.type == 2:
            if self.mode ==0:
                return pygame.Rect(self.x - (enemy2aX /2), self.y - (enemy2aY /2), enemy2aX, enemy2aY).collidepoint((missile.x, missile.y))
            if self.mode ==1:
                return pygame.Rect(self.x - (enemy2bX /2), self.y - (enemy2bY /2), enemy2bX, enemy2bY).collidepoint((missile.x, missile.y))

    def fire(self):
        if time.time() - self.fireTimer > fireDelay:
            self.fireTimer = time.time()
            bombs.append(Bomb(self.x, self.y))

#-------------------------------------------------------------------------------------------------------------------------
# Define List and Class for bombs
#-------------------------------------------------------------------------------------------------------------------------
bomb = [
    pygame.image.load("Bomb1.png"),
    pygame.image.load("Bomb2.png"),
    pygame.image.load("Bomb3.png"),
    pygame.image.load("Bomb4.png"),
    pygame.image.load("Bomb5.png")
    ]
bombX, bombY = bomb[0].get_size()

bombs = []

class Bomb:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.animation =0

    def draw(self):
        pygame.draw.line(screen, (0,255,0), (self.x,self.y), (self.x, self.y+5), 1)
        screen.blit(bomb[self.animation], (self.x-(bombX /2), self.y-(bombY /2)))

    def move(self):
        self.y += 10

#-------------------------------------------------------------------------------------------------------------------------
# Set other game variables
#-------------------------------------------------------------------------------------------------------------------------
Button1_image = pygame.image.load("Button.png")
Button2_image = pygame.image.load("ButtonActive.png")
buttonX, buttonY = Button1_image.get_size()

clock = pygame.time.Clock()

score = 0
totalScore = 0
level = 1
maxLevel = 30 # Target level to beat in order to clear the game
levelTimer = 0
levelDelay = 60 # Counts in seconds
pauseTime = 0
menu = False
menuButton = 0
menu2 = False
helpMessage = True
toggle = True
select = True

autopilot = False
autodirection = 1

#-------------------------------------------------------------------------------------------------------------------------
#/////////////////////////////////////////////////////////////////////////////////////////////////////
# Main Game Loop - Start of loop
#-------------------------------------------------------------------------------------------------------------------------
while True:
    # Force Pygame to process the loop without needing to access events
    pygame.event.pump()
    # Set Framerate
    clock.tick(60)

    if menu == False:
        pygame.mixer.fadeout(300)
        pygame.mixer.music.load('music_track00.wav')
        pygame.mixer.music.play(-1)
        menu = True

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
        menuButton = 3  # Quit game
    if pressedKeys[K_d]:
        menuButton = 4  # Upgrades

    screen.blit (fontOne.render("Score: " + str(totalScore), True, (200,0,50)), ( (screenX-gameX)/2+10, (screenY-gameY)/2+10 ) )

    #   Draws the Menu Buttons
    if menuButton == 1:
        screen.blit(Button2_image, ((screenX-buttonX)/2, (screenY-buttonY)/2+100)) # Start Game Button
        screen.blit (fontTwo.render("Start Game", True, (10,10,10)), ((screenX-fontTwo.size("Start Game")[0])/2, (screenY-fontTwo.size("Start Game")[1])/2+100-2)) # font.size returns [width,height] of the (text)
    else:
        screen.blit(Button1_image, ((screenX-buttonX)/2, (screenY-buttonY)/2+100))
        screen.blit (fontTwo.render("Start Game", True, (10,10,10)), ((screenX-fontTwo.size("Start Game")[0])/2, (screenY-fontTwo.size("Start Game")[1])/2+100-4))

    if menuButton == 2:
        screen.blit(Button2_image, ((screenX-buttonX)/2-(buttonX*1.25), (screenY-buttonY)/2+225)) # Credits
        screen.blit (fontTwo.render("Credits", True, (10,10,10)), ((screenX-fontTwo.size("Credits")[0])/2-(buttonX*1.25), (screenY-fontTwo.size("Credits")[1])/2+225-2))
    else:
        screen.blit(Button1_image, ((screenX-buttonX)/2-(buttonX*1.25), (screenY-buttonY)/2+225))
        screen.blit (fontTwo.render("Credits", True, (10,10,10)), ((screenX-fontTwo.size("Credits")[0])/2-(buttonX*1.25), (screenY-fontTwo.size("Credits")[1])/2+225-4))

    if menuButton == 3:
        screen.blit(Button2_image, ((screenX-buttonX)/2, (screenY-buttonY)/2+350)) # Quit Game
        screen.blit (fontTwo.render("Quit Game", True, (10,10,10)), ((screenX-fontTwo.size("Quit Game")[0])/2, (screenY-fontTwo.size("Quit Game")[1])/2+350-2))
    else:
        screen.blit(Button1_image, ((screenX-buttonX)/2, (screenY-buttonY)/2+350))
        screen.blit (fontTwo.render("Quit Game", True, (10,10,10)), ((screenX-fontTwo.size("Quit Game")[0])/2, (screenY-fontTwo.size("Quit Game")[1])/2+350-4))

    if menuButton == 4:
        screen.blit(Button2_image, ((screenX-buttonX)/2+(buttonX*1.25), (screenY-buttonY)/2+225)) # Upgrades Button
        screen.blit (fontTwo.render("Upgrade", True, (10,10,10)), ((screenX-fontTwo.size("Upgrade")[0])/2+(buttonX*1.25), (screenY-fontTwo.size("Upgrade")[1])/2+225-2))
    else:
        screen.blit(Button1_image, ((screenX-buttonX)/2+(buttonX*1.25), (screenY-buttonY)/2+225))
        screen.blit (fontTwo.render("Upgrade", True, (10,10,10)), ((screenX-fontTwo.size("Upgrade")[0])/2+(buttonX*1.25), (screenY-fontTwo.size("Upgrade")[1])/2+225-4))

    # Sets the Help Message on or off and draws to the screen if needed
    if pressedKeys[K_F1]:
        if toggle:
            helpMessage =not helpMessage
            toggle = False
    else:
        toggle = True

    if helpMessage == True:
         screen.blit (fontHelp.render("Press F1 to toggle instructions", True, (255,255,255)), (0,0) )
         screen.blit (fontHelp.render("W", True, (255,255,255)), (0,50) )
         screen.blit (fontHelp.render("Move Up", True, (255,255,255)), (200,50) )
         screen.blit (fontHelp.render("S", True, (255,255,255)), (0,80) )
         screen.blit (fontHelp.render("Move Down", True, (255,255,255)), (200,80) )
         screen.blit (fontHelp.render("A", True, (255,255,255)), (0,110) )
         screen.blit (fontHelp.render("Move Left", True, (255,255,255)), (200,110) )
         screen.blit (fontHelp.render("D", True, (255,255,255)), (0,140) )
         screen.blit (fontHelp.render("Move Right", True, (255,255,255)), (200,140) )
         screen.blit (fontHelp.render("Enter", True, (255,255,255)), (0,190) )
         screen.blit (fontHelp.render("Select", True, (255,255,255)), (200,190) )

    pygame.display.update()

    # Exit game process
    if pressedKeys[K_RETURN] and menuButton ==3:
        pygame.mixer.quit()
        pygame.display.quit()
        sys.exit()

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
            # Force Pygame to process the loop without needing to access events
            pygame.event.pump()
            # Set Framerate
            clock.tick(60)

            pressedKeys = pygame.key.get_pressed()

            if time.time() - levelTimer > levelDelay:
                level += 1
                levelTimer = time.time()

            # Start Rendering to screen
            # Scrolls the background image and then renders it to the screen
            backgroundScroll +=1
            if (backgroundScroll > backgroundY):
                backgroundScroll = 0
            screen.blit(gameBackground_image, ((screenX-gameX)/2, (screenY-gameY)/2+backgroundScroll))
            screen.blit(gameBackground_image, ((screenX-gameX)/2, (screenY-gameY)/2+backgroundScroll-backgroundY))

            # Spawns new enemies if the timer has elapsed
            if time.time() - lastTimeEnemySpawned > spawnDelay-(level/(maxLevel +10)*spawnDelay): # Spawn delay goes to 0 at 10 levels past game completion.
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

            # Loop to fire move and draw for all enemies
            i = 0
            while i < len(enemies):
                enemies[i].move()
                enemies[i].bounce()
                enemies[i].draw()
                enemies[i].animation = (enemies[i].animation + 1) % 4
                if enemies[i].type == 2 and enemies[i].mode == 1:
                    enemies[i].fire()
                # Deletes enemies if they reach the bottom of the screen
                if enemies[i].y > (screenY + gameY)/2:
                    del enemies[i]
                    i -= 1
                # Check collisions between enemies and the player
                elif spaceship.hit_by(enemies[i]):
                    del enemies[i]
                    i -= 1
                    health -= level *5 +10
                    # Sound effect for losing health
                i += 1

            # Loop to move and draw all bombs
            e=0
            while e < len(bombs):
                bombs[e].move()
                bombs[e].draw()
                bombs[e].animation = (bombs[e].animation + 1) % len(bomb)
                # Check bombs are still in play or deletes them
                if bombs[e].y > (screenY + gameY)/2 +10:
                    del bombs[e]
                    e -= 1
                # Check collisions between bombs and player
                elif spaceship.hit_by(bombs[e]):
                    del bombs[e]
                    e-=1
                    health -= level *5 +10
                    # Sound effect for losing health
                e += 1

            # Nested to loop to check collisions between missiles and enemies
            i = 0
            while i < len(enemies):
                j=0
                while j < len(missiles):
                    if enemies[i].hit_by(missiles[j]):
                        explosions.append(Explosion(missiles[j].x, missiles[j].y))
                        del missiles[j]
                        # Sound effect for hitting enemies
                        #enemyHit.play()
                        # Reduces health of enemies and then destroys them if health is gone
                        enemies[i].health-=bulletDamage
                        if enemies[i].health <= 0:
                            del enemies[i]
                            score += level **2 +50
                            i -= 1
                            # Sound effect for enemies dying
                            #enemyKill.play()
                        break
                    j +=1
                i += 1

            # Loop to draw all explosions
            n=0
            while n < len(explosions):
                explosions[n].draw()
                explosions[n].animation += 1
                if explosions[n].animation > len(explosion)-1:
                    del explosions[n]
                    n -= 1
                n += 1

            # Draws masking borders around the play area: pygame.draw.rect(Surface, (r, g, b, transparency), (left, top, boxSize, boxSize), outlineThickness)
            pygame.draw.rect(screen, (backgroundColour), ( 0, 0, (screenX-gameX)/2, screenY ), 0)
            pygame.draw.rect(screen, (backgroundColour), ( (screenX+gameX)/2, 0, (screenX-gameX)/2, screenY ), 0)
            pygame.draw.rect(screen, (backgroundColour), ( (screenX-gameX)/2, 0, gameX, (screenY-gameY)/2 ), 0)
            pygame.draw.rect(screen, (backgroundColour), ( (screenX-gameX)/2, (screenY+gameY)/2, gameX, (screenY-gameY)/2 ), 0)

            # Draws Health Bar and stats
            pygame.draw.rect (screen, (200,0,50), ( (screenX-gameX)/2+10, (screenY-gameY)/2+10, health/maxHealth*(armour*75+200), 50 ) )
            screen.blit (fontOne.render("Level: " + str(level), True, (200,0,50)), ( (screenX+gameX-fontOne.size("Timer: 00.0")[0]-fontOne.size("Level: 00")[0])/2, (screenY-gameY)/2+10 ) )
            screen.blit (fontOne.render("Timer: " + str(round(levelDelay-time.time() + levelTimer,1)), True, (200,0,50)), ( (screenX+gameX)/2-fontOne.size("Timer: 00.0")[0], (screenY-gameY)/2+75 ) )
            screen.blit (fontOne.render("Score: " + str(score), True, (200,0,50)), ( (screenX-gameX)/2+10, (screenY-gameY)/2+75 ) )

            # Sets the Help Message on or off and draws to the screen if needed
            if pressedKeys[K_F1]:
                if toggle:
                    helpMessage =not helpMessage
                    toggle = False
            else:
                toggle = True

            if helpMessage == True:
                 screen.blit (fontHelp.render("Press F1 to toggle instructions", True, (255,255,255)), (0,0) )
                 screen.blit (fontHelp.render("W", True, (255,255,255)), (0,50) )
                 screen.blit (fontHelp.render("Move Up", True, (255,255,255)), (200,50) )
                 screen.blit (fontHelp.render("S", True, (255,255,255)), (0,80) )
                 screen.blit (fontHelp.render("Move Down", True, (255,255,255)), (200,80) )
                 screen.blit (fontHelp.render("A", True, (255,255,255)), (0,110) )
                 screen.blit (fontHelp.render("Move Left", True, (255,255,255)), (200,110) )
                 screen.blit (fontHelp.render("D", True, (255,255,255)), (0,140) )
                 screen.blit (fontHelp.render("Move Right", True, (255,255,255)), (200,140) )
                 screen.blit (fontHelp.render("Enter", True, (255,255,255)), (0,190) )
                 screen.blit (fontHelp.render("Select", True, (255,255,255)), (200,190) )

            pygame.display.update()

#-------------------------------------------------------------------------------------------------------------------------
# Game Mode - Win Screen
#-------------------------------------------------------------------------------------------------------------------------

            if level > maxLevel:
                pass

#-------------------------------------------------------------------------------------------------------------------------
# Game Mode - Pause Menu
#-------------------------------------------------------------------------------------------------------------------------
            if pressedKeys [K_ESCAPE]:
                menuButton = 0
                pauseTime = time.time()
                while True:
                    # Force Pygame to process the loop without needing to access events
                    pygame.event.pump()
                    # Set Framerate
                    clock.tick(60)

                    # Refresh the game image
                    screen.blit(gameBackground_image, ((screenX-gameX)/2, (screenY-gameY)/2+backgroundScroll))
                    screen.blit(gameBackground_image, ((screenX-gameX)/2, (screenY-gameY)/2+backgroundScroll-backgroundY))
                    spaceship.draw()
                    j=0
                    while j < len(missiles):
                        missiles[j].draw()
                        j += 1
                    i = 0
                    while i < len(enemies):
                        enemies[i].draw()
                        i += 1
                    e=0
                    while e < len(bombs):
                        bombs[e].draw()
                        e += 1
                    n=0
                    while n < len(explosions):
                        explosions[n].draw()
                        n += 1
                    # Draws masking borders around the play area: pygame.draw.rect(Surface, (r, g, b, transparency), (left, top, boxSize, boxSize), outlineThickness)
                    pygame.draw.rect(screen, (backgroundColour), ( 0, 0, (screenX-gameX)/2, screenY ), 0)
                    pygame.draw.rect(screen, (backgroundColour), ( (screenX+gameX)/2, 0, (screenX-gameX)/2, screenY ), 0)
                    pygame.draw.rect(screen, (backgroundColour), ( (screenX-gameX)/2, 0, gameX, (screenY-gameY)/2 ), 0)
                    pygame.draw.rect(screen, (backgroundColour), ( (screenX-gameX)/2, (screenY+gameY)/2, gameX, (screenY-gameY)/2 ), 0)

                    # Draws Health Bar and stats
                    pygame.draw.rect (screen, (200,0,50), ( (screenX-gameX)/2+10, (screenY-gameY)/2+10, health/maxHealth*(armour*75+200), 50 ) )
                    screen.blit (fontOne.render("Level: " + str(level), True, (200,0,50)), ( (screenX+gameX-fontOne.size("Timer: 00.0")[0]-fontOne.size("Level: 00")[0])/2, (screenY-gameY)/2+10 ) )
                    screen.blit (fontOne.render("Timer: " + str(round(levelDelay-pauseTime + levelTimer,1)), True, (200,0,50)), ( (screenX+gameX)/2-fontOne.size("Timer: 00.0")[0], (screenY-gameY)/2+75 ) )
                    screen.blit (fontOne.render("Score: " + str(score), True, (200,0,50)), ( (screenX-gameX)/2+10, (screenY-gameY)/2+75 ) )

                    # Darkens the game while paused
                    pauseFade = pygame.Surface((gameX,gameY), pygame.SRCALPHA, 32)
                    pauseFade.fill((0, 0, 0, 150))
                    screen.blit(pauseFade, ((screenX-gameX)/2,(screenY-gameY)/2))


                    pressedKeys = pygame.key.get_pressed()

                    if pressedKeys[K_w]:
                        menuButton = 1  # Resume Game
                    if pressedKeys[K_a]:
                        menuButton = 2  # ????
                    if pressedKeys[K_s]:
                        menuButton = 3  # Quit to menu
                    if pressedKeys[K_d]:
                        menuButton = 4  # ????

                    if pressedKeys[K_RETURN] and menuButton ==1:
                        levelTimer += time.time()-pauseTime
                        break
                    if pressedKeys[K_RETURN] and menuButton ==3:
                        health = 0
                        break

                    #   Draws the Menu Buttons
                    if menuButton == 1:
                        screen.blit(Button2_image, ((screenX-buttonX)/2, (screenY-buttonY)/2+100)) # Resume Game Button
                        screen.blit (fontTwo.render("Resume Game", True, (10,10,10)), ((screenX-fontTwo.size("Resume Game")[0])/2, (screenY-fontTwo.size("Resume Game")[1])/2+100-2))
                    else:
                        screen.blit(Button1_image, ((screenX-buttonX)/2, (screenY-buttonY)/2+100))
                        screen.blit (fontTwo.render("Resume Game", True, (10,10,10)), ((screenX-fontTwo.size("Resume Game")[0])/2, (screenY-fontTwo.size("Resume Game")[1])/2+100-4))

                    if menuButton == 2:
                        screen.blit(Button2_image, ((screenX-buttonX)/2-(buttonX*1.25), (screenY-buttonY)/2+225)) # Credits
                        screen.blit (fontTwo.render("????", True, (10,10,10)), ((screenX-fontTwo.size("????")[0])/2-(buttonX*1.25), (screenY-fontTwo.size("????")[1])/2+225-2))
                    else:
                        screen.blit(Button1_image, ((screenX-buttonX)/2-(buttonX*1.25), (screenY-buttonY)/2+225))
                        screen.blit (fontTwo.render("????", True, (10,10,10)), ((screenX-fontTwo.size("????")[0])/2-(buttonX*1.25), (screenY-fontTwo.size("????")[1])/2+225-4))

                    if menuButton == 3:
                        screen.blit(Button2_image, ((screenX-buttonX)/2, (screenY-buttonY)/2+350)) # Quit Game
                        screen.blit (fontTwo.render("Quit to Menu", True, (10,10,10)), ((screenX-fontTwo.size("Quit to Menu")[0])/2, (screenY-fontTwo.size("Quit to Menu")[1])/2+350-2))
                    else:
                        screen.blit(Button1_image, ((screenX-buttonX)/2, (screenY-buttonY)/2+350))
                        screen.blit (fontTwo.render("Quit to Menu", True, (10,10,10)), ((screenX-fontTwo.size("Quit to Menu")[0])/2, (screenY-fontTwo.size("Quit to Menu")[1])/2+350-4))

                    if menuButton == 4:
                        screen.blit(Button2_image, ((screenX-buttonX)/2+(buttonX*1.25), (screenY-buttonY)/2+225)) # Upgrades Button
                        screen.blit (fontTwo.render("????", True, (10,10,10)), ((screenX-fontTwo.size("????")[0])/2+(buttonX*1.25), (screenY-fontTwo.size("????")[1])/2+225-2))
                    else:
                        screen.blit(Button1_image, ((screenX-buttonX)/2+(buttonX*1.25), (screenY-buttonY)/2+225))
                        screen.blit (fontTwo.render("????", True, (10,10,10)), ((screenX-fontTwo.size("????")[0])/2+(buttonX*1.25), (screenY-fontTwo.size("????")[1])/2+225-4))
                    # Sets the Help Message on or off and draws to the screen if needed
                    if pressedKeys[K_F1]:
                        if toggle:
                            helpMessage =not helpMessage
                            toggle = False
                    else:
                        toggle = True

                    if helpMessage == True:
                        screen.blit (fontHelp.render("Press F1 to toggle instructions", True, (255,255,255)), (0,0) )
                        screen.blit (fontHelp.render("W", True, (255,255,255)), (0,50) )
                        screen.blit (fontHelp.render("Move Up", True, (255,255,255)), (200,50) )
                        screen.blit (fontHelp.render("S", True, (255,255,255)), (0,80) )
                        screen.blit (fontHelp.render("Move Down", True, (255,255,255)), (200,80) )
                        screen.blit (fontHelp.render("A", True, (255,255,255)), (0,110) )
                        screen.blit (fontHelp.render("Move Left", True, (255,255,255)), (200,110) )
                        screen.blit (fontHelp.render("D", True, (255,255,255)), (0,140) )
                        screen.blit (fontHelp.render("Move Right", True, (255,255,255)), (200,140) )
                        screen.blit (fontHelp.render("Enter", True, (255,255,255)), (0,190) )
                        screen.blit (fontHelp.render("Select", True, (255,255,255)), (200,190) )

                    pygame.display.update()
#-------------------------------------------------------------------------------------------------------------------------
# Game Mode - Debug
#-------------------------------------------------------------------------------------------------------------------------
            if pressedKeys[K_KP_PLUS] and time.time() > levelTimer+0.2:
                level += 1
                levelTimer = time.time()

            if pressedKeys[K_KP_ENTER]:
                autopilot = True
            if pressedKeys[K_KP_PERIOD]:
                autopilot = False
            if autopilot == True:
                if spaceship.x > (screenX + gameX)/2 -spaceshipX-((engine+1)**1.4*4) or spaceship.x < (screenX - gameX)/2 + ((engine+1)**1.4*4):
                    autodirection *= -1
                spaceship.x += autodirection * ( (engine+1)**1.4*4)
                if time.time() - lastTimePlayerFired > firingDelay:
                    spaceship.fire()
                    lastTimePlayerFired = time.time()
        autopilot = False
#-------------------------------------------------------------------------------------------------------------------------
# Game Mode - Reset after death
#-------------------------------------------------------------------------------------------------------------------------
        totalScore += score
        score = 0

        menuButton = 0

        spaceship.x = (screenX-spaceshipX)/2
        spaceship.y = (screenY + gameY) /2 -(spaceshipY*1.5)

        armour = 0
        engine = 0
        noseGun = 1
        rWingGun = 0
        lWingGun = 0

        missiles = []
        explosions = []
        enemies = []
        bombs = []

#-------------------------------------------------------------------------------------------------------------------------
# Game Mode - End of loop
#/////////////////////////////////////////////////////////////////////////////////////////////////////
#-------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------------
#/////////////////////////////////////////////////////////////////////////////////////////////////////
# Upgrade Mode - Start of loop
#-------------------------------------------------------------------------------------------------------------------------
    if pressedKeys[K_RETURN] and menuButton ==4:
        pygame.mixer.fadeout(300)
        pygame.mixer.music.load('music_track02.wav')
        pygame.mixer.music.play(-1)
        menu = False
        menu2 = False
        menuButton = 0
        select = True

        while True:
            # Force Pygame to process the loop without needing to access events
            pygame.event.pump()
            # Set Framerate
            clock.tick(60)

            # Start Rendering to screen
            screen.fill(backgroundColour)
            # Draws the game surface area: pygame.draw.rect(Surface, (r, g, b, transparency), (left, top, boxSize, boxSize), outlineThickness)
            pygame.draw.rect(screen, (150,150,150), ( (screenX-gameX)/2, (screenY-gameY)/2, gameX, gameY ), 0)

            screen.blit (fontOne.render("Score: " + str(totalScore), True, (200,0,50)), ( (screenX-gameX)/2+10, (screenY-gameY)/2+10 ) )

            pressedKeys = pygame.key.get_pressed()

            if pressedKeys[K_w] and not menu2:
                menuButton = 1  # Weapons
            if pressedKeys[K_a] and not menu2:
                menuButton = 2  # Armour
            if pressedKeys[K_s] and not menu2:
                menuButton = 3  # Quit to menu
            if pressedKeys[K_d] and not menu2:
                menuButton = 4  # Thrusters

            if pressedKeys[K_w] and menu2:
                menuButton = 5  # Main Gun
            if pressedKeys[K_a] and menu2:
                menuButton = 6  # Left Gun
            if pressedKeys[K_s] and menu2:
                menuButton = 7  # Back
            if pressedKeys[K_d] and menu2:
                menuButton = 8  # Right Gun

            if pressedKeys[K_RETURN]:
                if menuButton == 1 and select:
                    menu2 = True
                    menuButton = 7
                    select = False

                if menuButton == 2 and select:
                    if  armour < 3 and totalScore > armourCost [armour]:
                        totalScore -= armourCost [armour]
                        armour += 1
                    select = False

                if menuButton == 3 and select:
                    break

                if menuButton == 4 and select:
                    if  engine < 3 and totalScore > engineCost [engine]:
                        totalScore -= engineCost [engine]
                        engine += 1
                    select = False

                if menuButton == 5 and select:
                    if  noseGun < 3 and totalScore > nGunCost [noseGun]:
                        totalScore -= nGunCost [noseGun]
                        noseGun += 1
                    select = False

                if menuButton == 6 and select:
                    if  lWingGun < 3 and totalScore > lGunCost [lWingGun]:
                        totalScore -= lGunCost [lWingGun]
                        lWingGun += 1
                    select = False

                if menuButton == 7 and select:
                    menu2 = False
                    menuButton = 1
                    select = False

                if menuButton == 8 and select:
                    if  rWingGun < 3 and totalScore > rGunCost [rWingGun]:
                        totalScore -= rGunCost [rWingGun]
                        rWingGun += 1
                    select = False

            else:
                select = True

            #   Draws the Menu Buttons
            if not menu2:
                if menuButton == 1:
                    screen.blit(Button2_image, ((screenX-buttonX)/2, (screenY-buttonY)/2+100)) # Weapons
                    screen.blit (fontTwo.render("Weapons", True, (10,10,10)), ((screenX-fontTwo.size("Weapons")[0])/2, (screenY-fontTwo.size("Weapons")[1])/2+100-2))
                else:
                    screen.blit(Button1_image, ((screenX-buttonX)/2, (screenY-buttonY)/2+100))
                    screen.blit (fontTwo.render("Weapons", True, (10,10,10)), ((screenX-fontTwo.size("Weapons")[0])/2, (screenY-fontTwo.size("Weapons")[1])/2+100-4))

            if menuButton == 2:
                screen.blit(Button2_image, ((screenX-buttonX)/2-(buttonX*1.25), (screenY-buttonY)/2+225)) # Armour
                screen.blit (fontTwo.render("Armour", True, (10,10,10)), ((screenX-fontTwo.size("Armour")[0])/2-(buttonX*1.25), (screenY-fontTwo.size("Armour")[1])/2+225-2))
            else:
                screen.blit(Button1_image, ((screenX-buttonX)/2-(buttonX*1.25), (screenY-buttonY)/2+225))
                screen.blit (fontTwo.render("Armour", True, (10,10,10)), ((screenX-fontTwo.size("Armour")[0])/2-(buttonX*1.25), (screenY-fontTwo.size("Armour")[1])/2+225-4))

            if menuButton == 3:
                screen.blit(Button2_image, ((screenX-buttonX)/2, (screenY-buttonY)/2+350)) # Menu
                screen.blit (fontTwo.render("Quit to Menu", True, (10,10,10)), ((screenX-fontTwo.size("Quit to Menu")[0])/2, (screenY-fontTwo.size("Quit to Menu")[1])/2+350-2))
            else:
                screen.blit(Button1_image, ((screenX-buttonX)/2, (screenY-buttonY)/2+350))
                screen.blit (fontTwo.render("Quit to Menu", True, (10,10,10)), ((screenX-fontTwo.size("Quit to Menu")[0])/2, (screenY-fontTwo.size("Quit to Menu")[1])/2+350-4))

            if menuButton == 4:
                screen.blit(Button2_image, ((screenX-buttonX)/2+(buttonX*1.25), (screenY-buttonY)/2+225)) # Thrusters
                screen.blit (fontTwo.render("Thrusters", True, (10,10,10)), ((screenX-fontTwo.size("Thrusters")[0])/2+(buttonX*1.25), (screenY-fontTwo.size("Thrusters")[1])/2+225-2))
            else:
                screen.blit(Button1_image, ((screenX-buttonX)/2+(buttonX*1.25), (screenY-buttonY)/2+225))
                screen.blit (fontTwo.render("Thrusters", True, (10,10,10)), ((screenX-fontTwo.size("Thrusters")[0])/2+(buttonX*1.25), (screenY-fontTwo.size("Thrusters")[1])/2+225-4))

            if menu2:
                if menuButton == 5:
                    screen.blit(Button2_image, ((screenX-buttonX)/2, (screenY-buttonY)/2+0)) # Main Gun
                    screen.blit (fontTwo.render("Main Gun", True, (10,10,10)), ((screenX-fontTwo.size("Main Gun")[0])/2, (screenY-fontTwo.size("Main Gun")[1])/2+0-2))
                else:
                    screen.blit(Button1_image, ((screenX-buttonX)/2, (screenY-buttonY)/2+0))
                    screen.blit (fontTwo.render("Main Gun", True, (10,10,10)), ((screenX-fontTwo.size("Main Gun")[0])/2, (screenY-fontTwo.size("Main Gun")[1])/2+0-4))

                if menuButton == 6:
                    screen.blit(Button2_image, ((screenX-buttonX)/2-(buttonX*1.25), (screenY-buttonY)/2+50)) # Left Wing
                    screen.blit (fontTwo.render("Left Gun", True, (10,10,10)), ((screenX-fontTwo.size("Left Gun")[0])/2-(buttonX*1.25), (screenY-fontTwo.size("Left Gun")[1])/2+50-2))
                else:
                    screen.blit(Button1_image, ((screenX-buttonX)/2-(buttonX*1.25), (screenY-buttonY)/2+50))
                    screen.blit (fontTwo.render("Left Gun", True, (10,10,10)), ((screenX-fontTwo.size("Left Gun")[0])/2-(buttonX*1.25), (screenY-fontTwo.size("Left Gun")[1])/2+50-4))

                if menuButton == 7:
                    screen.blit(Button2_image, ((screenX-buttonX)/2, (screenY-buttonY)/2+100)) # Back
                    screen.blit (fontTwo.render("Back", True, (10,10,10)), ((screenX-fontTwo.size("Back")[0])/2, (screenY-fontTwo.size("Back")[1])/2+100-2))
                else:
                    screen.blit(Button1_image, ((screenX-buttonX)/2, (screenY-buttonY)/2+100))
                    screen.blit (fontTwo.render("Back", True, (10,10,10)), ((screenX-fontTwo.size("Back")[0])/2, (screenY-fontTwo.size("Back")[1])/2+100-4))

                if menuButton == 8:
                    screen.blit(Button2_image, ((screenX-buttonX)/2+(buttonX*1.25), (screenY-buttonY)/2+50)) # Right Wing
                    screen.blit (fontTwo.render("Right Gun", True, (10,10,10)), ((screenX-fontTwo.size("Right Gun")[0])/2+(buttonX*1.25), (screenY-fontTwo.size("Right Gun")[1])/2+50-2))
                else:
                    screen.blit(Button1_image, ((screenX-buttonX)/2+(buttonX*1.25), (screenY-buttonY)/2+50))
                    screen.blit (fontTwo.render("Right Gun", True, (10,10,10)), ((screenX-fontTwo.size("Right Gun")[0])/2+(buttonX*1.25), (screenY-fontTwo.size("Right Gun")[1])/2+50-4))

            # Draws the Spaceship on the screen
            if noseGun > 0:
                ship = pygame.transform.rotozoom(noseGun_image[noseGun], -60,2.8)
                shipX, shipY = ship.get_size()
                screen.blit(ship, ((screenX - shipX) /2, (screenY - gameY)/2-100))
                  
            if rWingGun > 0:
                ship = pygame.transform.rotozoom(rWingGun_image[rWingGun], -60,2.8)
                shipX, shipY = ship.get_size()
                screen.blit(ship, ((screenX - shipX) /2, (screenY - gameY)/2-100))
                  
            if lWingGun > 0:
                ship = pygame.transform.rotozoom(lWingGun_image[lWingGun], -60,2.8)
                shipX, shipY = ship.get_size()
                screen.blit(ship, ((screenX - shipX) /2, (screenY - gameY)/2-100))
                  
            ship = pygame.transform.rotozoom(spaceship_image, -60,2.8)
            shipX, shipY = ship.get_size()
            screen.blit(ship, ((screenX - shipX) /2, (screenY - gameY)/2-100))
                  
            if engine > 0:
                ship = pygame.transform.rotozoom(engine_image[engine], -60,2.8)
                shipX, shipY = ship.get_size()
                screen.blit(ship, ((screenX - shipX) /2, (screenY - gameY)/2-100))
                  
            if armour > 0:
                ship = pygame.transform.rotozoom(armour_image[armour], -60,2.8)
                shipX, shipY = ship.get_size()
                screen.blit(ship, ((screenX - shipX) /2, (screenY - gameY)/2-100))
            
            # Sets the Help Message on or off and draws to the screen if needed
            if pressedKeys[K_F1]:
                if toggle:
                    helpMessage =not helpMessage
                    toggle = False
                else:
                    toggle = True

            if helpMessage == True:
                screen.blit (fontHelp.render("Press F1 to toggle instructions", True, (255,255,255)), (0,0) )
                screen.blit (fontHelp.render("W", True, (255,255,255)), (0,50) )
                screen.blit (fontHelp.render("Move Up", True, (255,255,255)), (200,50) )
                screen.blit (fontHelp.render("S", True, (255,255,255)), (0,80) )
                screen.blit (fontHelp.render("Move Down", True, (255,255,255)), (200,80) )
                screen.blit (fontHelp.render("A", True, (255,255,255)), (0,110) )
                screen.blit (fontHelp.render("Move Left", True, (255,255,255)), (200,110) )
                screen.blit (fontHelp.render("D", True, (255,255,255)), (0,140) )
                screen.blit (fontHelp.render("Move Right", True, (255,255,255)), (200,140) )
                screen.blit (fontHelp.render("Enter", True, (255,255,255)), (0,190) )
                screen.blit (fontHelp.render("Select", True, (255,255,255)), (200,190) )

            pygame.display.update()
#-------------------------------------------------------------------------------------------------------------------------
# Upgrade Mode - Debug
#-------------------------------------------------------------------------------------------------------------------------
            if pressedKeys[K_F2]:
                noseGun = 1
            if pressedKeys[K_F3]:
                noseGun = 2
            if pressedKeys[K_F4]:
                noseGun = 3

            if pressedKeys[K_F5]:
                lWingGun = 0
            if pressedKeys[K_F6]:
                lWingGun = 1
            if pressedKeys[K_F7]:
                lWingGun = 2
            if pressedKeys[K_F8]:
                lWingGun = 3

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
# Upgrade Mode - On exit to menu
#-------------------------------------------------------------------------------------------------------------------------
        menuButton = 0

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
