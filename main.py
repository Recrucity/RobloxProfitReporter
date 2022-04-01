# Made by Recrucity#4040

import requests
import configparser
import os
import time

# Config
config = configparser.ConfigParser()
config.read_file(open(r"config.ini"))
checkTime = int(config.get("main", "checktime"))
userId = str(config.get("main", "userid"))

# Discord
webhook = str(config.get("discord", "webhook"))
topmessage = str(config.get("discord", "message"))
title = str(config.get("discord", "title"))

while True:

    data = requests.get("https://inventory.roblox.com/v1/users/" + userId + "/assets/collectibles").json()["data"]
    itemAmount = len(data)
    userRap = 0

    for i in range(itemAmount):
        itemData = data[i]
        itemRap = itemData["recentAveragePrice"]
        print("RAP: " + str(itemRap))

        userRap = userRap + itemRap

    print("Total RAP: " + str(userRap))

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
        message = "**You've made profit since Last Time!**\nTotal Profit: " + str(profit) + " R$"
        color = 65353
    elif userRap < int(lastDay):
        loss = f'{int(lastDay) - userRap}'
        message = "**You've lost RAP Since Last Time**\nTotal Loss: " + str(loss) + " R$"
        color = 16711680
    else:
        message = "**Your RAP Has not Changed Since Last Time**"
        color = 16777215

    data = {
        "content" : topmessage,
        "username" : "Profit Reporter"
    }

    data["embeds"] = [
        {
            "title": title,
            "description": message,
            "color": color
        }
    ]
    requests.post(webhook, json=data)

    f = open("lastday.txt", "w")
    f.write(str(userRap))
    f.close()

    time.sleep(checkTime)

# Made by Recrucity#4040
