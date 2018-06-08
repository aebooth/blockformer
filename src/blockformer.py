from blockformer_core import *
from blockformer_init import *


window = Window(1400,500,700,300,60,"Blockformer")

#initialize variables


window.platforms.append(Platform(window,100,100,height=30))
window.platforms.append(Platform(window,0,0,window.width,20))

player = Player(window,0,40)
window.player_sprites.append(player)


window.run()
