import pygame
import random
import time
from pygame.locals import *

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
        self.player_animations = None
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
        self.player_animations.draw()
        self.player_sprite.draw()
        self.hbar_sprite.draw()

    def update(self, **kwargs):
        self.player_animations.update(**kwargs)
        self.player_sprite.update(**kwargs)
        self.current_level().update(**kwargs)
        
        sprite_list = self.current_level().sprites()
        collision_indices = self.player_sprite.rect.collidelistall(sprite_list)
        for index in collision_indices:
            collision = self.player_sprite.collide(sprite_list[index])
            if collision is not None:
                self.player_sprite.on_collision(collision)
                sprite_list[index].on_collision(collision)

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
        return self.background + self.platforms + self.enemies

    def move_all(self):
        for sprite in self.sprites():
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
    def __init__(self,window,x,y,width,height,color,name="Sprite"):
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
        self.name = name

    def move(self, dx=None, dy=None):
        if dx == None or dy == None:
            self.x = self.x + int(self.vx)
            self.y = self.y + int(self.vy)
        else:
            self.x = self.x + dx
            self.y = self.y + dy
        self.rect.x = self.window.screen_x(self.x)
        self.rect.y = self.window.screen_y(self.y)
    

    def draw(self):
        self.window.screen.blit(self.image,self.rect)

    def get_collision_code(self, sprite):
        #corner cases
        #top left
        if self.rect.bottom <= sprite.rect.top and self.rect.right <= sprite.rect.left:
            return CollisionEvent(sprite,"brtl")
        #top right
        elif self.rect.bottom <= sprite.rect.top and self.rect.left >= sprite.rect.right:
            return CollisionEvent(sprite,"bltr")
        #bottom left
        elif self.rect.top >= sprite.rect.bottom and self.rect.right <= sprite.rect.left:
            return CollisionEvent(sprite,"trbl")
        #bottom right
        elif self.rect.top >= sprite.rect.bottom and self.rect.left >= sprite.rect.right:
            return CollisionEvent(sprite,"tlbr")
        #top and bottom middle cases
        if (self.rect.right < sprite.rect.right and self.rect.right > sprite.rect.left) or (self.rect.left < sprite.rect.right and self.rect.left > sprite.rect.left) or (self.rect.left <= sprite.rect.left and self.rect.right >= sprite.rect.right):
            #below
            if self.rect.bottom <= sprite.rect.top + 2:
                return CollisionEvent(sprite,"bbtt")
            #above
            if self.rect.top >= sprite.rect.bottom - 2:
                return CollisionEvent(sprite,"ttbb")
        #left and right middle cases
        if (self.rect.bottom < sprite.rect.bottom and self.rect.bottom > sprite.rect.top) or (self.rect.top < sprite.rect.bottom and self.rect.top > sprite.rect.top):
            #to the right
            if self.rect.left >= sprite.rect.right - 2:
                return CollisionEvent(sprite,"llrr")
            #to the left
            if self.rect.right <= sprite.rect.left + 2:
                return CollisionEvent(sprite,"rrll")
        else:
            print("Something broke with collision codes....")
            # pass

    def collide(self,sprite):
        #Move back to before we were colliding

        #Heres the slight modification that I made for the minimums
        if abs(self.vy) <= 1 and abs(self.vx) <= 1:
            self.move(-self.vx*2,-self.vy*2)
        elif abs(self.vx) <= 1:
            self.move(-self.vx*2,-self.vy)
        elif abs(self.vy) <= 1:
            self.move(-self.vx,-self.vy*2)
        else:
            self.move(-self.vx,-self.vy)
        sprite.move(-sprite.vx,-sprite.vy)
        

        player_old_vx = self.vx
        player_old_vy = self.vy
        self.vx //= 10
        self.vy //= 10
        sprite_old_vxs = sprite.vx
        sprite_old_vys = sprite.vy
        sprite.vx //= 10
        sprite.vy //= 10

        for i in range(10):
            self.move()
            sprite.move()
            collision = self.get_collision_code(sprite)
            if collision is not None:
                self.vx = player_old_vx
                self.vy = player_old_vy
                return collision

        self.vx = player_old_vx - 10 * self.vx
        self.vy = player_old_vy - 10 * self.vy
        sprite.vx = sprite_old_vxs - 10 * sprite.vx
        sprite.vy = sprite_old_vys - 10 * sprite.vy

        if abs(self.vy) <= 1 and abs(self.vx) <= 1:
            self.move(self.vx*2,self.vy*2)
        elif abs(self.vx) <= 1:
            self.move(self.vx*2,self.vy)
        elif abs(self.vy) <= 1:
            self.move(self.vx,self.vy*2)
        else:
            self.move(self.vx,self.vy)
        sprite.move()
        collision = self.get_collision_code(sprite)
        if collision is not None:
            return collision
        self.vx = player_old_vx
        self.vy = player_old_vy
        sprite.vx = sprite_old_vxs
        sprite.vy = sprite_old_vys

        return None
    
    def on_collision(self,CollisionEvent):
        pass
        

    def update(self,**kwargs):
        pass

