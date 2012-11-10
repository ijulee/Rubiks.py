from cube_graphics import Cube_graphics
from cube import Cube

if __name__ == "__main__":
    cube = Cube()
    window = Cube_graphics(cube)
    while True:
        if window.scene.kb.keys:
            s = window.scene.kb.getkey()
        
            # w, a, s, d, o, p
            if (s == 'w'):
                window.rot_X(1)#c.rotate('X', 1)
            elif (s == 's'):
                window.rot_X(-1)#c.rotate('X', -1)
            elif (s == 'a'):
                window.rot_Y(1)#c.rotate('Y', 1)
            elif (s == 'd'):
                window.rot_Y(-1)#c.rotate('Y', -1)
            elif (s == 'o'):
                cube.reset()
                window.update_faces()
            elif (s == 'p'):
                cube.randomize()
                window.update_faces()
            elif (s == 'up'):
                window.turn_R(1)#c.turn('R', 1)
            elif (s == 'down'):
                window.turn_R(-1)#c.turn('R', -1)
            elif (s == 'left'):
                window.turn_U(1)#c.turn('U', 1)
            elif (s == 'right'):
                window.turn_U(-1)#c.turn('U', -1)
