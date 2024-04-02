import json
import random

from constants import SAVE_FILE_PATH, SCREEN_HEIGHT, SCREEN_WIDTH
from potion import Potion


class Game:
    def __init__(self, total_money: int, sell_value: int, inside_pot: Potion | None):
        self.total_money = total_money
        self.sell_value = sell_value
        self.inside_pot = inside_pot
        self.sell_value = inside_pot.value if inside_pot else 0

    def to_dict(self):
        return {
            "total_money": self.total_money,
            "sell_value": self.sell_value,
            "inside_pot": self.inside_pot.to_dict() if self.inside_pot else None,
        }

    def save_game(self):
        with open(SAVE_FILE_PATH, "w") as file:
            json.dump(self.to_dict(), file)

    def add_potion(self, potion_obj: Potion):
        if self.inside_pot is None:
            potion_obj.x = SCREEN_WIDTH / 2
            potion_obj.y = SCREEN_HEIGHT / 2
            potion_obj.speed = 0
            self.inside_pot = potion_obj

            self.sell_value += potion_obj.value
        else:
            self.sell_value += potion_obj.value

    def sell(self):
        if self.inside_pot is None:
            return

        self.total_money += self.sell_value
        self.sell_value = 0
        self.inside_pot = None

    def enhance(self) -> bool:
        if self.inside_pot is None:
            return False

        shot = random.random()
        if shot < self.inside_pot.enhance_chance:
            # success
            self.sell_value *= self.inside_pot.enhance_value
            return True
        else:
            self.inside_pot = None
            self.sell_value = 0
            return False

    @staticmethod
    def new_game():
        return Game(0, 0, None)


# Funkcja do wczytywania postępu gry
def load_game() -> Game:
    try:
        with open(SAVE_FILE_PATH, "rb") as file:
            saved_game = json.load(file)

            if saved_game["inside_pot"] is not None:
                potion_value = saved_game["inside_pot"]["value"]
                potion_color = saved_game["inside_pot"]["color"]
                potion_tier = saved_game["inside_pot"]["tier"]
                potion_x = saved_game["inside_pot"]["x"]
                potion_y = saved_game["inside_pot"]["y"]
                potion_enhance_chance = saved_game["inside_pot"]["enhance_chance"]
                potion_enhance_value = saved_game["inside_pot"]["enhance_value"]

                return Game(
                    saved_game["total_money"],
                    saved_game["sell_value"],
                    Potion(
                        potion_value,
                        potion_color,
                        potion_tier,
                        potion_x,
                        potion_y,
                        0,
                        potion_enhance_chance,
                        potion_enhance_value,
                    ),
                )
            else:
                return Game(
                    saved_game["total_money"],
                    saved_game["sell_value"],
                    None,
                )
    except FileNotFoundError:
        return Game.new_game()
