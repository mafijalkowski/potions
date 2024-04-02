import random
import time

import pygame
from pygame import Color, Rect, Surface

import potion
from constants import (
    BACKGROUND_COLOR,
    BUTTON_BG_COLOR,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TEXT_COLOR,
)
from game import load_game
from notification import Notification
from potion import Potion


def draw_text(
    text: str,
    where: Rect | tuple[float, float],
    screen: Surface,
    *,
    text_color: Color = TEXT_COLOR,
    background_color: Color = BACKGROUND_COLOR,
):
    rendered_text = font.render(
        text,
        True,
        text_color,
        background_color,
    )

    screen.blit(rendered_text, where)
    return rendered_text


def draw_button(
    text: str,
    where: Rect,
    bg_color: Color,
    screen: Surface,
) -> Rect:
    rect = pygame.draw.rect(screen, bg_color, where)
    text_surface = draw_text(text, where, screen, background_color=bg_color)
    return text_surface.get_rect(center=rect.center)


def draw_notification(notification: Notification, screen: Surface):
    _ = draw_text(notification.message, (SCREEN_WIDTH - 400, 10), screen)


if __name__ == "__main__":
    # Inicjalizacja Pygame
    pygame.init()

    # Ustawienie rozmiaru ekranu

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("potion maker")

    # Lista przechowująca potiony
    numbers: list[Potion] = []
    notifications: list[Notification] = []
    czastmp = time.time()
    defdelay = 0.5
    delay = defdelay
    lvldelay = 0.3
    defspeed = SCREEN_WIDTH * 0.002

    # Ustawienia czcionki
    font = pygame.font.Font(None, 36)

    # Klasa reprezentująca pojedynczą liczbę

    game = load_game()

    # Główna pętla gry
    running = True

    while running:
        screen.fill(BACKGROUND_COLOR)

        delay = defdelay if game.inside_pot is None else 0.3
        # Dodanie nowych liczb co pewien czas
        if len(numbers) < 100 and time.time() - czastmp >= delay:
            pot = potion.get_random_potion()
            numbers.append(pot)  # Tworzenie nowego obiektu Potion
            czastmp = time.time()

        for potion_obj in numbers:
            potion_obj.update()
            potion_obj.draw(screen)

            # Usunięcie liczby, gdy przekroczy ona prawą krawędź ekranu
            if potion_obj.x > SCREEN_WIDTH * 0.8:
                numbers.remove(potion_obj)

        if game.inside_pot is not None:
            game.inside_pot.update()
            game.inside_pot.draw(screen)

        draw_text(
            f"Hajs: {game.total_money}",
            (SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.05),
            screen,
        )

        for notification in notifications:
            if notification.still_alive():
                draw_notification(notification, screen)
            else:
                notifications.remove(notification)

        sell_button = draw_button(
            f"SELL ({game.sell_value:.2f})",
            Rect(SCREEN_WIDTH * 0.2, SCREEN_HEIGHT * 0.8, 110, 40),
            BUTTON_BG_COLOR,
            screen,
        )

        enhance_button = None
        if game.inside_pot is not None:
            _ = draw_text(
                f"Enhance probability ({game.inside_pot.enhance_chance})",
                (SCREEN_WIDTH * 0.7, SCREEN_HEIGHT * 0.7),
                screen,
            )
            enhance_button = draw_button(
                f"Enhance by ({game.inside_pot.enhance_value})",
                Rect(SCREEN_WIDTH * 0.8, SCREEN_HEIGHT * 0.8, 110, 40),
                BUTTON_BG_COLOR,
                screen,
            )

        # Obsługa zdarzeń
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.save_game()  # Zapisanie postępu gry przed wyjściem
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos: tuple[int, int] = event.pos

                for potion_obj in numbers:
                    if potion_obj.get_rect().collidepoint(mouse_pos):
                        numbers.remove(potion_obj)
                        game.add_potion(potion_obj)
                        # Ustawienie prędkości na podstawową, gdy kociol jest pusty
                        # usunąłbym to i zrobił szufladę ze wszystkimi składnikami
                        # zamiast używać tej taśmy
                        delay = defdelay
                        break  # usuń pierwszy składnik i skończ przechodzenie po kolejnych

                # Sprzedaż (sell)
                if sell_button.collidepoint(mouse_pos):
                    game.sell()
                    delay = defdelay
                if enhance_button is not None and enhance_button.collidepoint(
                    mouse_pos
                ):
                    did_ehnance = game.enhance()
                    if did_ehnance:
                        notifications.append(Notification("potion enhanced!"))
                    else:
                        notifications.append(Notification("enhancement failed!"))

            elif event.type == pygame.KEYDOWN:
                pass

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    # Zakończenie Pygame
    pygame.quit()
