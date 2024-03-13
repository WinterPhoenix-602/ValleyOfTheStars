from CustomMessages import *
from new_game import newGame
from load_game import loadGame

# Displays the main menu and prompts the user to choose between starting a new game, loading a saved game, or ending the program.
def mainMenu():
    while True:
        # Displays the options for the main menu as a table
        slow_table([["1: New Game"], ["2: Load Game"], ["3: Exit"]], tablefmt="fancy_outline")
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
                player, tiles_dict, quests_dict, currentTile, encounterTables_dict = newGame()
            case 2:
                # Loads a saved game
                player, tiles_dict, quests_dict, currentTile, encounterTables_dict = loadGame()
                if player == 0:
                    continue
            case 3:
                # Exits the program
                exit()
        # Returns the initial game state based on the user's choice
        return player, tiles_dict, quests_dict, currentTile, encounterTables_dict