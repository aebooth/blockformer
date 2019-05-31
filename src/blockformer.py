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

window.player_animations = AnimatedSprite(window, 0,0)

superblock = Spritesheet("./blockformer/src/thump_sheetv5.png",96,96,0)
superblock.add_sequence("jump_left",0,1)
superblock.add_sequence("jump_right",1,1)
superblock.add_sequence("walk_right",2,8)
superblock.add_sequence("walk_left",3,8)
superblock.add_sequence("run_right",2,8)
superblock.add_sequence("run_left",3,8)
superblock.add_sequence("stand_left",4,1)
superblock.add_sequence("stand_right",5,1)

window.player_animations.animations["jump_right"] = Animation(superblock.sequences["jump_right"],2,"stop")
window.player_animations.animations["jump_left"] = Animation(superblock.sequences["jump_left"],2,"stop")
window.player_animations.animations["walk_right"] = Animation(superblock.sequences["walk_right"],3,"loop")
window.player_animations.animations["walk_left"] = Animation(superblock.sequences["walk_left"],3,"loop")
window.player_animations.animations["run_right"] = Animation(superblock.sequences["run_right"],2,"loop")
window.player_animations.animations["run_left"] = Animation(superblock.sequences["run_left"],2,"loop")
window.player_animations.animations["stand_left"] = Animation(superblock.sequences["stand_left"],2,"loop")
window.player_animations.animations["stand_right"] = Animation(superblock.sequences["stand_right"],2,"loop")

window.player_animations.set_active_animation("stand_right")

window.start()
