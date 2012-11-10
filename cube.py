"""
PREVIOUSLY WRITTEN CODE WITH CORRECTIONS BY I-JUI LEE (ERIC)
Faces: FURBLD
Corners (0-7): BLU, FLU, FRU, BRU, FLD, BLD, BRD, FRD
Edges (8-19): LU, FU, RU, BU, FR, FL, BL, BR, LD, BD, RD, FD

0  BLU | 1  FLU | 2  FRU | 3  BRU | 4  FLD
5  BLD | 6  BRD | 7  FRD | 8  LU  | 9  FU
10 RU  | 11 BU  | 12 FR  | 13 FL  | 14 BL
15 BR  | 16 LD  | 17 BD  | 18 RD  | 19 FD
"""
NAME = 'FURLDB'
CSTR = 'RYGBWO'

PERM = [[[1, 4, 7, 2], [13, 19, 12,  9]],
        [[0, 1, 2, 3], [ 8,  9, 10, 11]],
        [[2, 7, 6, 3], [12, 18, 15, 10]],
        [[0, 5, 4, 1], [14, 16, 13,  8]],
        [[4, 5, 6, 7], [16, 17, 18, 19]],
        [[3, 6, 5, 0], [15, 17, 14, 11]]]

ORIE = [[(1, 1), ( 9, 1), (2, 2), (13, 0), (12, 0), (4, 2), (19, 1), (7, 1)],
        [(0, 0), (11, 0), (3, 0), ( 8, 0), (10, 0), (1, 0), ( 9, 0), (2, 0)],
        [(2, 1), (10, 1), (3, 2), (12, 1), (15, 1), (7, 2), (18, 1), (6, 1)],
        [(0, 1), ( 8, 1), (1, 2), (14, 1), (13, 1), (5, 2), (16, 1), (4, 1)],
        [(4, 0), (19, 0), (7, 0), (16, 0), (18, 0), (5, 0), (17, 0), (6, 0)],
        [(3, 1), (11, 1), (0, 2), (15, 0), (14, 0), (6, 2), (17, 1), (5, 1)]]

COLORS = [(1, 3, 5), (1, 0, 3), (1, 2, 0), (1, 5, 2),
          (4, 3, 0), (4, 5, 3), (4, 2, 5), (4, 0, 2),
          (1, 3), (1, 0), (1, 2), (1, 5),
          (0, 2), (0, 3), (5, 3), (5, 2),
          (4, 3), (4, 5), (4, 2), (4, 0)]

CORNERS = 0
EDGES = 1

class Cube:
    PERM = {NAME[i]: PERM[i] for i in range(6)}

    def __init__(self, state = None):
        self.perm = list(range(20))
        self.orie = [0] * 20
        if state:
            self.apply_state(state)

    def state(self):
        return [[(self.perm[i], self.orie[i]) for i in range(8)],
                [(self.perm[i], self.orie[i]) for i in range(8,20)]]
    
    @property
    def solved(self):
        return self.perm == list(range(20)) and self.orie == [0] * 20

    def reset(self):
        self.perm = list(range(20))
        self.orie = [0] * 20

    def _turn(self, name):
        data = Cube.PERM[name]
        cycle(self.perm, data)
        cycle(self.orie, data)
        if name in 'FB':
            for i in range(4):
                self.orie[data[EDGES][i]] += 1
        if name in 'FRBL':
            for i in range(4):
                self.orie[data[CORNERS][i]] += [2, 1, 2, 1][i]    
    
    def turn(self, name, rep):
        rep %= 4
        for i in range(rep):
            self._turn(name)
        self.normalize()

    def normalize(self):
        for i in range(8):
            self.orie[i] %= 3
        for i in range(8, 20):
            self.orie[i] %= 2

    def apply_state(self, state):
        if type(state) == Cube:
            perm, orie = state.perm, state.orie
        else:
            if len(state) != 2:
                raise ValueError('invalid state')
            perm, orie = state

        perm = map_to_cycles(perm)
        cycle(self.perm, perm)
        cycle(self.orie, perm)
        for i in len(orie):
            self.orie[i] += orie[i]
            
        self.normalize()

    def apply_moves(self, moves):
        f, d = Cube.parse(moves)
        for i in range(len(f)):
            self.turn(f[i], d[i])

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

    def getcolors(self):
        # get corresponding cubie color data for each facelet
        cubies = [ [ COLORS[self.perm[facelet[0]]] for facelet in face ]
                  for face in ORIE ]
        # corresponding orientation
        ories =  [ [ -self.orie[facelet[0]]+facelet[1] for facelet in face ]
                  for face in ORIE ]
        
        colors = [ [ cubies[i][j][ories[i][j]%len(cubies[i][j])] for j in range(8) ] for i in range(6) ]
        
        colors = [colors[i][:4] + [i] + colors[i][4:] for i in range(6)]

        return colors
        '''c = [[COLORS[self.perm[cubie[0]]]
              [(self.orie[cubie[0]] + cubie[1])%len(COLORS[self.perm[cubie[0]]])]
              for cubie in face]
             for face in ORIE]
        c = [c[i][:4] + [i] + c[i][4:] for i in range(6)]
        return c'''

    def __str__(self):
        c = [''.join([CSTR[cubie] for cubie in face])
             for face in self.getcolors()]
        return '   %s\n   %s\n   %s\n'%(c[1][:3], c[1][3:6], c[1][6:9]) + \
               c[3] [:3] + c[0] [:3] + c[2] [:3] + c[5] [:3] + '\n' + \
               c[3][3:6] + c[0][3:6] + c[2][3:6] + c[5][3:6] + '\n' + \
               c[3][6:9] + c[0][6:9] + c[2][6:9] + c[5][6:9] + '\n' + \
               '   %s\n   %s\n   %s\n'%(c[4][:3], c[4][3:6], c[4][6:9])
               
    
def map_to_cycles(m):
    cycles = []
    visited = []
    try:
        for i in range(len(m)):
            if i not in visited:
                visited.append(i)
                j = m[i]
                cycle = [i]
                while j != i:
                    if j in visited:
                        raise ValueError('not bijective')
                    else:
                        visited.append(j)
                    cycle.append(j)
                    j = m[j]
                if cycle != [i]:
                    cycles.append(cycle)
    except IndexError:
        raise ValueError("invalid map")
    return cycles

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

    return c


