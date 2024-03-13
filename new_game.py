import json
from ItemClass import *
from QuestlineClass import *
from EntityClasses import Player
from LocationTileClass import *

# Initializes the base game state
def newGame():
    # Open the newGamePath file and load its contents into currentGame_dict
    while True:
        # Extract the tile data from newGameTiles
        tiles_dict, currentTile = extractData(newGameTiles, Tile)
        # Etract the quest data from newGameQuests
        quests_dict = extractData(newGameQuests, Questline)
        for quest in quests_dict:
            if type(quest) == str and quest not in ["active", "completed", "inactive"]:
                quests_dict["inactive"].append(quest)
        # Extract the player data from newGamePlayer
        player = extractData(newGamePlayer, Player)
        # Extract the enemy data from newGameEnemies
        ENEMY_DICT = extractData(newGameEnemies, Enemy)
        # Extract the encounter tables from newGameEncounters
        encounterTables_dict = extractData(newGameEncounters, Encounter, ENEMY_DICT)
        # Prompt the player to enter a name and create a new Player object with that name
        while True:
            slow_table("What would you like to name your character?", tablefmt="fancy_grid")
            player.name = input("? ")
            clrscr()
            if len(player.name) > 25:
                slow_table("I'm sorry, your name must be shorter than 25 characters.", tablefmt="fancy_outline")
                continue
            elif player.name == "":
                slow_table("Defaulting to 'Newbie'.", tablefmt="fancy_outline")
                player.name = "Newbie"
            break
        return player, tiles_dict, quests_dict, currentTile, encounterTables_dict

def extractData(dataFilePath, dataClass, ENEMY_DICT=None):
    with open(dataFilePath, "r") as dataFile:
            data_dict = json.load(dataFile)
            dataFile.close()
    # Create a new
    for objectType in data_dict:
        if (
            dataClass != Encounter
            and dataClass == Questline
            and objectType not in ["active", "completed", "inactive"]
            or dataClass not in [Encounter, Questline]
        ):
            a = dataClass(objectType)
            a.reader(data_dict[objectType])
            data_dict[objectType] = a
        elif dataClass == Encounter:
            for encounterType in data_dict[objectType]:
                if encounterType == "passive":
                    for encounter in data_dict[objectType][encounterType]:
                        a = PassiveEncounter(encounterType=encounter)
                        a.reader(data_dict[objectType][encounterType][encounter])
                        data_dict[objectType][encounterType][encounter] = a
                if encounterType == "hostile":
                    for encounter in data_dict[objectType][encounterType]:
                        a = CombatEncounter(encounterType=encounter, base_enemy_dict=ENEMY_DICT)
                        a.reader(data_dict[objectType][encounterType][encounter])
                        data_dict[objectType][encounterType][encounter] = a
                        continue
    # Set the current tile to the starting tile
    if dataClass == Tile:
        return data_dict, data_dict["Crossroads"]
    elif (
        dataClass == Questline
        or dataClass != Player
        and dataClass in [Enemy, Encounter]
    ):
        return data_dict
    elif dataClass == Player:
        return data_dict["Newbie"]