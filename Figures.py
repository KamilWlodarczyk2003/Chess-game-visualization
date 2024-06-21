from OpenGL.GL import *
import pygame
from LoadMesh import *
from Mesh import *

dict = {
            "a": (0, 0.37, 8),
            "b": (0, 0.37, 7),
            "c": (0, 0.37, 6),
            "d": (0, 0.37, 5),
            "e": (0, 0.37, 4),
            "f": (0, 0.37, 3),
            "g": (0, 0.37, 2),
            "h": (0, 0.37, 1),
            "1": (8, 0.37, 0),
            "2": (7, 0.37, 0),
            "3": (6, 0.37, 0),
            "4": (5, 0.37, 0),
            "5": (4, 0.37, 0),
            "6": (3, 0.37, 0),
            "7": (2, 0.37, 0),
            "8": (1, 0.37, 0),

        }


def translacja(coord):
    x = float(dict[coord[0]][0]) + float(dict[coord[1]][0])
    y = float(dict[coord[0]][1]) + float(dict[coord[1]][1])
    z = float(dict[coord[0]][2]) + float(dict[coord[1]][2])

    return (x, y, z)



class Team:

    class Pion:
        def __init__(self, plik, start):
            self.wzor = LoadMesh(plik, GL_TRIANGLES)
            self.position = translacja(start)
            self.x, self.y, self.z = self.position
            self.y = 0.74

    class Kon:
        def __init__(self, plik, start):
            self.wzor = LoadMesh(plik, GL_TRIANGLES)
            self.position = translacja(start)
            self.x, self.y, self.z = self.position
            self.y = 0.74

    class Krol:
        def __init__(self, plik, start):
            self.wzor = LoadMesh(plik, GL_TRIANGLES)
            self.position = translacja(start)
            self.x, self.y, self.z = self.position
            self.y = 0.74

    class Queen:
        def __init__(self, plik, start):
            self.wzor = LoadMesh(plik, GL_TRIANGLES)
            self.position = translacja(start)
            self.x, self.y, self.z = self.position
            self.y = 0.74

    class Skos:
        def __init__(self, plik, start):
            self.wzor = LoadMesh(plik, GL_TRIANGLES)
            self.position = translacja(start)
            self.x, self.y, self.z = self.position
            self.y = 0.74

    class Tower:
        def __init__(self, plik, start):
            self.wzor = LoadMesh(plik, GL_TRIANGLES)
            self.position = translacja(start)
            self.x, self.y, self.z = self.position
            self.y = 0.74

    def __init__(self, kolor):
        self.pieces = []
        self.kolor = kolor

        # Initialize pawns
        for file in "abcdefgh":
            start_pos = file + "2" if kolor == "white" else file + "7"
            self.pieces.append(self.Pion("figures/pion.obj", start_pos))

        # Initialize knights
        self.pieces.append(self.Kon("figures/kon.obj", "b1" if kolor == "white" else "b8"))
        self.pieces.append(self.Kon("figures/kon.obj", "g1" if kolor == "white" else "g8"))

        # Initialize kings
        self.pieces.append(self.Krol("figures/king.obj", "e1" if kolor == "white" else "e8"))

        # Initialize queens
        self.pieces.append(self.Queen("figures/queen.obj", "d1" if kolor == "white" else "d8"))

        # Initialize bishops
        self.pieces.append(self.Skos("figures/skos.obj", "c1" if kolor == "white" else "c8"))
        self.pieces.append(self.Skos("figures/skos.obj", "f1" if kolor == "white" else "f8"))

        # Initialize rooks
        self.pieces.append(self.Tower("figures/tower.obj", "a1" if kolor == "white" else "a8"))
        self.pieces.append(self.Tower("figures/tower.obj", "h1" if kolor == "white" else "h8"))

    def draw_piony(self):
        if self.kolor == "white":
            glColor3f(0.9, 0.9, 0.9)
        else:
            glColor3f(0, 0, 0)
        for piece in self.pieces:

            piece.wzor.draw(pygame.Vector3(piece.x, piece.y, piece.z))

    def move_piece(self, start, end):
        start_pos = translacja(start)
        end_pos = translacja(end)
        for piece in self.pieces:
            if (abs(piece.position[0] - start_pos[0])) < 0.1 and abs(piece.position[1] - start_pos[1]) < 0.1 and abs(piece.position[2] - start_pos[2]) < 0.1:
                piece.position = end_pos
                return piece

