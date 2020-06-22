# Imports
import os
import json
import discord
import random


# Load Token
# Note that this is read from a file that is never uploaded to github
token = ""
with open("token.txt", "r") as f:
    token = f.read()


# Load Messages
messages = []
_dir = "Data"
for filename in os.listdir(_dir):
    with open(os.path.join(_dir, filename), "r") as f:
        messages.append(json.load(f))

print("Loaded Messages as:")
print(json.dumps(messages, indent=4))


# Class
class NoahBotClient(discord.Client):
    async def on_ready(self):
        print("Awake")


    async def on_message(self, message):
        print(f"Message from {message.author}: {message.content}")
        if message.author != self.user:
            global messages
            message_out = None
            girl_messaging = False

            for role in message.author.roles:
                if "girls" == str(role).lower():
                    girl_messaging = True
                    break
            
            if girl_messaging:
                for category in messages:
                    prompt_present_in_message = True
                    keywords = category["prompt"].split("+")
                    for keyword in keywords:
                        if keyword not in message.content:
                            prompt_present_in_message = False
                            break
                    if prompt_present_in_message:
                            message_out = random.choice(category["messages"])
                            message_out = message_out.replace("[p]", message.author.mention)
                            break
            
            if message_out != None:
                await message.channel.send(message_out)


# Run Bot
client = NoahBotClient(token)
client.run()