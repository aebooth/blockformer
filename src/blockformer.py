from blockformer_core import *
from blockformer_init import *


window = Window(1400,500,700,300,60,"Blockformer")

#initialize variables


window.current_level().platforms.append(Platform(window,100,100,height=30))
window.current_level().platforms.append(Platform(window,300,200,height=30))
window.current_level().platforms.append(Platform(window,0,20,window.width,20))

motion = MotionSpecification(window,150,500,0,500,2,1)
window.current_level().platforms.append(MovingPlatform(window,motion,200,100,height=30))

window.player_sprite = Player(window,0,200)
# bad_motion = MotionSpecification(window,100,101,500,100,0,2)
bad_motion = MotionSpecification(window,50,500,100,300,0,1)
window.current_level().enemies.append(BadGuy(window,100,200,motion=bad_motion))

window.start()
