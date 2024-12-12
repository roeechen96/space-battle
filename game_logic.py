from typing import List

from constants import *
from spaceship import Spaceship
from utilities import draw_window, draw_winner, load_assets


class Game:
    def __init__(self):
        self.red: Spaceship = Spaceship(
            700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT, RED, VEL
        )
        self.yellow: Spaceship = Spaceship(
            100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT, YELLOW, VEL
        )
        self.assets: Dict[str, pygame.Surface] = load_assets()
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.running: bool = True
        self.power_ups: List[pygame.Rect] = []
        self.boundary: pygame.Rect = pygame.Rect(50, 50, WIDTH - 100, HEIGHT - 100)
        self.frames_since_last_shrink: int = 0

    def shrink_boundary(self) -> None:

        shrink_interval = 120
        shrink_rate = 2

        self.frames_since_last_shrink += 1
        if self.frames_since_last_shrink >= shrink_interval:
            if (
                self.boundary.width > 200 and self.boundary.height > 200
            ):  # Minimum boundary size
                self.boundary.inflate_ip(-shrink_rate, -shrink_rate)  # Reduce size
                self.boundary.x += shrink_rate // 2  # Adjust position
                self.boundary.y += shrink_rate // 2
            self.frames_since_last_shrink = 0  # Reset the counter

    def draw_boundary(self) -> None:

        pygame.draw.rect(
            WIN, (255, 0, 0), self.boundary, 2
        )  # Red rectangle for the shrinking boundary
        pygame.draw.rect(WIN, BLACK, BORDER)

    def restrict_to_boundary(self, spaceship):

        if not self.boundary.contains(spaceship.rect):

            if spaceship.rect.x < self.boundary.x:
                spaceship.rect.x = self.boundary.x
            if (
                spaceship.rect.x + spaceship.rect.width
                > self.boundary.x + self.boundary.width
            ):
                spaceship.rect.x = (
                    self.boundary.x + self.boundary.width - spaceship.rect.width
                )
            if spaceship.rect.y < self.boundary.y:
                spaceship.rect.y = self.boundary.y
            if (
                spaceship.rect.y + spaceship.rect.height
                > self.boundary.y + self.boundary.height
            ):
                spaceship.rect.y = (
                    self.boundary.y + self.boundary.height - spaceship.rect.height
                )

    def handle_bullets(self) -> None:

        for bullet in self.yellow.bullets[:]:
            bullet.x += BULLET_VEL
            if self.red.rect.colliderect(bullet):
                pygame.event.post(pygame.event.Event(RED_HIT))
                self.yellow.bullets.remove(bullet)
            elif bullet.x > WIDTH:
                self.yellow.bullets.remove(bullet)

        for bullet in self.red.bullets[:]:
            bullet.x -= BULLET_VEL
            if self.yellow.rect.colliderect(bullet):
                pygame.event.post(pygame.event.Event(YELLOW_HIT))
                self.red.bullets.remove(bullet)
            elif bullet.x < 0:
                self.red.bullets.remove(bullet)

    def draw(self) -> None:

        draw_window(
            WIN,
            self.assets,
            self.red,
            self.yellow,
            self.red.bullets,
            self.yellow.bullets,
            self.red.health,
            self.yellow.health,
        )
        self.red.draw_health_bar(WIN)
        self.yellow.draw_health_bar(WIN)
        self.draw_boundary()

        pygame.display.update()

    def main(self) -> None:

        while self.running:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LCTRL:
                        self.yellow.shoot()
                    if event.key == pygame.K_RCTRL:
                        self.red.shoot()
                if event.type == RED_HIT:
                    self.red.health -= 1
                if event.type == YELLOW_HIT:
                    self.yellow.health -= 1

            winner_text = ""
            if self.red.health <= 0:
                winner_text = "Yellow Wins!"
            elif self.yellow.health <= 0:
                winner_text = "Red Wins!"

            if winner_text:
                draw_winner(WIN, winner_text)
                self.running = False
                break

            self.shrink_boundary()

            keys = pygame.key.get_pressed()
            self.yellow.move(
                keys,
                {
                    "left": pygame.K_a,
                    "right": pygame.K_d,
                    "up": pygame.K_w,
                    "down": pygame.K_s,
                },
                self.boundary,
                BORDER.x,
            )
            self.red.move(
                keys,
                {
                    "left": pygame.K_LEFT,
                    "right": pygame.K_RIGHT,
                    "up": pygame.K_UP,
                    "down": pygame.K_DOWN,
                },
                self.boundary,
                BORDER.x + BORDER.width,
            )

            self.restrict_to_boundary(self.yellow)
            self.restrict_to_boundary(self.red)

            self.handle_bullets()

            self.draw()

        pygame.quit()
