import pygame, sys, time
from pygame.locals import *
pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((640, 480))

text = []
text.append([
"This is the first text",
"This is the second text",
"This is the third text",
"This is the final text"
])
text.append([
"This is the fourth text",
"This is the fifth text",
"This is the sixth text",
"This is the final text"
])


class Typewriter:
    def __init__(self):
        self.message = 0
        self.letter = 0
        self.fontSize = 30
        self.font = pygame.font.Font(None, self.fontSize)
        self.lineGap = 5
        self.typeSpd = .2
        self.typeLast = time.time()
        
    def nextText(self,page):
        if self.message < len(text[page]):
            self.message +=1
            self.letter = 0

    def typing (self,page):
        n = 0
        while n < self.message:
            screen.blit (self.font.render(text[page][n], True, (255,0,155)), (0,(self.fontSize + self.lineGap)*n) )
            n +=1
        if self.message < len(text[page]):
            if self.letter < len (text[page][self.message])-1:
                screen.blit (self.font.render(text[page][self.message][:self.letter], True, (255,0,155)), (0,(self.fontSize + self.lineGap) * self.message) )
                if time.time() - self.typeLast > self.typeSpd:
                    self.letter +=1
                    self.typeLast = time.time()
            else:
                typewriter.nextText(page)

typewriter = Typewriter()


while True:
    pygame.event.pump()
    clock.tick(60)
    screen.fill((100,100,100))
    
    typewriter.typing(0)

    pygame.display.update()

    pressedKeys = pygame.key.get_pressed()
    if pressedKeys[K_RETURN]:
        break

while True:
    pygame.event.pump()
    clock.tick(60)
    screen.fill((100,100,100))
    
    typewriter.typing(1)

    pygame.display.update()

