import time

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from LoadMesh import *
from Camera import *
from Figures import *
import numpy as np
from Reading import *

pygame.init()

# ustawienia ekranu
screen_width = 1000
screen_height = 800
background_color = (0.2, 0.2, 0.2, 1)
drawing_color = (1, 1, 1, 1)

#ustawienia światła
light_position = (5, 10, 5, 1.0)
light_ambient = (0.2, 0.2, 0.2, 1.0)
light_diffuse = (1.0, 1.0, 1.0, 1.0)
light_specular = (1.0, 1.0, 1.0, 1.0)

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('Szachy')
camera = Camera()
biale = Team("white")
czarne = Team("black")
mesh = LoadMesh("tests/cube.obj", GL_TRIANGLES)

#wczytanie ruchów z pliku
read = MoveReader("game1.txt")


def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    # Ustalenie pozycji światła na środek planszy
    light_position = (12, 4, 10)

    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)

    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 100)


def initialise():   #inicjalizacja ustawień
    glClearColor(background_color[0], background_color[1], background_color[2], background_color[3])
    glColor(drawing_color)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, (screen_width / screen_height), 0.1, 201.0)


def camera_init():      #wustawienia kamery
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glViewport(0, 0, screen.get_width(), screen.get_height())
    glEnable(GL_DEPTH_TEST)
    camera.update(screen.get_width(), screen.get_height())


def draw_world_axes():      #rysowanie osi X Y Z
    glLineWidth(4)
    sphere = gluNewQuadric()

    # X-axis (red)
    glBegin(GL_LINES)
    glColor3f(1, 0, 0)
    glVertex3d(-1000, 0, 0)
    glVertex3d(1000, 0, 0)
    glEnd()

    glPushMatrix()
    glTranslate(100, 0, 0)
    gluSphere(sphere, 1, 10, 10)
    glPopMatrix()

    # Y-axis (green)
    glBegin(GL_LINES)
    glColor3f(0, 1, 0)
    glVertex3d(0, -1000, 0)
    glVertex3d(0, 1000, 0)
    glEnd()

    glPushMatrix()
    glTranslate(0, 100, 0)
    gluSphere(sphere, 1, 10, 10)
    glPopMatrix()

    # Z-axis (blue)
    glBegin(GL_LINES)
    glColor3f(0, 0, 1)
    glVertex3d(0, 0, -1000)
    glVertex3d(0, 0, 1000)
    glEnd()
    glPushMatrix()
    glTranslate(0, 0, 100)
    gluSphere(sphere, 1, 10, 10)
    glPopMatrix()

    glLineWidth(1)

    # Reset color to white
    glColor3f(1, 1, 1)


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    camera_init()
    setup_lighting()
    glTranslated(0.5, -0.5, 0.5)
    for x in range(10):
        for z in range(10):
            if x == 0 or x == 9 or z == 0 or z == 9:
                glColor3f(0.71, 0.40, 0.16)
            elif (x % 2 == 0 and z % 2 != 0) or (x % 2 != 0 and z % 2 == 0):
                glColor3f(0.36, 0.25, 0.20)
            else:
                glColor3f(1, 1, 1)
            mesh.draw(pygame.Vector3(x, 0, z))

    glPushMatrix()
    biale.draw_piony()
    czarne.draw_piony()
    glPopMatrix()



def move_piece(start, end):     #szuka figury na podanej pozycji
    start_pos = translacja(start)
    end_pos = translacja(end)
    print(f"Finding piece at start position: {start_pos}")
    for piece in czarne.pieces:
        if abs(piece.x - start_pos[0]) < 0.1 and abs(piece.y - start_pos[1]) < 0.1 and abs(
                piece.z - start_pos[2]) < 0.1:
            print(f"Found black piece at {start_pos}: {piece}")
            return piece, start_pos, end_pos
    for piece in biale.pieces:
        if abs(piece.x - start_pos[0]) < 0.1 and abs(piece.y - start_pos[1]) < 0.1 and abs(
                piece.z - start_pos[2]) < 0.1:
            print(f"Found white piece at {start_pos}: {piece}")
            return piece, start_pos, end_pos
    print("No piece found at the start position.")
    return None


def remove_piece_at_position(position, team):   #usuwa figure z pola
    for piece in team.pieces:
        if abs(piece.x - position[0]) < 0.1 and abs(piece.y - position[1]) < 0.1 and abs(piece.z - position[2]) < 0.1:
            team.pieces.remove(piece)
            print(f"Removed piece at {position}: {piece}")
            return


def current_move(begin, end):   #odpowiada za ruch figury
    global move_s, moving, move_v
    if not moving:
        move_s = move_piece(begin, end)
        if move_s is None:
            print("No piece found to move.")
            return

        piece, start_pos, end_pos = move_s

        for team in (czarne, biale):
            remove_piece_at_position(end_pos, team)

        move_v = pygame.Vector3(end_pos[0] - start_pos[0], end_pos[1] - start_pos[1], end_pos[2] - start_pos[2])
        moving = True

    piece, start_pos, end_pos = move_s
    distance = pygame.Vector3(piece.x - end_pos[0], piece.y - end_pos[1], piece.z - end_pos[2]).length()
    if distance > 0.1:
        piece.x += 0.03 * move_v[0]
        piece.y += 0.03 * move_v[1]
        piece.z += 0.03 * move_v[2]
    else:
        piece.x, piece.y, piece.z = end_pos
        print(f"Piece moved to {end_pos}")
        moving = False


done = False
initialise()
pygame.event.set_grab(True)
pygame.mouse.set_visible(False)

moving = False
move_s = None
move_v = None
current = ()
move_counter = -1

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                done = True
            if event.key == pygame.K_f:
                camera.reset()
            if event.key == K_RIGHT:
                if not moving:
                    move_counter += 1
                    current = read.moves[move_counter]
                    print(current[0])
                    current_move(current[0], current[1])

    if moving:
        current_move(current[0], current[1])
    display()
    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()
