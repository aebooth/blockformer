from blockformer_core import *
from blockformer_init import *

window = Window(10080,1720,720,480,60,"The Test")

window.current_level().platforms.append(Platform(window,0,window.height*2,60,window.height*2))
window.current_level().platforms.append(Platform(window,0,500,560,window.height,name="MainFlaoor"))
window.current_level().platforms.append(Water(window,560,460,240,window.height,color=(0,0,255)))
window.current_level().platforms.append(Platform(window,560,100,240,window.height))
window.current_level().platforms.append(Platform(window,0,window.height,560,600))
window.current_level().platforms.append(Platform(window,0,600,60,500))
# window.current_level().platforms.append(Platform(window,520,660,80,500))
# window.current_level().platforms.append(Platform(window,600,700,80,500))
# window.current_level().platforms.append(Platform(window,680,740,81,500))
window.current_level().platforms.append(Platform(window,800,500,80,500))
window.current_level().platforms.append(Platform(window,1100,400,80,500))
window.current_level().platforms.append(Platform(window,1400,300,80,500))
window.current_level().platforms.append(Platform(window,1700,200,80,500))
# window.current_level().platforms.append(Platform(window,1780,320,80,40,color=(255,255,255)))
window.current_level().platforms.append(Platform(window,2000,200,500,500))
# window.current_level().platforms.append(Platform(window,2800,900,60,420))
window.current_level().platforms.append(Platform(window,2800,400,260,500))
window.current_level().platforms.append(Platform(window,3000,580,6000,500))

window.player_sprite = Player(window,360,580,color=(100,100,100),health=200)

window.hbar_sprite = HUD(window,5,5,direction="horzr",maxwidth=200,input="health")
window.sbar_sprite = HUD(window,5,window.height-5,direction="horzr",maxwidth=100,height=10,input="shield",color=(0,0,100))
window.bbar_sprite = HUD(window,5,window.height-25,height=10,direction="horzr",maxwidth=300,input="breath",color=(0,0,255))

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