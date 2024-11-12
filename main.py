import os
from dotenv import load_dotenv

import discord
from discord.ext import commands
from discord import app_commands

from responses import get_response
from roles import add_sem_roles
from channels import  edit_per_channel

# Load Toaken from Safe File
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
print(TOKEN)

# Intents Setup
intents = discord.Intents.all()
client = discord.Client(intents=intents, command_prefix="uwu")
tree = app_commands.CommandTree(client)
GUILD_ID = discord.Object(id="1305824039557791834")

# Message Functionality
async def send_message(message: discord.message, user_message: str) -> None:
    if not user_message: # If user_message is empty
        print('(Message is empty, maybe intents not enabled?)')
        return
    
    # var := user_message == ... ist ein one-liner :)
    if is_private := user_message[0] == '?':    # for private Messages (Start with "?")
        user_message = user_message[1:]         # slice off the "?" 

    try:
        response: str = get_response(user_message)
        if not response: # If response is empty
            return
        await message.author.send(response) if is_private else await message.channel.send(response)  # If private -> Author, else -> Channel
    except discord.errors.HTTPException as e:   # for HTTP Errors wie Bad Requests
        print(e)
    except Exception as e:
        print(e, type(e))

# Startup Handling
@client.event
async def on_ready() -> None:
    print(f'{client.user} has connected to Discord!')
    try:        
        await tree.sync(guild=GUILD_ID) # Sync the Commands
        print("Synced")
    except Exception as e:
        print(e)

# Message Handling
@client.event
async def on_message(message: discord.message) -> None:
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

    # print(f'[{channel}] {username}: "{user_message}"') # print the message to the console

    await send_message(message, user_message) # send the message to the send_message function / to Console

# Slash Command to Assign Roles
@tree.command(name="assign_roles", description="Assign roles based on existing roles", guild=GUILD_ID)
@app_commands.checks.has_permissions(administrator=True)
async def assign_roles(interaction: discord.Interaction):
    if not interaction.guild.me.guild_permissions.manage_roles:
        await interaction.response.send_message("I do not have permission to manage roles.", ephemeral=True)
        return
    for member in interaction.guild.members:
        if member == client.user:
            continue
        await add_sem_roles(member)
    await interaction.response.send_message("Roles have been assigned.", ephemeral=True)

# Check for member_updates to assign semester rules
@client.event
async def on_member_update(before: discord.Member, after: discord.Member) -> None:
    if before.roles == after.roles:
        return
    await add_sem_roles(after)

@tree.command(name="assign_roles_channel", description="Assign to Channels to limit access of other roles ", guild=GUILD_ID)
@app_commands.checks.has_permissions(administrator=True)
async def assign_roles_channel(interaction: discord.Interaction, role: discord.Role):
    await edit_per_channel(interaction.channel, role)
# Run the Bot
def main() -> None:
    client.run(TOKEN)

if __name__ == '__main__':
    main()