import os
from dotenv import load_dotenv

import discord
from discord.ext import commands
from discord import app_commands

from responses import get_response
from roles import add_sem_roles, remove_sem_roles
from channels import  edit_per_channel

import asyncio
import yt_dlp as youtube_dl

# Load Toaken from Safe File
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Intents Setup
intents = discord.Intents.all()
client = discord.Client(intents=intents, command_prefix="uwu")
tree = app_commands.CommandTree(client)
GUILD_ID = discord.Object(id="1305824039557791834")

# Music Setup
voice_clients = {}

yt_dl_opts = {'format': 'bestaudio/best'}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)

ffmpeg_opts = {'options': '-vn'}    # no video

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
        await tree.sync() # Sync the Commands
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

# Check for member_updates to assign semester rules
@client.event
async def on_member_update(before: discord.Member, after: discord.Member) -> None:
    if len(before.roles) == len(after.roles):
        pass                   # Falls man hier iwann mal stolpert: in roles.py eine if Abfrage schreiben für len(rmvd_roles) = 0

    elif len(before.roles) > len(after.roles):
        await remove_sem_roles(after, before.roles)

    else:
        await add_sem_roles(after)

    print("--------------------")
    return

# Event to check if the bot is alone in a voice channel and disconnect
@client.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    if member == client.user:
        return

    voice_client = voice_clients.get(member.guild.id)
    if voice_client and len(voice_client.channel.members) == 1:
        await voice_client.disconnect()
        print("Disconnected as I am alone in the voice channel.")
        del voice_clients[member.guild.id]


# Slash Command to Assign Roles
@tree.command(name="assign_roles", description="Assign roles based on existing roles")
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


# Slash Command Assign Role to certain Channel
@tree.command(name="assign_role_channel", description="Assign to Channels to limit access of other roles ")
@app_commands.checks.has_permissions(administrator=True)
async def assign_roles_channel(interaction: discord.Interaction, role: discord.Role):
    try:
        await edit_per_channel(interaction.channel, role)
        await interaction.response.send_message("Channel has been updated", ephemeral=True)
    
    except Exception as e:
        await interaction.response.send_message(e, ephemeral=True)


# Slash Commmand for basic Music Functionality
@tree.command(name="play", description="Play a song")
#@app_commands.checks.has_permissions(administrator=True)
async def play(interaction: discord.Interaction, url: str):
    if not interaction.guild.me.guild_permissions.connect:
        await interaction.response.send_message("I do not have permission to connect to a voice channel.", ephemeral=True)
        return

    if not interaction.guild.me.guild_permissions.speak:
        await interaction.response.send_message("I do not have permission to speak in a voice channel.", ephemeral=True)
        return

    if not interaction.user.voice:
        await interaction.response.send_message("You are not connected to a voice channel.", ephemeral=True)
        return

    try:
        voice_channel = interaction.user.voice.channel
        if  voice_channel.guild.id not in voice_clients:
            voice_client = await voice_channel.connect()
            voice_clients[interaction.guild.id] = voice_client
        else:
            await interaction.response.send_message("I am already connected to a voice channel.", ephemeral=True)

        loop = asyncio.get_event_loop()     # get the event loop -> läuft im Hintergrund
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
        
        song = data['url']

        voice_client.play(discord.FFmpegPCMAudio(song, **ffmpeg_opts))

        await interaction.response.send_message("Playing song", ephemeral=True)

    except Exception as e:
        await interaction.response.send_message(e, ephemeral=True)

# Run the Bot
def main() -> None:
    client.run(TOKEN)

if __name__ == '__main__':
    main()