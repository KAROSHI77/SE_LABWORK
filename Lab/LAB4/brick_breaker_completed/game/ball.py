import pygame
import math

class Ball:
    def __init__(self, x, y, speed=5.0, radius=8):
        self.radius = radius
        self.base_speed = speed
        self.x = float(x)
        self.y = float(y)
        self.dx = speed * 0.72
        self.dy = -speed * 0.72
        self.rect = pygame.Rect(0, 0, radius * 2, radius * 2)
        self._sync_rect()

    def _sync_rect(self):
        self.rect.center = (round(self.x), round(self.y))

    def reset(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.dx = self.base_speed * 0.72
        self.dy = -self.base_speed * 0.72
        self._sync_rect()

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self._sync_rect()

    def speed_up(self, factor=1.03):
        speed = math.hypot(self.dx, self.dy) * factor
        angle = math.atan2(self.dy, self.dx)
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed

    def draw(self, screen):
        pygame.draw.circle(screen, (245, 245, 245), self.rect.center, self.radius)
