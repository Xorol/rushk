# WIP extension; don't load it

import interactions as ipy
from .base_ext import RushkExtension

class DebugExtension(RushkExtension):
    @ipy.slash_command()
    async def kill(self, ctx: ipy.SlashContext):
        pass

def setup(bot):
    DebugExtension(bot)