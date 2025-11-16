import pygame
import random


class Starfield:
    def __init__(self, screen_width: int, screen_height: int, star_count: int = 80):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.star_count = star_count

        # Setiap star: (x, y, speed, size)
        self.stars: list[tuple[float, float, float, int]] = []
        self._create_stars()

    def _create_stars(self):
        self.stars.clear()
        for _ in range(self.star_count):
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height)
            speed = random.uniform(40, 160)
            size = random.randint(1, 3)
            self.stars.append([x, y, speed, size])

    def update(self, dt: float):
        for star in self.stars:
            star[1] += star[2] * dt  # y += speed * dt

            # Jika bintang lewat bawah, reset ke atas dengan posisi random
            if star[1] > self.screen_height:
                star[0] = random.randint(0, self.screen_width)
                star[1] = 0
                star[2] = random.uniform(40, 160)
                star[3] = random.randint(1, 3)

    def draw(self, surface: pygame.Surface):
        for x, y, _, size in self.stars:
            pygame.draw.circle(surface, (255, 255, 255), (int(x), int(y)), size)
