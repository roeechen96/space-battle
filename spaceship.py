from typing import List

from constants import *


class Spaceship:
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        color: Tuple[int, int, int],
        velocity: int,
        health: int = 10,
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.color: Tuple[int, int, int] = color
        self.velocity: int = velocity
        self.health: int = health
        self.max_health: int = health
        self.bullets: List[pygame.Rect] = []

    def draw_health_bar(self, win: pygame.Surface) -> None:
        pygame.draw.rect(
            win, (255, 0, 0), (self.rect.x, self.rect.y - 10, self.rect.width, 5)
        )
        health_width = (self.health / self.max_health) * self.rect.width
        pygame.draw.rect(
            win, (0, 255, 0), (self.rect.x, self.rect.y - 10, health_width, 5)
        )

    def move(
        self,
        keys: pygame.key.ScancodeWrapper,
        controls: Dict[str, int],
        boundary: pygame.Rect,
        border_x: int,
    ) -> None:
        if keys[controls["left"]] and self.rect.x - self.velocity > max(
            boundary.x, border_x
        ):  # LEFT
            self.rect.x -= self.velocity
        if keys[
            controls["right"]
        ] and self.rect.x + self.velocity + self.rect.width < min(
            boundary.x + boundary.width, border_x
        ):
            self.rect.x += self.velocity
        if keys[controls["up"]] and self.rect.y - self.velocity > boundary.y:  # UP
            self.rect.y -= self.velocity
        if (
            keys[controls["down"]]
            and self.rect.y + self.velocity + self.rect.height
            < boundary.y + boundary.height
        ):
            self.rect.y += self.velocity

    def shoot(self) -> None:
        if len(self.bullets) < MAX_BULLETS:
            bullet = pygame.Rect(
                self.rect.x + self.rect.width,
                self.rect.y + self.rect.height // 2 - 2,
                10,
                5,
            )
            self.bullets.append(bullet)
