from visual import *
import time
from cube import Cube


side = 60.
DISP_COLORS = [(1.0, 1.0, 0.0),
               (1.0, 1.0, 1.0),
               (1.0, 0.0, 0.0),
               (1.0, 0.6, 0.0),
               (0.0, 0.0, 1.0),
               (0.0, 1.0, 0.0)]


        
def delay(ms):
    start = time.clock()
    while time.clock() - start < ms/1000:
        ''
        

class Cube_graphics:

    def __init__(self, cube):
        ### DISPLAY/SCENE STUFF ###

        self.scene = display(height = 500, width = 500)
        self.scene.title= "Rubik's Cube"
        self.scene.foreground = (1,1,1)
        self.scene.background = color.gray(.3)
        self.scene.ambient = color.gray(.9)

                       
        ##scene.lights = [distant_light(direction=(0, 0, 100), color=color.gray(0.8)),
        ## distant_light(direction=(-0.88, -0.22, -0.44), color=color.gray(0.3))]


        # puts view at an angle
        self.scene.forward=rotate(self.scene.forward, angle = pi/4, axis = self.scene.up)
        crossp = cross(self.scene.forward, self.scene.up)
        self.scene.forward = rotate(self.scene.forward, angle = -pi/6, axis = crossp)
        self.scene.up = rotate(self.scene.up, angle = -pi/6, axis = crossp)

        self.scene.range = 125

        ### END DISPLAY/SCENE STUFF ###
        

        ### CUBE SET-UP ###
        
        #all_faces will contain 6 arrays [ [U] [D] [F] [B] [L] [R] ]
        self.cube = cube
        self.all_faces = [make_face_U(),make_face_D(),make_face_F(),
             make_face_B(),make_face_L(),make_face_R()]
        self.all_facelets = []
        for face in self.all_faces:
            self.all_facelets += face

        ### END CUBE SET-UP ###    


    ##input state will give array of 6 arrays that give the colors of each face
    def update_faces(self):
        state = self.cube.getcolors()
        for i in range(6):
            for j in range(9):
                self.all_faces[i][j].color = DISP_COLORS[state[i][j]]

        
    ### ROTATION ###

    def rot_Y(self, direction):
        # call the corresponding function of cube abstraction
        self.cube.rotate('Y', direction)

        # animate
        for i in range(120):
            delay(2)
            for facelet in self.all_facelets:
                facelet.rotate(angle=-direction*pi/320,axis = (0,1,0), origin =(0,0,0))
            

        for facelet in self.all_facelets:
            facelet.rotate(angle=direction*pi*3/8,axis = (0,1,0), origin =(0,0,0))

        # update colors
        self.update_faces()

    
    def rot_X(self, direction):
        # call the corresponding function of cube abstraction
        self.cube.rotate('X', direction)

        # animate
        for i in range(120):
            delay(2)
            for facelet in self.all_facelets:
                facelet.rotate(angle=-direction*pi/320,axis = (1,0,0), origin =(0,0,0))
            
            
        for facelet in self.all_facelets:
            facelet.rotate(angle=direction*pi*3/8,axis = (1,0,0), origin =(0,0,0))

        # update colors
        self.update_faces()

    ### TURNS ###

    def turn_U(self, drt):
        faces = self.all_faces[0]+self.all_faces[2][0:3]+self.all_faces[5][0:3]+\
                self.all_faces[3][0:3]+self.all_faces[4][0:3]

        self.cube.turn('U', drt)

        for i in range(120):
            delay(2)
            for facelet in faces:
                facelet.rotate(angle=-drt*pi/320, axis = (0,1,0), origin=(0,0,0))
            
        #turn back
        for facelet in faces:
            facelet.rotate(angle=drt*pi*3/8, axis = (0,1,0), origin=(0,0,0))
        #update colors
        self.update_faces()
            

    def turn_R(self,drt):
        faces = self.all_faces[5]+[
                self.all_faces[0][2],self.all_faces[0][5],self.all_faces[0][8],
                self.all_faces[2][2],self.all_faces[2][5],self.all_faces[2][8],
                self.all_faces[3][0],self.all_faces[3][3],self.all_faces[3][6],
                self.all_faces[1][2],self.all_faces[1][5],self.all_faces[1][8]]

        self.cube.turn('R', drt)
        for i in range(120):
            delay(2)
            for facelet in faces:
                facelet.rotate(angle=-drt*pi/320, axis = (1,0,0), origin=(0,0,0))

        #turn back
        for facelet in faces:
            facelet.rotate(angle=drt*pi*3/8, axis = (1,0,0), origin=(0,0,0))
        #update colors
        self.update_faces()


##    def turn_D(self, drt):
##        return;

##    def turn_F():
##        return;
##
##    def turn_B():
##        return;
##
##    def turn_L():
##        return;
##

    ### END TURNS ###

    def solved_state(self):
        if self.cube.solved:       
            self.all_facelets.material=materials.emissive
        



### INITIALIZE/ MAKE THE CUBE ###
f_size= 35
thickness = 1
mtrl = materials.emissive


#UPPER FACE
def make_face_U():
    faces = [box(axis=(0,0,1),length =f_size, height=thickness, width=f_size,
                 material= mtrl) for i in range(9)]

    index = 0
    while index < 9:
        for z in [-40,0,40]:
            for x in [-40,0,40]:
                curr_box = faces[index]
                curr_box.pos = (x,side,z)
                curr_box.color = (1,1,0.3) #yellow
                index += 1

    return faces;

#DOWN FACE
def make_face_D():
    faces = [box(axis=(0,0,1),length =f_size, height=thickness, width=f_size,
                 material= mtrl) for i in range(9)]

    index = 0
    while index < 9:
        for z in [40,0,-40]:
            for x in [-40,0,40]:
                curr_box = faces[index]
                curr_box.pos = (x,0-side,z)
                curr_box.color = (1,1,1) #white
                index += 1

    return faces;


#FRONT FACE
def make_face_F():
    faces = [box(length =f_size, height=f_size, width=thickness,
                 material= mtrl) for i in range(9)]

    index = 0
    while index < 9:
        for y in [40,0,-40]:
            for x in [-40,0,40]:
                curr_box = faces[index]
                curr_box.pos = (x,y,side)
                curr_box.color = (1,0,0) # red
                index += 1

    return faces;

#BACK FACE
def make_face_B():
    faces = [box(length =f_size, height=f_size, width=thickness,
                 material= mtrl) for i in range(9)]

    index = 0
    while index < 9:
        for y in [40,0,-40]:
            for x in [40,0,-40]:
                curr_box = faces[index]
                curr_box.pos = (x,y,0-side)
                curr_box.color = (1.0,.6,0) # orange
                index += 1

    return faces;


# LEFT FACE
def make_face_L():
    faces = [box(axis=(0,0,1),length =f_size, height=f_size, width=thickness,
                 material= mtrl) for i in range(9)]

    index = 0
    while index < 9:
        for y in [40,0,-40]:
            for z in [-40,0,40]:
                curr_box = faces[index]
                curr_box.pos = (0-side,y,z)
                curr_box.color = (0,0,1) # blue
                index += 1

    return faces;

#RIGHT FACE
def make_face_R():
    faces = [box(axis=(0,0,1),length =f_size, height=f_size, width=thickness,
                 material= mtrl) for i in range(9)]

    index = 0
    while index < 9:
        for y in [40,0,-40]:
            for z in [40,0,-40]:
                curr_box = faces[index]
                curr_box.pos = (side,y,z)
                curr_box.color = (0,1,0) #green
                index += 1

    return faces;

### END INITIALIZE/ MAKE THE CUBE ###

