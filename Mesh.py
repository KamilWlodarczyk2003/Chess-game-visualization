from OpenGL.GL import *
import pygame

class Mesh:

    def __init__(self, verticies, triangles, draw_type, translation):
        self.vertices = verticies
        self.triangles = triangles
        self.draw_type = draw_type
        self.translation = translation

    def draw(self, move = pygame.Vector3(0, 0, 0)):
        glPushMatrix()
        glTranslatef(move.x, move.y, move.z)
        glTranslatef(self.translation.x, self.translation.y, self.translation.z)
        for t in range(0, len(self.triangles) , 3):
            glBegin(self.draw_type)
            glVertex3fv(self.vertices[self.triangles[t]])
            glVertex3fv(self.vertices[self.triangles[t + 1]])
            glVertex3fv(self.vertices[self.triangles[t + 2]])
            glEnd()
        glPopMatrix()