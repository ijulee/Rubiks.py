# Show a character key when pressed without using Enter key
# hide the Tkinter GUI window, only console shows

import tkinter as tk

def key(event):
    """shows key or tk code for the key"""
    if event.keysym == 'Escape':
        root.destroy()
    if event.char == event.keysym:
        # w, a, s, d, o, p
        if (event.char == 'w'):
            print("when whiny winter wanes")
        elif (event.char == 'a'):
            print("anaconda attacking apples")
        elif (event.char == 's'):
            print("super sexy shenanigans")
        elif (event.char == 'd'):
            print("deadly dementors dying")
        elif (event.char == 'o'):
            print("ooooooh sayy caaan you ooooh")
        elif (event.char == 'p'):
            print("puh- puh- puh- puh- power")
    else:
        if (event.keysym == 'Up'):
            print("What goes UP....")
        elif (event.keysym == 'Down'):
            print("Must come DOWN....")
        elif (event.keysym == 'Left'):
            print("left left a b a b")
        elif (event.keysym == 'Right'):
            print("right right start select")
root = tk.Tk()
print( "Press a key (Escape key to exit):" )
root.bind_all('<Key>', key)
root.withdraw()
root.mainloop()
