# Date: 2023-03-02
# Description: Contains the Tile class, which is used to create the tiles that make up the map

from pygame import *
from tabulate import tabulate
from EncounterClasses import *
from EntityClasses import Player
from CustomMessages import *
from abc import ABC, abstractmethod
clrscr()


class Tile:
    def __init__(self, id="tile00", name="", description="", actions=None, visited=True, image="EmptyPlain.png", mapCoords=(0, 0), encounterTable=None):
        if actions is None:
            actions = {}
        if encounterTable is None:
            encounterTable = []
        self._id = id
        self._name = name
        self._description = description
        self._actions = actions
        self._visited = visited
        self._image = image
        self._mapCoords = mapCoords
        self._encounterTable = encounterTable

    # Getters
    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return "\n\n".join(self._description)

    @property
    def actions(self):
        return self._actions

    @property
    def visited(self):
        return self._visited

    @property
    def image(self):
        return self._image

    @property
    def mapCoords(self):
        return self._mapCoords

    @property
    def encounterTable(self):
        return self._encounterTable

    # Setters
    @id.setter
    def id(self, id):
        self._id = id

    @name.setter
    def name(self, name):
        self._name = name

    @description.setter
    def description(self, description):
        self._description = description

    @actions.setter
    def actions(self, actions):
        self._actions = actions

    @visited.setter
    def visited(self, visited=False):
        self._visited = visited

    @image.setter
    def image(self, image):
        self._image = image

    @mapCoords.setter
    def mapCoords(self, mapCoords):
        self._mapCoords = mapCoords

    @encounterTable.setter
    def encounterTable(self, encounterTable):
        self._encounterTable = encounterTable

    # Sets attributes from input dictionary
    def reader(self, tiles_dict):
        for key in tiles_dict:
            try:
                setattr(self, key, tiles_dict[key])
            except Exception:
                print("No such attribute, please consider adding it in init.")
                continue
        # If the description is not an empty string
        if self._description != "":
            # Format the description to fit the table
            formatForTable(self._description)
        # If there are available actions
        if self._actions != {}:
            # Convert each to dictionary to the appropriate action object
            for action in self._actions:
                if type(self._actions[action]) == dict:
                    # Convert Travel actions
                    if self._actions[action]["_action"] == "Travel":
                        a = Travel(action)
                        a.reader(self._actions[action])
                        self._actions[action] = a
                        continue
                    # Convert Rest actions
                    if self._actions[action]["_action"] == "Rest":
                        a = Rest(action)
                        a.reader(self._actions[action])
                        self._actions[action] = a
                        continue
                    # Convert Inspect actions
                    if self._actions[action]["_action"] == "Inspect":
                        a = InspectElement(action)
                        a.reader(self._actions[action])
                        self._actions[action] = a
                        continue
                    # Convert Speak actions
                    if self._actions[action]["_action"] == "Speak":
                        a = Speak(action)
                        a.reader(self._actions[action])
                        self._actions[action] = a

    def tileMenu(self, currentTile, turn=0, player=Player(), tiles_dict=None):
        if tiles_dict is None:
            tiles_dict = {}
        exitGame = False
        self._visited = True
        while True:
            # Print tile description and player status
            slow_table([[self._name], ["\n\n".join(self._description)]], tablefmt="fancy_grid")
            slow_table(player.__repr__(), headers='firstrow', tablefmt="fancy_outline", colalign=["left", "center", "left", "left", "left", "left", "center"])
            # Get the list of available actions
            optionsTable = self.tile_menu_options()
            # Print the list of available actions
            slow_table(optionsTable, headers="firstrow", tablefmt="fancy_outline")
            # Get player choice
            try:
                choice = int(input("? "))
                clrscr()
            except Exception:
                invalidChoice()
                continue
            # Perform the action
            currentTile, turn, tiles_dict, exitGame = self.process_action(choice, turn, player, tiles_dict)
            if currentTile != self:
                return currentTile, turn, tiles_dict, exitGame
            if exitGame in [True, "save"]:
                return currentTile, turn, tiles_dict, exitGame
            

    # Returns a table of options for the tile menu
    def tile_menu_options(self):
        optionsTable = [["", "What would you like to do?"]]
        for count, action in enumerate(self._actions):
            if not isinstance(self._actions[action], Action):
                raise InvalidAction("Invalid action type")
            # If the  action is locked, display it with it's index in red to indicate that it is locked
            if self._actions[action].locked == True:
                                    optionsTable.append(
                [f"{Fore.RED}{count + 1}:{Style.RESET_ALL}", f"{Fore.RED}{self._actions[action].name}{Style.RESET_ALL}"])
            # If the action is an Inspect or Speak action and has not been seen, display it with it's index in yellow to indicate that it is unseen
            elif isinstance(self._actions[action], (InspectElement, Speak)) and self._actions[action].seen == False:
                optionsTable.append(
                    [f"{Fore.YELLOW}{count + 1}:{Style.RESET_ALL}", f"{Fore.YELLOW}{self._actions[action].name}{Style.RESET_ALL}"])
            # If the action is an Inspect or Speak action and has been seen, display it with it's index in gray to indicate that it is seen
            elif self._actions[action].seen == True and (
                isinstance(self._actions[action], (InspectElement, Speak))
            ):
                optionsTable.append(
                    [f"{Fore.LIGHTBLACK_EX}{count + 1}:{Style.RESET_ALL}", f"{Fore.LIGHTBLACK_EX}{self._actions[action].name}{Style.RESET_ALL}"])
            # If the action is not locked, display it with it's index in green to indicate that it is unlocked
            else:
                optionsTable.append(
                    [f"{Fore.GREEN}{count + 1}:{Style.RESET_ALL}", f"{Fore.GREEN}{self._actions[action].name}{Style.RESET_ALL}"])
        # Add options for opening inventory, displaying map, and exiting game
        optionsTable.extend(
            iter(
                [
                    [f"{count + 2}:", "Player Status"],
                    [f"{count + 3}:", "Display Map"],
                    [f"{count + 4}:", "Save Game"],
                    [f"{count + 5}:", "Exit Game"],
                ]
            )
        )
        return optionsTable

    def process_action(self, choice, turn, player, tiles_dict):
        for count, action in enumerate(self._actions):
            if count + 1 == choice:
                # If the action is locked, display a message and return to the tile menu
                if self._actions[action].locked == True:
                    invalidChoice(self._actions[action].locked_message)
                    return self, turn, tiles_dict, False
                # If the player chose a Travel action, update the current tile and process passive actions
                elif isinstance(self._actions[action], Travel):
                    currentTile = self._actions[action].take_action(tiles_dict)
                    turn = player.passive_actions(turn)
                    return currentTile, turn, tiles_dict, False
                # If the player chose a Rest action, process passive actions
                elif isinstance(self._actions[action], Rest):
                    self._actions[action].take_action(tiles_dict, player)
                    turn = player.passive_actions(turn)
                    return self, turn, tiles_dict, False
                # If the player chose an Inspect action, display information and process passive actions
                elif isinstance(self._actions[action], InspectElement):
                    self._actions[action].take_action(tiles_dict, self)
                    turn = player.passive_actions(turn)
                    return self, turn, tiles_dict, False
                # If the player chose a Speak action, begin conversation, then process passive actions
                elif isinstance(self._actions[action], Speak) and self._actions[action].locked == False:
                    self._actions[action].take_action(tiles_dict)
                    turn = player.passive_actions(turn)
                    return self, turn, tiles_dict, False
            # If the player chose to open their inventory, do so
            elif len(self._actions) + 1 == choice:
                player.display_status()
                return self, turn, tiles_dict, False
            # If the player chose to look at the map, display it
            elif len(self._actions) + 2 == choice:
                self.displayMap(tiles_dict)
                return self, turn, tiles_dict, False
            # If the player chose to save the game, break from loop
            elif len(self._actions) + 3 == choice:
                return self, turn, tiles_dict, "save"
            # If the player chose to exit the game, break from loop
            elif len(self._actions) + 4 == choice:
                return self, turn, tiles_dict, True
            # If the player input an invalid choice, display error message and continue the loop
            elif choice > len(self._actions) + 3 or choice < 1:
                invalidChoice()
                return self, turn, tiles_dict, False

    # Displays map with visited tiles
    def displayMap(self, tiles_dict):
        invalidChoice("Not yet implemented.")

    def __repr__(self):
        return tabulate([[self._name], ["\n\n".join(self._description)]], tablefmt="fancy_grid")


