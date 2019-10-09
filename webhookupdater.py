import requests
import json


data = dict()
# for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
data["content"] = input("Message content\n")
data["username"] = "KairanNotes"

# leave this out if you dont want an embed
data["embeds"] = []
embed = dict()
# for all params, see https://discordapp.com/developers/docs/resources/channel#embed-object
embed["description"] = input("Text in embed\n")
embed["title"] = input("Title of embed\n")
data["embeds"].append(embed)
open("hooks.txt", "a").close()
for url in open("hooks.txt", "r"):
    url = "".join(url.split())
    result = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully to {1}, code {0}.".format(result.status_code, url))

# result: https://i.imgur.com/DRqXQzA.png
