from blockformer_core import *
from blockformer_init import *


window = Window(1400,500,700,300,60,"Blockformer")

#initialize variables


window.current_level().platforms.append(Platform(window,100,100,height=30))
window.current_level().platforms.append(Platform(window,0,20,window.width,20))

motion = MotionSpecification(window,150,500,500,0,2,1)
window.current_level().platforms.append(MovingPlatform(window,motion,200,100,height=30))

window.player_sprite = Player(window,0,200)
window.current_level().enemies.append(BadGuy(window,100,200))

window.start()