class Action(ABC):
    def __init__(self, name="", description="", locked=False, locked_message="", update_tile=None, seen=False):
        if update_tile is None:
            update_tile = {}
        self._name = name
        self._description = description
        self._locked = locked
        self._locked_message = locked_message
        self._update_tile = update_tile
        self._seen = seen
    
    # Getters
    @property
    def name(self):
        return self._name
    
    @property
    def description(self):
        return self._description
    
    @property
    def locked(self):
        return self._locked
    
    @property
    def locked_message(self):
        return self._locked_message
    
    @property
    def update_tile(self):
        return self._update_tile
    
    @property
    def seen(self):
        return self._seen
    
    # Setters
    @locked.setter
    def locked(self, value):
        self._locked = value
    
    @seen.setter
    def seen(self, value):
        self._seen = value

    # Sets attributes from input dictionary
    def reader(self, input_dict):
        for key in input_dict:
            try:
                setattr(self, key, input_dict[key])
            except Exception:
                print("No such attribute, please consider adding it in init.")
        # If the description is not an empty string
        if self._description != "":
            formatForTable(self._description)

    # Takes action
    @abstractmethod
    def take_action(self, tiles_dict):
        pass

    # Updates action values
    def update_tile_attribute(self, dict, update):
        for key, value in update.items():
            if key in dict and isinstance(dict[key], Tile):
                for key2, value2 in value.items():
                    self.update_tile_attribute(getattr(dict[key], key2), value2)
            elif isinstance(dict[key], Action):
                for key2, value2 in value.items():
                    setattr(dict[key], key2, value2)
                self._update_tile = {}
        return dict


