import pygame
from OpenGL.GLU import *
from math import *


class Camera:
    def __init__(self):
        # Zmiana początkowej pozycji kamery
        self.eye = pygame.math.Vector3(11, 8, 5)

        # Ustawienie, aby kamera patrzyła na punkt (5.5, 0, 5.5)
        look_at_point = pygame.math.Vector3(5, 0, 5)
        self.forward = (look_at_point - self.eye).normalize()

        # Przeliczenie self.right oraz self.up
        self.right = self.forward.cross(pygame.Vector3(0, 1, 0)).normalize()
        self.up = self.right.cross(self.forward).normalize()

        # Zmiana domyślnych wartości yaw i pitch
        self.yaw = degrees(atan2(self.forward.z, self.forward.x))
        self.pitch = degrees(asin(self.forward.y))

        self.last_mouse = pygame.math.Vector2(0, 0)
        self.mouse_sensitivityX = 0.1
        self.mouse_sensitivityY = 0.1
        self.key_sensitivity = 0.1

        # Ustawienie self.look
        self.look = self.eye + self.forward

    def rotate(self, yaw, pitch):
        self.yaw += yaw
        self.pitch += pitch
        if self.pitch > 89.0:
            self.pitch = 89.0
        if self.pitch < -89:
            self.pitch = -89.0
        self.forward.x = cos(radians(self.yaw)) * cos(radians(self.pitch))
        self.forward.y = sin(radians(self.pitch))
        self.forward.z = sin(radians(self.yaw)) * cos(radians(self.pitch))
        self.forward = self.forward.normalize()
        self.right = self.forward.cross(pygame.Vector3(0, 1, 0)).normalize()
        self.up = self.right.cross(self.forward).normalize()

    def reset(self):
        # Zmiana początkowej pozycji kamery
        self.eye = pygame.math.Vector3(11, 8, 5)

        # Ustawienie, aby kamera patrzyła na punkt (5.5, 0, 5.5)
        look_at_point = pygame.math.Vector3(5, 0, 5)
        self.forward = (look_at_point - self.eye).normalize()

        # Przeliczenie self.right oraz self.up
        self.right = self.forward.cross(pygame.Vector3(0, 1, 0)).normalize()
        self.up = self.right.cross(self.forward).normalize()

        # Zmiana domyślnych wartości yaw i pitch
        self.yaw = degrees(atan2(self.forward.z, self.forward.x))
        self.pitch = degrees(asin(self.forward.y))


        # Ustawienie self.look
        self.look = self.eye + self.forward

    def update(self, w, h):     #zmiana kamery w czasie
        mouse_pos = pygame.mouse.get_pos()
        mouse_change = self.last_mouse - pygame.math.Vector2(mouse_pos)
        pygame.mouse.set_pos(w / 2, h / 2)
        self.last_mouse = pygame.mouse.get_pos()
        self.rotate(-mouse_change.x * self.mouse_sensitivityX, mouse_change.y * self.mouse_sensitivityY)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            self.eye -= self.forward * self.key_sensitivity

        if keys[pygame.K_w]:
            self.eye += self.forward * self.key_sensitivity

        if keys[pygame.K_a]:
            self.eye -= self.right * self.key_sensitivity
        if keys[pygame.K_d]:
            self.eye += self.right * self.key_sensitivity

        self.look = self.eye + self.forward
        gluLookAt(self.eye.x, self.eye.y, self.eye.z,
                  self.look.x, self.look.y, self.look.z,
                  self.up.x, self.up.y, self.up.z)