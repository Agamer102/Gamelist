# GameList
#### Video Demo:  <https://youtu.be/UiZeXK7X6oI>
## Overview

Gamelist, a simple command-line Python script that can help you keep track of the games you've played and the time you've played it for.
It's very common that many people have different launchers and sites for different games that all individually keep track of your playtime, or not at all. 
This program offers a solution to this problem in the form of a simple command-line script, that can add, remove, or change the time played of any game.
It also supports importing your Steam library (requires free Steam API key) and adding games via steam appid. The program saves the data persistently as a .csv file that can be copied and elsewhere.

## Requirements

This program has the following requirements

* Python
* Requests module (https://pypi.org/project/requests/)
* Tabulate module (https://pypi.org/project/tabulate/)
* Pytest for testing (https://pypi.org/project/pytest/)

## Installation

* Install the relevant modules in requirements.txt
* Create a gamelist.csv file (if not already present)
* Create a config.ini file (if not already present):
  * At the top insert the section [keys]
  * Set steamapi equal to your Steam api key (obtainable via: https://steamcommunity.com/dev)
  * Set steamaccid equal to your Steam ID (viewable via: https://store.steampowered.com/account/)
* (optional) save your previous game list in the root directory of the program as gamelist.csv, formatted correctly.

Note that if you want Steam library functionality, config.ini **must** be configured properly.

## Usage

* Running the script will present a main menu.
* To list current games, submit 1. Note that if a gamelist.csv does not exit, this will case an exit.
* To add a game, submit 2. In the submenu:
  * Submit 1 to manually add your game. This will prompt you for a name, time played and steam appid (optional)
  * Submit 2 to add your game via steam appid. This will only prompt you for a time played and steam appid
  * Submit 3 to automatically add and update your steam library (requires correct config.ini file)
  * Submit 4 to return to the main menu
* To edit an added game, submit 3. In the submenu:
  * Submit 1 to add time to a game. This will further prompt you for a name/list id for the time to be added. Please note name must be written exactly as seen in list.
  * Submit 2 to change time of a. This will further prompt you for a name/list id for the time to be changed. Please note name must be written exactly as seen in list.
  * Submit 3 to delete an entry. This will further prompt you for a list id. Please note that only list id is supported currently for this operation.
* To update via your steam library, submit 4. Please note this requires correct config.ini file. There is no difference in this method and the method mentioned in submit 2.
* To exit the program, submit 5 or ctrl + C.

NOTE: Time when inputted, can be formatted in the format 0h 00m or 0h 00min or a number of minutes with m/min (i.e. 370m, 470min). The hours section is optional. The minutes must be a positive integer between 0 (inclusive) and 60 if an hour is included.

## Contributing

I most likely will not be accepting any contributions , as I am new to github and python. However feel free to use any part or whole of this program for your own usecases !

CS50P final project of Adithya Dissanayake