class Travel(Action):
    def __init__(self, name="", direction="", targetTile="", locked=False, locked_message="", update_tile=None, seen=False):
        if update_tile is None:
            update_tile = {}
        super().__init__(name, locked=locked, locked_message=locked_message, update_tile=update_tile, seen=seen)
        self._direction = direction
        self._targetTile = targetTile

    @property
    def direction(self):
        return self._direction

    @property
    def targetTile(self):
        return self._targetTile

    def take_action(self, tiles_dict=None):
        # Call the parent class's take_action method
        super().take_action(tiles_dict)
        if tiles_dict is None:
            tiles_dict = {}
        # If the action has an update_tile attribute, update the target tile's attributes
        if self._update_tile != {}:
            self.update_tile_attribute(tiles_dict, self._update_tile)
        # Return the tile the player is now on
        return tiles_dict[self._targetTile]


class InspectElement(Action):
    def __init__(self, name="", description="", locked=False, locked_message="", update_tile=None, seen=False, change_name=None, change_description=None, change_image=None):
        if update_tile is None:
            update_tile = {}
        if change_name is None:
            change_name = [False]
        if change_description is None:
            change_description = [False]
        if change_image is None:
            change_image = [False]
        super().__init__(name, description, locked, locked_message, update_tile, seen)
        self._change_name = change_name
        self._change_description = change_description
        self._change_image = change_image

    # Getters
    @property
    def change_name(self):
        return self._change_name

    @property
    def change_description(self):
        return self._change_description

    @property
    def change_image(self):
        return self._change_image
    
    # Process the action
    def take_action(self, tiles_dict, currentTile):
        # Call the parent class's take_action method
        super().take_action(tiles_dict)
        # Display the name and description of the current tile
        slow_table([[self._name], ["\n\n".join(self._description)]], tablefmt="fancy_grid")
        # Modify the tile's name if necessary
        if self._change_name[0] == True:
            currentTile.name = self._change_name[1]
        # Modify the tile's description if necessary
        if self._change_description[0] == True:
            for count, paragraph in enumerate(self._change_description[1]):
                self._change_description[1][count] = textwrap.fill(
                    self._change_description[1][count], 100)
            currentTile.description = self._change_description[1]
        # Modify the tile's image if necessary
        if self._change_image[0] == True:
            currentTile.image = self._change_image[1]
        # Wait for user input before setting the seen property to True
        waitForKey("inspect")
        self._seen = True
        # If the action has an update_tile attribute, update the target tile's attributes
        if self._update_tile != {}:
            self.update_tile_attribute(tiles_dict, self._update_tile)

