import os

from constants import *


def load_assets():
    yellow_ship = pygame.image.load(os.path.join(ASSETS_DIR, "spaceship_yellow.png"))
    red_ship = pygame.image.load(os.path.join(ASSETS_DIR, "spaceship_red.png"))
    space_bg = pygame.image.load(os.path.join(ASSETS_DIR, "space.png"))
    return {
        "yellow_ship": pygame.transform.rotate(
            pygame.transform.scale(yellow_ship, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90
        ),
        "red_ship": pygame.transform.rotate(
            pygame.transform.scale(red_ship, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270
        ),
        "space_bg": pygame.transform.scale(space_bg, (WIDTH, HEIGHT)),
    }


def draw_window(
    win, assets, red, yellow, red_bullets, yellow_bullets, red_health, yellow_health
):
    win.blit(assets["space_bg"], (0, 0))
    pygame.draw.rect(win, BLACK, pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT))

    red_health_text = HEALTH_FONT.render(f"Health: {red_health}", 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(f"Health: {yellow_health}", 1, WHITE)
    win.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    win.blit(yellow_health_text, (10, 10))

    win.blit(assets["yellow_ship"], (yellow.rect.x, yellow.rect.y))
    win.blit(assets["red_ship"], (red.rect.x, red.rect.y))

    for bullet in red_bullets + yellow_bullets:
        color = RED if bullet in red_bullets else YELLOW
        pygame.draw.rect(win, color, bullet)

    pygame.display.update()


def draw_winner(win, text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    win.blit(
        draw_text,
        (
            WIDTH / 2 - draw_text.get_width() / 2,
            HEIGHT / 2 - draw_text.get_height() / 2,
        ),
    )
    pygame.display.update()
    pygame.time.delay(5000)
