# Made by Recrucity#4040
# TODO: Embeds say how often profit reports are sent // DONE
# TODO: Style improvements. (Code blocks over robux profit etc) // DONE
# TODO: Add Mutli-Account Support (Maybe difficult, Probably not that difficult)

import requests
import configparser
import os
import time
from colorama import init

init()

# Config
config = configparser.ConfigParser()
config.read_file(open(r"config.ini"))
timeType = config.get("main", "time")
checkTime = int(config.get("main", "checktime"))
userId = config.get("main", "userid")

# Discord
webhook = str(config.get("discord", "webhook"))
topmessage = str(config.get("discord", "message"))
title = str(config.get("discord", "title"))

while True:

    data = requests.get("https://inventory.roblox.com/v1/users/" + userId + "/assets/collectibles").json()["data"]
    itemAmount = len(data)
    userRap = 0

    print(colorama.Fore.CYAN + "CHECKING " + colorama.Fore.RESET + "Checking your limiteds...")

    for i in range(itemAmount):
        itemData = data[i]
        itemRap = itemData["recentAveragePrice"]

        userRap = userRap + itemRap
        print(
            colorama.Fore.CYAN + "CHECKED " + colorama.Fore.RESET + " Checked limited #" + str(i + 1) + " (RAP: " + str(
                itemRap) + ")")

    if os.path.exists("lastday.txt"):
        f = open("lastday.txt", "r")
        lastDay = int(f.read())
        f.close()
    else:
        f = open("lastday.txt", "w+")
        f.write(str(userRap))
        f.close()
        f = open("lastday.txt", "r")
        lastDay = int(f.read())
        f.close()

    profit = 0
    loss = 0

    if userRap > int(lastDay):
        profit = f'{userRap - int(lastDay):,}'
        message = "You've made profit since Last Time!\nTotal Profit: `" + str(profit) + " R$`\nFrom `" + str(f'{lastDay:,}')\
                  + " R$` to `" + str(f'{userRap:,}') + " R$`\n \nNext profit report will be sent in "\
                  + str(checkTime) + " " + str(timeType)
        color = 65353
    elif userRap < int(lastDay):
        loss = f'{int(lastDay) - userRap}'
        message = "You've lost RAP since last time!\nTotal Loss: `" + str(loss) + " R$`\nFrom `" + str(f'{lastDay:,}')\
                  + " R$` to `" + str(f'{userRap:,}') + " R$`\n \nNext profit report will be sent in "\
                  + str(checkTime) + " " + str(timeType)
        color = 16711680
    else:
        message = "Your RAP Has not Changed Since Last Time"
        color = 16777215

    data = {
        "content": topmessage,
        "username": "Profit Reporter"
    }

    data["embeds"] = [
        {
            "title": title,
            "description": message,
            "color": color
        }
    ]
    requests.post(webhook, json=data)
    print(colorama.Fore.LIGHTGREEN_EX + "SUCCESS " + colorama.Fore.RESET + "Posted Profit Report to Discord!")

    f = open("lastday.txt", "w")
    f.write(str(userRap))
    f.close()

    print(colorama.Fore.LIGHTBLUE_EX + "WAITING " + colorama.Fore.RESET + "Waiting for " + str(
        checkTime) + " " + timeType)
    if timeType == "seconds":
        time.sleep(checkTime)
    elif timeType == "minutes":
        time.sleep(checkTime * 60)
    elif timeType == "hours":
        time.sleep(checkTime * 3600)
    elif timeType == "days":
        time.sleep(checkTime * 86400)

# Made by Recrucity#4040
