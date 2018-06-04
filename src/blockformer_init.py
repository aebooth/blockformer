import pygame

from blockformer_core import *
#all game-specific classes and methods go here

class Hero(SmartSprite):
    def __init__(self,window):
        SmartSprite.__init__(self,window,width=20,height=20)
        self.frames = 0

    def update(self, *args):
        for event in pygame.event.get(pygame.KEYDOWN):
            key = pygame.key.name(event.key).lower()
            if key =="w":
                self.vy = self.vy + 10
            if key == "a":
                self.vx = self.vx - 10
            if key == "d":
                self.vx = self.vx + 10
            if key =="s":
                self.vy = self.vy - 10
            pygame.event.clear()
        # for collider in self.get_colliders(self.window.platforms):
        #     print("collider: " + str(collider.rect))
        #     print("self: " + str(self.drawable_sprite.rect))
        #     print()
        for vector in self.get_collide_vectors(self.window.platforms):
            if vector[1] < 0:
                self.vy = self.vy - vector[1]
        super(Hero, self).update()
        self.vx = 0
        self.vy = 0


    def gravity(self):
        pass


if __name__ == '__main__':
    pass