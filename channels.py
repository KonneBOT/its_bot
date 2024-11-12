import discord

def edit_per_channel(discord_channel, discord_role):
    discord_channel.set_permissions(discord_role, read_messages=True)
    return True