# Date: 2023-03-12
# Description: Contains the Entity class and its subclasses, which are used to create entities for the game.

import abc
import copy
import re
from CustomMessages import *
from random import randint
from ItemClass import *
from colorama import Fore
from colorama import Style
from tabulate import tabulate


# Abstract base class
class Entity(abc.ABC):
    def __init__(self, name="", level=0, levelProgress=0, nextLevel=0, statPoints=0, health=0, constitution=0, mana=0, intelligence=0, strength=0, endurance=0, agility=0, inventory=None, equippedWeapon=Weapon(), equippedShield=Shield()):
        if inventory is None:
            inventory = {}
        self._name = name # Name of the entity
        self._level = level # Level of the entity
        self._levelProgress = levelProgress # Progress towards the next level
        self._nextLevel = nextLevel # Amount of experience needed to reach the next level
        self._statPoints = statPoints # Amount of stat points the entity has available to spend
        self._health = health # Current health of the entity
        self._constitution = constitution # Constitution of the entity
        self._maxHealth = constitution * 10 # Maximum health of the entity
        self._mana = mana # Current mana of the entity
        self._intelligence = intelligence # Intelligence of the entity
        self._maxMana = intelligence * 5 # Maximum mana of the entity
        self._strength = strength # Strength of the entity
        self._damage = strength * 2 # Damage of the entity
        self._endurance = endurance # Endurance of the entity
        self._defense = endurance * 2 # Defense of the entity
        self._agility = agility # Agility of the entity
        self._inventory = inventory # Inventory of the entity
        self._equippedWeapon = equippedWeapon # Equipped weapon of the entity
        self._equippedShield = equippedShield # Equipped shield of the entity

    # Getters
    @property
    def name(self):
        return self._name

    @property
    def level(self):
        return self._level

    @property
    def levelProgress(self):
        return self._levelProgress

    @property
    def nextLevel(self):
        return self._nextLevel

    @property
    def levelTable(self):
        return self._levelTable

    @property
    def health(self):
        return self._health

    @property
    def constitution(self):
        return self._constitution
    
    @property
    def maxHealth(self):
        return self._maxHealth

    @property
    def mana(self):
        return self._mana

    @property
    def intelligence(self):
        return self._intelligence
    
    @property
    def maxMana(self):
        return self._maxMana

    @property
    def strength(self):
        return self._strength
    
    @property
    def damage(self):
        return self._damage

    @property
    def endurance(self):
        return self._endurance
    
    @property
    def defense(self):
        return self._defense

    @property
    def agility(self):
        return self._agility

    @property
    def inventory(self):
        return self._inventory

    @property
    def equippedWeapon(self):
        return self._equippedWeapon

    @property
    def equippedShield(self):
        return self._equippedShield

    # Setters
    @name.setter
    def name(self, name=""):
        self._name = name

    @level.setter
    def level(self, level=0):
        self._level = level

    @levelProgress.setter
    def levelProgress(self, levelProgress=0):
        self._levelProgress = levelProgress

    @nextLevel.setter
    def nextLevel(self, nextLevel=0):
        self._nextLevel = nextLevel

    @levelTable.setter
    def levelTable(self, levelTable=None):
        if levelTable is None:
            levelTable = []
        self._levelTable = levelTable

    @health.setter
    def health(self, health=0):
        self._health = health

    @constitution.setter
    def constitution(self, constitution=0):
        self._constitution = constitution
        # Sets max health based on constitution
        self._maxHealth = 50 + self._maxHealth + self._constitution * 10
    
    @mana.setter
    def mana(self, mana=0):
        self._mana = mana

    @intelligence.setter
    def intelligence(self, intelligence=0):
        self._intelligence = intelligence
        # Sets max mana based on intelligence
        self._maxMana = 25 + self._intelligence * 5

    @strength.setter
    def strength(self, strength):
        self._strength = strength
        # Sets damage based on strength
        self._damage = self._strength * 2

    @endurance.setter
    def endurance(self, endurance):
        self._endurance = endurance
        # Sets defense based on endurance
        self._defense = self._endurance * 2

    @agility.setter
    def agility(self, agility=0):
        self._agility = agility

    @inventory.setter
    def inventory(self, inventory=None):
        if inventory is None:
            inventory = {}
        self._inventory = inventory

    @equippedWeapon.setter
    def equippedWeapon(self, equippedWeapon=Weapon()):
        self._equippedWeapon = equippedWeapon

    @equippedShield.setter
    def equippedShield(self, equippedShield=Shield()):
        self._equippedShield = equippedShield

    # Sets attributes from input dictionary
    def reader(self, input_dict=None):
        if input_dict is None:
            input_dict = {}
        entity_dict = copy.deepcopy(input_dict)
        for key in entity_dict:
            try:
                if key != "quantity":
                    setattr(self, key, entity_dict[key])
            except Exception:
                slow_line(
                    "No such attribute, please consider adding it in init.")
                continue
        # Sets entity level from input dictionary
        self.level_up(level=self._level)
        # Converts items from dictionary into appropriate objects
        for itemType in self._inventory:
            # Convert Weapons
            if itemType == "Weapon":
                for weapon in self._inventory[itemType]:
                    a = Weapon(itemType, weapon)
                    a.reader(self._inventory[itemType][weapon])
                    self._inventory[itemType][weapon] = a
                    continue
            # Convert Shields
            if itemType == "Shield":
                for shield in self._inventory[itemType]:
                    a = Shield(itemType, shield)
                    a.reader(self._inventory[itemType][shield])
                    self._inventory[itemType][shield] = a
                    continue
            # Convert Consumables
            if itemType == "Consumable":
                for consumable in self._inventory[itemType]:
                    a = Consumable(itemType, consumable)
                    a.reader(self._inventory[itemType][consumable])
                    self._inventory[itemType][consumable] = a
                    continue
            # Convert Ingredients
            if itemType == "Ingredient":
                for ingredient in self._inventory[itemType]:
                    a = Ingredient(itemType, ingredient)
                    a.reader(self._inventory[itemType][ingredient])
                    self._inventory[itemType][ingredient] = a
                    continue
        # Equips items as specified by input dictionary
        self._equippedWeapon = self._inventory["Weapon"][self._inventory["Equipped"]["Weapon"]]
        self._equippedShield = self._inventory["Shield"][self._inventory["Equipped"]["Shield"]]

    # Sets stats based on level
    def level_up(self, exp=0, level=0):
        # Initialize a variable to keep track of how many levels were gained
        levelChange = 0
        # If the level is 1, set the level to 1, set the required exp to reach the next level to 50, and set the stat points to 10
        if level == 1:
            self.level = 1
            self._nextLevel = self._level * 50
            self._statPoints = 10
        # If a specific level was provided, calculate the required exp to reach that level
        elif level > 1:
            exp = 25 * ((level + self._level) - 1) * (level - self._level)
            # If the requested level is lower than the current level, subtract the current progress
            if level < self._level:
                exp -= self._levelProgress
        # If some amount of exp was provided, add it to the current progress
        if exp != 0:
            self._levelProgress += exp
            # Keep leveling up as long as there's enough progress to reach the next level
            while self._levelProgress >= self._nextLevel:
                # Subtract the required exp to level up from the progress
                self._levelProgress = self._levelProgress - self._nextLevel
                # Increase the level and levelChange counter
                self._level += 1
                levelChange += 1
                # Increase the stat points by 10
                self._statPoints +=  10
                # Update the required exp for the next level
                self._nextLevel = self._level * 50
            # If the progress is negative, level down until it's positive
            while self._levelProgress < 0:
                # Subtract the required exp for the previous level from the progress
                self._levelProgress = self._levelProgress + self._nextLevel - 50
                # Decrease the level and levelChange counter
                self._level -= 1
                levelChange -= 1
                # Update the required exp for the next level
                self._nextLevel = self._level * 50
        # Return a tuple of the actual exp gained and the number of levels gained
        return exp, levelChange
    
    @abstractmethod
    def distribute_stats(self):
        raise NotImplementedError

    # Modify a specified attribute (health or mana) by adding or subtracting a given value
    def modify_attribute(self, attribute="", change=0):
        # Initialize a variable to hold the message to be returned
        message = ""
        # Check if the attribute is health
        if attribute == "health":
            # If the change is positive and won't cause the health to exceed the maxHealth, add change to health and set message to heal
            if change >= 1 and self._health + change <= self._maxHealth:
                self._health += change
                message = "heal"
            # If the change is negative, subtract it from the health and set the message to "damage"
            elif change < 1:
                self._health += change
                message = "damage"
            # If the change is positive but would cause health to exceed maxHealth, set change to the amount needed to reach maxHealth and set message to "overheal"
            else:
                change = self._maxHealth - self._health
                self._health += (self._maxHealth - self._health)
                message = "overheal"
        # Check if the attribute is mana
        if attribute == "mana":
            # If the change is positive and won't cause the mana to exceed the maxMana, add change to mana and set message to "regen mana"
            if change > 1 and self._mana + change <= self._maxMana:
                self._mana += change
                message = "regen mana"
            # If the change is negative, subtract it from the mana and set the message to "expend mana"
            elif change < 1:
                self._mana += change
                message = "expend mana"
            # If the change is positive but would cause mana to exceed maxMana, set change to the amount needed to reach maxMana and set message to "over regen mana"
            elif change > 1:
                change = self._maxMana - self._mana
                self._mana += (self._maxMana - self._mana)
                message = "over regen mana"
        # Return the message and the final change (in case it was modified to fit within the attribute's limits)
        return message, change

    # Uses a melee attack on input target
    def melee_attack(self, target):
        # Calculate the crit chance of the attack (based on agility)
        if self._agility > target.agility:
            crit_chance = 10 + (1 * (self._agility - target.agility))
        elif self._agility < target.agility:
            crit_chance = 10 - (1 * (target.agility - self._agility))
        else:
            crit_chance = 10
        # Generate a random number between 1 and 100 to determine if the attack hits
        attempt = randint(1, 100)
        # If the attack does not crit, calculate the damage and set the result to "hit"
        if attempt > crit_chance:
            damage, result = self.compute_damage(target)
        # If the attack crits, calculate the damage and set the result to "crit"
        else:
            damage, result = self.compute_damage(target)
            damage *= 2
            result = "crit"
        target.modify_attribute("health", -damage)
        # Return the result of the attack
        return result, damage

    # Finds damage done by an attack
    def compute_damage(self, target):
        # Calculate the damage of the attack (base damage plus damage from equipped weapon)
        damage = self._damage + self._equippedWeapon.damage
        # Calculate the defense of the target (base defense plus defense from equipped shield)
        defense = target.defense + target._equippedShield.defense
        # If the damage is greater than the defense, set the result to "hit"
        if damage > defense:
            result = "hit"
        # If the damage is greater than target base defense, set the result to "shield block"
        elif damage > target.defense:
            result = "shield block"
        # If the damage is less than or equal to target base defense, set the result to "block"
        else:
            result = "block"
        # Return the maximum of 0 and the difference between damage and defense (to ensure the damage dealt is never negative)
        return max(damage - defense, 0), result


