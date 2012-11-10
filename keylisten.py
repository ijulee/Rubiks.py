import tkinter as tk
from cube import Cube
"""
Show a character key when pressed without using Enter key
hide the Tkinter GUI window, only console shows
"""
c = Cube()

def key(event):
    """shows key or tk code for the key"""
    if event.keysym == 'Escape':
        root.destroy()
    if event.char == event.keysym:
        # w, a, s, d, o, p
        if (event.char == 'w'):
            c.rotate('X', 1)
        elif (event.char == 's'):
            c.rotate('X', -1)
        elif (event.char == 'a'):
            c.rotate('Y', 1)
        elif (event.char == 'd'):
            c.rotate('Y', -1)
        elif (event.char == 'o'):
            c.reset();
        elif (event.char == 'p'):
            print("Remember to implement randomize()!!!")
    else:
        if (event.keysym == 'Up'):
            c.turn('R', 1)
        elif (event.keysym == 'Down'):
            c.turn('R', -1)
        elif (event.keysym == 'Left'):
            c.turn('U', 1)
        elif (event.keysym == 'Right'):
            c.turn('U', -1)
    print('\n'+str(c))

