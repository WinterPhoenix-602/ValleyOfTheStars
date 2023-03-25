# 2023-03-02
# Main Game File

import json
import copy
import os
import shelve
import CustomMessages
import EntityClasses
import LocationTileClass
import datetime
import tabulate
import ItemClass
from random import randint
from ItemClass import *
from CustomMessages import *
from EntityClasses import Player
from LocationTileClass import *
from datetime import datetime
from tabulate import tabulate

"""# enables colors on windows
if os.name == 'nt':
    os.system("reg add HKEY_CURRENT_USER\\Console /v VirtualTerminalLevel /t REG_DWORD /d 1")
    clrscr()"""


# The main function of the game
def main():
    while True:
        # Start the main menu and get initial game state
        player, tiles_dict, currentTile, encounterTables_dict = mainMenu()
        turn = 0
        while True:
            # Check if current tile has an encounter and if it should trigger
            if (
                len(currentTile.encounterTable) > 0
                and turn > 0
                and randint(1, 100) <= currentTile.encounterTable[1]
            ):
                # Determine whether encounter is passive or hostile and choose a random encounter from the appropriate encounter table
                passiveOrHostile = "hostile" if randint(
                    1, 100) <= currentTile.encounterTable[3] else "passive"
                encounter = str(randint(
                    1, len(encounterTables_dict[currentTile.encounterTable[0]][passiveOrHostile])))
                # Start the encounter and update the encounter table's cooldown
                if passiveOrHostile == "hostile":
                    victory = encounterTables_dict[currentTile.encounterTable[0]
                                         ]["hostile"][encounter].start_encounter(player, turn)
                    # Check if player has won the encounter
                    if victory == False:
                        # Return to main menu
                        break
                    if exitGame == True:
                        break
                elif passiveOrHostile == "passive":
                    encounterTables_dict[currentTile.encounterTable[0]
                                         ]["passive"][encounter].start_encounter(player)
                currentTile.encounterTable[1] = currentTile.encounterTable[2]
            # Display the tile menu and update game state based on user input
            currentTile, turn, tiles_dict, exitGame = currentTile.tileMenu(
                currentTile, turn, player, tiles_dict)
            # Check if player has chosen to exit the game
            if exitGame == True:
                # End the game and check if player wants to play again
                exitGame = endGame(exitGame, tiles_dict,
                                   player, currentTile, encounterTables_dict)
            if exitGame == True:
                # Return to main menu
                break
            # Check if player has chosen to save the game
            if exitGame == "save":
                # Save the game
                saveMenu(tiles_dict, player, currentTile, encounterTables_dict)

# Displays the main menu and prompts the user to choose between starting a new game, loading a saved game, or ending the program.
def mainMenu():
    while True:
        # Displays the options for the main menu as a table
        slow_table(tabulate([["1: New Game"], ["2: Load Game"], [
            "3: Exit"]], tablefmt="fancy_outline"))
        # Prompts the user to input their choice and converts it to an integer
        try:
            choice = int(input("? "))
        except Exception:
            # Displays an error message and prompts the user to try again
            invalidChoice()
            continue
        # Checks if the user's choice is a valid option (1, 2, or 3)
        if choice < 1 or choice > 3:
            # Displays an error message and prompts the user to try again
            invalidChoice()
            continue
        # Clears the screen
        clrscr()
        # Determines which menu option the user chose
        match choice:
            case 1:
                # Starts a new game
                player, tiles_dict, currentTile, encounterTables_dict = newGame()
            case 2:
                # Loads a saved game
                player, tiles_dict, currentTile, encounterTables_dict = loadGame()
                if player == 0:
                    continue
            case 3:
                # Exits the program
                exit()
        # Returns the initial game state based on the user's choice
        return player, tiles_dict, currentTile, encounterTables_dict

