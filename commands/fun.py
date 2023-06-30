import interactions as ipy
import utils

class FunCommands(ipy.Extension):
  @ipy.slash_command(
    name="pancak",
    description="Learn how to make Pancaks!"
  )
  async def pancak(self, ctx: ipy.InteractionContext):
    await ctx.send("Paiju:\n- Mud ndu\n- Vi udi oncu\n- Vi hlynna onso, nothii\n- Vi maein oncu\n- Vi nobi onden\n- Qen bu'a onmu\nKveun:\n- Vi'iin, anoavhat wn jima wnd cametu tancam qenmun je.\n- Tan'iin, amiisvhat wn bu'a wnd kiitau yn wnd jima yn.\n- Leb'iin, ajavhat oajio paijyu syd kiipe yn meq akashvhat.\n- Chas'iin, akpevhat vud zytynyu tanmhai nkor.\n")

  @ipy.slash_command(
    name="edcypher",
    description="Encrypt your messages with Ed's Cypher!"
  )
  @ipy.slash_option(
    name="mode",
    description="Whether to encrypt or decrypt",
    opt_type=ipy.OptionType.STRING,
    required=True,
    choices=[
      ipy.SlashCommandChoice(name="Encrypt", value="encrypt"),
      ipy.SlashCommandChoice(name="Decrypt", value="decrypt")
    ]
  )
  async def edcypher(self, ctx: ipy.InteractionContext, mode: str):
    modal = ipy.Modal(
      ipy.ShortText(label="Key", custom_id="key"),
      ipy.ShortText(label="Offset", custom_id="offset"),
      ipy.ParagraphText(label="Plaintext", custom_id="plaintext"),
      title="Edcypher"
    )
    await ctx.send_modal(modal=modal)
    modal_ctx: ipy.ModalContext = await ctx.bot.wait_for_modal(modal)
    
    key = modal_ctx.responses["key"]
    offset = modal_ctx.responses["offset"]
    plaintext = modal_ctx.responses["plaintext"]

    plaintext = [ord(i) for i in plaintext]
    key = [ord(i) * key.count(i) for i in key]

    try:
      offset = int(offset)
    except ValueError:
      await modal_ctx.send("Your offset must be a number!", ephemeral=True)
      return

    out = []

    for i, j in enumerate(plaintext):
      if mode == "encrypt":
        out.append(chr(j + key[i % len(key)] + offset))
      else:
        out.append(chr(j - key[i % len(key)] - offset))
    out = ''.join(out)
    await modal_ctx.send(out)