class Speak(Action):
    def __init__(self, name="", description="", locked=False, locked_message="", update_tile=None, seen=False, response=None, options=None):
        if update_tile is None:
            update_tile = {}
        if response is None:
            response = [""]
        if options is None:
            options = {}
        super().__init__(name, description, locked, locked_message, update_tile, seen)
        self._response = response
        self._options = options

    # Getters
    @property
    def options(self):
        return self._options

    # Sets attributes from input dictionary
    def reader(self, input_dict):
        super().reader(input_dict)
        # If the Speak action has options, create a new Speak action for each option and call reader on each option
        if self._options != {}:
            for option in self._options:
                a = Speak(option)
                a.reader(self._options[option])
                self._options[option] = a
        # Wrap each response in the Speak action to 100 characters
        if self._response != [""]:
            for count, paragraph in enumerate(self._response):
                self._response[count] = textwrap.fill(
                    self._response[count], 100)

    def take_action(self, tiles_dict=None):
        # Call the parent class's take_action method
        super().take_action(tiles_dict)
        while True:
            # If the response is not empty, print it as a table
            if self._response != [""]:
                slow_table("\n\n".join(self._response), tablefmt="fancy_grid")
            # If there are options available for the Speak object, display them
            if self._options != {}:
                optionsTable = self.optionsMenu()
                slow_table(optionsTable, headers="firstrow", tablefmt="fancy_grid")
                # Prompt the user to select an option
                try:
                    choice = int(input("? "))
                    # If the choice is greater than the number of available options, prompt the user to select again
                    if choice > len(self._options) + 1:
                        invalidChoice()
                        continue
                except Exception:
                    # If the choice is not a number, prompt the user to select again
                    invalidChoice()
                    continue
                # Clear the screen and take action based on the user's choice
                clrscr()
                for count, option in enumerate(self._options):
                    if count + 1 == choice:
                        self._options[option].take_action()
                if count + 2 == choice:
                    break
                # Update the _seen property based on if all options have been seen
                for option in self._options:
                    if self._options[option].seen == True:
                        self._seen = True
                        # If the action has an update_tile attribute, update the target tile's attributes
                        if self._update_tile != {}:
                            self.update_tile_attribute(tiles_dict, self._update_tile)
                for option in self._options:
                    if self._options[option].seen == False:
                        self._seen = False
                        # If the action has an update_tile attribute, update the target tile's attributes
                        if self._update_tile != {}:
                            self.update_tile_attribute(tiles_dict, self._update_tile)
            # If there are no options available, wait for user input to continue
            else:
                waitForKey("conversation")
                # Sets the _seen property to True
                self._seen = True
                # If the action has an update_tile attribute, update the target tile's attributes
                if self._update_tile != {}:
                    self.update_tile_attribute(tiles_dict, self._update_tile)
                break

    def optionsMenu(self):
        optionsTable = [["", "What would you like to say?"]]
        for count, option in enumerate(self._options):
            # If an option is another Speak object and has not been seen before, display it with its index in yellow
            if isinstance(self._options[option], Speak) and self._options[option].seen == False:
                # If the option's description is more than one line, format each line
                if len(self._options[option].description[0].splitlines(True)) > 1:
                    optionDescription = [
                        f"{Fore.YELLOW}{escape_ansi(line)}{Style.RESET_ALL}".format(
                            line
                        )
                        for line in self._options[option]
                        .description[0]
                        .splitlines()
                    ]
                    self._options[option].description[0] = "\n".join(optionDescription)
                optionsTable.append(
                    [f"{Fore.YELLOW}{count + 1}:{Style.RESET_ALL}", f"{Fore.YELLOW}{self._options[option].description[0]}{Style.RESET_ALL}"])
            # If an option is another Speak object and has been seen before, display it with its index in light black. If the option's description is more than one line, format each line
            elif len(self._options[option].description[0].splitlines(True)) > 1:
                optionDescription = [
                    f"{Fore.LIGHTBLACK_EX}{escape_ansi(line)}{Style.RESET_ALL}".format(
                        line
                    )
                    for line in self._options[option]
                    .description[0]
                    .splitlines()
                ]
                self._options[option].description[0] = "\n".join(optionDescription)
                optionsTable.append(
                    [f"{Fore.LIGHTBLACK_EX}{count + 1}:{Style.RESET_ALL}", f"{Fore.LIGHTBLACK_EX}".join(self._options[option].description[0].splitlines(True))])
            else:
                optionsTable.append(
                    [f"{Fore.LIGHTBLACK_EX}{count + 1}:{Style.RESET_ALL}", f"{Fore.LIGHTBLACK_EX}{self._options[option].description[0]}{Style.RESET_ALL}"])
        optionsTable.append([f"{count + 2}:", "Go Back"])
        return optionsTable

