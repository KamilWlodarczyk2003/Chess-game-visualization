from OpenGL.GL import *
from Mesh import *
import pygame



class LoadMesh(Mesh):
    def __init__(self, file_name,  draw_type, position = pygame.Vector3(0,0,0)):
        self.file_name = file_name
        vertices, triangles = self.load_drawing()
        super().__init__(vertices, triangles, draw_type, position)

    def load_drawing(self):
        vertices = []
        triangles = []
        with open(self.file_name) as fp:
            line = fp.readline()
            while line:
                if line[:2] == 'v ':
                    vx, vy ,vz = [float(value) for value in line[2:].split()]
                    vertices.append((vx, vy, vz))
                if line.startswith('f '):
                    face_vertices = [value.split('/')[0] for value in line[2:].split()]
                    if len(face_vertices) >= 3:
                        t1, t2, t3 = face_vertices[:3]
                        triangles.append(int(t1) - 1)
                        triangles.append(int(t2) - 1)
                        triangles.append(int(t3) - 1)
                line = fp.readline()
        return vertices, triangles