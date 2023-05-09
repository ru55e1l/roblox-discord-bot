import discord
from typing import List
from collections import deque


class FilePaginatorView(discord.ui.View):
    def __init__(
            self,
            files: List[discord.File]
    ) -> None:
        super().__init__(timeout=30)

        self._initial = files[0]
        self._len = len(files)
        self._current_page = 1
        self._files = files
        self._fileQueue = deque(files)



    @discord.ui.button(label='⬅️')
    async def previous(self, interaction: discord.Interaction, _):
        self._fileQueue.rotate(1)
        attachments = [self._fileQueue[0]]
        await interaction.response.edit_message(attachments=attachments)

    @discord.ui.button(label='➡️')
    async def next(self, interaction: discord.Interaction, _):
        self._fileQueue.rotate(-1)
        attachments = [self._fileQueue[0]]
        await interaction.response.edit_message(attachments=attachments)

    @property
    def initial(self):
        return self._initial