# player class
class Player(Entity):
    def __init__(self, name="Newbie", level=1, levelProgress=0, nextLevel=50, statPoints=0, health=50, constitution=5, mana=25, intelligence=5, strength=5, endurance=5, agility=5, equippedWeapon=Weapon(), equippedShield=Shield(), shieldDuration=0, inventory=None):
        if inventory is None:
            inventory = {}
        super().__init__(name, level, levelProgress, nextLevel, statPoints, health, constitution, mana, intelligence, strength, endurance, agility, equippedWeapon, equippedShield)
        self._shieldDuration = shieldDuration
        self._inventory = inventory

    @property
    def shieldDuration(self):
        return self._shieldDuration

    @property
    def inventory(self):
        return self._inventory

    @shieldDuration.setter
    def shieldDuration(self, shieldDuration):
        self._shieldDuration = shieldDuration

    @inventory.setter
    def inventory(self, inventory):
        self._inventory = inventory

    # Display level up message and ask if the player wants to increase an attribute
    def level_up(self, exp=0, level=0):
        exp, levelChange = super().level_up(exp, level)
        if self._level == 1:
            self._statPoints = 0
        # If the character gained experience, print a message indicating the amount of experience gained
        if exp > 0:
            slow_table(
                tabulate([[f"{Fore.YELLOW}You gained {int(exp // 1)} experience.{Style.RESET_ALL}"]], tablefmt="fancy_outline"))
            # If the character leveled up, print a message indicating their new level
            if levelChange > 0:
                slow_table(tabulate(
                    [[f"{Fore.YELLOW}You leveled up! {self._level - levelChange} -> {self._level}{Style.RESET_ALL}"]], tablefmt="fancy_outline"))
                # Ask the player if they want to increase an attribute
                while True:
                    slow_table(tabulate([["", "Would you like to distribute your stat points?"], ["1:", "Yes"], ["2:", "No"]], headers="firstrow", tablefmt="fancy_outline"))
                    try:
                        choice = int(input("? "))
                    except ValueError:
                        invalidChoice()
                        continue
                    if choice == 1:
                        clrscr()
                        self.stats_menu()
                        break
                    elif choice == 2:
                        break
                    else:
                        invalidChoice()
        # If the character lost experience, print a message indicating the amount of experience lost
        elif exp < 0:
            slow_table(
                tabulate([[f"{Fore.YELLOW}You lost {-int(exp // 1)} experience.{Style.RESET_ALL}"]], tablefmt="fancy_outline"))
            # If the character leveled down, print a message indicating their new level
            if levelChange < 0:
                slow_table(tabulate(
                    [[f"{Fore.YELLOW}You leveled down. {self._level - levelChange} -> {self._level}{Style.RESET_ALL}"]], tablefmt="fancy_outline"))

    # Allows the player to distribute their stat points
    def stats_menu(self):
        # Loops until the player has no stat points left, or until they choose to exit
        statsChange = [0, 0, 0, 0, 0]
        while self._statPoints > sum(statsChange):
            # Displays the player's stats
            slow_table(tabulate(
                [
                ["Current Stats", f"+{self._statPoints - sum(statsChange)}"],
                ["Constitution:", f"{self._constitution} + {statsChange[0]}"],
                ["Health:", f"{self._maxHealth} + {statsChange[0] * 10}"],
                ["Intelligence:", f"{self._intelligence} + {statsChange[1]}"],
                ["Mana:", f"{self._maxMana} + {statsChange[1] * 5}"],
                ["Strength:", f"{self._strength} + {statsChange[2]}"],
                ["Damage:", f"{self._damage} + {statsChange[2] * 2}"],
                ["Endurance:", f"{self._endurance} + {statsChange[3]}"],
                ["Defense:", f"{self._defense} + {statsChange[3] * 2}"],
                ["Agility:", f"{self._agility} + {statsChange[4]}"],
                ], 
                headers="firstrow", tablefmt="fancy_outline", colalign=("right", "center")))
            # Asks the player which stat they want to increase
            slow_table(tabulate(
                [
                ["", "Which stat would you like to increase?"],
                ["1:", "Constitution"],
                ["2:", "Intelligence"],
                ["3:", "Strength"],
                ["4:", "Endurance"],
                ["5:", "Agility"],
                ["6:", "Go Back"]
                ],
                headers="firstrow", tablefmt="fancy_outline"))
            try:
                choice = int(input("? "))
            except ValueError:
                invalidChoice()
                continue
            if choice == 1:
                statsChange = self.increase_stat(
                    "How many points would you like to add to Constitution?",
                    statsChange,
                    0,
                )
            elif choice == 2:
                statsChange = self.increase_stat(
                    "How many points would you like to add to Intelligence?",
                    statsChange,
                    1,
                )
            elif choice == 3:
                statsChange = self.increase_stat(
                    "How many points would you like to add to Strength?",
                    statsChange,
                    2,
                )
            elif choice == 4:
                statsChange = self.increase_stat(
                    "How many points would you like to add to Endurance?",
                    statsChange,
                    3,
                )
            elif choice == 5:
                statsChange = self.increase_stat(
                    "How many points would you like to add to Agility?", statsChange, 4
                )
            elif choice == 6:
                if sum(statsChange) > 0:
                    if confirm := self.confirm_stats(statsChange):
                        return self.set_stats(statsChange)
                return
            else:
                invalidChoice()
        # Displays message indicating that the player has no stat points left
        slow_table(tabulate(
            [[f"{Fore.YELLOW}You have no stat points left.{Style.RESET_ALL}"]], tablefmt="fancy_outline"))
        # Asks the player if they want to confirm their stat changes
        if sum(statsChange) == 0:
            return
        elif confirm := self.confirm_stats(statsChange):
            return self.distribute_stats(statsChange)

    def distribute_stats(self, statsChange):
        self._constitution += statsChange[0]
        self._intelligence += statsChange[1]
        self._strength += statsChange[2]
        self._endurance += statsChange[3]
        self._agility += statsChange[4]
        self._statPoints -= sum(statsChange)
        self._maxHealth = self._constitution * 10
        self._health = self._maxHealth
        self._maxMana = self._intelligence * 5
        self._mana = self._maxMana
        self._defense = self._endurance * 2
        self._damage = self._strength * 2
        return

    def increase_stat(self, statMessage, statsChange, statsChangeIndex):
        # Asks the player how many stat points they want to increase the stat by
        while True:
            slow_table(tabulate([[statMessage]], tablefmt="fancy_outline"))
            try:
                increase = int(input("? "))
            except ValueError:
                invalidChoice("That's not a valid number.")
                continue
            if increase <= self._statPoints:
                break
            else:
                invalidChoice("You don't have enough stat points.")
        statsChange[statsChangeIndex] += increase
        clrscr()
        return statsChange
        
    def confirm_stats(self, statsChange):
        # Displays change between old and new stats
        slow_table(tabulate(
            [
            ["Stat", "Old Stats", "New Stats"],
            ["Constitution:", self._constitution, self._constitution + statsChange[0]],
            ["Health:", self._maxHealth, self._maxHealth + statsChange[0] * 10],
            ["Intelligence:", self._intelligence, self._intelligence + statsChange[1]],
            ["Mana:", self._maxMana, self._maxMana + statsChange[1] * 10],
            ["Strength:", self._strength, self._strength + statsChange[2]],
            ["Damage:", self.damage, self.damage + statsChange[2] * 2],
            ["Endurance:", self._endurance, self._endurance + statsChange[3]],
            ["Defense:", self._defense, self._defense + statsChange[3] * 2],
            ["Agility:", self._agility, self._agility + statsChange[4]],
            ],
            headers="firstrow", tablefmt="fancy_outline", colalign=("right", "center", "center")))
        # Asks the player to confirm their changes
        while True:
            slow_table(tabulate(
                [
                ["", "Are you sure you want to make these changes?"],
                ["1:", "Yes"],
                ["2:", "No"]
                ],
                headers="firstrow", tablefmt="fancy_outline"))
            try:
                choice = int(input("? "))
            except ValueError:
                invalidChoice()
                continue
            if choice == 1:
                return True
            elif choice == 2:
                return False
            else:
                invalidChoice()

    def get_challenge(self):
        # Determines the range of levels for a challenge based on the player's level
        challengeRange = [1, self._level + 1]
        if self._level > 3:
            challengeRange[0] = self._level - 2
        return challengeRange

    # Displays appropriate message for attribute modification
    def modify_attribute(self, attribute, change):
        # Calls parent class method to modify attribute and receives message and new change value
        message, change = super().modify_attribute(attribute, change)
        # Displays appropriate messages based on the message received
        if message == "heal":
            # Displays heal message with the amount healed
            slow_table(tabulate(
                [[f"{Fore.GREEN}You are healed for {change} health points.{Style.RESET_ALL}"]], tablefmt="fancy_grid"))
        if message == "overheal":
            # Displays overheal message with the amount healed
            if change == 1:
                slow_table(tabulate(
                    [[f"{Fore.GREEN}You are healed for {change} health point.{Style.RESET_ALL}"]], tablefmt="fancy_grid"))
            else:
                slow_table(tabulate(
                    [[f"{Fore.GREEN}You are healed for {change} health points.{Style.RESET_ALL}"]], tablefmt="fancy_grid"))
        if message == "regen mana":
            # Displays mana regeneration message with the amount regenerated
            slow_table(tabulate(
                [[f"{Fore.LIGHTCYAN_EX}Your mana regenerates {change} points.{Style.RESET_ALL}"]], tablefmt="fancy_grid"))
        if message == "expend mana":
            # Displays mana expenditure message with the amount expended
            slow_table(
                tabulate([[f"{Fore.LIGHTCYAN_EX}You expend {change} mana.{Style.RESET_ALL}"]], tablefmt="fancy_grid"))
        if message == "over regen mana":
            # Displays over-regen message with the amount regenerated
            if change == 1:
                slow_table(tabulate(
                    [[f"{Fore.LIGHTCYAN_EX}Your mana regenerates {change} point.{Style.RESET_ALL}"]], tablefmt="fancy_grid"))
            elif change > 0:
                slow_table(tabulate(
                    [[f"{Fore.LIGHTCYAN_EX}Your mana regenerates {change} points.{Style.RESET_ALL}"]], tablefmt="fancy_grid"))

    # Displays appropriate message for melee attack
    def melee_attack(self, target):
        # Call parent class's melee_attack method to determine success and damage
        result, damage = super().melee_attack(target)
        # If the attack successfully hit and did damage
        if result == "hit":
            # Display a message indicating the damage dealt
            slow_table(tabulate(
                [[f"You hit {target.name} and deal {Fore.RED}{damage}{Style.RESET_ALL} damage!"]], tablefmt="fancy_outline"))
        # If the attack hit but was blocked by the target's shield
        elif result == "shield block":
            # Display a message indicating the shield blocked the attack
            slow_table(tabulate(
                [[f"You attempt to attack with your {self._equippedWeapon.name}, but it glances off of their {target.equippedShield.name}!"]], tablefmt="fancy_outline"))
        elif result == "block":
            # Display a message indicating the target blocked the attack
            slow_table(tabulate(
                [[f"You attempt to attack with your {self._equippedWeapon.name}, but {target.name} deflects the blow!"]], tablefmt="fancy_outline"))
        # If the attack critically hit
        elif result == "crit":
            # Display a message indicating the attack critically hit
            slow_table(tabulate(
                [[f"You strike a critical blow, delivering a crushing hit that leaves {target.name} reeling!"]], tablefmt="fancy_outline"))

    # Casts fireball on input targets
    def cast_fireball(self, targets):
        self.modify_attribute("mana", -5)
        for enemy in targets:
            # Reduces target's health by 80% of caster's intelligence rounded down
            targets[enemy].modify_attribute(
                "health", -int((self._intelligence * 0.8) // 1))
            # Displays damage dealt to target by fireball
            slow_table(tabulate(
                [[f"The fire engulfs {targets[enemy].name} and deals {Fore.RED}{int((self._intelligence * 0.8) // 1)}{Style.RESET_ALL} damage!"]], tablefmt="fancy_outline"))

    # Casts force bolt on input target
    def cast_force_bolt(self, target):
        self.modify_attribute("mana", -5)
        # Reduces target's health by 150% of caster's intelligence rounded down
        target.modify_attribute("health", -int((self._intelligence * 1.5) // 1))
        # Displays damage dealt to target by force bolt
        slow_table(tabulate(
            [[f"The bolt of force strikes {target.name} and deals {Fore.RED}{int((self._intelligence * 1.5) // 1)}{Style.RESET_ALL} damage!"]], tablefmt="fancy_outline"))

    # Adds/subtracts turns to shield duration and updates defense accordingly
    def modify_shieldDuration(self, turns):
        if turns > 0:
            if self._shieldDuration > 0:
                # Displays message for reinforcing shield duration
                slow_table(tabulate(
                    [[f"{Fore.LIGHTCYAN_EX}Your mana flows out to reinforce your protection.{Style.RESET_ALL}"]], tablefmt="fancy_outline"))
            else:
                # Displays message for creating a new shield
                slow_table(tabulate(
                    [[f"{Fore.LIGHTCYAN_EX}Your mana surges out into a shining shield, helping to protect you from harm.{Style.RESET_ALL}"]], tablefmt="fancy_outline"))
                # Doubles defense while shield is active
                self._defense = self._defense * 2
        # Updates shield duration
        self._shieldDuration += turns
        # Displays message when shield duration ends and updates defense accordingly
        if self._shieldDuration == 0:
            slow_table(tabulate([[f"{Fore.BLACK}Your shield flickers and dies.{Style.RESET_ALL}"]],
                                     tablefmt="fancy_outline"))
            self._defense = int(self._defense / 2)

    # Equips selected item
    def equip_item(self, selected):
        if selected not in [self._equippedWeapon, self._equippedShield]:
            # If selected item is a weapon
            if type(selected) == Weapon:
                # If switching from a weapon to a different weapon
                if escape_ansi(selected.name) != "Fists" and escape_ansi(self._equippedWeapon.name) != "Fists":
                    slow_table(tabulate(
                        [[f"You stow away your {self._equippedWeapon.name} and equip your {selected.name}."]], tablefmt='fancy_outline') + "\n")
                # If switching from a weapon to fists
                elif escape_ansi(self._equippedWeapon.name) != "Fists":
                    slow_table(tabulate(
                        [[f"You stow away your {self._equippedWeapon.name}."]], tablefmt="fancy_outline") + "\n")
                # If equipping a weapon
                else:
                    slow_table(tabulate(
                        [[f"You equip your {selected.name}."]], tablefmt="fancy_outline") + "\n")
                # Set equipped weapon
                self._equippedWeapon = selected
            # If selected item is a shield
            if type(selected) == Shield:
                # If switching from a shield to a different shield
                if escape_ansi(selected.name) != "Fists" and escape_ansi(self._equippedShield.name) != "Fists":
                    slow_table(tabulate(
                        [[f"You stow away your {self._equippedShield} and equip your {selected.name}."]], tablefmt="fancy_outline") + "\n")
                # If switching from a shield to fists
                elif escape_ansi(self._equippedShield.name) != "Fists":
                    slow_table(tabulate(
                        [[f"You stow away your {self._equippedShield.name}."]], tablefmt="fancy_outline") + "\n")
                # If equipping a shield
                else:
                    slow_table(tabulate(
                        [[f"You equip your {selected.name}."]], tablefmt="fancy_outline") + "\n")
                # Set equipped shield
                self._equippedShield = selected
        # If selected item is already equipped
        else:
            slow_table(
                (
                    tabulate(
                        [["You decided what you have is good enough for now."]],
                        tablefmt="fancy_outline",
                    )
                    + "\n"
                )
            )

    # Displays player status and options
    def display_status(self):
        while True:
            # Displays the player's stats
            slow_table(tabulate(
                [
                ["Current Stats", f"+{self._statPoints} Stat Points"],
                ["Constitution:", f"{self._constitution}"],
                ["Health:", f"{self._maxHealth}"],
                ["Intelligence:", f"{self._intelligence}"],
                ["Mana:", f"{self._maxMana}"],
                ["Strength:", f"{self._strength}"],
                ["Damage:", f"{self._damage}"],
                ["Endurance:", f"{self._endurance}"],
                ["Defense:", f"{self._defense}"],
                ["Agility:", f"{self._agility}"]
                ],
                headers="firstrow", tablefmt="fancy_outline", colalign=("right", "center")))
            # Displays player options
            slow_table(
                tabulate(
                    [
                        ["", "What would you like to do?"],
                        ["1:", "Open Inventory"],
                        ["2:", "Distribute Stat Points"],
                        ["3:", "Go Back"]
                    ],
                    headers="firstrow",
                    tablefmt="fancy_outline",
                )
            )
            # Asks player for input
            try:
                statusChoice = int(input("? "))
                clrscr()
            except Exception:
                invalidChoice()
                return
            match statusChoice:
                # Opens inventory
                case 1:
                    self.openInventory()
                # Distributes stat points
                case 2:
                    self.stats_menu()
                # Exits status display
                case 3:
                    break
                # Invalid choice
                case _:
                    invalidChoice()

    # Opens player inventory
    def openInventory(self):
        # Sort inventory for better display
        self.sort_inventory()
        while True:
            # Print inventory table
            slow_table(self.full_inventory_table())
            # Print options for the player to choose from
            inventoryMenu = self.inventory_menu()
            slow_table(
                tabulate(inventoryMenu, headers="firstrow", tablefmt="fancy_outline"))
            try:
                inventoryChoice = int(input("? "))
                clrscr()
            except Exception:
                invalidChoice()
                continue
            match inventoryChoice:
                # Equip a weapon
                case 1:
                    self.sub_inventory_menu("Weapon")
                # Equip a shield
                case 2:
                    self.sub_inventory_menu("Shield")
                # Use a consumable item
                case 3:
                    self.sub_inventory_menu("Consumable")
                # Exit inventory display
                case 4:
                    break
                case _:
                    invalidChoice()

    # Returns a table for the options in the inventory menu
    def inventory_menu(self):
        inventoryMenu = [["What would you like to do?"]]
        for itemType in self._inventory:
            if itemType == "Gold":
                continue
            if len(self._inventory[itemType]) > 0:
                if itemType in ["Weapon", "Shield"]:
                    inventoryMenu.append(
                        [f"{len(inventoryMenu)}:", f"Equip {itemType}"])
                elif itemType == "Consumable":
                    inventoryMenu.append(
                        [f"{len(inventoryMenu)}:", f"Use {itemType}"])
            elif itemType in ["Weapon", "Shield"]:
                inventoryMenu.append(
                    [
                        f"{Fore.RED}{len(inventoryMenu)}:{Style.RESET_ALL}",
                        f"{Fore.RED}Equip {itemType}{Style.RESET_ALL}"
                    ]
                )
            elif itemType == "Consumable":
                inventoryMenu.append(
                    [
                        f"{Fore.RED}{len(inventoryMenu)}:{Style.RESET_ALL}",
                        f"{Fore.RED}Use {itemType}{Style.RESET_ALL}"
                    ]
                )
        inventoryMenu.append((["4:", "Go Back"]))
        return inventoryMenu

    # Displays a table of a specific inventory type, and allows the player to select an item to equip/use
    def sub_inventory_menu(self, inv_type):
        # If there are no items of the specified type in the inventory, display a message and return to inventory menu
        if len(self._inventory[inv_type]) <= 0:
            slow_table(tabulate(
                [[f'You have no {inflectEngine.plural(inv_type)} in your inventory.']], tablefmt="fancy_outline"))
            return "Go Back"
        # If there are items of the specified type in the inventory, display a table of the items
        elif inv_type in ["Weapon", "Shield"]:
            slow_table(
                tabulate([[f"Which {inv_type} would you like to equip?"]], tablefmt="fancy_grid"))
        elif inv_type == "Consumable":
            slow_table(
                tabulate([[f"Which {inv_type} would you like to use?"]], tablefmt="fancy_grid"))
        slow_table(self.sub_inventory_table(inv_type, subMenu=True))
        try:
            # Get player input 
            itemChoice = int(input("? "))
            clrscr()
        except Exception:
            # If the player input is not a number, display an error message and return to inventory menu
            invalidChoice()
            return "Go Back"
        # If the player input is not a valid choice, display an error message and return to inventory menu
        if itemChoice > len(self._inventory[inv_type]) + 1:
            invalidChoice()
            return "Go Back"
        # If the player input is a valid choice, equip/use the item
        for count, item in enumerate(self._inventory[inv_type]):
            if count + 1 == itemChoice and inv_type in ["Weapon", "Shield"]:
                self.equip_item(
                    self._inventory[inv_type][item])
                break
            elif count + 1 == itemChoice and inv_type == "Consumable":
                self.use_item(self._inventory[inv_type][item])
                break
            # If player chooses to go back, display a message and return to inventory menu
            if count + 1 == len(self._inventory[inv_type]):
                if inv_type in ["Weapon", "Shield"]:
                    slow_table(tabulate(
                        [["You decided what you have is good enough for now."]], tablefmt="fancy_outline") + "\n")
                    return "Go Back"
                elif inv_type == "Consumable":
                    slow_table(tabulate(
                        [["You decided not to use anything."]], tablefmt="fancy_outline") + "\n")
                    return "Go Back"


    # Uses selected item
    def use_item(self, item=Consumable()):
        # Check if the item is in the Consumable category of the inventory
        if escape_ansi(item.name) not in self._inventory["Consumable"]:
            return
        # Print a message indicating that the item is being used
        if "Potion" in item.name:
            slow_table(tabulate(
                [[f"You pop the cork from the vial, and down the {item.name} within."]], tablefmt="fancy_outline") + "\n")
        else:
            slow_table(tabulate(
                [[f"You quickly scarf down the {item.name}."]], tablefmt="fancy_outline") + "\n")
            # Modify player attributes based on the item's stats
        for stat in item.stats:
            if stat == "Health":
                self.modify_attribute("health", item.stats["Health"])
            elif stat == "Mana":
                self.modify_attribute("mana", item.stats["Mana"])
        # Reduce the item's quantity by 1 and remove it from inventory if the quantity reaches 0
        item.quantity = item.quantity - 1
        if item.quantity == 0:
            del self._inventory["Consumable"][escape_ansi(item.name)]

    # Adds an item to the player's inventory
    def add_item(self, item):
        # Check if the item already exists in the inventory, and increase its quantity if it does
        if escape_ansi(item.name) in self._inventory[item.itemType]:
            self._inventory[item.itemType][escape_ansi(
                item.name)].quantity += item.quantity
        # Add the item to the inventory if it does not exist
        else:
            self._inventory[item.itemType][escape_ansi(item.name)] = item

    # Modifies the player's gold amount
    def modify_gold(self, goldAmount):
        # Increase or decrease the player's gold based on the input goldAmount, and print a message indicating the change
        self._inventory["Gold"] += goldAmount
        slow_table(tabulate(
            [[f"You gained {Fore.LIGHTYELLOW_EX}{goldAmount} Gold.{Style.RESET_ALL}"]], tablefmt="fancy_grid"))

    # Sorts inventory dictionary by item type, and then by rarity and relevant stat value
    def sort_inventory(self):
        sorted_inventory = {
            'Gold': self._inventory['Gold'],
            'Headers': self._inventory['Headers'],
            'Equipped': self._inventory['Equipped'],
            'Weapon': dict(sorted(self._inventory['Weapon'].items(), key=self.sort_by_rarity_and_stats)),
            'Shield': dict(sorted(self._inventory['Shield'].items(), key=self.sort_by_rarity_and_stats)),
            'Consumable': dict(sorted(self._inventory['Consumable'].items(), key=self.sort_by_rarity_and_stats)),
            'Ingredient': self._inventory['Ingredient']
        }
        # Replaces current inventory dictionary with sorted version
        self._inventory = sorted_inventory

    # Determines rarity of item and relevant stat value based on item type
    def sort_by_rarity_and_stats(self, item):
        rarity = item[1].blank_rarity
        if type(item[1]) == Weapon:
            stats = {"Damage": item[1].damage}
        if type(item[1]) == Shield:
            stats = {"Defense": item[1].defense,
                     "Health Change": item[1].healthChange}
        if type(item[1]) == Consumable:
            stats = item[1].stats
        # Sets default stats value if none are found
        if not stats:
            stats = {'None': 0}
        # Retrieves the relevant stat value and returns a tuple for sorting
        relevant_stat_value = next(iter(stats.values()))
        return (rarity, -relevant_stat_value)

    # Returns formatted table representation of player inventory
    def full_inventory_table(self):
        # Initialize empty string and list for sub table
        inventoryTableString = ""
        subTable = []
        # Iterate through each item type in inventory
        for itemType in self._inventory:
            # Adds Gold amount to inventoryTableString
            if itemType == "Gold":
                inventoryTableString += f"{tabulate([[f'{Fore.LIGHTYELLOW_EX}Gold:{Style.RESET_ALL}', f'{Fore.LIGHTYELLOW_EX}{self._inventory[itemType]}{Style.RESET_ALL}']], tablefmt='fancy_grid')}\n"
                continue
            # Create sub-table for the current item type
            subTable = self.sub_inventory_table(itemType)
            # If sub-table has more than one row, add to inventoryTableString
            if len(subTable) > 1:
                inventoryTableString += f"{tabulate(subTable, headers='firstrow', tablefmt='fancy_outline', colalign=('right', 'left', 'left'))}\n"
        # Return formatted inventory table string
        return inventoryTableString

    # Returns a sub-table for a given item type
    def sub_inventory_table(self, itemType, subMenu=False):
        # If itemType is not "Headers", add the item type header to the sub table
        if itemType != "Headers":
            subTable = [self._inventory["Headers"][itemType]]
        # If itemType is "Equipped", add rows for equipped weapon and shield
        if itemType == "Equipped":
            subTable.append(["Weapon", self._equippedWeapon.name,
                            self._equippedWeapon.get_stats_string()])
            subTable.append(["Shield", self._equippedShield.name,
                            self._equippedShield.get_stats_string()])
            return subTable
        # If not a submenu and itemType is not "Headers", add rows for each item in inventory
        elif subMenu == False and itemType != "Headers":
            for item in self._inventory[itemType]:
                if self._inventory[itemType][item].quantity > 0:
                    subTable.append([self._inventory[itemType][item].name, self._inventory[itemType]
                                    [item].get_stats_string(), self._inventory[itemType][item].quantity])
            return subTable
        # If a submenu and itemType is not "Headers", add numbered rows for each item in inventory and a "Go Back" option
        elif itemType != "Headers":
            for count, item in enumerate(self._inventory[itemType]):
                if self._inventory[itemType][item].quantity > 0:
                    subTable.append([f"{count + 1}:", self._inventory[itemType][item].name, self._inventory[itemType]
                                    [item].get_stats_string(), self._inventory[itemType][item].quantity])
            subTable.append([f"{count + 2}:", "Go Back"])
            return tabulate(subTable, headers="firstrow", tablefmt="fancy_outline")
        # If itemType is "Headers", return empty list
        return []

    # Perform passive actions for the player on a given turn
    def passive_actions(self, turn):
        # increment turn counter
        turn += 1
        # every other turn, increase player's mana by 5
        if turn % 2 == 0:
            self.modify_attribute("mana", 5)
        # if player's shield duration is greater than 0, decrement it by 1
        if self._shieldDuration > 0:
            self.modify_shieldDuration(-1)
        # return updated turn counter
        return turn

    # Returns formatted list representation
    def __repr__(self):
        table = [
            [
                "Name",
                "Level",
                "Health",
                "Mana",
                "Damage",
                "Defense",
                "Agility"
            ],
            [
                self._name,
                f"{Fore.YELLOW}{self._level} {int(self._levelProgress // 1)}/{self._nextLevel}{Style.RESET_ALL}",
                f"{Fore.GREEN}{int(self._health)}/{self._maxHealth}{Style.RESET_ALL}",
                f"{Fore.LIGHTCYAN_EX}{self._mana}/{self._maxMana}{Style.RESET_ALL}",
                f"{Fore.RED}{self._damage} + {self._equippedWeapon.damage}{Style.RESET_ALL}",
                f"{Fore.BLUE}{self._defense} + {self._equippedShield.defense}{Style.RESET_ALL}",
                f"{Fore.LIGHTGREEN_EX}{self._agility}{Style.RESET_ALL}"
            ]
        ]
        if self._shieldDuration > 0:
            table[0].append(
                f"{Fore.LIGHTCYAN_EX}Force Shield{Style.RESET_ALL}")
            table[1].append(
                f"{Fore.LIGHTCYAN_EX}{self._shieldDuration} turns left{Style.RESET_ALL}")
            table[1][
                5] = f"{Fore.BLUE}{self._defense} + {self._equippedShield.defense}{Style.RESET_ALL} ({self._equippedShield.name})"
        return tabulate(table, headers='firstrow', tablefmt="fancy_outline", colalign=["left", "center", "left", "left", "left", "left", "center"])


# enemy class
class Enemy(Entity):
    def __init__(self, name="", level=0, levelProgress=0, nextLevel=0, statPoints=0, levelTable=None, health=0, constitution=0, mana=0, intelligence=0, strength=0, endurance=0, agility=0, inventory=None, equippedWeapon=Weapon(), equippedShield=Shield()):
        if levelTable is None:
            levelTable = (0, 0, 0, 0, 0)
        if inventory is None:
            inventory = {}
        super().__init__(name, level, levelProgress, nextLevel, statPoints, health, constitution, mana, intelligence, strength, endurance, agility, inventory, equippedWeapon, equippedShield)
        self._levelTable = levelTable

    # Increases the enemy's level, health, and mana
    def level_up(self, exp=0, level=0):
        # Call the level_up method of the parent class to update level and attributes
        super().level_up(exp, level)
        # Distribute stats based on the enemy's leveltable
        self.distribute_stats()
        # Set the enemy's health and mana to their max values
        self._health = self._maxHealth
        self._mana = self._maxMana
    
    # Distributes stats based on the enemy's leveltable
    def distribute_stats(self):
        # Add the appropriate number of points to each stat based on the enemy's leveltable
        self._constitution += self._levelTable["con"] * self._statPoints
        self._intelligence += self._levelTable["int"] * self._statPoints
        self._strength += self._levelTable["str"] * self._statPoints
        self._endurance += self._levelTable["end"] * self._statPoints
        self._agility += self._levelTable["agi"] * self._statPoints
        # Reset the stat points to 0
        self._statPoints = 0
        # Update the enemy's health, mana, damage, and defense based on their new stats
        self._maxHealth = self._constitution * 10
        self._maxMana = self._intelligence * 5
        self._damage = self._strength * 2
        self._defense = self._endurance * 2

    """# Displays appropriate message for attribute modification (currently unused)
    def modify_attribute(self, attribute, change):
        # Calls parent class method to modify attribute and receives message and new change value
        super().modify_attribute(attribute, change)
        # Displays appropriate messages based on the message received
        if attribute == "health":
            if change >= 1 and self._health + change < self._maxHealth:
                slow_table(tabulate(
                    [[f"{Fore.GREEN}{self._name} is healed for {change} health points.{Style.RESET_ALL}"]], tablefmt="fancy_outline"))
            elif change >= 1 and self._health != self._maxHealth:
                if self._maxHealth - self._health == 1:
                    slow_table(tabulate(
                        [[f"{Fore.GREEN}{self._name} is healed for {self._maxHealth - self._health} health point.{Style.RESET_ALL}"]], tablefmt="fancy_outline"))
                else:
                    slow_table(tabulate(
                        [[f"{Fore.GREEN}{self._name} is healed for {self._maxHealth - self._health} health points.{Style.RESET_ALL}"]], tablefmt="fancy_outline"))
        if attribute == "mana":
            if change > 1 and self._mana + change <= self._maxMana:
                slow_table(tabulate(
                    [[f"{Fore.LIGHTCYAN_EX}{self._name}'s mana regenerates {change} points.\n{Style.RESET_ALL}"]], tablefmt="fancy_outline"))
            elif change < 1:
                slow_table(tabulate(
                    [[f"{Fore.LIGHTCYAN_EX}{self._name}'s expends {change} mana.{Style.RESET_ALL}"]], tablefmt="fancy_outline"))
            elif self._mana != 50:
                slow_table(tabulate(
                    [[f"{Fore.LIGHTCYAN_EX}{self._name}'s mana regenerates {50 - self._mana} points.{Style.RESET_ALL}"]], tablefmt="fancy_outline") + "\n")"""

    # Displays appropriate message for melee attack
    def melee_attack(self, target):
        # Call parent class's melee_attack method to determine success and damage
        result, damage = super().melee_attack(target)
        # If the attack successfully hit
        if result == "hit":
            # Display a message indicating the damage dealt
            slow_table(tabulate(
                [[f"{self._name} hits you and deals {Fore.RED}{damage}{Style.RESET_ALL} damage!{Style.RESET_ALL}"]], tablefmt="fancy_outline"))
        # If the attack hit but was blocked by the player's shield
        elif result == "shield block":
            # Display a message indicating the shield blocked the attack
            slow_table(tabulate(
                [[f"{self._name} attempts to attack with its {self._equippedWeapon.name}, but you deflect it with your {target.equippedShield.name}!{Style.RESET_ALL}"]], tablefmt="fancy_outline"))
        # If the attack hit but was blocked by the player's base defense
        elif result == "block":
            # Display a message indicating the player blocked the attack
            slow_table(tabulate(
                [[f"{self._name} swings its {self._equippedWeapon.name} at you, but you parry the attack!{Style.RESET_ALL}"]], tablefmt="fancy_outline"))
        # If the attack critically hit
        elif result == "crit":
            # Display a message indicating that they crit
            slow_table(tabulate(
                [[f"{self.name} lands a critical hit, striking a devastating blow and dealing {Fore.RED}{damage}{Style.RESET_ALL} damage!"]], tablefmt="fancy_outline"))

    # Displays death message, deletes self from encounter
    def death(self, encounter):
        slow_table(tabulate(
            [[f"{self._name} {Fore.LIGHTBLACK_EX}falls on the floor, dead.{Style.RESET_ALL}"]], tablefmt="fancy_outline"))
        del encounter.enemies_dict[self._name]

    # Returns stat list
    def get_stats_list(self):
        return [
            f"{self._name}",
            f"{Fore.YELLOW}{self._level}{Style.RESET_ALL}",
            f"{Fore.GREEN}{int(self._health)}/{int(self._maxHealth)}{Style.RESET_ALL}",
            f"{Fore.LIGHTCYAN_EX}{int(self._mana)}/{int(self._maxMana)}{Style.RESET_ALL}",
            f"{Fore.RED}{int(self._damage)} + {self._equippedWeapon.damage}{Style.RESET_ALL}",
            f"{Fore.BLUE}{int(self._defense)} + {self._equippedShield.defense}{Style.RESET_ALL}",
            f"{Fore.LIGHTGREEN_EX}{int(self._agility)}{Style.RESET_ALL}"
        ]

    # Returns formatted list representation
    def __repr__(self):
        return tabulate([["Name", "Level", "Health", "Mana", "Damage", "Defense", "Agility"], self.get_stats_list()], headers='firstrow', tablefmt="fancy_outline", colalign=["left", "center", "center", "center", "center", "center", "center"])


def entityTesting():
    # Testing
    import json
    a = Player()
    e = Enemy("Dire Rabbit")
    with open(mainPath + "\\SaveFiles\\NewGame.json", "r") as saveFile:
        currentGame_dict = json.load(saveFile)
        saveFile.close()
    player_dict = currentGame_dict["player"]
    a.reader(player_dict)
    """a.level_up(100, 2)"""
    print(e)
    e.reader(currentGame_dict["encounterTables"]
             ["Plains"]["hostile"]["3"]["_enemies"]["Dire Rabbit"])
    print(e)
    e.level_up(level=2)
    print(e)
    e.level_up(level=3)
    print(e)
    """a.openInventory()"""


# If file is run directly, run testing()
if __name__ == "__main__":
    entityTesting()
