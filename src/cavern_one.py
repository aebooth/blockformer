from blockformer_core import *
from blockformer_init import *

window = Window(10080,680,720,480,60,"The Test")

window.current_level().platforms.append(Water(window,0,240,window.width,200))
window.current_level().platforms.append(Platform(window,0,680,40,680))
window.current_level().platforms.append(Platform(window,0,680,window.width,40))
window.current_level().platforms.append(Platform(window,0,40,window.width,40))
window.current_level().platforms.append(Platform(window,0,520,160,680))
window.current_level().platforms.append(Platform(window,0,480,200,680))
window.current_level().platforms.append(Platform(window,0,440,240,680))
window.current_level().platforms.append(Platform(window,0,400,280,680))
window.current_level().platforms.append(Platform(window,0,360,320,680))
window.current_level().platforms.append(Platform(window,0,320,360,680))
window.current_level().platforms.append(Platform(window,0,280,640,120))

window.player_sprite = Player(window,40,600,color=(100,100,100),health=200)

window.hbar_sprite = HUD(window,5,5,direction="horzr",maxwidth=200,input="health")
window.sbar_sprite = HUD(window,5,window.height-5,direction="horzr",maxwidth=100,height=10,input="shield",color=(0,0,100))
window.bbar_sprite = HUD(window,5,window.height-25,height=10,direction="horzr",maxwidth=600,input="breath",color=(0,0,255))

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