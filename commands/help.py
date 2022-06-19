import interactions, utils

HELP_STRS = {
  "help":"Let's say you're looking at this command:\n`/dictionary search <dictionary> <term> [<specificity>]`\n\nHow do you read it? Simple. The first part is just the command, `<dictionary>` is surrounded by `<these>`, which means it's required. `[<specificity>]` is surrounded by `[<these>]`, which means it's optional. See? Simple",
  "dictionary-search":"`/dictionary search <dictionary> <term> [<specificity>]`\n> Searches `dictionary` for `term`, and gives you the results\n\n`dictionary` - The dictionary to search in\n`term` - The term to search for\n`specificity` - Optional. The specificity of the search. If set to \"broad\", it will give results that contain `term`, if it's set to \"narrow\", it'll only give results that are `term`, case-sensitive. Defaults to \"broad\".",
  "dictionary-info":"`/dictionary info <dictionary>`\n> Gives you an overview of `dictionary`\n\n`dictionary` - The dictionary to get an overview of",
  "dictionary-random":"`/dictionary random <dictionary>`\n> Gives you a random word from `dictionary`\n\n`dictionary` - The dictionary to get a random word from. It can even be set to random, random-ception!",
  "edcypher":"`/edcypher`\n> Encrypt your messages with Ed's Cypher. It has no arguments, as your super secret message is gotten through fancy pop-ups",
  "tsevhu-ipa":"`/tsevhu ipa`\n> Turns your tsevhu text into IPA! It has no arguments because your text is gotten through modals.",
  "wiki-random":"`\wikipedia random [<pages>]`\n> Gets a random page from Wikipedia\n\n`pages` - Optional. The number of random pages to get. Be careful, the command takes longer the bigger this number is. Also, you'll only get a summary of the page if this is set to 1. Defaults to 1.",
  "wiki-view":"`/wikipedia view <page>`\n> Gives a summary of `page` as a Wikipedia page. Also provides a link to the page.\n\n`page` - The page to get a summary of."
}

HELP_CHOICES = [
  interactions.Choice(name="How to read help messages", value="help"),
  interactions.Choice(name="/dictionary search", value="dictionary-search"),
  interactions.Choice(name="/dictionary info", value="dictionary-info"),
  interactions.Choice(name="/dictionary random", value="dictionary-random"),
  interactions.Choice(name="/edcypher", value="edcypher"),
  interactions.Choice(name="/tsevhu ipa", value="tsevhu-ipa"),
  interactions.Choice(name="/wikipedia random", value="wiki-random"),
  interactions.Choice(name="/wikipedia view", value="wiki-view"),
]

class HelpCommand(interactions.Extension):
  def __init__(self, client: interactions.Client) -> None:
    self.client = client

  @interactions.extension_command(
    name="help",
    description="Get some help with commands!",
    scope=utils.ids.KOILANG,
    options=[
      interactions.Option(
        name="command",
        description="The command to get help on... duh",
        type=interactions.OptionType.STRING,
        choices=HELP_CHOICES,
        required=True
      )
    ]
  )
  async def help_command(self, ctx: interactions.CommandContext, command: str):
    await ctx.send(HELP_STRS[command])

def setup(client):
  HelpCommand(client)
