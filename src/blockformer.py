from blockformer_core import *
from blockformer_init import *

window = Window(1400,500,300,300,60,"Blockformer")

#initialize variables

#Landscape(self,color,x,y,width=20,height=20)
landscape = Landscape(window,(0,255,0),0,0,window.width,100)
window.background.add(landscape.drawable_sprite)

sprite = Hero(window)
window.sprites.add(sprite.drawable_sprite)
window.non_rendering_sprites.add(sprite)

window.run()
