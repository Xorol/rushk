# Base extension class with auto-defer and channel checking
# to be subclassed by all other extension classes in the
# `extensions` folder. This extension should *never* be loaded

import interactions as ipy

# List of IDs of channels in which you can use Rushk
ALLOWED_CHANNELS = [
    773676901146296320, # #bot
    791860532960559105, # #well-technically
]

# List of roles that bypass the channel check
BYPASS_CHANNEL_CHECK_ROLES = [
    1214386781953204304, # Tsevhu Helper
]

# List of servers Rushk can be used in
SERVER_SCOPES = [
    719617569908064348 # koilang
]

class RushkExtension(ipy.Extension):
    def __init__(self, client: ipy.Client):
        self.client = client

        self.add_ext_auto_defer(time_until_defer=1)
        self.add_ext_check(self.channel_check)
    
    async def channel_check(self, ctx: ipy.BaseContext) -> bool:
        return ctx.channel_id in ALLOWED_CHANNELS or ctx.author.has_any_role(BYPASS_CHANNEL_CHECK_ROLES)
