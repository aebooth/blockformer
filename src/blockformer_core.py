import pygame
import random
import time
import sys
from pygame.locals import *

#Animate1
def load_image(name):
    image = pygame.image.load(name)
    return image

class Window:
    def __init__(self,width=700,height=500,screen_width=700,screen_height=500,frames_per_second=60,title="my game"):
        pygame.init()
        pygame.key.set_repeat(1, 1000//frames_per_second)
        self.screen = pygame.display.set_mode((screen_width,screen_height))
        pygame.display.set_caption(title)
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height= screen_height
        self.left_bound = 0
        self.lower_bound = 0
        self.clock = pygame.time.Clock()
        self.frames_per_second = frames_per_second
        self.player_sprite = None
        self.hbar_sprite = None
        self.sbar_sprite = None
        self.bbar_sprite = None
        self.my_sprite = TestSprite()
        self.my_group = pygame.sprite.Group(self.my_sprite)
        self.current_level_index = 0
        self.levels = []
        self.levels.append(Level(self))

    def current_level(self):
        return self.levels[self.current_level_index]

    def screen_x(self,x):
        return x - self.left_bound

    def screen_y(self,y):
        return self.screen_height-(y-self.lower_bound)

    def x(self,x):
        return x

    def y(self,y):
        return self.height - y

    def advance_frame(self):
        pygame.display.flip()
        self.clock.tick(self.frames_per_second)

    def clear(self):
        # self.screen.fill((255,255,255))
        self.screen.fill((100,100,100))
    def draw(self):
        self.current_level().draw()
        self.player_sprite.draw()
        self.hbar_sprite.draw()
        self.sbar_sprite.draw()
        self.bbar_sprite.draw()
        self.my_group.draw(self.screen)

    def update(self, **kwargs):
        self.my_sprite.update(**kwargs)
        self.my_group.update(**kwargs)
        self.player_sprite.update(**kwargs)
        self.current_level().update(**kwargs)
        self.hbar_sprite.update(**kwargs)
        self.sbar_sprite.update(**kwargs)
        self.bbar_sprite.update(**kwargs)
        self.follow_player()

    def change_level(self, level_delta = 1):
        self.current_level_index = self.current_level_index + level_delta

    def follow_player(self):
        old_left = self.left_bound
        old_lower = self.lower_bound

        new_left = self.player_sprite.x-self.screen_width // 2
        if new_left < 0:
            self.left_bound = 0
        elif new_left > self.width-self.screen_width:
            self.left_bound = self.width-self.screen_width
        else:
            self.left_bound = new_left

        new_lower = self.player_sprite.y - 3*self.screen_height // 4
        if new_lower < 0:
            self.lower_bound = 0
        elif new_lower > self.height-self.screen_height:
            self.lower_bound = self.height-self.screen_height
        else:
            self.lower_bound = new_lower
        self.current_level().move_all()

    def start(self,*args):
        while True:
            if len(pygame.event.get(pygame.QUIT)) > 0:
                break

            # Do variable changing here
            self.update(*args)
            # Do screen clearing here
            self.clear()

            # Do drawing here
            self.draw()

            # Finish up frame
            self.advance_frame()
        pygame.quit()

class Level:
    def __init__(self,window):
        self.window = window
        self.background = []
        self.platforms = []
        self.enemies = []

    def move_all(self):
        for sprite in (self.background+self.platforms+self.enemies):
            sprite.rect.x = self.window.screen_x(sprite.x)
            sprite.rect.y = self.window.screen_y(sprite.y)

    def draw(self):
        for sprite in self.background:
            sprite.draw()
        for sprite in self.platforms:
            sprite.draw()
        for sprite in self.enemies:
            sprite.draw()

    def update(self,**kwargs):
        for sprite in self.background:
            sprite.update(**kwargs)
        for sprite in self.platforms:
            sprite.update(**kwargs)
        for sprite in self.enemies:
            sprite.update(**kwargs)

class Sprite:
    def __init__(self,window,x,y,width,height,color):
        self.window = window
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(window.screen_x(x), window.screen_y(y), width, height)
        self.image = pygame.Surface((width,height))
        self.image.fill(color)

    def move(self,dx,dy):
        self.x = self.x + dx
        self.y = self.y + dy
        self.rect.x = self.window.screen_x(self.x)
        self.rect.y = self.window.screen_y(self.y)

    def draw(self):
        self.window.screen.blit(self.image,self.rect)

    def collide(self, sprites):
        pass

    def on_collision(self,sprite):
        pass

    def update(self,**kwargs):
        pass

class Player(Sprite):
    def __init__(self,window,x,y,width=40,height=80,color=(200,0,255),health=200,shield=100):
        Sprite.__init__(self,window,x,y,width,height,color)
        self.current_num_jumps = 0
        self.max_upward = 10
        self.max_forward = 7
        self.max_downward = -16
        self.ground_friction = .86
        self.x = x
        self.y = y
        self.health = health
        self.shield = shield
        self.breath_timer = 600
        self.drown_timer = 300
        self.shield_timer = 0
        self.underwater = False
        self.dive = False
    def gravity(self):
        if self.vy > self.max_downward:
            self.vy = self.vy - .5
        else:
            self.vy = self.max_downward

    def friction(self):
        if self.current_num_jumps == 0:
            if self.vx > 1 or self.vx < -1:
                self.vx = self.vx * self.ground_friction
            else:
                self.vx = 0
        if self.current_num_jumps >= 0:
            if self.vx > self.max_forward:
                self.vx = self.max_forward
            if self.vx < -self.max_forward:
                self.vx = -self.max_forward

    def breathhold(self):
        if self.underwater == True:
            self.breath_timer -= 1
            if self.breath_timer <= 0:
                self.breath_timer = 0
                self.drown_timer -= 1
                if self.drown_timer <= 0:
                    self.health -= 20
                    self.drown_timer = 300
            else:
                self.drown_timer = 300
        elif self.underwater == False:
            self.breath_timer += 4
            if self.breath_timer > 600:
                self.breath_timer = 600

    def shieldregen(self):
        if self.shield_timer > 0:
            self.shield_timer -= 1
        elif self.shield_timer == 0:
            self.shield += 1

    def update(self,**kwargs):
        if self.health > 200:
            self.health = 200
        if self.health <= 0:
            pygame.quit()
        if self.shield > 100:
            self.shield = 100
        if self.shield < 0:
            self.shield = 0
        print("HP:",self.health,"Shield:",self.shield,self.shield_timer)
        for event in pygame.event.get(): pass
        key = pygame.key.get_pressed()
        if key[K_q]:
            print(self.x,self.y)
        if key[K_y]:
            self.vy = 10
        if key[K_RALT]:
            self.y = 100
            self.x = 1400
        if key[K_SPACE] or key[K_w] or key[K_UP]:
            if self.current_num_jumps <= 7:
                if self.vx > 6 or self.vx < -6:
                    self.vy = self.max_upward + 2
                    self.current_num_jumps = self.current_num_jumps + 1
                else:
                    self.vy = self.max_upward
                    self.current_num_jumps = self.current_num_jumps + 1
        if key[K_a] or key[K_LEFT]:
            if key[K_b]:
                if self.current_num_jumps <= 1:
                    self.vx = self.vx - 1.2
                else:
                    self.vx = self.vx - .3
            elif self.current_num_jumps <= 1:
                self.vx = self.vx - 1.05
            else:
                self.vx = self.vx - .4
        if key[K_d] or key[K_RIGHT]:
            if key[K_b]:
                if self.current_num_jumps <= 1:
                    self.vx = self.vx + 1.2
                else:
                    self.vx = self.vx + .3
            elif self.current_num_jumps <= 1:
                self.vx = self.vx + 1.05
            else:
                self.vx = self.vx + .4
        if key[K_s] or key[K_DOWN]:
            self.dive = True
            if self.current_num_jumps == 0:
                self.vx *= .75
            else:
                self.vy += self.max_downward
                self.current_num_jumps = 8
        if key[K_b]:
            self.max_forward = 10
            pygame.event.clear()
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.image = pygame.Surface((self.width,self.height))
        self.image.fill(self.color)
        self.shieldregen()
        self.breathhold()
        self.gravity()
        self.friction()
        self.move(self.vx,self.vy)

    def on_collision(self,sprite):
        if isinstance(sprite,Platform):
            self.current_num_jumps = 0
            self.max_forward = 7

        if isinstance(sprite,MovingPlatform):
            self.move(sprite.motion.vx,sprite.motion.vy)

class TestSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(TestSprite, self).__init__()
        self.images = []
        self.images.append(load_image('thump_stand_r96.png'))
        self.images.append(load_image('thump_stand_l96.png'))

        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(0, 480, 96, 96)
    # def position(self,sprites):
    #     for sprite in sprites:
    #         self.rect = pygame.Rect(sprite.x, sprite.y, 48, 48)

    def update(self, **kwargs):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]
        # self.position([self.window.player_sprite])

