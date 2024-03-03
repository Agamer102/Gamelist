import csv
import sys
import re
import requests
import json
from tabulate import tabulate
from configparser import ConfigParser

headers = ["listid", "steamid", "name", "time"]


def main():
    while True:
        print(
            "Main Menu\n1. List games\n2. Add game\n3. Edit game\n4. Update steamlibrary\n5. Exit"
        )
        selection = input("> ")
        match selection:
            case "1":
                list_games()
            case "2":
                add_menu()
            case "3":
                edit_menu()
            case "4":
                update_steamlibrary()
            case "5":
                sys.exit("Goodbye")
            case _:
                print("Invalid")


def add_menu():
    print(
        "Add game\n1. Add manually\n2. Add with steam appid\n3. Auto add with Steam library\n4. Main menu"
    )
    selection = input("> ")
    match selection:
        case "1":
            add_game()
            print("Game successfully added")
        case "2":
            add_game(steam=steam_request(input("Steam Appid: ")))
            print("Game successfully added")
        case "3":
            update_steamlibrary()
            print("Steamlibrary successfully added")
        case "4":
            return
        case _:
            print  ("Invalid")


def edit_menu():
    print("Edit game\n1. Add time to game\n2. Change game time\n3. Delete game\n4. Main menu")
    selection = input("> ")
    match selection:
        case "1":
            change_time(*add_time(input("Id/Name: ").strip(), verify_time(input("Add time: "))))
            print("Playtime successfully added")
        case "2":
            change_time(input("Id/Name: "), verify_time(input("New time: ")))
            print("Playtime successfully changed")
        case "3":
            delete_game(input("Id: "))
            print("Game successfully deleted")
        case "4":
            return
        case _:
            print("Invalid")


def add_game(filename="gamelist.csv", steam=None, steamlib=None):
    if steam:
        game = {
            "listid": getid(),
            "steamid": steam["steamid"],
            "name": steam["name"],
            "time": verify_time(input("Time: ")),
        }
    elif steamlib:
        game = {
            "listid": getid(),
            "steamid": steamlib["appid"],
            "name": steamlib["name"],
            "time": steamlib["time"],
        }
    else:
        game = {
            "listid": getid(),
            "steamid": input("Steam id: "),
            "name": input("Name: "),
            "time": verify_time(input("Time: ")),
        }

    keys = game.keys()

    gamesw = open(filename, "a", newline="")
    gamesr = open(filename).read()

    writer = csv.DictWriter(gamesw, keys)

    if gamesr.strip() == "":
        gamesr = gamesr.strip()
        writer.writeheader()

    writer.writerow(game)

    gamesw.close()


def list_games(lst=False, filename="gamelist.csv"):
    try:
        games = []
        gamesn = []
        with open(filename) as file:
            reader = csv.DictReader(file)
            for row in reader:
                games.append(list(row.values()))
                gamesn.append(row["name"])

    except FileNotFoundError:
        sys.exit("No games in list or list does not exist")
    else:
        if lst:
            return gamesn
        else:
            print(tabulate(games, headers, tablefmt="grid"))


def change_time(id, new_time, filename="gamelist.csv"):
    try:
        games = []
        with open(filename) as file:
            reader = csv.DictReader(file)
            for row in reader:
                    if row["listid"] == id:
                        row["time"] = new_time
                    if row["name"] == id:
                        row["time"] = new_time
                    games.append(row)
        with open(filename, "w", newline="") as file:
            writer = csv.DictWriter(file, headers)
            writer.writeheader()
            for row in games:
                writer.writerow(row)

    except FileNotFoundError:
        sys.exit("List does not exist")


def add_time(id, add_time, filename="gamelist.csv"):
    try:
        with open(filename) as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["listid"] == id:
                    hoursi, minsi = verify_time(row["time"], strip=True)
                    hoursa, minsa = verify_time(add_time, strip=True)
                    return id, format_time(hoursa + hoursi, minsa + minsi)
                if row["name"] == id:
                    hoursi, minsi = verify_time(row["time"], strip=True)
                    hoursa, minsa = verify_time(add_time, strip=True)
                    return id, format_time(hoursa + hoursi, minsa + minsi)
    except FileNotFoundError:
        sys.exit("List does not exist")


def getid(filename="gamelist.csv"):
    try:
        with open(filename) as scraped:
            final_line = scraped.readlines()[-1]
        lsttmp = final_line.split(",")
        return int(lsttmp[0]) + 1
    except ValueError:
        return 1
    except IndexError:
        return 1
    except FileNotFoundError:
        return 1


def verify_time(time, strip=False):
    if matches := re.search(r"^(\d\d*h)? ?([0-5]\d?)?(m|min)?$", time):
        hours = 0
        mins = 0
        if matches[1]:
            hours = int(matches[1].strip("h"))
        if matches[2]:
            mins = int(matches[2].strip("m").strip("min"))
        if strip == False:
            return f"{hours}h {mins:02d}m"
        else:
            return hours, mins
    elif matches := re.search(r"^(\d+)?(m|min)$", time):
        mins = int(matches[1].strip("m").strip("min"))
        return format_time(0, mins)
    else:
        raise ValueError("Invalid time")


def format_time(hours, mins):
    if mins > 59:
        hours += mins // 60
        mins -= 60 * (mins // 60)
    return f"{hours}h {mins:02d}m"


def steam_request(appid):
    response = requests.get(
        url="http://store.steampowered.com/api/appdetails/", params={"appids": appid}
    ).json()
    try:
        if response:
            return {"steamid": appid, "name": response[appid]["data"]["name"]}
        else:
            raise ValueError("Invalid steam appid")
    except KeyError:
        raise ValueError("Invalid steam appid")


def update_steamlibrary(filename="gamelist.csv"):
    try:
        config = ConfigParser()
        config.read("config.ini")
        steamapikey = config.get("keys", "steamapi")
        steamaccid = config.get("keys", "steamaccid")
        library = requests.get(
            f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={steamapikey}&steamid={steamaccid}&include_appinfo=true&include_played_free_games=true&format=json"
        ).json()

    except requests.exceptions.JSONDecodeError:
        sys.exit("Invalid API key or account id")

    else:
        names = list_games(lst=True)
        for game in library["response"]["games"]:
            if game["name"] in names:
                change_time(game["name"], format_time(0, int(game["playtime_forever"])))
            else:
                add_game(
                    steamlib={
                        "name": game["name"],
                        "appid": game["appid"],
                        "time": format_time(0, int(game["playtime_forever"])),
                    }
                )


def delete_game(id, filename="gamelist.csv"):
    try:
        games = []
        found = False
        with open(filename) as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["listid"] == id:
                    found = True
                elif found:
                    listid = row["listid"]
                    listid = int(listid)
                    listid -= 1
                    row["listid"] = str(listid)
                    games.append(row)
                else:
                    games.append(row)
        with open(filename, "w", newline="") as file:
            writer = csv.DictWriter(file, headers)
            writer.writeheader()
            for row in games:
                writer.writerow(row)

    except FileNotFoundError:
        sys.exit("List does not exist")


if __name__ == "__main__":
    main()
