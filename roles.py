import discord
async def update_sem_roles(member: discord.Member) -> None:
    role_maps = []
    for i in range(1, 8):
        role_map = {
            "ITS": f'{i}. Sem - ITS',
            "TI": f'{i}. Sem - TI',
            "WIN": f'{i}. Sem - WIN',
            "DCT": f'{i}. Sem - DCT',
            "WIW": f'{i}. Sem - WIW',
        }
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
    elif "ITS" not in roles and "TI" not in roles and "WIN" not in roles:
        print(f"Member {member.name} has no course role.")
        return

    for sem in role_numbers:
        if "ITS" in roles:
            if not discord.utils.get(member.guild.roles, name=role_maps[sem-1]["ITS"]) in member.roles:
                await member.add_roles(discord.utils.get(member.guild.roles, name=role_maps[sem-1]["ITS"]))
                print(f"Added role '{sem}. Sem - ITS' to {member.name}")
        if "TI" in roles:
            if not discord.utils.get(member.guild.roles, name=role_maps[sem-1]["TI"]) in member.roles:
                await member.add_roles(discord.utils.get(member.guild.roles, name=role_maps[sem-1]["TI"]))
                print(f"Added role '{sem}. Sem - TI' to {member.name}")
        if "WIN" in roles:
            if not discord.utils.get(member.guild.roles, name=role_maps[sem-1]["WIN"]) in member.roles:
                await member.add_roles(discord.utils.get(member.guild.roles, name=role_maps[sem-1]["WIN"]))
                print(f"Added role '{sem}. Sem - WIN' to {member.name}")
    return

async def remove_old_sem_roles(member: discord.Member, old_roles: list) -> None:

    if len(old_roles) == len(member.roles) or len(old_roles) < len(member.roles):
        return
    
    rmvd_role = [role.name for role in old_roles if role not in member.roles][0]           # nur noch die gelöschte Rolle bleibt übrig
    sem_numbers = [int(role.name[-1]) for role in member.roles if role.name[-1].isdigit()]       # Semesterzahlen extrahieren
    studiengaenge = [role.name for role in member.roles if role.name in ["ITS", "TI", "WIN"]]   # Studiengänge extrahieren

    print(f"Removed role: {rmvd_role}")

    if rmvd_role[-1].isdigit(): # Wenn die gelöschte Rolle eine Semesterrolle war
        sem = rmvd_role[-1]
        for studiengang in studiengaenge:
            await member.remove_roles(discord.utils.get(member.guild.roles, name=f"{sem}. Sem - {studiengang}"))
            print(f"Removed role '{sem}. Sem - {studiengang}' from {member.name}")

    elif rmvd_role in ["ITS", "TI", "WIN"]: # Wenn die gelöschte Rolle ein Studiengang war
        for sem in sem_numbers:
            await member.remove_roles(discord.utils.get(member.guild.roles, name=f"{sem}. Sem - {rmvd_role}"))
            print(f"Removed role '{sem}. Sem - {rmvd_role}' from {member.name}")
    return 

#TODO Erstelle alle notwendigen Rollen falls nicht vorhanden
async def create_roles():
    return