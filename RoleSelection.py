import discord
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

