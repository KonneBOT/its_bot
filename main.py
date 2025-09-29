import os
from dotenv import load_dotenv

import discord
from discord.ext import commands
from discord import app_commands

from responses import get_response
from roles import update_sem_roles, remove_old_sem_roles, sort_sem_roles, create_sem_roles, delete_sem_roles
from channels import  edit_per_channel, update_modul_channels, create_modul_channels_list

# Load Toaken from Safe File
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
print(TOKEN)

# Intents Setup
intents = discord.Intents.all()
client = discord.Client(intents=intents, command_prefix="uwu")
tree = app_commands.CommandTree(client)
GUILD_ID = discord.Object(id="1305824039557791834")

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
    
    #username: str = message.author.name # get Username we're talking to
    user_message: str = message.content # get the message content
    #channel: str = str(message.channel) # get the channel we're talking in

    #print(f'[{channel}] {username}: "{user_message}"') # print the message to the console

    await send_message(message, user_message) # send the message to the send_message function / to Console

# Slash Command to Assign Roles
@tree.command(name="assign_roles", description="Assign roles based on existing roles")
@app_commands.checks.has_permissions(administrator=True)
async def assign_roles(interaction: discord.Interaction):
    if not interaction.guild.me.guild_permissions.manage_roles:
        await interaction.response.send_message("I do not have permission to manage roles.", ephemeral=True)
        return
    await interaction.response.send_message("Roles are being assigned.", ephemeral=True)
    for member in interaction.guild.members:
        if member == client.user:
            continue

        await update_sem_roles(member)

    await interaction.edit_original_response(content="Roles have been assigned.")

# Check for member_updates to assign semester rules
@client.event
async def on_member_update(before: discord.Member, after: discord.Member) -> None:
    if len(before.roles) == len(after.roles):
        pass                   # Falls man hier iwann mal stolpert: in roles.py eine if Abfrage schreiben für len(rmvd_roles) = 0

    elif len(before.roles) > len(after.roles):
        await remove_old_sem_roles(after, before.roles)

    else:
        await update_sem_roles(after)

    print("--------------------")
    return


@tree.command(name="assign_role_channel", description="Assign to Channels to limit access of other roles ")
@app_commands.checks.has_permissions(administrator=True)
async def assign_roles_channel(interaction: discord.Interaction, role: discord.Role):
    try:
        await edit_per_channel(interaction.channel, role)
        await interaction.response.send_message("Channel has been updated", ephemeral=True)
    
    except Exception as e:
        await interaction.response.send_message(e, ephemeral=True)


@tree.command(name="create_roles", description="Create all missing Roles")
@app_commands.checks.has_permissions(administrator=True)
async def create_roles(interaction: discord.Interaction):
    try:
        await interaction.response.send_message("Roles are being created", ephemeral=True)
        await create_sem_roles(interaction.guild)
        await interaction.edit_original_response(content="Roles have been created")

    except Exception as e:
        await interaction.edit_original_response(content=f"{e}")

@tree.command(name="delete_roles", description="Delete all sem roles")
@app_commands.checks.has_permissions(administrator=True)
async def delete_roles(interaction: discord.Interaction):
    try:
        await interaction.response("Roles are being deleted", ephemeral=True)
        await delete_sem_roles(interaction.guild)
        await interaction.edit_original_response(content="Roles have been deleted")

    except Exception as e:
        await interaction.edit_original_response(content=f"{e}")

@tree.command(name="sort_roles", description="Sort roles in discord role overview")
@app_commands.checks.has_permissions(administrator=True)
async def sort_roles(interaction: discord.Interaction):
    try:
        await interaction.response("Roles are being sorted", ephemeral=True)
        await sort_sem_roles(interaction.guild)
        await interaction.edit_original_response(content="Roles have been sorted")

    except Exception as e:
        await interaction.edit_original_response(content=f"{e}")

@tree.command(name="update_channels_pdf", description="create or update channels, given from a course catalogue pdf")
@app_commands.checks.has_permissions(administrator=True)
async def update_channels_pdf(interaction: discord.Interaction, attachment: discord.Attachment, createnewchannel: bool):
    try:
        await interaction.response.send_message("Channel will be updated ...", ephemeral=True)
        await update_modul_channels(interaction, attachment, createnewchannel)
        await interaction.edit_original_response(content="Channel have been updated")

    except Exception as e:
        await interaction.edit_original_response(content=f"{e}")

