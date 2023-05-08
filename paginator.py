import discord
from typing import List
from collections import deque


class PaginatorView(discord.ui.View):
    def __init__(
            self,
            embeds: List[discord.Embed],
            files: List[discord.File]
    ) -> None:
        super().__init__(timeout=30)

        self._embeds = embeds
        self._queue = deque(embeds)
        self._initial = embeds[0]
        self._len = len(embeds)
        self._current_page = 1
        self._files = files
        self._fileQueue = deque(files)


        for embed in self._embeds:
            embed.set_footer(text=f"Page {self._embeds.index(embed) + 1}/{self._len}")


    @discord.ui.button(label='⬅️')
    async def previous(self, interaction: discord.Interaction, _):
        self._queue.rotate(1)
        self._fileQueue.rotate(1)
        embed = self._queue[0]
        attachments = [self._fileQueue[0]]
        await interaction.response.edit_message(embed=embed, attachments=attachments)

    @discord.ui.button(label='➡️')
    async def next(self, interaction: discord.Interaction, _):
        self._queue.rotate(-1)
        self._fileQueue.rotate(-1)
        embed = self._queue[0]
        attachments = [self._fileQueue[0]]
        await interaction.response.edit_message(embed=embed, attachments=attachments)

    @property
    def initial(self):
        return self._initial