class BadGuy(Sprite):
    def __init__(self,window,x,y,width=40,height=80,color=(255,0,0),motion=None):
        Sprite.__init__(self,window,x,y,width,height,color)
        self.motion = motion

    def collide(self, sprites):
        for sprite in sprites:
            if sprite.rect.colliderect(self.rect):
                sprite.on_collision(self)
                self.on_collision(sprite)

    def on_collision(self,sprite):
        if isinstance(sprite,Player):
            sprite.shield_timer = 180
            sprite.shield -= 20
            if sprite.shield <= 0:
                sprite.health -= 20

    def update(self,**kwargs):
        self.motion.move(self)
        # if self.motion is not None:
        #     self.motion.move(self)
        self.collide([self.window.player_sprite])

class HUD(Sprite):
    def __init__(self,window,x,y,input,width=200,height=20,color=(0,200,0)):
        Sprite.__init__(self,window,x,y,width,height,color)
        self.width = width
        self.input = input
    def stat_display(self,sprites):
        for sprite in sprites:
            if self.input == "health":
                self.width = sprite.health
                if self.width > 200:
                    self.width = 200
            if self.input == "shield":
                self.width = sprite.shield
                if sprite.shield <= 9:
                    self.width = 1
                    self.y = -100
                else:
                    self.y = 5
                if self.width > 100:
                    self.width = 100
                if self.width%10 > 0:
                    self.width -= 1
            if self.input == "breath":
                self.color = (0,0,255)
                self.width = sprite.breath_timer/2
                if sprite.breath_timer >= 590:
                    self.y = -100
                else:
                    self.y = 25
                if self.width > 300:
                    self.width = 300
                if sprite.breath_timer <= 0:
                    self.color = (200,0,0)
                    self.width = sprite.drown_timer/2
    def update(self, **kwargs):
        self.stat_display([self.window.player_sprite])
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.image = pygame.Surface((self.width,self.height))
        self.image.fill(self.color)

