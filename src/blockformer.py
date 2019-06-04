from blockformer_core import *
from blockformer_init import *

window = Window(6000,6000,720,480,60,"The Platforms")

#initialize variables

window.current_level().platforms.append(Water(window,1300,1200,2000,window.height,color=(0,0,75)))
window.current_level().platforms.append(DeathBarrier(window,-window.width/2,-200,window.width*2,height=window.height,color=(255,0,0)))
window.current_level().platforms.append(Bubbles(window,1540,1000,vx=0,vy=1,width=40,height=1000,color=(0,50,200)))
window.current_level().platforms.append(Heal(window,1040,100,20,20,color=(150,200,0)))
window.current_level().platforms.append(Heal(window,1120,100,20,20,color=(150,200,0)))

window.current_level().platforms.append(Platform(window,0,200,width=200,height=20))
window.current_level().platforms.append(Platform(window,160,200,width=50,height=200))
window.current_level().platforms.append(Platform(window,360,200,width=50,height=200))
window.current_level().platforms.append(Platform(window,560,200,width=50,height=200))
window.current_level().platforms.append(Platform(window,760,200,width=50,height=200))
window.current_level().platforms.append(Platform(window,960,200,width=50,height=200))
window.current_level().platforms.append(Platform(window,1000,40,width=200,height=200))
window.current_level().platforms.append(Platform(window,1180,80,width=40,height=200))
window.current_level().platforms.append(Platform(window,1220,120,width=40,height=200))
window.current_level().platforms.append(Platform(window,1260,160,width=40,height=200))
window.current_level().platforms.append(Platform(window,1300,200,width=40,height=200))
# window.current_level().platforms.append(Platform(window,1340,180,width=200,height=10))
window.current_level().platforms.append(Platform(window,1340,20,width=400,height=20))
window.current_level().platforms.append(Platform(window,3300,200,width=40,height=200))
window.current_level().platforms.append(Platform(window,3340,20,width=400,height=10))
window.current_level().platforms.append(Platform(window,4460,20,width=480,height=10))
window.current_level().platforms.append(Platform(window,4500,200,width=400,height=200))
window.current_level().platforms.append(Platform(window,5500,200,width=window.width,height=100))

# motion = MotionSpecification(window,150,500,0,500,2,1)
# window.current_level().platforms.append(MovingPlatform(window,motion,200,100,height=30))

window.player_sprite = Player(window,0,200,color=(255,0,255),health=200,shield=100)
# window.my_sprite = TestSprite(window,window.player_sprite.x,window.player_sprite.y)
# bad_motion2 = MotionSpecification(window,100,101,500,100,0,2)
# bad_motion = MotionSpecification(window,260,260,50,100,0,2)
# window.current_level().enemies.append(BadGuy(window,100,400,motion=bad_motion))

window.hbar_sprite = HUD(window,5,5,direction="horzr",maxwidth=200,input="health")
window.sbar_sprite = HUD(window,5,5,direction="horzr",maxwidth=100,height=10,input="shield",color=(0,0,100))
window.bbar_sprite = HUD(window,5,25,height=10,direction="horzr",maxwidth=300,input="breath",color=(0,0,255))

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
