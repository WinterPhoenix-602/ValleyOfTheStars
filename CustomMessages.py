# Date: 2023-03-14
# Description: Contains functions for displaying messages to the user.

import os
import textwrap
from colorama import Fore, Style
import time
from tabulate import tabulate
import inflect
import re

# Create an inflect engine for pluralizing words
inflectEngine = inflect.engine()
# Define the path to the current module's directory
mainPath = os.path.dirname(__file__)
# Define the path to "NewGame.json"
newGameTiles = os.path.join(mainPath, "NewGameFiles\\Tiles.json")
newGameQuests = os.path.join(mainPath, "NewGameFiles\\Quests.json")
newGamePlayer = os.path.join(mainPath, "NewGameFiles\\Player.json")
newGameEnemies = os.path.join(mainPath, "NewGameFiles\\Enemies.json")
newGameEncounters = os.path.join(mainPath, "NewGameFiles\\Encounters.json")
# Define the path to "SaveFileInfo.json"
saveFileInfoPath = os.path.join(mainPath, "SaveFiles\\SaveFileInfo.json")

# Clears terminal/console
def clrscr():
    # Use the appropriate command to clear the screen based on the OS
    os.system('cls' if os.name == 'nt' else 'clear')

# Removes ANSI escape sequences from a string
def escape_ansi(line=""):
    ansi_escape =re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line)

# Waits for the user to press Enter before continuing
def waitForKey(encounterType="", message=""):
    if encounterType == "combat":
        # If the encounter type is combat, display a victory message
        slow_table(message)
    elif encounterType == "inspect":
        # If the encounter type is inspect, display a message indicating interest
        slow_table("Interesting...")
    # If the encounter type is conversation, rest, or passive, do nothing
    slow_table("Press Enter to Continue")
    # Wait for the user to press Enter before continuing
    input()
    # Clear the screen
    clrscr()

# Prints an error message for an invalid choice
def invalidChoice(invalidChoice = "I'm sorry, that is not a valid choice."):
    # Construct the error message in red using the colorama library
    invalidChoice = f"{Fore.RED}{invalidChoice}{Style.RESET_ALL}"
    # Clear the screen
    clrscr()
    # Display the error message
    slow_table(invalidChoice)

# Prints a slow of text with a delay b etween each character
def slow_line(string="Testing, 1, 2.", delay=0.025, end="\n"):
    # If the end parameter is valid, do nothing
    if end not in ["\n", ""]:
        raise InvalidEndline("contains invalid endline character")
    # Iterate over the characters in the input string
    for character in string:
        # Print the Character with no endline, wait for specified delay
        print(character, end="")
        time.sleep(delay)
    # Print the specified endline character
    print(end, end="")

# Prints a formatted table with a delay between each line
def slow_table(string=None, tablefmt="fancy_grid", headers=False, colalign=(), delay=0.05):
    if string is None:
        string = [["Testing"], [1], [2]]
    if type(string) == str:
        # If the input is a string, wrap it to 100 characters
        string = textwrap.fill(string, 100, break_long_words=False, break_on_hyphens=False)
        # Wrap the string in a table
        string = tabulate([[string]], tablefmt=tablefmt)
    elif type(string) == list and headers is False:
        # Wrap the string in a table
        string = tabulate(string, tablefmt=tablefmt, colalign=colalign)
    elif type(string) == list:
        # Wrap the string in a table
        string = tabulate(string, tablefmt=tablefmt, headers=headers, colalign=colalign)
    # Split the string into lines and iterate over each one
    for line in string.splitlines():
        #Print the line, wait for specified delay
        print(line)
        time.sleep(delay)

# Formats a description for display
def formatForTable(inputText="", wrap=100):
    # If the text is a string, wrap it to the specified width
    if type(inputText) == str:
        return textwrap.fill(inputText, wrap, break_long_words=False, break_on_hyphens=False)
    # If the text is contained in a list, iterate over each element and wrap it to the specified width
    elif type(inputText) == list:
        for count, paragraph in enumerate(inputText):
            inputText[count] = textwrap.fill(
                inputText[count], wrap, break_long_words=False, break_on_hyphens=False)
        return inputText


# Defines a custom exception for invalid endline characters
class InvalidEndline(Exception):
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)


# Defines a custom exception for invalid rarity values
class InvalidRarity(Exception):
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)

# Defines a custom exception for invalid action values
class InvalidAction(Exception):
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)

# Testing function
def messageTesting():
    print(inflectEngine.plural("fish"))
    waitForKey("combat", "You have defeated the enemy!")
    waitForKey("inspect", "Interesting...")
    waitForKey("conversation")
    waitForKey("passive")
    invalidChoice()

# If this file is run directly, run testing()
if __name__ == "__main__":
    messageTesting()