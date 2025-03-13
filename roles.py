import discord

courses = ["ITS", "TI", "WIN", "DTC", "WIW"]


async def update_sem_roles(member: discord.Member) -> None:
    role_maps = []
    for i in range(1, 8):
        role_map = {}
        for course in courses:
            role_map[course] = f'{i}. Sem - {course}'
        role_maps.append(role_map)

    roles = [role.name for role in member.roles]

    # Check for orphaned "i. Sem - XXX" Roles (ohne "Semester i")
    roles_sem = [role for role in roles if role[0].isdigit()] # Wenn erste Stelle eine Zahl ist erfüllt schon Schema "i. Sem - XXX"
    for role in roles_sem:
        sem = role[0]
        if not f"Semester {sem}" in roles:
            await member.remove_roles(discord.utils.get(member.guild.roles, name=role))
            print(f"Removed orphaned role '{role}' from {member.name}")

    # Add the new "i. Sem - XXX" Roles to the member
    role_numbers = [int(role[-1]) for role in roles if role[-1].isdigit()]

    if role_numbers == []:  # Wenn keine Semesterrolle vorhanden ist
        print(f"Member {member.name} has no semester role.")
        return
    elif not any(x in roles for x in courses): #Wenn keine Cours rolle hat
        print(f"Member {member.name} has no course role.")
        return

    for sem in role_numbers:
        for course in courses:
            if course in roles:
                if not discord.utils.get(member.guild.roles, name=role_maps[sem - 1][course]) in member.roles:
                    await member.add_roles(discord.utils.get(member.guild.roles, name=role_maps[sem - 1][course]))
                    print(f"Added role '{sem}. Sem - {course}' to {member.name}")
    return


async def remove_old_sem_roles(member: discord.Member, old_roles: list) -> None:
    if len(old_roles) == len(member.roles) or len(old_roles) < len(member.roles):
        return

    rmvd_role = [role.name for role in old_roles if role not in member.roles][0]  # nur noch die gelöschte Rolle bleibt übrig
    sem_numbers = [int(role.name[-1]) for role in member.roles if role.name[-1].isdigit()]  # Semesterzahlen extrahieren
    studiengaenge = [role.name for role in member.roles if role.name in courses]  # Studiengänge extrahieren

    print(f"Removed role: {rmvd_role}")

    if rmvd_role[-1].isdigit():  # Wenn die gelöschte Rolle eine Semesterrolle war
        sem = rmvd_role[-1]
        for studiengang in studiengaenge:
            await member.remove_roles(discord.utils.get(member.guild.roles, name=f"{sem}. Sem - {studiengang}"))
            print(f"Removed role '{sem}. Sem - {studiengang}' from {member.name}")

    elif rmvd_role in courses:  # Wenn die gelöschte Rolle ein Studiengang war
        for sem in sem_numbers:
            await member.remove_roles(discord.utils.get(member.guild.roles, name=f"{sem}. Sem - {rmvd_role}"))
            print(f"Removed role '{sem}. Sem - {rmvd_role}' from {member.name}")
    return


def create_expected_roles() -> list:
    expextedroles = []
    for i in range(1, 8):
        for course in courses:
            expextedroles.append(f'{i}. Sem - {course}')
    return expextedroles


async def create_sem_roles(guild: discord.Guild) -> None:
    roles = await guild.fetch_roles()
    rolenames = [role.name for role in roles]
    expectedroles = create_expected_roles()
    for i, role in enumerate(expectedroles):
        if role not in rolenames:
            await guild.create_role(name=role)
    return


async def delete_sem_roles(guild: discord.Guild) -> None:
    roles = await guild.fetch_roles()
    expectedroles = create_expected_roles()
    for role in roles:
        if role.name in expectedroles:
            await role.delete()
    return


async def sort_sem_roles(guild: discord.Guild) -> None:
    expectedroles = create_expected_roles()
    start = discord.utils.get(guild.roles, name=expectedroles[0]).position
    for name in expectedroles:
        role = discord.utils.get(guild.roles, name=name)
        await role.edit(position=start, reason='sort')
        start = start - 1
    return
