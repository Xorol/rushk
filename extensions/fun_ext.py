import interactions as ipy

from .base_ext import RushkExtension, SERVER_SCOPES


class FunExtension(RushkExtension):
    
    @ipy.slash_command(
        name="pancak",
        description="Learn how to make Pancaks!",
        scopes=SERVER_SCOPES
    )
    async def pancak(self, ctx: ipy.SlashContext):
        await ctx.send("Paiju:\n- Mud ndu\n- Vi udi oncu\n- Vi hlynna onso, nothii\n- Vi maein oncu\n- Vi nobi onden\n- Qen bu'a onmu\nKveun:\n- Vi'iin, anoavhat wn jima wnd cametu tancam qenmun je.\n- Tan'iin, amiisvhat wn bu'a wnd kiitau yn wnd jima yn.\n- Chas'iin, akpevhat vud zytynyu tanmhai nkor.\n- Leb'iin, ajavhat oajio paijyu syd kiipe yn meq akashvhat.")


def setup(bot: ipy.Client):
    FunExtension(bot)