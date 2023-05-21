# Project Name: Valley of the Stars

## README

---

### Configuration Instructions

To show colored text in the console, you need to enable ANSI Escape codes. By default, Windows does not have ANSI Escape codes enabled, while MacOS and Linux usually do. Follow the steps below to enable colored text on Windows:

1. Open the command prompt.
2. Run the following command:

   ```
   reg add HKEY_CURRENT_USER\Console /v VirtualTerminalLevel /t REG_DWORD /d 1
   ```

Once ANSI Escape codes are enabled, colored text should be displayed in the console.
---

### Installation Instructions

This project does not require any installation. It can be run directly from the source files.

---

### Operating Instructions

To run the Valley of the Stars project, follow the instructions below:

1. Locate the file named `Valley_Of_The_StarsV(version number).py`.
2. Double-click on the file to execute it.

---

### File Manifest

The project directory contains the following files:

- **Map Folder:**
  - Map.png
  - MapBackground.png
  - ValleyMap.wonderdraft_map

- **NewGameFiles Folder:**
  - Encounters.json
  - Enemies.json
  - Player.json
  - Quests.json
  - Tiles.json

- **SaveFiles Folder:**
  - SaveFileInfo.json

- CombatTesting.py
- CustomMessages.py
- EncounterClasses.py
- EntityClasses.py
- HierarchyChart.jpg
- ItemClass.py
- LocationTileClass.py
- QuestlineClass.py
- README.txt
- requirements.txt

---

## Known Bugs

- Questlines: The questline feature has been recently implemented and is currently non-functional.

---

### Contact Information

For any inquiries or issues regarding the Valley of the Stars project, please contact the author via email:

Author Email: clwilson602@gmail.com

---
