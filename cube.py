"""
Faces: UDFBLR
Corners (0-7): BLU, FLU, FRU, BRU, FLD, BLD, BRD, FRD
Edges (8-19): LU, FU, RU, BU, FR, FL, BL, BR, LD, BD, RD, FD

0 U | 1 D
2 F | 3 B
4 L | 5 R

0 BLU | 1 FLU | 2 FRU | 3 BRU
4 FLD | 5 BLD | 6 BRD | 7 FRD

 0 LU |  1 FU |  2 RU |  3 BU
 4 FR |  5 FL |  6 BL |  7 BR
 8 LD |  9 BD | 10 RD | 11 FD

*********************************
Relevant attributes of class Cube
*********************************
solved: True if cube is in a solved state
reset(): resets cube to stadard orientation solved state
turn(face): turns FACE by 1 quarter turn
rotate(axis): rotates cube along AXIS by 1 quarter turn
getcolors(): returns a list of the list of facelet colors on each face
"""

FACE   = 'UDFBLR'
COLORS = 'YWROBG'

TURN_EDGE = [[ 0,  1,  2,  3],
             [ 8,  9, 10, 11],
             [ 5, 11,  4,  1],
             [ 7,  9,  6,  3],
             [ 6,  8,  5,  0],             
             [ 4, 10,  7,  2]]

TURN_CORNER = [[0, 1, 2, 3],
               [4, 5, 6, 7],
               [1, 4, 7, 2], 
               [3, 6, 5, 0],
               [0, 5, 4, 1],
               [2, 7, 6, 3]]

ORIE_CORNER = [[(0, 0), (3, 0), (1, 0), (2, 0)],
               [(4, 0), (7, 0), (5, 0), (6, 0)],
               [(1, 1), (2, 2), (4, 2), (7, 1)],
               [(3, 1), (0, 2), (6, 2), (5, 1)],
               [(0, 1), (1, 2), (5, 2), (4, 1)],               
               [(2, 1), (3, 2), (7, 2), (6, 1)]]
               
ORIE_EDGE = [[( 3, 0), ( 0, 0), ( 2, 0), ( 1, 0)],
             [(11, 0), ( 8, 0), (10, 0), ( 9, 0)],
             [( 1, 1), ( 5, 0), ( 4, 0), (11, 1)],
             [( 3, 1), ( 7, 0), ( 6, 0), ( 9, 1)],
             [( 0, 1), ( 6, 1), ( 5, 1), ( 8, 1)],
             [( 2, 1), ( 4, 1), ( 7, 1), (10, 1)]]

COLOR_CORNER = [(0,4,3),(0,2,4),(0,5,2),(0,3,5),
                (1,4,2),(1,3,4),(1,5,3),(1,2,5)]
COLOR_EDGE = [(0,4),(0,2),(0,5),(0,3),
              (2,5),(2,4),(3,4),(3,5),
              (1,4),(1,3),(1,5),(1,2)]

