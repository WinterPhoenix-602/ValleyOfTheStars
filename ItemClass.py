# Date: 2023-03-09
# Description: Contains the Item class and its subclasses, which are used to create items for the game.

from CustomMessages import *
from random import randint
from colorama import Fore, Style
from abc import ABC, abstractmethod


# Abstract base class for items
class Item(ABC):
    def __init__(self, itemType="", name="", rarity="", quantity=0, dropChance=0):
        self._itemType = itemType
        self._name = name
        self._rarity = rarity
        self._quantity = quantity
        self._dropChance = dropChance

    # Getters
    @property
    def itemType(self):
        return self._itemType
    
    @property
    def name(self):
        return self._name
    
    @property
    def rarity(self):
        return self._rarity
    
    @property
    def blank_rarity(self):
        return escape_ansi(self._rarity)

    @property
    def quantity(self):
        return self._quantity
    
    @property
    def dropChance(self):
        return self._dropChance

    # Setters
    @name.setter
    def name(self, name):
        self._name = self.rarity_color(name, self._rarity)

    @rarity.setter
    def rarity(self, rarity):
        # Set rarity property and update rarity color
        if rarity not in ["A", "B", "C", "D", "E", "F"]:
            raise InvalidRarity(f"input invalid rarity value. ({rarity})")
        self._rarity = self.rarity_color(rarity, rarity)
        return self._rarity

    @quantity.setter
    def quantity(self, quantity):
        self._quantity = max(quantity, 0)

    def reader(self, input_dict):
        for key in input_dict:
            try:
                # Check if quantity is random
                if key not in ["_minQuantity", "_maxQuantity"]:
                    setattr(self, key, input_dict[key])
                elif self._quantity == 0:
                    # Set quantity to random integer within given range
                    self._quantity = randint(input_dict["_minQuantity"], input_dict["_maxQuantity"])
            except Exception:
                print("No such attribute, please consider adding it in init.")
                continue
        self._name = self.rarity_color(self._name, self._rarity)
        self._rarity = self.rarity_color(self._rarity, self._rarity)

    # Abstract method to get a string with the item's stats
    @abstractmethod
    def get_stats_string(self):
        raise NotImplementedError

    # Update name and rarity properties with colors according to the rarity
    def rarity_color(self, string="", rarity=""):
        string = escape_ansi(string)
        rarity = escape_ansi(rarity)
        if rarity == "F":
            string = f"{Fore.LIGHTBLACK_EX}{string}{Style.RESET_ALL}"
        elif rarity == "E":
            string = f"{Fore.CYAN}{string}{Style.RESET_ALL}"
        elif rarity == "D":
            string = f"{Fore.GREEN}{string}{Style.RESET_ALL}"
        elif rarity == "C":
            string = f"{Fore.BLUE}{string}{Style.RESET_ALL}"
        elif rarity == "B":
            string = f"{Fore.MAGENTA}{string}{Style.RESET_ALL}"
        elif rarity == "A":
            string = f"{Fore.YELLOW}{string}{Style.RESET_ALL}"
        else:
            raise InvalidRarity(f"input invalid rarity value. ({rarity})")
        return string


# Concrete Weapon class
class Weapon(Item):
    def __init__(self, itemType="", name="", rarity="", quantity=0, damage=0):
        super().__init__(itemType, name, rarity, quantity)
        self._damage = damage

    # Getters
    @property
    def damage(self):
        return self._damage
    
    # Setters
    @damage.setter
    def damage(self, damage):
        self._damage = damage

    # Returns weapon damage bonus/malus
    def get_stats_string(self):
        statsString = ""
        if self._damage >= 0:
            statsString += f"{Fore.RED}+{self._damage} Damage{Style.RESET_ALL}"
        else:
            statsString += f"{Fore.RED}-{self._damage} Damage{Style.RESET_ALL}"
        return statsString

    
class Shield(Item):
    def __init__(self, itemType="", name="", rarity="", quantity=0, defense=0, healthChange=0):
        super().__init__(itemType, name, rarity, quantity)
        self._defense = defense
        self._healthChange = healthChange

    # Getters
    @property
    def defense(self):
        return self._defense

    @property
    def healthChange(self):
        return self._healthChange
    
    # Setters
    @defense.setter
    def defense(self, defense):
        self._defense = defense
    
    @healthChange.setter
    def healthChange(self, healthChange):
        self._healthChange = healthChange
    
    # Returns shield defense and max health bonuses/maluses
    def get_stats_string(self):
        statsString = ""
        if self._defense >= 0:
            statsString += f"{Fore.BLUE}+{self._defense} Defense{Style.RESET_ALL}"
        else:
            statsString += f"{Fore.BLUE}-{self._defense} Defense{Style.RESET_ALL}"
        if self._healthChange > 0:
            statsString += f"{Fore.GREEN}+{self._healthChange} Max Health{Style.RESET_ALL}"
        elif self._healthChange < 0:
            statsString += f"{Fore.GREEN}-{self._healthChange} Max Health{Style.RESET_ALL}"
        return statsString


class Consumable(Item):
    def __init__(self, itemType="", name="", rarity="", quantity=0, stats=None):
        if stats is None:
            stats = {}
        super().__init__(itemType, name, rarity, quantity)
        self._stats = stats

    # Getters
    @property
    def stats(self):
        return self._stats
    
    # Setters
    @stats.setter
    def stats(self, stats):
        self._stats = stats

    # Returns Consumable Effect
    def get_stats_string(self):
        statsString = ""
        for stat in self._stats:
            if stat == "Health":
                if self._stats[stat] >= 0:
                    statsString += f"{Fore.GREEN}+{self._stats[stat]} Health{Style.RESET_ALL}"
                else:
                    statsString += f"{Fore.GREEN}-{self._stats[stat]} Health{Style.RESET_ALL}"
                continue
            if stat == "Mana":
                if self._stats[stat] >= 0:
                    statsString += f"+{Fore.LIGHTCYAN_EX}{self._stats[stat]} Mana{Style.RESET_ALL}"
                else:
                    statsString += f"-{Fore.LIGHTCYAN_EX}{self._stats[stat]} Mana{Style.RESET_ALL}"
                continue
        return statsString


class Ingredient(Item):
    def __init__(self, itemType="", name="", rarity="", quantity=0, use=""):
        super().__init__(itemType, name, rarity, quantity)
        self._use = use

    # Getters
    @property
    def use(self):
        return self._use
    
    # Setters
    @use.setter
    def use(self, use):
        self._use = use

    # Returns use for uniform inventory display
    def get_stats_string(self):
        return self._use


def itemTesting():
    # Testing
    import json
    with open(mainPath + "\\SaveFiles\\NewGame.json", "r") as saveFile:
        currentGame_dict = json.load(saveFile)
        saveFile.close()
    items_dict = currentGame_dict["player"]["_inventory"]
    a = Weapon("Weapon", "Wooden Sword")
    a.reader(items_dict["Weapon"]["Wooden Sword"])
    for rarityLetter in ["A", "B", "C", "D", "E", "F"]:
        a.rarity = rarityLetter
        a.name = "Wooden Sword"
        print(f"{a.name} ({a.rarity})")
    input()

# If file is run directly, run testing()
if __name__ == "__main__":
    itemTesting()
