from blockformer_core import *
from blockformer_init import *

window = Window(3000,1000,720,480,60,"The Platforms")

#initialize variables

window.current_level().platforms.append(DeathBarrier(window,0,-50,window.width,height=500))
#window.current_level().platforms.append(Platform(window,0,1,window.width,20))
window.current_level().platforms.append(Water(window,1300,300,1000,400,color=(0,0,200)))
window.current_level().platforms.append(Heal(window,1700,200,20,20,color=(100,200,0)))
window.current_level().platforms.append(Heal(window,1900,200,20,20,color=(100,200,0)))
window.hbar_sprite = Hbar(window,5,475,100,height=20,color=(0,200,0))

window.current_level().platforms.append(Platform(window,0,50,height=20))
window.current_level().platforms.append(Platform(window,100,100,height=20))
window.current_level().platforms.append(Platform(window,300,70,width=50,height=80))
window.current_level().platforms.append(Platform(window,1060,20,width=40,height=200))
window.current_level().platforms.append(Platform(window,1100,50,width=40,height=200))
window.current_level().platforms.append(Platform(window,1140,80,width=40,height=200))
window.current_level().platforms.append(Platform(window,1180,110,width=40,height=200))
window.current_level().platforms.append(Platform(window,1220,140,width=40,height=200))
window.current_level().platforms.append(Platform(window,1260,170,width=40,height=200))
window.current_level().platforms.append(Platform(window,1300,300,width=40,height=300))
window.current_level().platforms.append(Platform(window,2300,300,width=40,height=300))

motion = MotionSpecification(window,150,500,0,500,2,1)
window.current_level().platforms.append(MovingPlatform(window,motion,200,100,height=30))

window.player_sprite = Player(window,0,200)
bad_motion2 = MotionSpecification(window,100,101,500,100,0,2)
bad_motion = MotionSpecification(window,100,500,50,100,2,2)
window.current_level().enemies.append(BadGuy(window,100,200,motion=bad_motion2))

window.start()
