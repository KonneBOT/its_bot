import os
from dotenv import load_dotenv
from discord import Intents, Client, Message, errors, Interaction
from responses import get_response
from discord import app_commands
from roles import add_sem_roles

# Load Toaken from Safe File
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Intents Setup
intents: Intents = Intents.default()
intents.message_content = True
intents.members = True
client: Client = Client(intents=intents)
tree = app_commands.CommandTree(client)


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
    except errors.HTTPException as e:   # for HTTP Errors wie Bat Requests
        print(e)
    except Exception as e:
        print(e, type(e))

# Startup Handling
@client.event
async def on_ready() -> None:
    print(f'{client.user} has connected to Discord!')

# Message Handling
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:   # If the message is from the bot itself, stfu
        return
    
    if "vdi" in message.content.lower():
        if "nicht retten" in message.content.lower():
            await message.add_reaction('💥')
        else:
            await message.add_reaction('❌')
    
    username: str = message.author.name # get Username we're talking to
    user_message: str = message.content # get the message content
    channel: str = str(message.channel) # get the channel we're talking in

    print(f'[{channel}] {username}: "{user_message}"') # print the message to the console
    await send_message(message, user_message) # send the message to the send_message function / to Console

# Slash Command to Assign Roles
@tree.command(name="assign_roles", description="Assign roles based on existing roles")
async def assign_roles(interaction: Interaction):
    for member in interaction.guild.members:
        await add_sem_roles(member)
    await interaction.response.send_message("Roles have been assigned.", ephemeral=True)

# Run the Bot
def main() -> None:
    client.run(TOKEN)

if __name__ == '__main__':
    main()