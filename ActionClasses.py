# Date: 2023-03-02
# Description: Contains classes defining the actions that can be taken in the game, as well as quest lines.

from abc import ABC, abstractmethod
from CustomMessages import *
from LocationTileClass import Tile

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
    def take_action(self, tiles_dict, currentTile=Tile()):
        # Call the parent class's take_action method
        super().take_action(tiles_dict)
        # Display the name and description of the current tile
        slow_table(tabulate(
            [[self._name], ["\n\n".join(self._description)]], tablefmt="fancy_grid"))
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
                slow_table(
                    tabulate([["\n\n".join(self._response)]], tablefmt="fancy_grid"))
            # If there are options available for the Speak object, display them
            if self._options != {}:
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
                slow_table(
                    tabulate(optionsTable, headers="firstrow", tablefmt="fancy_grid"))
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
        slow_table(tabulate(
            [[self._name], ["\n\n".join(self._description)]], tablefmt="fancy_grid"))
        # Restore the player's health and mana to full, then wait for user input to continue
        player.health = player.maxHealth
        player.mana = player.maxMana
        waitForKey("rest")
        # If the action has an update_tile attribute, update the target tile's attributes
        if self._update_tile != {}:
            self.update_tile_attribute(tiles_dict, self._update_tile)

def actionTesting():
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

if __name__ == "__main__":
    actionTesting()