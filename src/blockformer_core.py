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
        self.background = pygame.sprite.Group()
        self.foreground = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.sprites = pygame.sprite.Group()
        self.non_rendering_sprites = pygame.sprite.Group()

    def get_screen_x(self,x):
        return x - self.left_bound

    def get_screen_y(self,y):
        return self.screen_height-(y-self.lower_bound)

    def advance_frame(self):
        pygame.display.flip()
        self.clock.tick(self.frames_per_second)

    def clear(self):
        self.screen.fill((255,255,255))

    def draw(self):
        self.background.draw(self.screen)
        self.platforms.draw(self.screen)
        self.sprites.draw(self.screen)
        self.foreground.draw(self.screen)

    def update(self,*args):
        self.non_rendering_sprites.update(*args)
        self.background.update(*args)
        self.platforms.update(*args)
        self.sprites.update(*args)
        self.foreground.update(*args)

    def scroll(self,dx,dy):
        for sprite in self.background.sprites():
            sprite.drawable_sprite.rect.move_ip(dx,dy)
        self.platforms.draw(self.screen)
        self.sprites.draw(self.screen)
        self.foreground.draw(self.screen)

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


class SmartSprite(pygame.sprite.Sprite):
    N = 0
    NE = 1
    E = 2
    SE = 3
    S = 4
    SW = 5
    W = 6
    NW = 7
    ON_TOP = -1

    def __init__(self,window,x=0,y=0,width=1,height=1,mass=1):
        pygame.sprite.Sprite.__init__(self)
        self.window = window
        self.rect = pygame.Rect(x,y,width,height)
        self.vx = 0
        self.vy = 0
        self.mass = mass
        self.drawable_sprite = pygame.sprite.Sprite()
        self.drawable_sprite.rect = pygame.Rect(self.window.get_screen_x(self.rect.x),
                                                self.window.get_screen_y(self.rect.y)-self.rect.height,
                                                self.rect.width,
                                                self.rect.height)
        self.drawable_sprite.image = pygame.Surface((width,height))
        self.drawable_sprite.image.fill((0,0,0))

    def update(self, *args):
        self.rect.move_ip(self.vx,self.vy)
        self.drawable_sprite.rect.move_ip(self.vx,self.vy)

    def exert_force_on(self,other,force):
        other.vx = other.vx + int(force[0]/other.mass)
        other.vy = other.vy + int(force[1] / other.mass)

    # TODO
    def force_window_to_follow(self):
        destx = self.rect.x + self.rect.width // 2 - self.width // 2
        if destx < 0:
            self.rect.x = 0
        elif destx <= self.xmax:
            self.rect.x = destx
        else:
            self.rect.x = self.xmax

        desty = sprite.y + sprite.rect.height//2 - self.height//2
        if desty < 0:
            self.rect.y = 0
        elif desty <= self.ymax:
            self.rect.y = desty
        else:
            self.rect.y = self.ymax

    def get_collide_vectors(self,others):
        collider_vectors = []
        collisions = pygame.sprite.spritecollide(self, others, False)
        for i in range(len(collisions)):
            collider_vectors[i] = self.get_vector_to(others[i])
        return collider_vectors

    def get_collide_directions(self,others):
        collider_directions = []
        collisions = pygame.sprite.spritecollide(self,others,False)
        for i in range(len(collisions)):
            collider_directions[i] = self.get_direction_to(others[i])
        return collider_directions

    def get_collide_positions(self,others):
        collider_positions = []
        collisions = pygame.sprite.spritecollide(self, others, False)
        for i in range(len(collisions)):
            collider_positions[i] = self.get_relative_position(others[i])
        return collider_positions



    """
    Returns a tuple with the following make-up (top left corner code , bottom right corner code)
    
           0     1     2     3
        -------------------------
    0   | 00  | 01  | 02 | 03  |
        ------=============------
    1   | 10  [ 11  | 12  ] 13  |
        -------------------------
    2   | 20  [ 21  | 22  ] 23  |
        ------=============------
    3   | 30  | 31  | 32  | 33  |
        -------------------------
    
    The codes produced by this method are based on the box above. Codes 11,12,21,22 are within the 
    actual rect of the sprite
   
    """

    def get_relative_position(self,other):
        x = -1
        y = -1

        if other.rect.left > self.rect.right:
            x = 3
        elif other.rect.left <= self.rect.right and other.rect.left > self.rect.centerx:
            x = 2
        elif other.rect.left <= self.rect.centerx and other.rect.left > self.rect.left:
            x = 1
        else:
            x = 0

        if other.rect.top > self.rect.bottom:
            y = 30
        elif other.rect.top <= self.rect.bottom and other.rect.top > self.rect.centery:
            y = 20
        elif other.rect.top <= self.rect.centery and other.rect.top > self.rect.top:
            y = 10
        else:
            y = 0

        tl = y+x

        x = -1
        y = -1

        if other.rect.right > self.rect.right:
            x = 3
        elif other.rect.right <= self.rect.right and other.rect.right > self.rect.centerx:
            x = 2
        elif other.rect.right <= self.rect.centerx and other.rect.right > self.rect.left:
            x = 1
        else:
            x = 0

        if other.rect.bottom > self.rect.bottom:
            y = 30
        elif other.rect.bottom <= self.rect.bottom and other.rect.bottom > self.rect.centery:
            y = 20
        elif other.rect.bottom <= self.rect.centery and other.rect.bottom > self.rect.top:
            y = 10
        else:
            y = 0

        br = y+x

        return (tl,br)

    def get_direction_to(self,other):
        (tl,br) = self.get_relative_position(other)
        if (tl / 10 <= 1 and tl % 10 <= 1) and (br / 10 <= 1 and br % 10 <= 1):
            return SmartSprite.NW
        elif (tl / 10 >= 2 and tl % 10 >= 2) and (br / 10 >= 2 and br % 10 >= 2):
            return SmartSprite.SE
        elif (tl / 10 >= 2 and tl % 10 <= 1) and (br / 10 >= 2 and br % 10 <= 1):
            return SmartSprite.SW
        elif (tl / 10 <= 1 and tl % 10 >= 2) and (br / 10 <= 1 and br % 10 >= 2):
            return SmartSprite.NE
        elif tl / 10 <= 1 and br / 10 <= 1:
            return SmartSprite.N
        elif tl / 10 >= 2 and br / 10 >= 2:
            return SmartSprite.S
        elif tl % 10 <= 1 and br % 10 <= 1:
            return SmartSprite.W
        elif tl % 10 >= 2 and br % 10 >= 2:
            return SmartSprite.E
        else:
            return -1

    def get_vector_to(self,other):
        return (other.rect.centerx - self.rect.centerx, other.rect.centery - self.rect.centery)


class Landscape(SmartSprite):
    def __init__(self,window,color,x,y,width=20,height=20):
        SmartSprite.__init__(self,window,x,y,width,height)
        self.color = color
        self.drawable_sprite.image.fill(self.color)

    def update(self,color):
        self.color = color
        self.image.fill(self.color)


class Platform(SmartSprite):
    def __init__(self, window, color, x, y, width=20, height=20):
       SmartSprite.__init__(self, x, y, width, height,1000000000)
       self.window = window
       self.color = color
       self.image = pygame.Surface([width, height])
       self.image.fill(self.color)

    def hold_up_stuff(self,sprites):
        colliders = pygame.sprite.spritecollide(self,sprites)
        for collider in colliders:
            position = self.get_relative_position(collider)
            if position[1] == 11 or position[1] == 12:
                vector = self.get_vector_to(collider)
                self.exert_force_on(collider,(0,collider.mass*vector[1]))



if __name__ == '__main__':
    pass