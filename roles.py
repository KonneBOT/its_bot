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
    role_maps = [role_map_sem1, role_map_sem2, role_map_sem3, role_map_sem4]

    roles = [role.name for role in member.roles]
    sem = None
    if "1. Semester" in roles:
        sem = 0
    elif "2. Semester" in roles:
        sem = 1
    elif "3. Semester" in roles:
        sem = 2
    elif "4. Semester" in roles:
        sem = 3
    
    if sem is None:
        print(f"Member {member.name} has no semester role.")
        return
    if "ITS" not in roles and "TI" not in roles and "WIN" not in roles:
        print(f"Member {member.name} has no course role.")
        return

    if "ITS" in roles:
        await member.add_roles(discord.utils.get(member.guild.roles, name=role_maps[sem]["ITS"]))
        print(f"Added role '{sem+1}. Sem - ITS' to {member.name}")
    if "TI" in roles:
        await member.add_roles(discord.utils.get(member.guild.roles, name=role_maps[sem]["TI"]))
        print(f"Added role '{sem+1}. Sem - TI' to {member.name}")
    if "WIN" in roles:
        await member.add_roles(discord.utils.get(member.guild.roles, name=role_maps[sem]["WIN"]))
        print(f"Added role '{sem+1}. Sem - WIN' to {member.name}")

    return

async def remove_double_sem_roles(member: discord.Member) -> None:
    roles = [role.name for role in member.roles]
    sem = None
    if "1. Semester" in roles:
        sem = 0
    elif "2. Semester" in roles:
        sem = 1
    elif "3. Semester" in roles:
        sem = 2
    elif "4. Semester" in roles:
        sem = 3