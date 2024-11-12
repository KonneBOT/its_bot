import discord

role_numbers = None
async def add_sem_roles(member: discord.Member) -> None:
    global role_numbers
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
    role_maps = [role_map_sem1, role_map_sem2, role_map_sem3, role_map_sem4]

    roles = [role.name for role in member.roles]

    role_numbers = [int(role[:1]) for role in roles if role[:1].isdigit()]  # !!!! FÜR ITS DISCORD UMSTELLEN AUF [-1:] !!!!
    
    if role_numbers == []:  # Wenn keine Semesterrolle vorhanden ist
        print(f"Member {member.name} has no semester role.")
        return
    elif "ITS" not in roles and "TI" not in roles and "WIN" not in roles:
        print(f"Member {member.name} has no course role.")
        return
    else:
        old_roles = [role.name for role in member.roles]

    for sem_num,sem in enumerate(role_numbers):
        if "ITS" in roles:
            await member.add_roles(discord.utils.get(member.guild.roles, name=role_maps[sem]["ITS"]))
            print(f"Added role '{sem+1}. Sem - ITS' to {member.name}")
            await remove_double_sem_roles(member, old_roles)
        if "TI" in roles:
            await member.add_roles(discord.utils.get(member.guild.roles, name=role_maps[sem]["TI"]))
            print(f"Added role '{sem+1}. Sem - TI' to {member.name}")
            await remove_double_sem_roles(member, old_roles)
        if "WIN" in roles:
            await member.add_roles(discord.utils.get(member.guild.roles, name=role_maps[sem]["WIN"]))
            print(f"Added role '{sem+1}. Sem - WIN' to {member.name}")
            await remove_double_sem_roles(member, old_roles)

    return

async def remove_double_sem_roles(member: discord.Member, old_roles: list) -> None:

    new_roles = [role.name for role in member.roles if role.name not in old_roles] # nur noch die neue Rolle bleiben übrig

    if len(new_roles) == 0:
        print(f"Member {member.name} has no new roles.")
        return
    
    if len(role_numbers) > 1:   # Wenn mehr als eine Semesterrolle vorhanden ist soll nichts gelöscht werden
        print(f"Member {member.name} has more than one semester role.")
        return
    
    # Else nur eine Rolle also muss die andere geändert werden!
    sem = new_roles[0][:1] # Semester aus der Rolle extrahieren
    anti_sem = [sem_number for sem_number in role_numbers if sem_number[:1] != sem][0] # die eine alte Semester Rollennummer extrahieren
    for num in anti_sem:
        sem_roles = [role for role in old_roles if f"{num}. Semester - " in role.name]
        for role in sem_roles:
            await member.remove_roles(discord.utils.get(member.guild.roles, name=role))
            print(f"Removed role '{role}' from {member.name}")


    