class Player(Sprite):
    def __init__(self,window,x,y,width=40,height=80,color=(200,0,255),health=200):
        Sprite.__init__(self,window,x,y,width,height,color,name="Player")
        self.current_num_jumps = 0
        self.max_upward = 10
        self.max_forward = 4
        self.max_downward = -16
        self.frictionv = .8
        self.gravityv = .5
        self.health = 200
        self.breath = 0
    def gravity(self):
        if self.vy > self.max_downward:
            self.vy = self.vy - self.gravityv
        else:
            self.vy = self.max_downward

    def friction(self):
        if self.current_num_jumps == 0:
            if self.vx > 1 or self.vx < -1:
                self.vx = self.vx * self.frictionv
            else:
                self.vx = 0
    def terminal_velocity(self):
        if self.vx > self.max_forward:
            self.vx = self.max_forward
        if self.vx < -self.max_forward:
            self.vx = -self.max_forward

    def reset_values(self):
        if self.current_num_jumps == 0:
            self.max_upward = 10
            self.max_forward = 4
            self.max_downward = -16
            self.frictionv = .8
            self.gravityv = .5

    def update(self,**kwargs):
        if self.y < 0:
            pygame.quit()
        print(self.vx,self.vy)
        for event in pygame.event.get(): 
            pass
        key = pygame.key.get_pressed()
        if key[K_LALT]:
            self.x = 2900
            self.y = 480
        if key[K_q]:
            print(self.x, self.y)
        if key[K_y]:
            self.vy = 10
        if key[K_SPACE] or key[K_w] or key[K_UP]:
            if self.current_num_jumps <= 10:
                if self.vx > 5 or self.vx < -5:
                    self.vy = self.max_upward + 2
                elif self.vx > 3 or self.vx < -3:
                    self.vy = self.max_upward + 1
                else:
                    self.vy = self.max_upward
                self.current_num_jumps = self.current_num_jumps + 1
        if key[K_a] or key[K_LEFT]:
            if key[K_b]:
                if self.current_num_jumps <= 1:
                    self.vx = self.vx - 2
                else:
                    self.vx = self.vx - .25
            elif self.current_num_jumps <= 1:
                self.vx = self.vx - 1
            else:
                self.vx = self.vx - .5
        if key[K_d] or key[K_RIGHT]:
            if key[K_b]:
                if self.current_num_jumps <= 1:
                    self.vx = self.vx + 2
                else:
                    self.vx = self.vx + .25
            elif self.current_num_jumps <= 1:
                self.vx = self.vx + 1
            else:
                self.vx = self.vx + .5
        if key[K_s] or key[K_DOWN]:
            if self.current_num_jumps == 0:
                self.vx *= .6
            else:
                self.vy = -12
                self.current_num_jumps = 11
        if key[K_b]:
            # if self.current_num_jumps == 0:
            #     self.max_forward = 2
            # if self.current_num_jumps > 0:
            #     self.max_forward = 8
            # self.max_upward = 5
            # self.max_downward = -8
            # self.gravityv = .25
            self.max_forward = 6
            pygame.event.clear()
        if not key[K_0]:
            self.gravity()
        self.terminal_velocity()
        if not key[K_a] and not key[K_d]:
            self.friction()
        self.move()
        self.reset_values()

    def on_collision(self,collision_event):
        if isinstance(collision_event.sprite,Platform):
            #Corners
            # if collision_event.code == "brtl" or collision_event.code == "bltr":
            #     if abs(self.vx) > abs(self.vy):
            #         self.x += self.vx
            #         self.vy = 0
            #     else:
            #         self.y += self.vy
            #         self.vx = 0
            #Floor and Ceiling
            if collision_event.code == "bbtt":
                if self.vy < 0:
                    self.x += self.vx
                    self.y = collision_event.sprite.y + self.height
                    self.vy = 0
                    self.current_num_jumps = 0
            if collision_event.code == "ttbb":
                if self.vy > 0:
                    self.x += self.vx
                    self.y = collision_event.sprite.y - collision_event.sprite.height
                    self.vy = 0
            #Left Wall and Right Wall
            if collision_event.code == "rrll":
                if self.current_num_jumps == 0:
                    self.vx = 0        
                self.x = collision_event.sprite.x - self.width
                self.y += self.vy
            if collision_event.code == "llrr":
                if self.current_num_jumps == 0:
                    self.vx = 0
                self.x = collision_event.sprite.x + collision_event.sprite.width
                self.y += self.vy
                
            return True

        if isinstance(collision_event.sprite,MovingPlatform):
            self.vx = collision_event.sprite.motion.vx
            self.vy = collision_event.sprite.motion.vy
            self.move()
            return True
        if isinstance(collision_event.sprite,Water):
            self.x += self.vx
            self.y += self.vy
            self.vy = 0
            self.breath += 1
            self.max_upward = 5
            self.max_downward = -3
            self.max_forward = 4
            self.frictionv = .8
            self.current_num_jumps = 0
            if self.breath >= 5400:
                self.health -= 10
                self.breath = 0
            return True
        else:
            self.breath -= 2
            if self.breath < 0:
                self.breath = 0
            self.max_upward = 10
            self.max_downward = -10
            self.max_forward = 5
            self.frictionv = .88
            return False
        return False

