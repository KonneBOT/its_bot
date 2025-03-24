from pdf import extract_moduls
import discord
from roles import courses
import os
async def edit_per_channel(discord_channel, discord_role) -> None:
    await discord_channel.set_permissions(discord_role, view_channel=True)
    return

async def update_modul_channels(interaction: discord.Interaction, attachment: discord.Attachment, createnewchannel: bool) -> None:
    guild = interaction.guild
    course = attachment.filename.split('.')[0]
    if course not in courses:
        raise Exception(f'Course {course} does not exist, existing courses: {courses}')
    print(course)
    await attachment.save(fp=f"{course}.pdf")
    moduls = await extract_moduls(f"{course}.pdf")
    channels = await guild.fetch_channels()
    textchannels= [channel for channel in channels if isinstance(channel, discord.TextChannel)]
    roles = await guild.fetch_roles()
    categorychannels = [channel for channel in channels if isinstance(channel, discord.CategoryChannel)]
    missingmoduls = []
    for modul in moduls:
        x = False
        for role in roles:
            if role.name == f"{modul['Studiensemester']}. Sem - {course}":
                r = role
        for channel in textchannels:
            if modul["Modul"] == channel.name:
                x = True
                await edit_per_channel(channel, r)
                print(f"U {channel.name}, {r.name}")

        if not x:
            missingmoduls.append(modul)
    if createnewchannel:
        for modul in missingmoduls:
            for role in roles:
                if role.name == f"{modul['Studiensemester']}. Sem - {course}":
                    r = role
            category = [category for category in categorychannels if category.name == f"Module Semester {modul["Studiensemester"]}"]
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=False),
                r: discord.PermissionOverwrite(view_channel=True)
            }
            try:
                await category[0].create_text_channel(name=modul["Modul"], overwrites=overwrites)
                print(f"C {modul['Modul']}, {course}")
            except IndexError:
                pass
    os.remove(f"{course}.pdf")
