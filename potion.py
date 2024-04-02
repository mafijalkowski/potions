import os
import random

import pygame

from constants import IMAGE_FOLDER, SCREEN_HEIGHT, SCREEN_WIDTH


class Potion:
    def __init__(
        self,
        value: float,
        color: str,
        tier: int,
        x: float,
        y: float,
        speed: float = 2,
        enhance_chance: float = 1,
        enhance_value: float = 1,
    ):  # Poprawiono konstruktor, dodając argumenty
        self.value = value
        self.color = color
        self.tier = tier
        self.x = x
        self.y = y
        self.speed = speed
        self.click_margin = 3.5  # Margines kliknięcia
        self.image_name = f"{value}.{tier}.png"  # Nazwa pliku obrazu

        self.image = pygame.image.load(os.path.join(IMAGE_FOLDER, self.image_name))

        self.enhance_chance = enhance_chance
        self.enhance_value = enhance_value

    def get_rect(self):
        rect = self.image.get_rect(topleft=(self.x, self.y))

        # Rozszerzamy prostokąt kolizji o margines kliknięcia
        rect.inflate_ip(self.click_margin * 2, self.click_margin * 2)
        return rect

    def update(self):
        self.x += self.speed

    def to_dict(self):
        return {
            "value": self.value,
            "color": self.color,
            "tier": self.tier,
            "x": self.x,
            "y": self.y,
            "enhance_chance": self.enhance_chance,
            "enhance_value": self.enhance_value,
        }

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.get_rect())


def red_potion(tier: int) -> Potion:
    return Potion(1, "red", tier, SCREEN_WIDTH * 0.2, SCREEN_HEIGHT * 0.1, 2, 0.4, 10)


def blue_potion(tier: int) -> Potion:
    return Potion(2, "blue", tier, SCREEN_WIDTH * 0.2, SCREEN_HEIGHT * 0.1, 2, 0.8, 5)


def yellow_potion(tier: int) -> Potion:
    return Potion(
        3, "yellow", tier, SCREEN_WIDTH * 0.2, SCREEN_HEIGHT * 0.1, 2, 0.9, 1.12
    )


def get_random_potion():
    color = random.randint(1, 3)
    tier = random.randint(1, 3)
    if color == 1:
        return red_potion(tier)
    elif color == 2:
        return blue_potion(tier)
    else:
        return yellow_potion(tier)
