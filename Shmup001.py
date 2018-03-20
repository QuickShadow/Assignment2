import pygame, sys, random, time
from pygame.locals import *

# Set mixer defaults (frequency, size, channels, buffer
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()

# Load in sound files
#pygame.mixer.music.load('music_track00.wav')
#pygame.mixer.music.load('music_track01.wav')
#pygame.mixer.music.load('music_track02.wav')
#beep = pygame.mixer.Sound('beep.wav')
#shoot = pygame.mixer.Sound('shoot.wav')

# Load fonts
fontOne = pygame.font.Font("Barbarian NS.ttf", 50)
        # font has no numbers so score can't be displayed

# Set caption at top of screen
pygame.display.set_caption("Shmup")

# This function will create a full screen display Surface
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
screenX, screenY = pygame.display.get_surface().get_size()
# This sets the size of the game area
gameX = 1000
gameY = 1000

# Define colour as WHITE = (255, 255, 255)	
COLOUR = (255, 255, 255)

spaceship_image = pygame.image.load("Rocket.png")
spaceshipX, spaceshipY = spaceship_image.get_size()

enemy1_image = pygame.image.load("Invader.png").convert_alpha()
enemy1X, enemy1Y = enemy1_image.get_size()
enemy1_image.set_colorkey((255,255,255))


last_time_enemy_spawned = 0

clock = pygame.time.Clock()



class Enemies:

        # Give initial position
        # Move it downwards
        # Draw it!

        def __init__(self):
                self.x = random.randint((screenX - gameX)/2,(screenX + gameX) /2 -enemy1X)
                self.y = -enemy1Y
                # ACCELERATION
                self.dy = 0
                self.dx = 0

        def move(self):
                self.dy += 0.005
                self.dx += random.choice((-1,1))*self.dy*0.05
                #Set flight patterns for enemies here
                self.y += self.dy
                self.x += self.dx

        def bounce(self):
                if self.x < (screenX-gameX)/2 or self.x > (screenX + gameX) /2 -enemy1X:
                        self.dx *= -1

        def draw(self):
                screen.blit(enemy1_image, (self.x, self.y))

        def hit_by(self, missile):
                return pygame.Rect(self.x, self.y, 50, 50).collidepoint((missile.x, missile.y))




class Spaceship:

        def __init__(self):
                self.x = (screenX-spaceshipX)/2
                self.y = (screenY + gameY) /2 -(spaceshipY*1.5)

        def draw(self):
                screen.blit(spaceship_image, (self.x, self.y))

        def fire(self):
                missiles.append(Missile(self.x))
                #shoot.play()

        def move(self):
                if pressed_keys[K_RIGHT] and self.x < (screenX + gameX)/2 -spaceshipX:
                        self.x += 5
                if pressed_keys[K_LEFT] and self.x > (screenX - gameX)/2:
                        self.x -= 5
        def hit_by(self, enemies):
                return pygame.Rect(self.x, self.y, 50, 50).collidepoint((enemies.x, enemies.y))




class Missile:

        def __init__(self, x):
                self.x = spaceship.x + (spaceshipX /2)
                self.y = spaceship.y

        def draw(self):
                pygame.draw.line(screen, (255,0,0), (self.x,self.y), (self.x, self.y-5), 1) 

        def move(self):
                 self.y -= 10
                         


enemies = []
missiles = []

spaceship = Spaceship()

totalScore = 0
score = 0
menu = False

while 1:
        #SET FRAMERATE
        clock.tick(60)
        
        #Frame - Start Menu
        if menu == False:
                pygame.mixer.fadeout(300)
                pygame.mixer.music.load('music_track00.wav')
                pygame.mixer.music.play(-1)
                menu = True
                
        # EXIT PROCESS
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        pygame.mixer.quit()
                        pygame.display.quit()
                        sys.exit()
                        
        totalScore += score
        score = 0
        health = 100

        pressed_keys = pygame.key.get_pressed()

        #Start Game Mode
        #Frame - Game Loop
        if pressed_keys[K_RETURN]:
                pygame.mixer.fadeout(300)
                pygame.mixer.music.load('music_track01.wav')
                pygame.mixer.music.play(-1)
                menu = False
                
                while health > 0:
                        #SET FRAMERATE
                        clock.tick(60)
                        
                        # EXIT PROCESS
                        for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                        pygame.mixer.quit()
                                        pygame.display.quit()
                                        sys.exit()

                        pressed_keys = pygame.key.get_pressed()
                               
                        # RENDERING PROCESS
                        screen.fill(COLOUR)

                        if time.time() - last_time_enemy_spawned > 0.6:
                                enemies.append(Enemies())
                                last_time_enemy_spawned = time.time()

                         
                        spaceship.move()
                        spaceship.draw()

                        if pressed_keys[K_SPACE]:
                                spaceship.fire() 

                        j=0
                        while j < len(missiles):
                                missiles[j].move()
                                missiles[j].draw()
                                if missiles[j].y < (screenY - gameY)/2 -10:
                                        del missiles[j]
                                        j -= 1
                                j += 1


                        i = 0
                        while i < len(enemies):
                                enemies[i].move()		
                                enemies[i].draw()
                                enemies[i].bounce()
                                
                                if enemies[i].y > (screenY + gameY)/2:
                                        del enemies[i]
                                        i -= 1
                                i += 1

                        i = 0
                        while i < len(enemies):
                                j=0
                                while j < len(missiles):
                                        if enemies[i].hit_by(missiles[j]):
                                                del enemies[i]
                                                del missiles[j]
                                                score += 100
                                                i -= 1
                                                #beep.play()
                                                break
                                        j +=1
                                i += 1

                        i = 0
                        while i < len(enemies):
                            if spaceship.hit_by(enemies[i]):
                                del enemies[i]
                                health -= 10
                                i -= 1                     
                            i += 1

                        pygame.draw.rect(screen, (200,0,50), (10,10,health*3,50))
                        screen.blit(fontOne.render("Score: " + str(score), True, (200,0,50)), (350,5))
                        pygame.display.update() 

                        