class Platform(Sprite):
    def __init__(self,window,x,y,width=80,height=20,color=(50,50,50)):
        Sprite.__init__(self,window,x,y,width,height,color)
        self.height = height
        self.air_timer = 0
    def collide(self, sprites):
        for sprite in sprites:
            if sprite.rect.colliderect(self.rect):
                self.air_timer = 0
                sprite.on_collision(self)
                #Move sprite to top
                if sprite.rect.bottom <= self.rect.bottom and sprite.rect.bottom - sprite.vy < self.rect.bottom:
                    sprite.move(0,sprite.vy)
                    sprite.vy = 0
                #Move sprite to bottom
                if sprite.rect.top >= self.rect.centery:
                    sprite.move(0, -self.rect.bottom + sprite.rect.top)
                    sprite.vy = 0
                if sprite.rect.centery >= self.rect.top or sprite.rect.centery <= self.rect.bottom:
                    #Move sprite to left
                    if sprite.rect.centerx <= self.rect.left:
                        sprite.move(self.rect.left - sprite.rect.right,0)
                        sprite.vx = 0
                    #Move sprite to right
                    elif sprite.rect.centerx >= self.rect.right:
                        sprite.move(self.rect.right - sprite.rect.left,0)
                        sprite.vx = 0
            else:
                self.air_timer += 1
                if self.air_timer == 6:
                    sprite.current_num_jumps = 8

    def update(self,**kwargs):
        self.collide([self.window.player_sprite])

