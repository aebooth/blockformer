from blockformer_core import *
from blockformer_init import *

window = Window(10080,1720,720,480,60,"The Test")

window.hbar_sprite = Hbar(window,-10,475,100,height=1,color=(0,200,0))
window.current_level().platforms.append(Platform(window,0,window.height*2,60,window.height*2))
window.current_level().platforms.append(Platform(window,0,500,560,window.height,name="MainFloor"))
window.current_level().platforms.append(Platform(window,0,window.height,560,600))
window.current_level().platforms.append(Platform(window,0,600,60,500))
window.current_level().platforms.append(Platform(window,800,500,80,500))
# window.current_level().platforms.append(Platform(window,520,660,80,500))
# window.current_level().platforms.append(Platform(window,600,700,80,500))
# window.current_level().platforms.append(Platform(window,680,740,80,500))
window.current_level().platforms.append(Platform(window,1100,400,80,500))
window.current_level().platforms.append(Platform(window,1400,300,80,500))
window.current_level().platforms.append(Platform(window,1700,200,80,500))
# window.current_level().platforms.append(Platform(window,1780,320,80,40,color=(255,255,255)))
window.current_level().platforms.append(Platform(window,2000,200,500,500))
window.current_level().platforms.append(Platform(window,2800,900,60,420))
window.current_level().platforms.append(Platform(window,2799,400,260,500))
window.current_level().platforms.append(Platform(window,3000,580,60,500))

window.player_sprite = Player(window,360,580,color=(255,255,255))

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

window.player_animations.animations["jump_right"] = Animation(superblock.sequences["jump_right"],2)
window.player_animations.animations["jump_left"] = Animation(superblock.sequences["jump_left"],2)
window.player_animations.animations["walk_right"] = Animation(superblock.sequences["walk_right"],3)
window.player_animations.animations["walk_left"] = Animation(superblock.sequences["walk_left"],3)
window.player_animations.animations["run_right"] = Animation(superblock.sequences["run_right"],2)
window.player_animations.animations["run_left"] = Animation(superblock.sequences["run_left"],2)
window.player_animations.animations["stand_left"] = Animation(superblock.sequences["stand_left"],2)
window.player_animations.animations["stand_right"] = Animation(superblock.sequences["stand_right"],2)

window.player_animations.set_active_animation("stand_right")

window.start()