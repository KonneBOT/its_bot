from random import choice, randint
from DiscordClient import client
import discord
import codecs

zitate_channelid = 1154405716862435418
f = codecs.open("zitate.md", "r", "utf-8")
quotes = f.readlines()[2:]

async def get_response(user_input: str) -> str:

    lowered: str = user_input.lower()

    match True:
        case _ if lowered == "":
            return None
        case _ if lowered == "asdf":
            return choice(['I do not understand.', 'I am not sure what you mean.', 'Could you rephrase that?'])
        case _ if "hello there" in lowered:
            return "General Kenobi!"
        case _ if "hello" in lowered:
            return "Hello there!"
        case _ if "bye" in lowered:
            return "Goodbye!"
        case _ if "hower" in lowered:
            return choice(quotes).strip("\r\n")
        case _ if "lugo" in lowered:
            return await get_lugo_response()
        case _ if "roll" in lowered and "rollen" not in lowered:
            return f"You rolled a {randint(1, 6)}."
        case _:
            return None

async def get_lugo_response():
   messages = [message async for message in client.get_channel(zitate_channelid).history(limit=200)]
   messages_contents = []
   for message in messages:
        message_array = message.content.split('"')
        try:
            if message_array[0].lower().strip() == "lugo:":
                messages_contents.append(message_array[1])
        except: # random gifs und normale msg geben sonst index error da kein '"'
            pass
   return choice(messages_contents)