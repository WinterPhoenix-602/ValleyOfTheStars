import json
import os
import shelve
from CustomMessages import *
from EntityClasses import Player
from LocationTileClass import Tile
from datetime import datetime


# Function that saves the current game
def saveMenu(tiles_dict=None, quests_dict=None, player=Player(), currentTile=Tile(), encounterTables_dict=None):
    if tiles_dict is None:
        tiles_dict = {}
    if encounterTables_dict is None:
        encounterTables_dict = {}
    if quests_dict is None:
        quests_dict = {}
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
                slow_table([["", f"This will overwrite the current save for {saveFiles_dict[saveFiles_keyList[saveChoice - 1]]['name']}. Are you sure?"], [
                                "1:", "Yes"], ["2:", "No"], ["3:", "Go Back"]], headers="firstrow", tablefmt="fancy_outline")
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
            # Open the chosen save file and write the game data to it
            currentGame = shelve.open(saveFilePath, "c")
            currentGame["player"] = player
            currentGame["location"] = currentTile.id
            currentGame["tiles_dict"] = tiles_dict
            currentGame["quests_dict"] = quests_dict
            currentGame["encounterTables_dict"] = encounterTables_dict
            currentGame.close()
            # Update the save file information in the dictionary
            saveFiles_dict[f"Save{saveChoice}"]["name"] = player.name
            saveFiles_dict[f"Save{saveChoice}"]["info"] = f"(Last Saved: {datetime.now().replace(microsecond=0).isoformat(' ')} Location: {currentTile.name})"

            # Write the updated save file information to the save file information file
            with open(saveFileInfoPath, "w") as saveInfo:
                saveFiles_dict = json.dumps(saveFiles_dict, indent="    ")
                saveInfo.write(saveFiles_dict)
                saveInfo.close()

            # Inform the player that their progress has been saved
            slow_table("Your progress has been saved.", tablefmt="fancy_outline")
            # Display farewell message and wait for key
            slow_table("Thank you for playing.", tablefmt="fancy_outline")
            waitForKey()
        else:
            invalidChoice()
            continue
        return tiles_dict, player, currentTile, encounterTables_dict