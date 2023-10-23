# CharyTracker
Python database with TKinter UI to track in-game rewards from "Hunt: Showdown"

Hi, thanks for installing my Chary Tracker! I'm a computer science student, and created this project out a passion and necessity. 


It originally began with an interest of how many rewards it would take to get 'Bad Hand' - I must have tried at least 200 times before I even started recording the data, though. I first used a Google Sheets file for recording, but eventually that got too long and Chrome was such an intense browser it would cause issues for my computer when running. 


This program is technically intended for people who already have Chary spreadsheets, and to allow them to maintain them easier. Because of this, the program will not work if you do not follow these instructions:


1: You must have a 'hs_chary.csv' file in the same directory as the exe. 
1.1: This CSV must have a numeric index in the first column.
1.2: This CSV must have the first row reserved for headers only.
1.3: This CSV must have the following headers: 'REWARD INFORMATION', 'COLOR', 'CODE'
	e.g. reward information is '500 XP' or 'Bomblance', color is 1 - 4 for first - fourth reward of the day, and code is a shorthand for the type of reward following this system:
	      "Badhand" = 0, "Weapon" = 1, "Legendary (I)" = 2, "Legendary (U)" = 3,
        "Hunt Dollars" = 4, "Blood Bonds" = 5, "Hunter Slot" = 6, "Experience" = 7,
        "Upgrade Points" = 8, "Consumable" = 9, "Tool" = 10, "Loadout Slot" = 11, "Legendary (H)" = 12

2: The generated 'hunt_spreadsheet.txt' file must remain in the same directory as the exe.
