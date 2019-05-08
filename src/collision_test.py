from blockformer_core import *
from blockformer_init import *

window = Window(1720,480,720,480,60,"The Test")

window.hbar_sprite = Hbar(window,-10,475,100,height=1,color=(0,200,0))
window.current_level().platforms.append(Platform(window,-window.width,100,window.width*3,window.height))
window.current_level().platforms.append(Platform(window,600,300,600,400))
window.current_level().platforms.append(Platform(window,600,800,600,200))
window.current_level().platforms.append(Platform(window,100,400,60,300))
window.current_level().platforms.append(Platform(window,1520,100,window.width,100))

window.player_sprite = Player(window,360,500)

window.start()