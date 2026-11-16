import pygame

class Paddle:
    def __init__(self, x, y, width=100, height=14, speed=7):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.screen_width = 640

    def set_screen_width(self, width):
        self.screen_width = width

    def move(self, direction):
        self.rect.x += direction * self.speed
        self.rect.x = max(0, min(self.rect.x, self.screen_width - self.rect.width))

    def draw(self, screen):
        pygame.draw.rect(screen, (80, 180, 255), self.rect, border_radius=6)