# Rest action
class Rest(Action):
    def __init__(self, name="", description="", locked=False, locked_message="", update_tile=None, seen=False):
        if update_tile is None:
            update_tile = {}
        super().__init__(name, description, locked, locked_message, update_tile, seen)

    # Process the Rest action
    def take_action(self, tiles_dict, player):
        # Call the parent class's take_action method
        super().take_action(tiles_dict)
        # Display the name and description of the Rest action
        slow_table([[self._name], ["\n\n".join(self._description)]], tablefmt="fancy_grid")
        # Restore the player's health and mana to full, then wait for user input to continue
        player.health = player.maxHealth
        player.mana = player.maxMana
        waitForKey("rest")
        # If the action has an update_tile attribute, update the target tile's attributes
        if self._update_tile != {}:
            self.update_tile_attribute(tiles_dict, self._update_tile)

def tileTesting():
    # Testing
    import json
    p = Player()
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
    with open(mainPath + "\\NewGameFiles\\Encounters.json", "r") as encountersFile:
        encounters_dict = json.load(encountersFile)
        encountersFile.close()
    for biome in encounters_dict:
        for encounterType in encounters_dict[biome]:
            if encounterType == "passive":
                for encounter in encounters_dict[biome][encounterType]:
                    a = PassiveEncounter(encounterType=encounter)
                    a.reader(encounters_dict[biome][encounterType][encounter])
                    encounters_dict[biome][encounterType][encounter] = a
                    continue
            if encounterType == "hostile":
                for encounter in encounters_dict[biome][encounterType]:
                    a = CombatEncounter(encounterType=encounter, base_enemy_dict=enemies_dict)
                    a.reader(encounters_dict[biome][encounterType][encounter])
                    encounters_dict[biome][encounterType][encounter] = a
                    continue
    with open(mainPath + "\\NewGameFiles\\Tiles.json", "r") as tilesFile:
        tiles_dict = json.load(tilesFile)
        tilesFile.close()
    for tile in tiles_dict:
        a = Tile(tile)
        a.reader(tiles_dict[tile])
        tiles_dict[tile] = a
    currentTile = tiles_dict["CelestialSentinel"]
    currentTile.tileMenu(currentTile, 0, p, tiles_dict)

# If this file is run directly, run tileTesting()
if __name__ == "__main__":
    tileTesting()
