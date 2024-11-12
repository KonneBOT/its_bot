import discord

async def add_sem_roles(member: discord.Member) -> None:
    role_map_sem1 = {
        "ITS": "1. Sem - ITS",
        "TI": "1. Sem - TI",
        "WIN": "1. Sem - WIN"
    }
    role_map_sem2 = {
        "ITS": "2. Sem - ITS",
        "TI": "2. Sem - TI",
        "WIN": "2. Sem - WIN"
    }
    role_map_sem3 = {
        "ITS": "3. Sem - ITS",
        "TI": "3. Sem - TI",
        "WIN": "3. Sem - WIN"
    }
    role_map_sem4 = {
        "ITS": "4. Sem - ITS",
        "TI": "4. Sem - TI",
        "WIN": "4. Sem - WIN"
    }

    #TODO: Alle Erweitern auf DCT und WIW

    role_maps = [role_map_sem1, role_map_sem2, role_map_sem3, role_map_sem4]

    roles = [role.name for role in member.roles]

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

async def remove_sem_roles(member: discord.Member, old_roles: list) -> None:

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


    