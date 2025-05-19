#arquivo utilizar o window,vmouse e keyboard como uma variável global, para usar em todos os outros arquivos
from pplay.window import Window

window = Window(1050, 700)
window.set_title("window_main")
mouse = window.get_mouse()
keyboard = window.get_keyboard()

print(mouse.get_position())