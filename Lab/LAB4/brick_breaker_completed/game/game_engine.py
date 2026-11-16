import math
import array
import pygame
from .paddle import Paddle
from .ball import Ball
from .brick import Brick


class GameEngine:
    WIDTH = 640
    HEIGHT = 560

    DIFFICULTIES = {
        "Easy":   {"ball_speed": 4.2, "paddle_width": 120, "paddle_speed": 7},
        "Medium": {"ball_speed": 5.2, "paddle_width": 100, "paddle_speed": 7},
        "Hard":   {"ball_speed": 6.4, "paddle_width": 82,  "paddle_speed": 8},
    }

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.font = pygame.font.Font(None, 30)
        self.big_font = pygame.font.Font(None, 64)
        self.small_font = pygame.font.Font(None, 24)

        self.running = True
        self.state = "MENU"
        self.difficulty = "Medium"

        self.score = 0
        self.lives = 3
        self.move_left = False
        self.move_right = False

        self.sounds = {}
        self._make_sounds()

        self.start_game("Medium")

    def _make_sounds(self):
        # Short procedural sounds: no external .wav files are required.
        try:
            self.sounds["brick"] = self._tone(720, 0.06)
            self.sounds["paddle"] = self._tone(430, 0.07)
            self.sounds["wall"] = self._tone(260, 0.05)
            self.sounds["gameover"] = self._tone(180, 0.30)
            self.sounds["win"] = self._tone(900, 0.35)
        except pygame.error:
            self.sounds = {}

    def _tone(self, frequency, duration):
        sample_rate = 44100
        count = int(sample_rate * duration)
        volume = 0.22
        samples = array.array("h")
        for i in range(count):
            value = int(32767 * volume * math.sin(2 * math.pi * frequency * i / sample_rate))
            samples.append(value)
        return pygame.mixer.Sound(buffer=samples.tobytes())

    def play(self, name):
        sound = self.sounds.get(name)
        if sound:
            sound.play()

    def start_game(self, difficulty):
        self.difficulty = difficulty
        settings = self.DIFFICULTIES[difficulty]

        self.score = 0
        self.lives = 3
        self.state = "PLAYING"
        self.move_left = False
        self.move_right = False

        paddle_y = self.height - 45
        self.paddle = Paddle(
            (self.width - settings["paddle_width"]) // 2,
            paddle_y,
            settings["paddle_width"],
            14,
            settings["paddle_speed"],
        )
        self.paddle.set_screen_width(self.width)

        self.ball = Ball(
            self.width // 2,
            paddle_y - 15,
            settings["ball_speed"],
        )

        self.bricks = []
        rows, cols = 6, 9
        gap = 5
        side_margin = 35
        brick_width = (self.width - 2 * side_margin - (cols - 1) * gap) // cols
        brick_height = 22
        top = 65

        for row in range(rows):
            for col in range(cols):
                x = side_margin + col * (brick_width + gap)
                y = top + row * (brick_height + gap)
                self.bricks.append(Brick(x, y, brick_width, brick_height, row))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.state == "PLAYING":
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    self.move_left = True
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.move_right = True

            elif self.state == "MENU":
                if event.key in (pygame.K_1, pygame.K_KP1):
                    self.start_game("Easy")
                elif event.key in (pygame.K_2, pygame.K_KP2):
                    self.start_game("Medium")
                elif event.key in (pygame.K_3, pygame.K_KP3):
                    self.start_game("Hard")
                elif event.key in (pygame.K_ESCAPE, pygame.K_q):
                    self.running = False

            elif self.state in ("WIN", "GAME_OVER"):
                if event.key in (pygame.K_r, pygame.K_RETURN, pygame.K_SPACE):
                    self.state = "MENU"
                elif event.key in (pygame.K_ESCAPE, pygame.K_q):
                    self.running = False

        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self.move_left = False
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.move_right = False

    def handle_input(self):
        if self.state != "PLAYING":
            return
        if self.move_left and not self.move_right:
            self.paddle.move(-1)
        elif self.move_right and not self.move_left:
            self.paddle.move(1)

    def _lose_life(self):
        self.lives -= 1
        if self.lives <= 0:
            self.state = "GAME_OVER"
            self.play("gameover")
        else:
            self.ball.reset(self.paddle.rect.centerx, self.paddle.rect.top - 15)

    def _bounce_from_paddle(self):
        # Where the ball hits the paddle controls the horizontal angle.
        hit_pos = (self.ball.rect.centerx - self.paddle.rect.centerx) / (self.paddle.rect.width / 2)
        hit_pos = max(-1.0, min(1.0, hit_pos))

        speed = max(4.0, math.hypot(self.ball.dx, self.ball.dy))
        self.ball.dx = speed * hit_pos
        vertical = math.sqrt(max(1.0, speed * speed - self.ball.dx * self.ball.dx))
        self.ball.dy = -vertical

        self.ball.y = self.paddle.rect.top - self.ball.radius - 1
        self.ball._sync_rect()
        self.play("paddle")

    def _handle_brick_collision(self):
        for brick in self.bricks:
            if not brick.alive or not self.ball.rect.colliderect(brick.rect):
                continue

            # Accurate side detection: compare previous ball rectangle
            # with the brick to determine whether X or Y was crossed.
            prev_rect = self.ball.rect.copy()
            prev_rect.center = (
                round(self.ball.x - self.ball.dx),
                round(self.ball.y - self.ball.dy),
            )

            from_left = prev_rect.right <= brick.rect.left
            from_right = prev_rect.left >= brick.rect.right
            from_top = prev_rect.bottom <= brick.rect.top
            from_bottom = prev_rect.top >= brick.rect.bottom

            if from_left or from_right:
                self.ball.dx *= -1
                if from_left:
                    self.ball.x = brick.rect.left - self.ball.radius - 1
                else:
                    self.ball.x = brick.rect.right + self.ball.radius + 1
            elif from_top or from_bottom:
                self.ball.dy *= -1
                if from_top:
                    self.ball.y = brick.rect.top - self.ball.radius - 1
                else:
                    self.ball.y = brick.rect.bottom + self.ball.radius + 1
            else:
                # Corner/overlap case: choose the axis with smaller penetration.
                overlap_x = min(
                    abs(self.ball.rect.right - brick.rect.left),
                    abs(brick.rect.right - self.ball.rect.left),
                )
                overlap_y = min(
                    abs(self.ball.rect.bottom - brick.rect.top),
                    abs(brick.rect.bottom - self.ball.rect.top),
                )
                if overlap_x < overlap_y:
                    self.ball.dx *= -1
                else:
                    self.ball.dy *= -1

            self.ball._sync_rect()
            brick.alive = False
            self.score += 10
            self.play("brick")

            if not any(b.alive for b in self.bricks):
                self.state = "WIN"
                self.play("win")
            return

    def update(self):
        if self.state != "PLAYING":
            return

        self.ball.update()

        # Left/right walls
        if self.ball.rect.left <= 0:
            self.ball.x = self.ball.radius
            self.ball.dx = abs(self.ball.dx)
            self.ball._sync_rect()
            self.play("wall")
        elif self.ball.rect.right >= self.width:
            self.ball.x = self.width - self.ball.radius
            self.ball.dx = -abs(self.ball.dx)
            self.ball._sync_rect()
            self.play("wall")

        # Top wall
        if self.ball.rect.top <= 45:
            self.ball.y = 45 + self.ball.radius
            self.ball.dy = abs(self.ball.dy)
            self.ball._sync_rect()
            self.play("wall")

        # Paddle collision only while ball is moving downward.
        if self.ball.dy > 0 and self.ball.rect.colliderect(self.paddle.rect):
            self._bounce_from_paddle()

        self._handle_brick_collision()

        # Ball below the screen = lost life
        if self.ball.rect.top > self.height:
            self._lose_life()

    def _center_text(self, screen, text, font, y):
        surface = font.render(text, True, (245, 245, 245))
        screen.blit(surface, surface.get_rect(center=(self.width // 2, y)))

    def render(self, screen):
        screen.fill((18, 20, 30))

        if self.state == "MENU":
            self._center_text(screen, "BRICK BREAKER", self.big_font, 145)
            self._center_text(screen, "Choose difficulty", self.font, 225)
            self._center_text(screen, "1 - EASY   (slow ball / large paddle)", self.font, 270)
            self._center_text(screen, "2 - MEDIUM", self.font, 310)
            self._center_text(screen, "3 - HARD   (fast ball / small paddle)", self.font, 350)
            self._center_text(screen, "Press Q or ESC to exit", self.small_font, 420)
            return

        # Header
        pygame.draw.rect(screen, (28, 31, 44), (0, 0, self.width, 45))
        screen.blit(self.font.render(f"Score: {self.score}", True, (245,245,245)), (15, 10))
        screen.blit(self.font.render(f"Lives: {self.lives}", True, (245,245,245)), (275, 10))
        screen.blit(self.font.render(self.difficulty, True, (245,245,245)), (525, 10))

        for brick in self.bricks:
            brick.draw(screen)

        self.paddle.draw(screen)
        self.ball.draw(screen)

        if self.state in ("WIN", "GAME_OVER"):
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 175))
            screen.blit(overlay, (0, 0))

            title = "YOU WIN!" if self.state == "WIN" else "GAME OVER"
            subtitle = "All bricks cleared!" if self.state == "WIN" else "You ran out of lives."

            self._center_text(screen, title, self.big_font, 205)
            self._center_text(screen, subtitle, self.font, 275)
            self._center_text(screen, f"Final Score: {self.score}", self.font, 315)
            self._center_text(screen, "Press R / ENTER / SPACE to replay", self.font, 365)
            self._center_text(screen, "Press Q / ESC to exit", self.small_font, 405)
