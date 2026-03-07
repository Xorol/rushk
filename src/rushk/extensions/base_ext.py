# Base extension class with auto-defer and channel checking
# to be subclassed by all other extension classes in the
# `extensions` folder. This extension should *never* be loaded

import interactions as ipy
from importlib import resources as resources
import json

with resources.open_text("rushk.data", "config.json") as config_file:
    config = json.load(config_file)

environment = config["environments"][config["environment"]]

ALLOWED_CHANNELS = environment["channel_scopes"]
BYPASS_CHANNEL_CHECK_ROLES = environment["channel_check_override_roles"]
SERVER_SCOPES = environment["guild_scopes"]

del config, environment

class RushkExtension(ipy.Extension):
    def __init__(self, client: ipy.Client):
        self.client = client

        self.add_ext_auto_defer(time_until_defer=1)
        self.add_ext_check(self.channel_check)
    
    async def channel_check(self, ctx: ipy.BaseContext) -> bool:
        return ctx.channel_id in ALLOWED_CHANNELS or ctx.author.has_any_role(BYPASS_CHANNEL_CHECK_ROLES)