# --- Dropdown for role selection ---
class RoleSelect(discord.ui.Select):
    def __init__(self, roles, page, total_pages):
        options = [discord.SelectOption(label=r.name, value=str(r.id)) for r in roles]
        super().__init__(
            placeholder=f"Select roles (Page {page+1}/{total_pages})",
            min_values=0,
            max_values=len(options),
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        chosen_roles = [interaction.guild.get_role(int(v)) for v in self.values]
        self.view.selected_ids.update([r.id for r in chosen_roles])
        await interaction.response.send_message(
            f"✅ Stored {len(self.view.selected_ids)} role(s) so far.",
            ephemeral=True
        )


# --- Navigation buttons ---
class RoleSelectPrev(discord.ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.secondary, label="⬅️ Prev")

    async def callback(self, interaction: discord.Interaction):
        view: RoleSelectView = self.view
        view.page -= 1
        view.update_view()
        await interaction.response.edit_message(view=view)


class RoleSelectNext(discord.ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.secondary, label="Next ➡️")

    async def callback(self, interaction: discord.Interaction):
        view: RoleSelectView = self.view
        view.page += 1
        view.update_view()
        await interaction.response.edit_message(view=view)


# --- Submit button ---
class RoleSelectSubmit(discord.ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.success, label="✅ Submit")

    async def callback(self, interaction: discord.Interaction):
        view: RoleSelectView = self.view
        chosen_roles = [interaction.guild.get_role(rid) for rid in view.selected_ids]
        view.chosen_roles = chosen_roles
        await interaction.response.send_message(
            f"Finalized selection: {', '.join(r.name for r in chosen_roles) if chosen_roles else 'None'}",
            ephemeral=True
        )
        view.stop()


# --- Cancel button ---
class RoleSelectCancel(discord.ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.danger, label="❌ Cancel")

    async def callback(self, interaction: discord.Interaction):
        view: RoleSelectView = self.view
        view.chosen_roles = []  # clear roles
        await interaction.response.send_message("❌ Selection cancelled.", ephemeral=True)
        view.stop()


# --- View controller ---
class RoleSelectView(discord.ui.View):
    def __init__(self, roles, page=0, timeout=120):
        super().__init__(timeout=timeout)
        self.all_roles = [r for r in roles if not r.is_default()]
        self.page = page
        self.chosen_roles = []
        self.selected_ids = set()
        self.update_view()

    def update_view(self):
        self.clear_items()
        # Paginate roles
        start = self.page * 25
        end = start + 25
        page_roles = self.all_roles[start:end]
        total_pages = (len(self.all_roles) - 1) // 25 + 1

        # Dropdown
        self.add_item(RoleSelect(page_roles, self.page, total_pages))

        # Navigation
        if self.page > 0:
            self.add_item(RoleSelectPrev())
        if self.page < total_pages - 1:
            self.add_item(RoleSelectNext())

        # Submit + Cancel
        self.add_item(RoleSelectSubmit())
        self.add_item(RoleSelectCancel())


# --- Slash command ---
@tree.command(name="update_channels_list", description="create or update channels, given from a List")
@app_commands.checks.has_permissions(administrator=True)
async def update_channels_list(
    interaction: discord.Interaction,
    category: discord.CategoryChannel,
    messageidwithlist: str
):
    try:
        await interaction.response.send_message("Channel will be updated ...", ephemeral=True)

        roles = interaction.guild.roles
        view = RoleSelectView(roles)
        await interaction.followup.send(
            "Please select the roles to use (you can change pages, then press ✅ Submit or ❌ Cancel):",
            view=view,
            ephemeral=True
        )

        await view.wait()

        if not view.chosen_roles:
            await interaction.edit_original_response(content="No roles selected, cancelling.")
            return

        await create_modul_channels_list(interaction, category, view.chosen_roles, int(messageidwithlist))
        await interaction.edit_original_response(content="Channel have been updated")

    except Exception as e:
        await interaction.edit_original_response(content=f"{e}")

# Run the Bot
def main() -> None:
    client.run(TOKEN)

if __name__ == '__main__':
    main()