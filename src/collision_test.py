from blockformer_core import *
from blockformer_init import *

window = Window(2720,1720,1080,720,60,"The Test")

window.hbar_sprite = Hbar(window,-10,475,100,height=1,color=(0,200,0))
window.current_level().platforms.append(Platform(window,0,500,560,window.height,name="MainFloor"))
window.current_level().platforms.append(Platform(window,0,window.height*2,60,window.height*2))
window.current_level().platforms.append(Platform(window,0,600,60,500))
window.current_level().platforms.append(Platform(window,790,500,80,500))
window.current_level().platforms.append(Platform(window,520,660,80,500))
window.current_level().platforms.append(Platform(window,600,700,80,500))
window.current_level().platforms.append(Platform(window,680,740,80,500))
window.current_level().platforms.append(Platform(window,1100,400,80,500))
window.current_level().platforms.append(Platform(window,1400,300,80,500))
window.current_level().platforms.append(Platform(window,1700,200,80,500))
window.current_level().platforms.append(Platform(window,1780,320,80,40,color=(255,255,255)))

window.player_sprite = Player(window,360,580)
window.player_animations = AnimatedSprite(window, 0,0)

superblock = Spritesheet("./pygame-ezgo/aPiratedSpritesheet.png",64,64,0)
superblock.add_sequence("move_right",3,9)
superblock.add_sequence("move_left",1,9)
superblock.add_sequence("move_up",0,9)
superblock.add_sequence("move_down",2,9)

window.player_animations.animations["move_right"] = Animation(superblock.sequences["move_right"])
window.player_animations.animations["move_left"] = Animation(superblock.sequences["move_left"])
window.player_animations.animations["move_up"] = Animation(superblock.sequences["move_up"])
window.player_animations.animations["move_down"] = Animation(superblock.sequences["move_down"])

window.player_animations.set_active_animation("move_down")

window.start()