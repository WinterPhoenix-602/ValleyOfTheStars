from CustomMessages import *
import shelve
import json

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
            slow_table("Save file information has been corrupted, moved, or deleted.", tablefmt="fancy_outline")
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
        slow_table(loadMenuTable, headers="firstrow", tablefmt="fancy_outline")
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
        quests_dict = currentGame["quests_dict"]
        currentTile = tiles_dict[currentGame["location"]]
        encounterTables_dict = currentGame["encounterTables_dict"]
        currentGame.close()
        return player, tiles_dict, quests_dict, currentTile, encounterTables_dict