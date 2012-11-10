from keylisten import key
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    print( "Press a key (Escape key to exit):" )
    root.bind_all('<Key>', key)
    root.withdraw()
    root.mainloop()
