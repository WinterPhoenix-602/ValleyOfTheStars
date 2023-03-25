# Date: 2023-03-23
# Description: Allows selection of any existing Combat Encoounters for testing purposes.

import json
from CustomMessages import *
from EncounterClasses import CombatEncounter
from EntityClasses import Player

def main():
    maintain_progress = True
    while True:
        player, combat_encounters = get_encounters()
        biome, maintain_progress = biome_menu(player, combat_encounters, maintain_progress)
        if len(combat_encounters[biome]) > 0:
            encounter_menu(player, combat_encounters[biome])
        else:
            invalidChoice("No combat encounters found.")

def get_encounters():
    with open(mainPath + "\\SaveFiles\\NewGame.json", "r") as newGameFile:
        currentGame_dict = json.load(newGameFile)
        newGameFile.close()
    player = Player("Test Dummy")
    player.reader(currentGame_dict["player"])
    combat_encounters = {}
    for biome in currentGame_dict["encounterTables"]:
        combat_encounters[biome] = {}
        if "hostile" in currentGame_dict["encounterTables"][biome]:
            for encounter in currentGame_dict["encounterTables"][biome]["hostile"]:
                a = CombatEncounter()
                a.reader(currentGame_dict["encounterTables"][biome]["hostile"][encounter])
                a.generate_enemies(player)
                combat_encounters[biome][encounter] = a
    return player, combat_encounters

def biome_menu(player, combat_encounters,  maintain_progress=True):
    biome_menu_table = [["", "What would you like to do?", "Encounters"]]
    biome_menu_table.extend([f"{count + 1}:", biome, len(combat_encounters[biome])] for count, biome in enumerate(combat_encounters))
    biome_menu_table.extend(
        (
            [f"{len(combat_encounters) + 1}:", "Settings"],
            [f"{len(combat_encounters) + 2}:", "Exit"],
        )
    )
    while True:
        slow_table(tabulate(biome_menu_table, headers="firstrow", tablefmt="fancy_outline", colalign=("center", "left", "center")))
        try:
            biome = int(input("? "))
        except ValueError:
            invalidChoice()
            continue
        if biome in range(1, len(combat_encounters) + 1):
            return list(combat_encounters)[biome - 1], maintain_progress
        elif biome == len(combat_encounters) + 1:
            maintain_progress = settings_menu(player,  maintain_progress)
        elif biome == len(combat_encounters) + 2:
            exit()
        else:
            invalidChoice()

def settings_menu(player=Player("Test Dummy"), maintain_progress=True):
    player_menu_table = [
        ["", "What would you like to do?"],
        ["1:", "Change Name"],
        ["2:", "Change Level"],
        ["3:", "Redistribute Stats"],
        ["4:", "Toggle Maintain Damage [Currently: " + ("On" if maintain_progress else "Off") + "]"],
        ["5:", "Go Back"]
        ]
    while True:
        slow_table(tabulate(player_menu_table, headers="firstrow", tablefmt="fancy_outline", colalign=("center", "left")))
        try:
            choice = int(input("? "))
        except ValueError:
            invalidChoice()
            continue
        if choice == 1:
            slow_table(tabulate([["What would you like to change your name to?"]], tablefmt="fancy_outline"))
            player.name = input("? ")
        elif choice == 2:
            while True:
                try:
                    slow_table(tabulate([["What would you like to change your level to?"]], tablefmt="fancy_outline"))
                    player.level_up(level=int(input("? ")))
                except ValueError:
                    invalidChoice()
                    continue
                else:
                    break
        elif choice == 3:
            reset_stats(player)
            player.stats_menu()
        elif choice == 4:
            maintain_progress = not maintain_progress
            player_menu_table[4][1] = "Toggle Maintain Progress [Currently: " + ("On" if maintain_progress else "Off") + "]"
        elif choice == 5:
            return maintain_progress
        else:
            invalidChoice()


# TODO Rename this here and in `settings_menu`
def reset_stats(player=Player("Test Dummy")):
    player._constitution = 5
    player._strength = 5
    player._agility = 5
    player._intelligence = 5
    player._endurance = 5

def encounter_menu(player, combat_encounters, maintain_progress=True):
    encounter_menu_table = [["", "Select an Encounter to test:", "Enemies"]]
    encounter_menu_table.extend([f"{encounter[0]}:", encounter[1].name, len(combat_encounters[encounter[0]].enemies_dict)] for encounter in combat_encounters.items())
    encounter_menu_table.append([f"{len(combat_encounters) + 1}:", "Go Back"])
    while len(combat_encounters) > 0:
        slow_table(tabulate(encounter_menu_table, headers="firstrow", tablefmt="fancy_outline", colalign=("center", "left", "center")))
        try:
            encounter = int(input("? "))
        except ValueError:
            invalidChoice()
            continue
        if encounter in range(1, len(combat_encounters) + 1):
            combat_encounters[list(combat_encounters)[encounter - 1]].start_encounter(player)
            if not maintain_progress:
                player.health = player.maxHealth
                player.mana = player.maxMana
        elif encounter == len(combat_encounters) + 1:
            return
        else:
            invalidChoice()
    
if __name__ == "__main__":
    main()
