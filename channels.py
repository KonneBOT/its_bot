import discord

async def edit_per_channel(discord_channel, discord_role) -> None:
    await discord_channel.set_permissions(discord_role, view_channel=True)
    return


async def create_modul_channels_list(interaction: discord.Interaction, category: discord.CategoryChannel, roles, msgid) -> None:
    guild = interaction.guild
    channels =  category.text_channels
    textchannels= [channel.name for channel in channels]
    message = await interaction.channel.fetch_message(msgid)
    moduls = message.content.lower().replace(" ", "-").split('\n')


    for modul in moduls:
        if modul not in textchannels:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=False),
            }
            for role in roles:
                overwrites[role] = discord.PermissionOverwrite(view_channel=True)

            await category.create_text_channel(name=modul, overwrites=overwrites)
            print(f"C {modul}, {[role.name for role in roles]}")
        if modul in textchannels:
            channel = discord.utils.get(guild.channels, name=modul)
            for role in roles:
                await edit_per_channel(channel, role)
                print(f"M {channel.name}, {role.name}")
    return