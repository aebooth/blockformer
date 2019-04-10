import pygame
import random
import time
from pygame.locals import (K_SPACE, K_a, K_d, K_s, K_w, K_b, K_y)

class Window:
    def __init__(self,width=700,height=500,screen_width=700,screen_height=500,frames_per_second=60,title="my game"):
        pygame.init()
        pygame.key.set_repeat(1, 1000//frames_per_second)
        self.screen = pygame.display.set_mode((screen_width,screen_height))
        pygame.display.set_caption(title)
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.left_bound = 0
        self.lower_bound = 0
        self.clock = pygame.time.Clock()
        self.frames_per_second = frames_per_second
        self.player_sprite = None
        self.hbar_sprite = None
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
        self.screen.fill((255,255,255))

    def draw(self):
        self.current_level().draw()
        self.player_sprite.draw()
        self.hbar_sprite.draw()

    def update(self, **kwargs):
        self.player_sprite.update(**kwargs)
        self.current_level().update(**kwargs)
        
        player_old_vx = self.player_sprite.vx
        player_old_vy = self.player_sprite.vy
        self.player_sprite.vx //= 10
        self.player_sprite.vy //= 10
        old_vxs = []
        old_vys = []
        for sprite in self.current_level().sprites():
            old_vxs.append(sprite.vx)
            old_vys.append(sprite.vy)
            sprite.vx //= 10
            sprite.vy //= 10

        num_substeps_completed = 0    
        for i in range(10):
            self.player_sprite.move()
            self.current_level().move_all()
            self.player_sprite.collide(self.current_level().sprites())
            for sprite in self.current_level().sprites():
                sprite.collide(self.player_sprite)

        self.player_sprite.vx = player_old_vx - 10 * self.player_sprite.vx
        self.player_sprite.vy = player_old_vy - 10 * self.player_sprite.vy
        for i in range(len(self.current_level().sprites())):
            self.current_level().sprites[i].vx = old_vxs[i] - 10 * self.current_level().sprites[i].vx
            self.current_level().sprites[i].vy = old_vys[i] - 10 * self.current_level().sprites[i].vy
        self.player_sprite.move()
        self.current_level().move_all()

        self.player_sprite.vx = player_old_vx
        self.player_sprite.vy = player_old_vy
        for i in range(len(self.current_level().sprites())):
            self.current_level().sprites[i].vx = old_vxs[i]
            self.current_level().sprites[i].vy = old_vys[i]


        self.hbar_sprite.update(**kwargs)
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

    def sprites(self):
        return self.platforms + self.background + self.enemies

    def move_all(self):
        for sprite in (self.background+self.platforms+self.enemies):
            sprite.move()

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

    def move(self):
        self.x = self.x + self.vx
        self.y = self.y + self.vy
        self.rect.x = self.window.screen_x(self.x)
        self.rect.y = self.window.screen_y(self.y)

    def draw(self):
        self.window.screen.blit(self.image,self.rect)

    def collide(self, sprites):
        return False

    def on_collision(self,sprite):
        #Floor and Ceiling
        if self.rect.collide == bt or self.rect.collide == tb:
            self.y = -self.vy/10
            self.vy = 0

        #Left Wall and Right Wall
        if self.rect.collide == rl or self.rect.collide == lr:
            self.x = -self.vx/10
            self.vx = 0

    def update(self,**kwargs):
        pass

class Player(Sprite):
    def __init__(self,window,x,y,width=20,height=40,color=(200,0,255),health=100):
        Sprite.__init__(self,window,x,y,width,height,color)
        self.current_num_jumps = 0
        self.max_upward = 10
        self.max_forward = 5
        self.max_downward = -10
        self.x = x
        self.y = y
        self.frictionv = .88
        self.health = 100
        self.breath = 0
    def gravity(self):
        if self.vy > self.max_downward:
            self.vy = self.vy - .5
        else:
            self.vy = self.max_downward

    def friction(self):
        if self.current_num_jumps == 0:
            if self.vx > 1 or self.vx < -1:
                self.vx = self.vx * self.frictionv
            else:
                self.vx = 0
        if self.current_num_jumps >= 0:
            if self.vx > self.max_forward:
                self.vx = self.max_forward
            if self.vx < -self.max_forward:
                self.vx = -self.max_forward

    def dead(self):
        if self.health > 100:
            self.health = 100
        if self.health <= 0:
            pygame.quit()

    def update(self,**kwargs):
        # print("Health:",self.health,"Breath:",self.breath,"Coord:",self.x,self.y,"Speed:",self.vx,self.vy)
        for event in pygame.event.get(): pass
        key = pygame.key.get_pressed()
        if key[K_y]:
            self.vy = 10
        if key[K_SPACE] or key[K_w]:
            if self.current_num_jumps <= 7:
                if self.vx > 6 or self.vx < -6:
                    self.vy = self.max_upward + 1
                    self.current_num_jumps = self.current_num_jumps + 1
                else:
                    self.vy = self.max_upward
                    self.current_num_jumps = self.current_num_jumps + 1
        if key[K_a]:
            if key[K_b]:
                if self.current_num_jumps <= 1:
                    self.vx = self.vx - 1.2
                else:
                    self.vx = self.vx - .3
            elif self.current_num_jumps <= 1:
                self.vx = self.vx - 1.05
            else:
                self.vx = self.vx - .5
        if key[K_d]:
            if key[K_b]:
                if self.current_num_jumps <= 1:
                    self.vx = self.vx + 1.2
                else:
                    self.vx = self.vx + .3
            elif self.current_num_jumps <= 1:
                self.vx = self.vx + 1.05
            else:
                self.vx = self.vx + .5
        if key[K_s]:
            if self.current_num_jumps == 0:
                self.vx *= .75
            else:
                self.vy = -12
                self.current_num_jumps = 8
        if key[K_b]:
            self.max_forward = 10
        elif not key[K_b]:
            self.max_forward = 6
            pygame.event.clear()
        self.dead()
        self.gravity()
        self.friction()
        self.move()

    def on_collision(self,sprite):
        if isinstance(sprite,Platform):
            self.current_num_jumps = 0
            return True

        if isinstance(sprite,MovingPlatform):
            self.vx = self.motion.vx
            self.vy = self.motion.vy
            self.move()
            return True

        return False

class BadGuy(Sprite):
    def __init__(self,window,x,y,width=20,height=40,color=(255,0,0),motion=None):
        Sprite.__init__(self,window,x,y,width,height,color)
        self.motion = motion

    def collide(self, sprites):
        collided = False
        for sprite in sprites:
            if sprite.rect.colliderect(self.rect):
                sprite.on_collision(self)
                self.on_collision(sprite)
                collided = True
        return collided
                

    def on_collision(self,sprite):
        if isinstance(sprite,Player):
            sprite.health -= 10
            return True
        return False

    def update(self,**kwargs):
        # self.motion.move(self)
        self.collide([self.window.player_sprite])

class Hbar(Sprite):
    def __init__(self,window,x,y,width,height=20,color=(0,255,0)):
        Sprite.__init__(self,window,x,y,width,height,color)
        self.width = 0
    def stat_display(self,Player):
        self.width = 100
    def update(self, **kwargs):
        self.stat_display([self.window.player_sprite])

class Platform(Sprite):
    def __init__(self,window,x,y,width=80,height=20,color=(0,255,0)):
        Sprite.__init__(self,window,x,y,width,height,color)
        self.height = height
    
    def collide(self, sprites):
        return False
        # for sprite in sprites:
        #     if sprite.rect.colliderect(self.rect):
        #         sprite.on_collision(self)
        #         #Move sprite to top
        #         if sprite.rect.bottom <= self.rect.bottom or sprite.rect.bottom >= self.rect.bottom:
        #             sprite.move(0,-self.rect.top + sprite.rect.bottom)
        #             sprite.vy = 0
        #         #Move sprite to bottom
        #         if sprite.rect.top >= self.rect.centery:
        #             sprite.move(0, -self.rect.bottom + sprite.rect.top)
        #             sprite.vy = 0
        #         if sprite.rect.centery >= self.rect.top or sprite.rect.centery <= self.rect.bottom:
        #             #Move sprite to left
        #             if sprite.rect.centerx <= self.rect.left:
        #                 sprite.move(self.rect.left - sprite.rect.right,0)
        #                 sprite.vx = 0
        #             #Move sprite to right
        #             elif sprite.rect.centerx >= self.rect.right:
        #                 sprite.move(self.rect.right - sprite.rect.left,0)
        #                 sprite.vx = 0

    def update(self,**kwargs):
        self.collide([self.window.player_sprite])

class Water(Sprite):
    def __init__(self,window,x,y,width=80,height=20,color=(0,255,0)):
        Sprite.__init__(self,window,x,y,width,height,color)

    def collide(self, sprites):
        collided = False
        for sprite in sprites:
            if sprite.rect.colliderect(self.rect):
                sprite.breath += 1
                sprite.on_collision(self)
                sprite.max_upward = 5
                sprite.max_downward = -3
                sprite.max_forward = 4
                sprite.frictionv = .82
                sprite.current_num_jumps = 0
                if sprite.breath >= 540:
                    sprite.health -= 10
                    sprite.breath = 0
                collided = True
            else:
                sprite.breath -= 2
                if sprite.breath < 0:
                    sprite.breath = 0
                sprite.max_upward = 10
                sprite.max_downward = -10
                sprite.max_forward = 5
                sprite.frictionv = .88
            return collided

    def update(self,**kwargs):
        self.collide([self.window.player_sprite])

class DeathBarrier(Sprite):
    def __init__(self,window,x,y,width=80,height=30,color=(0,200,0)):
        Sprite.__init__(self,window,x,y,width,height,color)

    def collide(self, sprites):
        collided = False
        for sprite in sprites:
            if sprite.rect.colliderect(self.rect):
                sprite.on_collision(self)
                self.on_collision(sprite)
                collided = True
        return collided

    def on_collision(self,sprite):
        if isinstance(sprite,Player):
            sprite.health -= 10
            sprite.vy = 20
            return True
        return False    

    def update(self,**kwargs):
        self.collide([self.window.player_sprite])

class Heal(Sprite):
    def __init__(self,window,x,y,width=80,height=30,color=(0,200,0)):
        Sprite.__init__(self,window,x,y,width,height,color)

    def collide(self, sprites):
        collided = False
        for sprite in sprites:
            if sprite.rect.colliderect(self.rect):
                sprite.on_collision(self)
                self.on_collision(sprite)
                collided = True
        return collided

    def on_collision(self,sprite):
        if isinstance(sprite,Player):
            sprite.health += 50
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
    
    def move_sprite(self,sprite):
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
    def __init__(self,window,motion,x,y,width=80,height=20,color=(0,255,0)):
        Platform.__init__(self,window,x,y,width,height,color)
        self.motion = motion

    def update(self,**kwargs):
        super().collide([self.window.player_sprite])

    def move(self):
        self.motion.move(self)



if __name__ == '__main__':
    pass