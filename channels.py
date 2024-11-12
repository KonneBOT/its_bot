import discord

async def edit_per_channel(discord_channel, discord_role):
    await discord_channel.set_permissions(discord_role, view_Channel=True)
    return discord_role.permissions_for(discord_channel)