# 2023-03-02
# Main Game File

from menu import mainMenu
from save_game import saveMenu
from random import randint
from CustomMessages import *

"""# enables colors on windows
if os.name == 'nt':
    os.system("reg add HKEY_CURRENT_USER\\Console /v VirtualTerminalLevel /t REG_DWORD /d 1")
    clrscr()"""


# The main function of the game
def main():
    while True:
        # Start the main menu and get initial game state
        player, tiles_dict, quests_dict, currentTile, encounterTables_dict = mainMenu()
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
                currentTile, turn, player, tiles_dict, quests_dict)
            # Check if player has chosen to exit the game
            if exitGame == True:
                # End the game and check if player wants to play again
                exitGame = endGame(exitGame, tiles_dict, quests_dict,
                                   player, currentTile, encounterTables_dict)
            if exitGame == True:
                # Return to main menu
                break
            # Check if player has chosen to save the game
            if exitGame == "save":
                # Save the game
                saveMenu(tiles_dict, quests_dict, player, currentTile, encounterTables_dict)

# Gets player choices about saving the game and exiting the program
def endGame(exitGame, tiles_dict, quests_dict, player, currentTile, encounterTables_dict):
    # Loop until the player chooses to exit the game
    while exitGame == True:
        # Display options to the player in a table format
        slow_table([["", "Would you like to save your progress?"], ["1:", "Yes"], ["2:", "No"], ["3:", "Go Back"]], headers="firstrow", tablefmt="fancy_outline")
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
            slow_table([["", "Are you sure?"], ["1:", "Yes"], ["2:", "No"], ["3:", "Go Back"]], headers="firstrow", tablefmt="fancy_outline")
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
                slow_table("Thank you for playing.", tablefmt="fancy_outline")
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
        saveMenu(tiles_dict, quests_dict, player, currentTile, encounterTables_dict)
    return exitGame

main()