# Initializes the base game state
def newGame():
    # Open the newGamePath file and load its contents into currentGame_dict
    while True:
        with open(newGamePath, "r") as newGameFile:
            currentGame_dict = json.load(newGameFile)
            newGameFile.close()
        # Extract the player and tiles data from currentGame_dict and create objects for them
        player_dict = currentGame_dict["player"]
        tiles_dict = currentGame_dict["tiles"]
        for tile in tiles_dict:
            # Create a new Tile object and read its data from tiles_dict
            a = Tile(tile)
            a.reader(tiles_dict[tile])
            tiles_dict[tile] = a
        # Set the currentTile to the starting tile (tile00) in tiles_dict
        currentTile = tiles_dict["tile00"]
        # Extract the encounter tables from currentGame_dict and create objects for them
        encounterTables_dict = currentGame_dict["encounterTables"]
        for biome in encounterTables_dict:
            for encounterType in encounterTables_dict[biome]:
                # If the encounter type is "passive", create a new PassiveEncounter object and read its data from encounterTables_dict
                if encounterType == "passive":
                    for encounter in encounterTables_dict[biome][encounterType]:
                        a = PassiveEncounter(encounterType=encounterType)
                        a.reader(
                            encounterTables_dict[biome]["passive"][encounter])
                        encounterTables_dict[biome]["passive"][encounter] = a
                        continue
                # If the encounter type is "hostile", create a new CombatEncounter object and read its data from encounterTables_dict
                if encounterType == "hostile":
                    for encounter in encounterTables_dict[biome][encounterType]:
                        a = CombatEncounter(encounterType=encounterType)
                        a.reader(
                            encounterTables_dict[biome]["hostile"][encounter])
                        encounterTables_dict[biome]["hostile"][encounter] = a
                        continue
        # Prompt the player to enter a name and create a new Player object with that name
        while True:
            player = Player()
            slow_table(tabulate(
                [["What would you like to name your character?\nYour chosen name must be less than 25 characters long."]], tablefmt="fancy_grid"))
            player.name = input("? ")
            clrscr()
            if len(player.name) > 25:
                slow_table(
                    tabulate([["I'm sorry, that name is too long."]], tablefmt="fancy_outline"))
                continue
            player.reader(player_dict)
            break
        return player, tiles_dict, currentTile, encounterTables_dict

# Loads a saved game
def loadGame():
    while True:
        try:
            # Open the file containing information about saved games
            with open(saveFileInfoPath, "r") as savesInfo:
                # Load the JSON data from the file into a dictionary
                saveFiles_dict = json.load(savesInfo)
                savesInfo.close()
        except FileNotFoundError:
            # If the file is missing, report an error and exit the function
            slow_table(
                tabulate([["Save file information has been corrupted, moved, or deleted."]], tablefmt="fancy_outline"))
            break
        # Create a table showing the available saved games
        loadMenuTable = [["Which game save would you like to load?"]]
        for count, saveFile in enumerate(saveFiles_dict):
            loadMenuTable.append(
                [f"{count + 1}: {saveFiles_dict[saveFile]['name']} {saveFiles_dict[saveFile]['info']}"])
            if count + 1 == len(saveFiles_dict):
                # Add an option to go back to the main menu
                loadMenuTable.append(["6: Go Back"])
        # Display the table of saved games and prompt the user to choose one
        slow_table(tabulate(loadMenuTable, headers="firstrow",
                                 tablefmt="fancy_outline"))
        try:
            # Convert the user's input to an integer
            saveChoice = int(input("? "))
            # Clear the screen
            clrscr()
        except Exception:
            # If the user enters invalid input, display an error message and prompt again
            invalidChoice()
            continue
        # Depending on the user's choice, set the file path for the selected saved game
        if saveChoice in {1, 2, 3, 4, 5}:
            saveFilePath = os.path.join(
                mainPath, f"SaveFiles\\Save{saveChoice}")
        elif saveChoice == 6:
            # If the user chooses to go back, return to the main menu
            return 0, 0, 0, 0
        else:
            # If the user enters an invalid choice, display an error message and prompt again
            invalidChoice()
            continue
        try:
            # Open the selected saved game file
            currentGame = shelve.open(saveFilePath, "r")
        except Exception:
            # If the selected file doesn't exist, report an error and continue the loop
            invalidChoice("I'm sorry, that save slot is empty.")
            continue
        # Extract the necessary data from the saved game and return it
        player = currentGame["player"]
        tiles_dict = currentGame["tiles_dict"]
        currentTile = tiles_dict[currentGame["location"]]
        encounterTables_dict = currentGame["encounterTables_dict"]
        currentGame.close()
        return player, tiles_dict, currentTile, encounterTables_dict

# Gets player choices about saving the game and exiting the program


def endGame(exitGame, tiles_dict, player, currentTile, encounterTables_dict):
    # Loop until the player chooses to exit the game
    while exitGame == True:
        # Display options to the player in a table format
        slow_table(tabulate([["", "Would you like to save your progress?"], ["1:", "Yes"], [
                        "2:", "No"], ["3:", "Go Back"]], headers="firstrow", tablefmt="fancy_outline"))
        try:
            # Get the player's choice
            save = int(input("? "))
        except Exception:
            # If the input is not a valid integer, display an error message and continue the loop
            invalidChoice()
            continue
        # Clear the screen
        clrscr()
        # Handle the player's choice
        if save == 1:
            # If the player chooses to save and exit, break out of the loop
            save = "yes"
            break
        elif save == 2:
            # If the player chooses to exit without saving, display a confirmation prompt
            slow_table(tabulate([["", "Are you sure?"], ["1:", "Yes"], ["2:", "No"], [
                            "3:", "Go Back"]], headers="firstrow", tablefmt="fancy_outline"))
            try:
                # Get the player's confirmation
                surety = int(input("? "))
            except Exception:
                # If the input is not a valid integer, display an error message and continue the loop
                invalidChoice()
                continue
            # Clear the screen
            clrscr()
            # Handle the player's confirmation
            if surety == 1:
                # If the player confirms, display a farewell message, wait for a keypress, and return from the function
                slow_table(
                    tabulate([["Thank you for playing."]], tablefmt="fancy_outline"))
                waitForKey()
                return exitGame
            elif surety in {2, 3}:
                # If the player cancels the confirmation or chooses to go back, continue the loop
                continue
            else:
                # If the player makes an invalid choice, display an error message and continue the loop
                invalidChoice()
                continue
        elif save == 3:
            # If the player chooses to go back, set exitGame to False and return from the function
            exitGame = False
            return exitGame
        else:
            # If the player makes an invalid choice, display an error message and continue the loop
            invalidChoice()
            continue
    # If the player chose to save and exit, call saveMenu and return from the function
    if save == "yes":
        saveMenu(tiles_dict, player, currentTile, encounterTables_dict)
    return exitGame