class Cube:
    def __init__(self):
        # permutations
        self.face_perm   = list(range( 6))
        self.edge_perm   = list(range(12))
        self.corner_perm = list(range( 8))

        # orientations
        self.edge_orie   = [0] * 12
        self.corner_orie = [0] * 8

    @property
    def solved(self):
        colors = self.getcolors();
        return all([ all([ face[0]==face[i]
                           for i in range(9) ])
                     for face in colors ])

    def reset(self):
        self.face_perm   = list(range( 6))
        self.edge_perm   = list(range(12))
        self.corner_perm = list(range( 8))

        self.edge_orie   = [0] * 12
        self.corner_orie = [0] * 8

    def turn(self, face, rep=1):
        if face in 'UDFBLR':
            for i in range(rep%4):
                self._action(face)
            self._normalize()
        else:
            raise ValueError("There is no "+name+" face.")
            
    def rotate(self, axis, rep=1):
        if axis in 'XYZ':
            for i in range(rep%4):
                self._action(axis)
            self._normalize()
        else:
            raise ValueError("There is no "+axis+" axis.")

    def getcolors(self):
        # get corresponding color data for face facelets of each face
        face_colors = self.face_perm
        # get corresponding color data for edge facelets of each face
        edge_cubies = [ [ COLOR_EDGE[self.edge_perm[facelet[0]]]
                          for facelet in face ]
                        for face in ORIE_EDGE ]
        # get corresponding color data for corner facelets of each face 
        corner_cubies = [ [ COLOR_CORNER[self.corner_perm[facelet[0]]]
                            for facelet in face ]
                          for face in ORIE_CORNER ]
        
        # get orientation for edge facelets of each face
        edge_ories =  [ [ facelet[1]-self.edge_orie[facelet[0]]
                          for facelet in face ]
                        for face in ORIE_EDGE ]
        # get orientation for corner facelets of each face
        corner_ories = [ [ facelet[1]-self.corner_orie[facelet[0]]
                           for facelet in face ]
                         for face in ORIE_CORNER ]

        edge_colors = [ [ edge_cubies[i][j][edge_ories[i][j]%2]
                          for j in range(4) ]
                        for i in range(6) ]
        
        corner_colors = [ [ corner_cubies[i][j][corner_ories[i][j]%3]
                            for j in range(4) ]
                          for i in range(6) ]

        colors = [ [ corner_colors[i][0], edge_colors[i][0], corner_colors[i][1],
                       edge_colors[i][1], face_colors[i]   ,   edge_colors[i][2],
                     corner_colors[i][2], edge_colors[i][3], corner_colors[i][3] ]
                   for i in range (6) ]
        
        return colors
        
    def _action(self, name):
        # turns
        if name in FACE:
            face_num = FACE.find(name)
            # cycle the edges
            edge_cycle = TURN_EDGE[face_num]
            cycle(self.edge_perm, [edge_cycle])
            cycle(self.edge_orie, [edge_cycle])
            # cycle the corners
            corner_cycle = TURN_CORNER[face_num]
            cycle(self.corner_perm, [corner_cycle])
            cycle(self.corner_orie, [corner_cycle])
            # update edge orientations
            if name in 'FB':
                for i in range(4):
                    self.edge_orie[edge_cycle[i]] += 1
            # update corner orientations
            if name in 'FRBL':
                for i in range(4):
                    self.corner_orie[corner_cycle[i]] += [2, 1, 2, 1][i]

        # rotations
        if name == 'X':
            cycle(self.face_perm, [[0,2,1,3]])
            
            cycle(self.edge_perm, [[6,0,5,8],[4,10,7,2],[1,11,9,3]])
            cycle(self.edge_orie, [[6,0,5,8],[4,10,7,2],[1,11,9,3]])

            cycle(self.corner_perm, [[0,1,4,5],[2,7,6,3]])
            cycle(self.corner_orie, [[0,1,4,5],[2,7,6,3]])
            
            for i in range(4):
                self.corner_orie[[0,1,4,5][i]] += [2, 1, 2, 1][i]
                self.corner_orie[[2,7,6,3][i]] += [2, 1, 2, 1][i]
                self.edge_orie[[1,11,9,3][i]] += 1

            
        elif name == 'Y':
            cycle(self.face_perm, [[5,3,4,2]])
            
            cycle(self.edge_perm, [[0,1,2,3],[7,6,5,4],[11,10,9,8]])
            cycle(self.edge_orie, [[0,1,2,3],[7,6,5,4],[11,10,9,8]])

            cycle(self.corner_perm, [[0,1,2,3],[7,6,5,4]])
            cycle(self.corner_orie, [[0,1,2,3],[7,6,5,4]])

            for i in [4,5,6,7]:
                self.edge_orie[i] += 1
            
        elif name == 'Z':
            
            cycle(self.face_perm, [[0,4,1,5]])
            
            cycle(self.edge_perm, [[5,11,4,1],[7,3,6,9],[0,8,10,2]])
            cycle(self.edge_orie, [[5,11,4,1],[7,3,6,9],[0,8,10,2]])

            cycle(self.corner_perm, [[1,4,7,2],[3,0,5,6]])
            cycle(self.corner_orie, [[1,4,7,2],[3,0,5,6]])
            
            for i in range(4):
                self.corner_orie[[1,4,7,2][i]] += [2, 1, 2, 1][i]
                self.corner_orie[[3,0,5,6][i]] += [2, 1, 2, 1][i]

            for i in range(12):
                self.edge_orie[i] += 1
            

    def _normalize(self):
        for i in range(8):
            self.corner_orie[i] %= 3
        for i in range(12):
            self.edge_orie[i] %= 2
            
    def apply_moves(self, moves):
        f, d = Cube.parse(moves)
        for i in range(len(f)):
            self.turn(f[i], d[i])

    def __str__(self):
        c = [''.join([COLORS[cubie] for cubie in face])
             for face in self.getcolors()]
        return '   %s\n   %s\n   %s\n'%(c[0][:3], c[0][3:6], c[0][6:9]) + \
               c[4] [:3] + c[2] [:3] + c[5] [:3] + c[3] [:3] + '\n' + \
               c[4][3:6] + c[2][3:6] + c[5][3:6] + c[3][3:6] + '\n' + \
               c[4][6:9] + c[2][6:9] + c[5][6:9] + c[3][6:9] + '\n' + \
               '   %s\n   %s\n   %s\n'%(c[1][:3], c[1][3:6], c[1][6:9]) 

    def parse(moves):
        """MOVES is a string of turns. Each turn is a character indicating the
        name of the face, followed by a '\'' if the turn is 90 degrees counter-
        clockwise, a '2' if it is 180 degrees, or nothing if it is 90 degrees
        clockwise."""
        moves = list(moves)

        f = ''
        d = []
        while moves:
            char = moves.pop(0)
            if char in 'FURLDB':
                f += char
                if moves:
                    char = moves[0]
                    if char == '\'':
                        d.append(3)
                        moves.pop(0)
                    elif char == '2':
                        d.append(2)
                        moves.pop(0)
                    else:
                        d.append(1)
                else:
                    d.append(1)
        return (f, d)

    

