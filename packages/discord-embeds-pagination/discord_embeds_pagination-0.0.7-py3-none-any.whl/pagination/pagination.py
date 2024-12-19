import discord
from discord.ext.commands import Context
from typing import List, Union, Optional


class Pagination(discord.ui.View):

    def __init__(self, ctx: Union[Context, discord.Interaction], embeds: List[discord.Embed], timeout: Optional[float] = None):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.embeds = embeds
        self.index = 0
        self.message: Optional[discord.Message] = None
        self.page_button = PageButton()
        self.page_button.label = f"{self.index + 1}/{len(self.embeds)}"
        self.add_item(PrevButton())
        self.add_item(self.page_button)
        self.add_item(NextButton())

    async def interaction_check(self, interaction: discord.Interaction):
        if isinstance(self.ctx, Context):
            author_id = self.ctx.author.id
        else:
            author_id = self.ctx.user.id
        return interaction.user.id == author_id

    async def show(self):
        embed = self.embeds[self.index]
        self.page_button.label = f"{self.index + 1}/{len(self.embeds)}"
        await self.message.edit(embed=embed, view=self)

    async def init_messsage(self):
        if isinstance(self.ctx, Context):
            self.message = await self.ctx.reply(embed=self.embeds[0], view=self)
        else:
            await self.ctx.response.send_message(embed=self.embeds[0], view=self)
            self.message = await self.ctx.original_response()


class PrevButton(discord.ui.Button):

    def __init__(self):
        super().__init__(label="<", style=discord.ButtonStyle.gray)

    async def callback(self, interaction: discord.Interaction):
        self.view: Pagination
        await interaction.response.defer()
        if self.view.index == 0:
            self.view.index = len(self.view.embeds) - 1
        else:
            self.view.index -= 1
        await self.view.show()


class NextButton(discord.ui.Button):

    def __init__(self):
        super().__init__(label=">", style=discord.ButtonStyle.gray)

    async def callback(self, interaction: discord.Interaction):
        self.view: Pagination
        await interaction.response.defer()
        if self.view.index == len(self.view.embeds) - 1:
            self.view.index = 0
        else:
            self.view.index += 1
        await self.view.show()


class PageButton(discord.ui.Button):

    def __init__(self):
        super().__init__(label="", style=discord.ButtonStyle.gray)
        self.disabled = True