# Function that saves the current game


def saveMenu(tiles_dict=None, player=Player(), currentTile=Tile(), encounterTables_dict=None):
    if tiles_dict is None:
        tiles_dict = {}
    if encounterTables_dict is None:
        encounterTables_dict = {}
    # Open the file that contains information about save files and load its contents
    with open(saveFileInfoPath, "r") as saveInfo:
        saveFiles_dict = json.load(saveInfo)
        saveInfo.close()
    # Get a list of keys from the dictionary that contains the save files
    saveFiles_keyList = list(saveFiles_dict.keys())
    # Loop until the player chooses a valid slot to save the game
    while True:
        slow_table("Which slot would you like to save your progress in?")
        for count, saveFile in enumerate(saveFiles_dict):
            slow_table(
                f"{count + 1}: {saveFiles_dict[saveFile]['name']} {saveFiles_dict[saveFile]['info']}")
        try:
            saveChoice = int(input("? "))
            clrscr()
        except Exception:
            invalidChoice()
            continue
        # If the player's choice is not a valid save slot, prompt them to choose again
        if saveChoice > len(saveFiles_dict):
            invalidChoice()
            continue
        # If the save slot is not empty, prompt the player for confirmation before overwriting
        while True:
            if saveFiles_dict[saveFiles_keyList[saveChoice - 1]]["info"] != "(Empty)":
                slow_table(tabulate([["", f"This will overwrite the current save for {saveFiles_dict[saveFiles_keyList[saveChoice - 1]]['name']}. Are you sure?"], [
                                "1:", "Yes"], ["2:", "No"], ["3:", "Go Back"]], headers="firstrow", tablefmt="fancy_outline"))
                try:
                    surety = int(input("? "))
                except Exception:
                    invalidChoice()
                    continue
                clrscr()
                if surety in {1, 2, 3}:
                    break
                invalidChoice()
                continue
            else:
                surety = 1
                break
        # If the player cancels overwrite, restart the loop
        if surety == 2:
            continue
        # Assign the save file path based on the player's choice
        if saveChoice in {1, 2, 3, 4, 5}:
            saveFilePath = os.path.join(
                mainPath, f"SaveFiles\\Save{saveChoice}")
            saveGame(saveFilePath, saveChoice, tiles_dict, player,
                     currentTile, encounterTables_dict, saveFiles_dict)
        else:
            invalidChoice()
            continue
        return tiles_dict, player, currentTile, encounterTables_dict


def saveGame(saveFilePath, saveChoice, tiles_dict=None, player=Player(), currentTile=Tile(), encounterTables_dict=None, saveFiles_dict=None):
    if encounterTables_dict is None:
        encounterTables_dict = {}
    if saveFiles_dict is None:
        saveFiles_dict = {}
    # Open the chosen save file and write the game data to it
    currentGame = shelve.open(saveFilePath, "c")
    currentGame["player"] = player
    currentGame["location"] = currentTile.id
    currentGame["tiles_dict"] = tiles_dict
    currentGame["encounterTables_dict"] = encounterTables_dict
    currentGame.close()
    # Update the save file information in the dictionary
    saveFiles_dict[f"Save{str(saveChoice)}"]["name"] = player.name
    saveFiles_dict[f"Save{str(saveChoice)}"]["info"] = f"(Last Saved: {datetime.now().replace(microsecond=0).isoformat(' ')} Location: {currentTile.name})"

    # Write the updated save file information to the save file information file
    with open(saveFileInfoPath, "w") as saveInfo:
        saveFiles_dict = json.dumps(saveFiles_dict, indent="    ")
        saveInfo.write(saveFiles_dict)
        saveInfo.close()

    # Inform the player that their progress has been saved
    slow_table(
        tabulate([["Your progress has been saved."]], tablefmt="fancy_outline"))
    # Display farewell message and wait for key
    slow_table(
        tabulate([["Thank you for playing."]], tablefmt="fancy_outline"))
    waitForKey()


main()
