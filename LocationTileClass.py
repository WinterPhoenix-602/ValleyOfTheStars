# Date: 2023-03-02
# Description: Contains the Tile class, which is used to create the tiles that make up the map

from pygame import *
from tabulate import tabulate
from EncounterClasses import *
from EntityClasses import Player
from CustomMessages import *
from ActionClasses import *
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
            slow_table(tabulate(
                [[self._name], ["\n\n".join(self._description)]], tablefmt="fancy_grid"))
            slow_table(player.__repr__())
            # Get the list of available actions
            optionsTable = self.tile_menu_options()
            # Print the list of available actions
            slow_table(
                tabulate(optionsTable, headers="firstrow", tablefmt="fancy_outline"))
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
                    [f"{count + 2}:", "Display Player Status"],
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
                player.openInventory()
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

def tileTesting():
    # Testing
    import json
    from EntityClasses import Player
    with open(newGamePath, "r") as saveFile:
        newGame_dict = json.load(saveFile)
        saveFile.close()
    player_dict = newGame_dict["player"]
    tiles_dict = newGame_dict["tiles"]
    for tile in tiles_dict:
        a = Tile(tile)
        a.reader(tiles_dict[tile])
        tiles_dict[tile] = a
    currentTile = tiles_dict["CelestialSentinel"]
    p = Player()
    p.reader(player_dict)
    currentTile.tileMenu(currentTile, 0, p, tiles_dict)

# If this file is run directly, run tileTesting()
if __name__ == "__main__":
    tileTesting()
