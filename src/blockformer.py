from blockformer_core import *
from blockformer_init import *


window = Window(1400,500,300,300,60,"Blockformer")

#initialize variables
s1 = SmartSprite(window)
s2 = SmartSprite(window)

print(s1.get_colliders(s2))

#Landscape(self,color,x,y,width=20,height=20)
landscape = Landscape(window,(0,255,0),0,0,window.width,100)
window.background.add(landscape.drawable_sprite)

platform = Platform(window,(100,100,100),120,120,100,20)
window.platforms.add(platform.drawable_sprite)

sprite = Hero(window)
sprite.set_position(0,100)
window.sprites.add(sprite.drawable_sprite)

window.non_rendering_sprites.add(sprite)
window.non_rendering_sprites.add(platform)

window.run()
