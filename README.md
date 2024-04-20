**GAME OVERVIEW**:
The idea for this game was to make a tower defense game, where the player has to strategically place down defensive towers or structures along a path or map to prevent waves of enemies from reaching the end of the path. 
Each tower has a unique firing ability and a unique cost to build, where the goal of the game is to survive the waves of enemies and prevent them from reaching the end of the path. Players have to demonstrate quick thinking, efficient resource management over increasingly-difficult levels to achieve victory.
\
\
**HOW TO RUN THE GAME**:
To run the game, the player needs to set up their environment, where they first need to; 
1)	Install Python: Ensure Python 3.x is installed onto system

2)	Install PyGame: Use the ‘pip’ module that comes with Python to install PyGame. Can be done by running ‘pip install pygame’ in your Terminal or Command Prompt


3)	Setup IDE: Choose an IDE (Integrated Development Environment) like Pycharm, Visual Studio Code, or even a simpler editor like Sublime Text

After having these features setup, the next thing needed is the ZIP File. Download the ZIP file from where accessible, such as from GitHub, and extract everything inside into a folder on your device.

Then import the folder with the files onto the IDE, where then when you run the ‘main.py’ file, it should execute the full game.
\
**DEPENDENCIES**:
Only need pygame dependency, to download is mentioned above in 'HOW TO RUN THE GAME'
\
**FILES**:
README.md - README file
main.py - Main code file, run this file to run the game
enemy.py - Includes classes and functions about the enemies
tower.py - Includes classes and functions about the towers
menu.py - To do with the menu and different texts
game_functions.py - Miscellaneous functions that don't fit under a category
draw_grid_functions.py - Drawing the grid
Game Design Documentation.docx - Documentation for the game

'testing' Folder:
mouse_testing.py - Unit testing mouse coordinates
testing_maps.py - Testing different maps to see if enemies can traverse the map

'images' Folder:
grass.png - Grass picture
main_menu_bg.png - Main menu background
menu_small.png - Side menu small version
menu.png - Side menu
path.png - Path picture

    'enemy' Folder:
    All enemy pictures

    'tower' Folder:
    All tower pictures

'fonts' Folder:
Arial.ttf - Arial font
blocky_font.ttf - Blocky font

    'font_backgrounds' Folder:
    Controls Rect.png - Background for controls button
    Play Rect.png - Background for play button
    Quit Rect.png - Background for quit button