# Date: 2023-03-10
# Description: Contains the Encounter class and its subclasses, which are used to create encounters for the game.

from CustomMessages import *
from abc import ABC, abstractmethod
from EntityClasses import *
from colorama import Fore
from colorama import Style
from random import randint


class Encounter(ABC):
    def __init__(self, name="", encounterType="", startDescription=None, loot=None) -> None:
        if startDescription is None:
            startDescription = [""]
        if loot is None:
            loot = {}
        self._name = name
        self._encounterType = encounterType
        self._startDescription = startDescription
        self._loot = loot

    # getters
    @property
    def name(self):
        return self._name
    
    @property
    def encounterType(self):
        return self._encounterType

    @property
    def startDescription(self):
        return "\n\n".join(self._startDescription)
    
    @property
    def loot(self):
        return self._loot
    
    # setters
    @name.setter
    def name(self, name):
        self._name = name

    @encounterType.setter
    def encounterType(self, encounterType):
        self._encounterType = encounterType

    @startDescription.setter
    def startDescription(self, startDescription):
        self._startDescription = startDescription
    
    # Sets attributes from input dictionary
    def reader(self, input_dict):
        for key in input_dict:
            try:
                setattr(self, key, input_dict[key])
            except Exception:
                print("No such attribute, please consider adding it in init.")
                continue
        # If the description is not an empty string
        if self._startDescription != [""]:
            # Format the description to fit the table
            formatForTable(self._startDescription)
        # If there is loot for the encounter, convert each entry in the loot dictionary to the appropriate object
        for itemType in self._loot:
            # Convert Weapons
            if itemType == "Weapon":
                for weapon in self._loot[itemType]:
                    a = Weapon(itemType, weapon)
                    a.reader(self._loot[itemType][weapon])
                    self._loot[itemType][weapon] = a
                continue
            # Convert Shields
            if itemType == "Shield":
                for shield in self._loot[itemType]:
                    a = Shield(itemType, shield)
                    a.reader(self._loot[itemType][shield])
                    self._loot[itemType][shield] = a
                continue
            # Convert Consumables
            if itemType == "Consumable":
                for consumable in self._loot[itemType]:
                    a = Consumable(itemType, consumable)
                    a.reader(self._loot[itemType][consumable])
                    self._loot[itemType][consumable] = a
                continue
            # Convert Ingredients
            if itemType == "Ingredient":
                for ingredient in self._loot[itemType]:
                    a = Ingredient(itemType, ingredient)
                    a.reader(self._loot[itemType][ingredient])
                    self._loot[itemType][ingredient] = a
                continue
                
    @abstractmethod
    def start_encounter(self):
        raise NotImplementedError
    
    # Drops loot and adds it to player inventory
    def drop_loot(self, player=Player()):
        # Iterates through each loot item
        for itemType in self._loot:
            # If the loot is gold
            if itemType == "Gold":
                # Calculates the amount of gold to give to the player based on the challenge level
                goldAmount = randint(self._loot["Gold"][0], self._loot["Gold"][1]) * max(player.get_challenge())
                player.modify_gold(goldAmount)
                continue
            # If the loot is an item
            for item in self._loot[itemType]:
                # Checks if the item should be dropped based on its drop chance
                if randint(1, 100) <= self._loot[itemType][item].dropChance:
                    # Adds the loot to the player's inventory
                    player.add_item(self._loot[itemType][item])
        self.print_loot_string()
    
    # Prints a string containing the loot
    def print_loot_string(self):
        # Creates an empty string to hold the gains message
        gainsString = "You gained"
        # Appends the loot name and quantity to the gainsString message
        for count, itemType in enumerate(self._loot):
            for item in self._loot[itemType]:
                if itemType == "Gold":
                    continue
                if count + 1 < len(self._loot) and gainsString != "You gained":
                    gainsString += (
                        f', {Weapon().rarity_color(f"{self._loot[itemType][item].quantity} {inflectEngine.plural(escape_ansi(self._loot[itemType][item].name))}", self._loot[itemType][item].rarity)}'
                        if self._loot[itemType][item].quantity > 1
                        else f', {Weapon().rarity_color(f"{self._loot[itemType][item].quantity} {self._loot[itemType][item].name}", self._loot[itemType][item].rarity)}'
                    )
                elif count + 1 == len(self._loot) and gainsString != "You gained":
                    if self._loot[itemType][item].quantity > 1:
                        gainsString += f' and {Weapon().rarity_color(f"{self._loot[itemType][item].quantity} {inflectEngine.plural(escape_ansi(self._loot[itemType][item].name))}", self._loot[itemType][item].rarity)}'
                    else:
                        gainsString += f' and {Weapon().rarity_color(f"{self._loot[itemType][item].quantity} {self._loot[itemType][item].name}", self._loot[itemType][item].rarity)}'
                elif self._loot[itemType][item].quantity > 1:
                    gainsString += f' {Weapon().rarity_color(f"{self._loot[itemType][item].quantity} {inflectEngine.plural(escape_ansi(self._loot[itemType][item].name))}", self._loot[itemType][item].rarity)}'
                else:
                    gainsString += f' {Weapon().rarity_color(f"{self._loot[itemType][item].quantity} {self._loot[itemType][item].name}", self._loot[itemType][item].rarity)}'
        # Adds punctuation to the gainsString message
        if gainsString != "You gained":
            if "and" in gainsString:
                gainsString = gainsString.replace(", and", " and")
            else:
                gainsString = gainsString.replace(",", "")
            gainsString += "."
            # Prints the gainsString in a formatted table
            slow_table(gainsString)


