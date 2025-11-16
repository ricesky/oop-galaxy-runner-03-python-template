import pygame


class Player:
    def __init__(self, x: float, y: float, speed: float, screen_width: int, lives: int = 3):
        self.x = x
        self.y = y
        self.speed = speed
        self.screen_width = screen_width

        # Ukuran dan warna kapal
        self.width = 40
        self.height = 25
        self.color = (0, 220, 180)

        # Encapsulated state
        self._score = 0
        self._lives = lives

    # ---------- Properties dengan Validasi ----------

    @property
    def score(self) -> int:
        return self._score

    @score.setter
    def score(self, value: int):
        if value < 0:
            raise ValueError("Score tidak boleh negatif.")
        self._score = int(value)

    @property
    def lives(self) -> int:
        return self._lives

    @lives.setter
    def lives(self, value: int):
        if value < 0:
            raise ValueError("Lives tidak boleh negatif.")
        self._lives = int(value)

    # Convenience methods (opsional, tapi rapi)
    def add_score(self, points: int):
        if points < 0:
            raise ValueError("Penambahan score tidak boleh negatif.")
        self.score = self.score + points

    def lose_life(self, amount: int = 1):
        if amount < 0:
            raise ValueError("Pengurangan nyawa tidak boleh negatif.")
        new_lives = self.lives - amount
        # Jika mau, boleh clamp ke 0
        if new_lives < 0:
            new_lives = 0
        self.lives = new_lives

    def is_dead(self) -> bool:
        return self.lives <= 0

    # ---------- Input & Movement ----------

    def handle_input(self, dt: float):
        keys = pygame.key.get_pressed()
        dx = 0

        if keys[pygame.K_LEFT]:
            dx -= self.speed * dt
        if keys[pygame.K_RIGHT]:
            dx += self.speed * dt

        self.x += dx

        # Batasi supaya tidak keluar layar
        half_w = self.width / 2
        if self.x < half_w:
            self.x = half_w
        if self.x > self.screen_width - half_w:
            self.x = self.screen_width - half_w

    def update(self, dt: float):
        self.handle_input(dt)

    # ---------- Collision Helper ----------

    def get_rect(self) -> pygame.Rect:
        rect = pygame.Rect(0, 0, self.width, self.height)
        rect.centerx = int(self.x)
        rect.centery = int(self.y)
        return rect

    def draw(self, surface: pygame.Surface):
        rect = self.get_rect()

        # Gambar badan kapal
        pygame.draw.rect(surface, self.color, rect)

        # Gambar "hidung" kapal
        nose_points = [
            (rect.centerx, rect.top - 5),
            (rect.left, rect.top + 5),
            (rect.right, rect.top + 5),
        ]
        pygame.draw.polygon(surface, self.color, nose_points)