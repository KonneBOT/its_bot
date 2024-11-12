
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response

# Load Toaken from Safe File
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Intents Setup
intents: Intents = Intents.default()
intents.message_content = True 
client: Client = Client(intents=intents)

# Message Functionality
async def send_message(message: Message, user_message: str) -> None:
    if not user_message: # If user_message is empty
        print('(Message is empty, maybe intents not enabled?)')
        return
    
    # var := user_message == ... ist ein one-liner :)
    if is_private := user_message[0] == '?':    # for private Messages (Start with "?")
        user_message = user_message[1:]         # slice off the "?" 

    try:
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)  # If private -> Author, else -> Channel
    except Exception as e:
        print(e)

# Startup Handling
@client.event
async def on_ready() -> None:
    print(f'{client.user} has connected to Discord!')

# Message Handling
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:   # If the message is from the bot itself, stfu
        return
    
    username: str = message.author.name # get Username we're talking to
    user_message: str = message.content # get the message content
    channel: str = str(message.channel) # get the channel we're talking in

    print(f'[{channel}] {username}: "{user_message}"') # print the message to the console
    await send_message(message, user_message) # send the message to the send_message function / to Console

# Run the Bot
def main() -> None:
    client.run(TOKEN)

if __name__ == '__main__':
    main()