def cycle(L, cycles, rep = 1):
    """ Given list L and CYCLES, a list of cycles characterizing a mapping,
    apply the mapping REP times.
    """
    # indices must be in range
    merged = sum(cycles, [])
    if max(merged) >= len(L):
        raise ValueError("maximum index out of range")

    # no duplicate indices
    for i in range(len(merged)):
        if merged[i] in merged[i + 1:len(merged)]:
            raise ValueError("duplicate indices in cycles")

    while rep > 0:
        for c in cycles:
            dummy = L[c[0]]
            for i in range(len(c) - 1):
                L[c[i]] = L[c[i + 1]]
            L[c[-1]] = dummy
        rep -= 1
    return L

def cube_test():
    c = Cube();
    s = "RUR'F'UFU'R'FRF'U'"
    f, d = Cube.parse(s)
    for i in range(len(f)):
        c.turn(f[i], d[i])
    assert c.solved, "not solved: " + s

    s = "F2R2" * 6
    f, d = Cube.parse(s)
    for i in range(len(f)):
        c.turn(f[i], d[i])
    assert c.solved, "not solved: " + s

    s = "FUF'U'"*6
    f, d = Cube.parse(s)
    for i in range(len(f)):
        c.turn(f[i], d[i])
    assert c.solved, "not solved: " + s

    s = "R2D'R'DR'B2LU'L'B2" + \
        "L2DLD'LB2R'URB2" + \
        "R'FRF'U'F'UF2UF'U'F'LFL'"
    f, d = Cube.parse(s)
    for i in range(len(f)):
        c.turn(f[i], d[i])
    assert c.solved, "not solved: " + s
