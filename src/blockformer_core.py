import pygame

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

    def update(self, **kwargs):
        self.player_sprite.update(**kwargs)
        self.current_level().update(**kwargs)
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
        while (True):
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
    def __init__(self,window,x,y,width=20,height=40,color=(0,0,0)):
        Sprite.__init__(self,window,x,y,width,height,color)
        self.current_num_jumps = 0

    def gravity(self):
        MAX_DOWNWARD = -10
        if self.vy > MAX_DOWNWARD:
            self.vy = self.vy - 1
        else:
            self.vy = MAX_DOWNWARD

    def friction(self):
        if self.current_num_jumps == 0:
            if self.vx > 1 or self.vx < -1:
                self.vx = self.vx * .8
            else:
                self.vx = 0


    def update(self,**kwargs):
        for event in pygame.event.get(pygame.KEYDOWN):
            key = pygame.key.name(event.key).lower()
            if key == "w":
                if self.current_num_jumps <= 7:
                    self.vy = 10
                    self.current_num_jumps = self.current_num_jumps + 1
            if key == "a":
                if self.current_num_jumps <= 1:
                    self.vx = -5
                else:
                    self.vx = -2
            if key == "d":
                if self.current_num_jumps <= 1:
                    self.vx = 5
                else:
                    self.vx = 2
            if key == "s":
                self.vy = -10
            pygame.event.clear()
        self.gravity()
        self.friction()
        self.move(self.vx,self.vy)

    def on_collision(self,sprite):
        if isinstance(sprite,Platform):
            self.current_num_jumps = 0

        if isinstance(sprite,MovingPlatform):
            self.move(sprite.motion.vx,sprite.motion.vy)


class Platform(Sprite):
    def __init__(self,window,x,y,width=80,height=20,color=(0,255,0)):
        Sprite.__init__(self,window,x,y,width,height,color)

    def collide(self, sprites):
        for sprite in sprites:
            if sprite.rect.colliderect(self.rect):
                sprite.on_collision(self)
                #Move sprite to top
                if sprite.rect.bottom <= self.rect.centery:
                    sprite.move(0,-self.rect.top + sprite.rect.bottom)
                    sprite.vy = 0
                #Move sprite to bottom
                if sprite.rect.top >= self.rect.centery:
                    sprite.move(0, -self.rect.bottom + sprite.rect.top)
                    sprite.vy = 0

                if sprite.rect.centery >= self.rect.top and sprite.rect.centery <= self.rect.bottom:
                    #Move sprite to left
                    if sprite.rect.centerx <= self.rect.left:
                        sprite.move(self.rect.left - sprite.rect.right,0)
                        sprite.vx = 0
                    #Move sprite to right
                    elif sprite.rect.centerx >= self.rect.right:
                        sprite.move(self.rect.right - sprite.rect.left,0)
                        sprite.vx = 0



    def update(self,**kwargs):
        self.collide([self.window.player_sprite])

class MotionSpecification:
    def __init__(self,window,left,right,top,bottom,vxi,vyi):
        self.left = left
        self.right = right
        self.top = window.y(top)
        self.bottom = window.y(bottom)
        self.vx = vxi
        self.vy = vyi

class MovingPlatform(Platform):
    def __init__(self,window,motion,x,y,width=80,height=20,color=(0,255,0)):
        Platform.__init__(self,window,x,y,width,height,color)
        self.motion = motion

    def update(self,**kwargs):
        self.move(self.motion.vx,self.motion.vy)
        if self.x > self.motion.right - self.width:
            self.move(-self.motion.vx,0)
            self.motion.vx = -self.motion.vx
        elif self.x < self.motion.left:
            self.move(-self.motion.vx, 0)
            self.motion.vx = -self.motion.vx

        if self.y > self.motion.bottom - self.height:
            self.move(0,-self.motion.vy)
            self.motion.vy = -self.motion.vy
        elif self.y < self.motion.top:
            self.move(0,-self.motion.vy)
            self.motion.vy = -self.motion.vy
        super().collide([self.window.player_sprite])



if __name__ == '__main__':
    pass