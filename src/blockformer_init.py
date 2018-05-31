import pygame

from blockformer_core import *
#all game-specific classes and methods go here

class Hero(SmartSprite):
    def __init__(self,window):
        SmartSprite.__init__(self,window,width=20,height=20)

    def update(self, *args):
        #print(pygame.key.get_focused())
        for event in pygame.event.get(pygame.KEYDOWN):
            key = pygame.key.name(event.key).lower()
            if key =="w":
                self.vy = self.vy - 10
            if key == "a":
                self.vx = self.vx - 10
            if key == "d":
                self.vx = self.vx + 10
            if key =="s":
                self.vy = self.vy + 10
            pygame.event.clear()
        super(Hero, self).update()
        self.vx = 0
        self.vy = 0


if __name__ == '__main__':
    pass