class Water(Sprite):
    def __init__(self,window,x,y,width=80,height=20,color=(0,0,255)):
        Sprite.__init__(self,window,x,y,width,height,color)

    def collide(self, sprites):
        for sprite in sprites:
            if sprite.rect.colliderect(self.rect):
                sprite.on_collision(self)
                sprite.max_upward = 5
                sprite.max_downward = -2
                sprite.max_forward = 4
                sprite.ground_friction = .82
                if sprite.dive == False and sprite.rect.top >= self.rect.top:
                    sprite.dive = True
                if sprite.dive == False and sprite.rect.centery-8 >= self.rect.top:
                    sprite.vy = 0
                    sprite.vy += .5
                    if sprite.vy > 1:
                        sprite.vy = 1
                if sprite.rect.centery >= self.rect.top:
                    sprite.current_num_jumps = 0
                if sprite.rect.centery-10 >= self.rect.top:
                    sprite.underwater = True
                elif sprite.rect.centery-10 <= self.rect.top:
                    sprite.underwater = False
                    sprite.dive = False
            else:
                sprite.underwater = False
                sprite.dive = False
                # sprite.max_forward = 7
                sprite.max_upward = 10
                sprite.max_downward = -12
                sprite.ground_friction = .86

    def update(self,**kwargs):
        self.collide([self.window.player_sprite])

class Bubbles(Sprite):
    def __init__(self,window,x,y,vx,vy,width=20,height=80,color=(0,200,0)):
        Sprite.__init__(self,window,x,y,width,height,color)
        self.vx = vx
        self.vy = vy

    def collide(self, sprites):
        for sprite in sprites:
            if sprite.rect.colliderect(self.rect):
                sprite.on_collision(self)
                sprite.breath_timer = 600
                # if self.vx != 0:
                sprite.vx += self.vx
                # if self.vy != 0:
                sprite.vy += self.vy

    def update(self,**kwargs):
        self.collide([self.window.player_sprite])

class DeathBarrier(Sprite):
    def __init__(self,window,x,y,width=80,height=30,color=(0,200,0)):
        Sprite.__init__(self,window,x,y,width,height,color)

    def collide(self, sprites):
        for sprite in sprites:
            if sprite.rect.colliderect(self.rect):
                sprite.on_collision(self)
                self.on_collision(sprite)

    def on_collision(self,sprite):
        if isinstance(sprite,Player):
            sprite.shield_timer = 180
            sprite.shield -= 20
            if sprite.shield <= 0:
                sprite.health -= 20
            sprite.vy = 15

    def update(self,**kwargs):
        self.collide([self.window.player_sprite])

class Heal(Sprite):
    def __init__(self,window,x,y,width=80,height=30,color=(0,200,0)):
        Sprite.__init__(self,window,x,y,width,height,color)

    def collide(self, sprites):
        for sprite in sprites:
            if sprite.rect.colliderect(self.rect):
                sprite.on_collision(self)
                self.on_collision(sprite)

    def on_collision(self,sprite):
        if isinstance(sprite,Player):
            sprite.health += 100
            self.y = -1000

    def update(self,**kwargs):
        self.collide([self.window.player_sprite])

class MotionSpecification:
    def __init__(self,window,left,right,bottom,top,vxi,vyi):
        self.left = left
        self.right = right
        self.top = window.y(top)
        self.bottom = window.y(bottom)
        self.vx = vxi
        self.vy = vyi
    
    def move(self,sprite):
        sprite.move(self.vx,self.vy)

        if sprite.x > self.right - sprite.width:
            sprite.move(-self.vx,0)
            self.vx = -self.vx
        elif sprite.x < self.left:
            sprite.move(-self.vx, 0)
            self.vx = -self.vx

        if sprite.y > self.bottom - sprite.height:
            sprite.move(0,-self.vy)
            self.vy = -self.vy
        elif sprite.y < self.top:
            sprite.move(0,-self.vy)
            self.vy = -self.vy

class MovingPlatform(Platform):
    def __init__(self,window,motion,x,y,width=80,height=20,color=(0,0,150)):
        Platform.__init__(self,window,x,y,width,height,color)
        self.motion = motion

    def update(self,**kwargs):
        self.motion.move(self)
        super().collide([self.window.player_sprite])



if __name__ == '__main__':
    pass