class BadGuy(Sprite):
    def __init__(self,window,x,y,width=20,height=40,color=(255,0,0),motion=None):
        Sprite.__init__(self,window,x,y,width,height,color)
        self.motion = motion
                
class Hbar(Sprite):
    def __init__(self,window,x,y,width,height=1,color=(0,255,0)):
        Sprite.__init__(self,window,x,y,width,height,color)
        self.width = 0
    def stat_display(self,Player):
        self.width = 200
    def update(self, **kwargs):
        self.stat_display([self.window.player_sprite])

class Platform(Sprite):
    def __init__(self,window,x,y,width=80,height=20,color=(0,255,0),name="Platform"):
        Sprite.__init__(self,window,x,y,width,height,color,name="Platform")
        self.height = height

class Water(Sprite):
    def __init__(self,window,x,y,width=80,height=20,color=(0,255,0)):
        Sprite.__init__(self,window,x,y,width,height,color)

    def on_collision(self, sprite):
        collided = False
        if isinstance(sprite,Player):
            collided = True
        return collided

class DeathBarrier(Sprite):
    def __init__(self,window,x,y,width=80,height=30,color=(0,200,0)):
        Sprite.__init__(self,window,x,y,width,height,color)

    def on_collision(self,sprite):
        if isinstance(sprite,Player):
            sprite.health -= 10
            sprite.vy = 20
            return True
        return False    

class Heal(Sprite):
    def __init__(self,window,x,y,width=80,height=30,color=(0,200,0)):
        Sprite.__init__(self,window,x,y,width,height,color)

    def on_collision(self,collision_event):
        if isinstance(collision_event.sprite,Player):
            sprite.health += 50
            self.y = -1000


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

    # def update(self,**kwargs):
    #     self.move_sprite

class CollisionEvent:
    def __init__(self, sprite, code):
        self.sprite = sprite
        self.code = code

class AnimatedSprite(Sprite):
    def __init__(self, window, x, y,width=40,height=40,color=(0,0,0), animation=None, image=pygame.Surface((50,50))):
        Sprite.__init__(self,window,x,y,width,height,color)
        self.animations = {"default":animation}
        self.animation = self.animations["default"]
        self.image = image
        self.x = x
        self.y = y
        #The Sprite's rect represents its position in the viewport, not the window
        self.rect = pygame.Rect(self.x,self.y,self.image.get_rect().width,self.image.get_rect().height)
        self.window = window

    # don't override this
    # WARNING: Fails silently!!
    def set_active_animation(self, animation_name):
        if animation_name in self.animations:
            self.animation = self.animations[animation_name]
            self.image = self.animation.get_frame()

    # don't override this
    def animate(self):
        self.animation.advance()
        self.image = self.animation.get_frame()

    # override this
    def update(self):
        self.x = self.window.player_sprite.x
        self.y = self.window.player_sprite.y

class Spritesheet:
    def __init__(self,file_path,sprite_width,sprite_height,sprite_padding=0):
        self.sheet = pygame.image.load(file_path)
        self.sheet.convert()
        self.padding = sprite_padding
        self.sprite_rect = pygame.Rect(self.padding,self.padding,sprite_width,sprite_height)
        self.sequences = {}

    def add_sequence(self,name,start_row,num_frames):
        self.sprite_rect.y = start_row * (self.padding + self.sprite_rect.height)
        self.sprite_rect.x = self.padding
        frames = []
        for i in range(num_frames):
            frames.append(self.sheet.subsurface(self.sprite_rect))
            self.sprite_rect.move_ip(self.padding + self.sprite_rect.width , 0)
        self.sequences[name] = frames

class Animation:
    def __init__(self,frame_sequence):
        self.frames = frame_sequence
        self.current_frame = 0
        # Number of frames to wait before advancing
        self.advance_rate = 1
        self.frame_counter = 0

    def get_frame(self):
        return self.frames[self.current_frame]

    def advance(self):
        if self.frame_counter < self.advance_rate:
            self.frame_counter = self.frame_counter + 1
        else:
            self.current_frame = self.current_frame + 1
            if self.current_frame >= len(self.frames):
                self.current_frame = 0
            self.frame_counter = 0

if __name__ == '__main__':
    pass