class PassiveEncounter(Encounter):
    def __init__(self, name="", encounterType="", startDescription=None):
        if startDescription is None:
            startDescription = [""]
        super().__init__(name, encounterType, startDescription)

    def start_encounter(self, player=Player()):
        # Print encounter message and description
        slow_table([[f"You ran into a {self._name}!"], ["\n\n".join(self._startDescription)]], tablefmt="fancy_grid")
        # Adds any existing loot to player inventory
        self.drop_loot(player)
        # Waits for user input to continue
        waitForKey(self._encounterType)
    


class CombatEncounter(Encounter):
    def __init__(self, name="", encounterType="", base_enemy_dict=None, startDescription=None, enemies=None, victoryText=None, defeatText=None, expReward=0):
        if base_enemy_dict is None:
            base_enemy_dict = {}
        if startDescription is None:
            startDescription = [""]
        if enemies is None:
            enemies = {}
        if victoryText is None:
            victoryText = [""]
        if defeatText is None:
            defeatText = [""]
        super().__init__(name, encounterType, startDescription)
        self._base_enemy_dict = base_enemy_dict
        self._enemies = enemies
        self._enemies_dict = {}
        self._victoryText = victoryText
        self._defeatText = defeatText
        self._expReward = expReward

    # getters
    @property
    def enemies(self):
        return self._enemies

    @property
    def enemies_dict(self):
        return self._enemies_dict

    @property
    def victoryText(self):
        return "\n\n".join(self._victoryText)

    @property
    def expReward(self):
        return self._expReward

    # setters
    @enemies.setter
    def enemies(self, enemies):
        self._enemies = enemies

    @enemies_dict.setter
    def enemies_dict(self, enemies_dict):
        self._enemies_dict = enemies_dict

    @victoryText.setter
    def victoryText(self, victoryText):
        self._victoryText = victoryText

    @expReward.setter
    def expReward(self, expReward):
        self._expReward = expReward


    # sets attributes from input dictionary
    def reader(self, input_dict):
        super().reader(input_dict)        
        # If the victory text is not an empty string
        if self._victoryText != [""]:
            # Format the text to fit the table
            formatForTable(self._victoryText)
        # If the defeat text is not an empty string
        if self._defeatText != [""]:
            # Format the text to fit the table
            formatForTable(self._defeatText)

    def generate_enemies(self, player=Player()):
        # Creates Enemy objects based on encounter data and adds them to a dictionary
        for enemy, quantity in self._enemies.items():
            for number in range(quantity):
                if quantity != 1:
                    self._enemies_dict[f"{enemy} {number + 1}"] = copy.deepcopy(self._base_enemy_dict[enemy])
                    self._enemies_dict[f"{enemy} {number + 1}"].name = f"{Fore.LIGHTRED_EX}{enemy} {number + 1}{Style.RESET_ALL}"
                else:
                    self._enemies_dict[f"{enemy}"] = copy.deepcopy(self._base_enemy_dict[enemy])
                    self._enemies_dict[f"{enemy}"].name = f"{Fore.LIGHTRED_EX}{enemy}{Style.RESET_ALL}"
        # Randomly levels up the enemy based on the player's challenge range
        for enemy2 in self._enemies_dict.values():
            challenge = player.get_challenge()
            enemy2.level_up(level=randint(challenge[0], challenge[1]))
        # Calculates experience reward for the encounter based on enemy attributes
        self._expReward = 0
        for enemy in self._enemies_dict:
            self._expReward += randint(self._enemies_dict[enemy].maxHealth // 4, self._enemies_dict[enemy].maxHealth // 2) + self._enemies_dict[enemy].damage + \
                self._enemies_dict[enemy].defense + self._enemies_dict[enemy].equippedWeapon.damage + \
                self._enemies_dict[enemy].equippedShield.defense

    # Returns a string describing encountered enemies based on the quantity and type
    def encounterText(self):
        # Initialize empty encounter text
        encounterText = ""
        # Calculate total number of enemies
        totalEnemies = len(self._enemies_dict)
        totalEnemyTypes = len(self._enemies)
        # Case for encountering a single enemy
        if totalEnemies == 1:
            encounterText = f"You ran into a {list(self._enemies.keys())[0]}"
        # Case for encountering two of the same enemy
        elif totalEnemies == 2 and totalEnemyTypes == 1:
            encounterText = f"You ran into a pair of {inflectEngine.plural(list(self._enemies.keys())[0])}"
        # Case for encountering a group of enemies (3-5)
        elif totalEnemies >= 3 and totalEnemies <= 5:
            encounterText += "You ran into a group of "
        # Case for encountering a horde of enemies (6 or more)
        elif totalEnemies >= 6:
            encounterText += "You ran into a horde of "
        for count, (enemy, quantity) in enumerate(self._enemies.items(), start=1):
            # Case for encountering one type of enemy with a quantity greater than 2
            if totalEnemyTypes == 1 and totalEnemies > 2:
                encounterText += f"{quantity} {inflectEngine.plural(enemy)}"
            elif totalEnemyTypes == 2:
                # Add current enemy to encounter text with appropriate pluralization
                if count < totalEnemyTypes:
                    encounterText += (
                        f"{quantity} {enemy} and "
                        if self._enemies[enemy] == 1
                        else f"{quantity} {inflectEngine.plural(enemy)} and "
                    )
                elif self._enemies[enemy] == 1:
                    encounterText += f"{quantity} {enemy}"
                else:
                    encounterText += f"{quantity} {inflectEngine.plural(enemy)}"
            elif totalEnemies != 1 and totalEnemyTypes != 1:
                # Add current enemy to encounter text with appropriate pluralization and punctuation
                if count < totalEnemyTypes:
                    encounterText += (
                        f"{quantity} {enemy}, "
                        if quantity == 1
                        else f"{quantity} {inflectEngine.plural(enemy)}, "
                    )
                elif quantity == 1:
                    encounterText += f"and {quantity} {enemy}"
                else:
                    encounterText += f"and {quantity} {inflectEngine.plural(enemy)}"
        # Return encounter text
        return f"{encounterText}!"
    
    # Runs combat encounter
    def start_encounter(self, player=Player(), turn=0):
        # Generates enemies
        self.generate_enemies(player)
        # Prints encounter start description
        slow_table([[f"{Fore.LIGHTRED_EX}{self.encounterText()}{Style.RESET_ALL}"], ["\n\n".join(self._startDescription)]])
        # Runs the encounter while there are still enemies left
        while len(self._enemies_dict) > 0 and player.health > 0:
            # Displays enemy and player stats
            slow_table(self.combat_table(player), tablefmt="fancy_outline", colalign=("left", "center", "center", "center", "center", "center"))

            # Displays combat actions, gets choice of player
            slow_table([['What would you like to do?'], ['1: Melee Attack'], ['2: Cast Magic'], ['3: Use Item']], tablefmt="fancy_outline", headers="firstrow")
            try:
                choice = int(input("? "))
                clrscr()
            except Exception:
                invalidChoice()
                continue

            # Fulfills action chosen by player
            match choice:
                # Case 1 is melee attack
                case 1:
                    target = self.target_menu(player)
                    # If player chooses to go back, continue
                    if target == "Go Back":
                        continue
                    # Damages selected target
                    player.melee_attack(self._enemies_dict[target])
                # Case 2 is casting magic
                case 2:
                    spell = self.magic_menu(player)
                    # If player chooses to go back, continue
                    if spell == "Go Back":
                        continue
                # Case 3 is using an item
                case 3:
                    item = player.sub_inventory_menu("Consumable")
                    # If player chooses to go back, continue
                    if item == "Go Back":
                        continue
                case _:
                    invalidChoice()
                    continue

            print("")  # Adds spacing between player and enemy turn

            # Enemies take their turns
            for enemy in list(self._enemies_dict.keys()):
                if self._enemies_dict[enemy].health <= 0:
                    self._enemies_dict[enemy].death(self)
                else:
                    self._enemies_dict[enemy].melee_attack(player)

            print("")  # Adds spacing after enemy turns

            # Triggers passive actions
            turn = player.passive_actions(turn)
        if player.health <= 0:
            self.end_encounter(player, False)
            return False
        else:
            self.end_encounter(player, True)
            return True
    
    def target_menu(self, player):
        while True:
            # Displays target selection
            combatTable = [["", "Enemy", "Success Chance"]]
            for count, enemy in enumerate(self._enemies_dict):
                combatTable.append(
                    [f"{count + 1}:", f"{Fore.YELLOW}Lv. {self._enemies_dict[enemy].level}{Style.RESET_ALL} {self._enemies_dict[enemy].name}", f"{10 + (player.agility - self._enemies_dict[enemy].agility)}% Crit Chance"])
            combatTable.append([f"{count + 2}:", "Go Back", ""])
            slow_table(combatTable, headers="firstrow", tablefmt="fancy_outline")
            # Gets target selection from player
            try:
                attackEnemy = int(input("? "))
                clrscr()
                if attackEnemy > len(self._enemies_dict) + 1:
                    invalidChoice()
                    continue
                if attackEnemy == len(self._enemies_dict) + 1:
                    return "Go Back"
            except Exception:
                invalidChoice()
                continue
            return escape_ansi(self._enemies_dict[list(self._enemies_dict.keys())[attackEnemy - 1]].name)

    def magic_menu(self, player):
        while True:
            # Displays available spells, gets spell selection from player
            try:
                slow_table([["", "Name", "Mana Cost", "What would you like to cast?"], 
                            ["1:", "Fireball", 5, f"Deals {Fore.RED}{int(player.intelligence * 0.75 // 1)} Damage{Style.RESET_ALL} to All Enemies"], 
                            ["2:", "Force Bolt", 5, f"Deals {Fore.RED}{int(player.intelligence * 1.5 // 1)} Damage{Style.RESET_ALL} to 1 Enemy"], 
                            ["3:", "Force Shield", 15, f"Doubles {Fore.BLUE}Endurance{Style.RESET_ALL} for 3 Turns"], 
                            ["4:", "Heal", "Variable", "Heals for Double Mana Cost"], 
                            ["5:", "Go Back"]], 
                            headers="firstrow", tablefmt="fancy_outline")
                spell = int(input("? "))
                clrscr()
            except Exception:
                invalidChoice()
                continue
            if spell == 5:
                return "Go Back"
            # Casts selected spell
            self.cast_spell(spell, player)
            break
    
    def cast_spell(self, spell, player):
        # Instantiates low mana warning
        insufficientMana = "You don't have enough mana."
        while True:
            # Casts spell chosen by player
            match spell:
                # Case 1 is fireball
                case 1:
                    if player.mana >= 5:
                        player.cast_fireball(self._enemies_dict)
                        break
                    else:
                        invalidChoice(insufficientMana)
                        continue
                # Case 2 is force bolt
                case 2:
                    if player.mana >= 5:
                        # Displays target selection
                        target = self.target_menu(player)
                        # Damages selected target
                        player.cast_force_bolt(self._enemies_dict[target])
                        break
                    else:
                        invalidChoice(insufficientMana)
                        continue
                # Case 3 is shield
                case 3:
                    if player.mana >= 15:
                        player.modify_attribute("mana", -15)
                        player.modify_shieldDuration(3)
                        break
                    else:
                        invalidChoice(insufficientMana)
                        continue
                # Case 4 is heal
                case 4:
                    # Gets input mana from player
                    try:
                        heal = int(
                            input("How much mana will you expend? "))
                        clrscr()
                    except Exception:
                        invalidChoice("Not a valid amount of mana.")
                        continue
                    if heal <= player.mana and heal > 0:
                        player.modify_attribute("mana", -heal)
                        player.modify_attribute("health", heal * 2)
                        break
                    elif heal <= 0:
                        invalidChoice("You can't expend less than 1 mana.")
                        continue
                    else:
                        clrscr()
                        invalidChoice(insufficientMana)
                        continue
                # Case 5 is going back
                case 5:
                    return "Go Back"
                case _:
                    invalidChoice()
                    continue

    def end_encounter(self, player, victory):
        if victory == True:
            # Prints victory text
            slow_table("\n\n".join(self._victoryText), tablefmt="fancy_grid")
            # Adds exp reward to player level progress
            player.level_up(self._expReward)
            # Adds any existing loot to player inventory
            self.drop_loot(player)
            # Waits for user input before ending encounter
            waitForKey(self.encounterType, "A battle well fought.")
        else:
            # Prints defeat text
            slow_table("\n\n".join(self._defeatText), tablefmt="fancy_grid")
            # Waits for user input before ending encounter
            waitForKey(self.encounterType, "You have been defeated.")

    def combat_table(self, player):
        # Returns formatted table representation
        combatTable = [
            ["Enemy", "Health", "Mana", "Damage", "Defense", "Agility"]
            ]
        combatTable.extend(
            [
                f"{Fore.YELLOW}Lv. {self._enemies_dict[enemy].level}{Style.RESET_ALL} {self._enemies_dict[enemy].name}",
                f"{Fore.GREEN}{self._enemies_dict[enemy].health}/{self._enemies_dict[enemy].maxHealth}{Style.RESET_ALL}",
                f"{Fore.LIGHTCYAN_EX}{self._enemies_dict[enemy].mana}/{self._enemies_dict[enemy].maxMana}{Style.RESET_ALL}",
                f"{Fore.RED}{self._enemies_dict[enemy].damage + self._enemies_dict[enemy].equippedWeapon.damage}{Style.RESET_ALL}",
                f"{Fore.BLUE}{self._enemies_dict[enemy].defense + self._enemies_dict[enemy].equippedShield.defense}{Style.RESET_ALL}",
                f"{Fore.LIGHTGREEN_EX}{self._enemies_dict[enemy].agility}{Style.RESET_ALL}",
            ]
            for enemy in self._enemies_dict
        )
        combatTable.extend(player.combat_stats())
        # Sets line break to length of longest row
        lineBreak = ["", "", "", "", "", ""]
        length = [0, 0, 0, 0, 0, 0]
        for item in combatTable:
            for count, entry in enumerate(item):
                entryLength = len(escape_ansi(entry))
                if entryLength > length[count]:
                    length[count] = entryLength
                    lineBreak[count] = "─" * length[count]
        combatTable.insert(len(self._enemies_dict) + 1, lineBreak)
        return combatTable


def encounterTesting():
    # Testing
    import json
    p = Player()
    pE = PassiveEncounter()
    with open(mainPath + "\\NewGameFiles\\Player.json", "r") as playerFile:
        player_dict = json.load(playerFile)
        playerFile.close()
    p.reader(player_dict["Newbie"])
    with open(mainPath + "\\NewGameFiles\\Enemies.json", "r") as enemiesFile:
        enemies_dict = json.load(enemiesFile)
        enemiesFile.close()
    for enemy in enemies_dict:
        a = Enemy(enemy)
        a.reader(enemies_dict[enemy])
        enemies_dict[enemy] = a
    c = CombatEncounter(base_enemy_dict=enemies_dict)
    with open(mainPath + "\\NewGameFiles\\Encounters.json", "r") as encountersFile:
        encounters_dict = json.load(encountersFile)
        encountersFile.close()
    combat_encounter = encounters_dict["Plains"]["hostile"]["1"]
    passive_encounter = encounters_dict["Plains"]["passive"]["3"]
    """p.level_up(level=7)
    p.health = p.maxHealth
    p.mana = p.maxMana"""
    """c.reader(combat_encounter)
    c.start_encounter(p)"""
    """c.generate_enemies(p)
    print(c.encounterText())
    c.start_encounter(p)"""
    pE.reader(passive_encounter)
    pE.drop_loot(p)
    

# If this file is run directly, run testing()
if __name__ == "__main__":
    encounterTesting()