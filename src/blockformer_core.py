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
        self.background = []
        self.foreground = []
        self.platforms = []
        self.enemies = []
        self.player_sprites = []

    def screen_x(self,x):
        return x - self.left_bound

    def screen_y(self,y):
        return self.screen_height-(y-self.lower_bound)

    def x(self,x):
        return x

    def y(self,y):
        return self.height - y

    def update_drawings(self):
        pass

    def advance_frame(self):
        pygame.display.flip()
        self.clock.tick(self.frames_per_second)

    def clear(self):
        self.screen.fill((255,255,255))

    def draw(self):
        for sprite in self.background:
            sprite.draw()
        for sprite in self.platforms:
            sprite.draw()
        for sprite in self.enemies:
            sprite.draw()
        for sprite in self.player_sprites:
            sprite.draw()
        for sprite in self.foreground:
            sprite.draw()

    def update(self,**kwargs):
        for sprite in self.background:
            sprite.update(**kwargs)
        for sprite in self.foreground:
            sprite.update(**kwargs)
        for sprite in self.player_sprites:
            sprite.update(**kwargs)
        for sprite in self.platforms:
            sprite.update(**kwargs)
        for sprite in self.enemies:
            sprite.update(**kwargs)

    def follow(self,player):
        pass

    def run(self,*args):
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
        # print(self.vx)
        # print(self.vy)
        # print()
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
                self.vx = -10
            if key == "d":
                self.vx = 10
            if key == "s":
                self.vy = -10
            pygame.event.clear()
        self.gravity()
        self.friction()
        self.move(self.vx,self.vy)

    def on_collision(self,sprite):
        if isinstance(sprite,Platform):
            self.current_num_jumps = 0


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
        self.collide(self.window.player_sprites)


if __name__ == '__main__':
    pass