import pygame
import blockformer_core as bc

class BouncingBlock(bc.Sprite):
    def __init__(self,window,x,y):
        super().__init__(self,window,x,y,50,50,(255,0,0))
        
    def move(self,dx,dy):
        self.x = self.x + dx
        self.y = self.y + dy
        self.rect.x = self.window.screen_x(self.x)
        self.rect.y = self.window.screen_y(self.y)