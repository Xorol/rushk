import interactions, utils, json

SUGGESTIONS_FILE = "commands/suggestions.json"

with open(SUGGESTIONS_FILE, "r") as f:
  suggestions = json.load(f)

suggestion_choices = []

for i in suggestions:
  suggestion_choices.append(interactions.Choice(name = i["title"], value = i["title"]))

del suggestions

suggestion_statuses = ["New", "In progress", "Closed"]
suggestion_status_choices = []
for i in suggestion_statuses:
  suggestion_status_choices.append(interactions.Choice(name = i, value = i))

class SuggestionCommands (interactions.Extension):
  def __init(self, client):
    self.client = client

  async def status (self, ctx : interactions.CommandContext, kwargs):
    if ctx.author.user.id != utils.ids.XOROL:
      await ctx.send("You're not Xorol, only he can use this command!", ephemeral = True)
      return

    title = kwargs["suggestion"]
    new_status = kwargs["status"]

    with open(SUGGESTIONS_FILE, "r") as f:
      suggestions = json.load(f)

    found = False
    for i, j in enumerate(suggestions):
      if j["title"] == title:
        j["status"] = new_status
        suggestions[i] = j
        found = True
        break

    if not found:
      await ctx.send("You somehow picked a suggestion that doesn't exist...")
      return

    del found

    with open(SUGGESTIONS_FILE, "w") as f:
      json.dump(suggestions, f)

    await ctx.send(f"{title}'s status has now been updated to {new_status}!", ephemeral = True)

  async def suggest (self, ctx : interactions.CommandContext, kwargs):
    title = kwargs["title"]
    reserved_names = ["all", "View all suggestions"]
    if title in reserved_names:
      await ctx.send(f"Sorry, '{title}' is a reserved title, used for differentiating suggestions from the 'View all suggestions' option in the `/suggestion view` command")
      return
    
    desc = kwargs["description"]
    author = ctx.author.user

    with open(SUGGESTIONS_FILE, "r") as f:
      suggestions = json.load(f)

    suggestions.append({
      "title":title,
      "description":desc,
      "author":int(author.id),
      "status":"New"
    })

    with open(SUGGESTIONS_FILE, "w") as f:
      json.dump(suggestions, f)

    await ctx.send("Your suggestion has been saved!")

  async def view (self, ctx : interactions.CommandContext, kwargs):
    with open(SUGGESTIONS_FILE, "r") as f:
      suggestions = json.load(f)

    suggestion = kwargs["suggestion"]

    if suggestion == "all":
      if len(suggestions) == 0:
        await ctx.send("There are no suggestions. You can fix that by suggesting something!")
        return
        
      out = "Here's all current suggestions!"
      for i in suggestions:
        out += "\n> " + i["title"]

      await ctx.send(out)
      return

    found = False
    for i, j in enumerate(suggestions):
      if j["title"] == suggestion:
        suggestion = j
        found = True
        break

    if not found:
      await ctx.send("You somehow picked a suggestion that doesn't exist...")
      return

    del found

    author = await utils.bot.get_user(suggestion["author"], self.client)

    embedi = interactions.Embed(
      title = j["title"],
      description = j["description"],
      fields = [
        interactions.EmbedField(name = "Suggested by", value = author.username),
        interactions.EmbedField(name = "Status", value = suggestion["status"])
      ]
    )
    await ctx.send(embeds = embedi)

  @interactions.extension_command(
    name = "suggestion",
    description = "secret desc lol",
    scope = utils.ids.KOILANG,
    options = [
      interactions.Option(
        name = "suggest",
        description = "Suggest something to be added to Rushk!",
        type = interactions.OptionType.SUB_COMMAND,
        options = [
          interactions.Option(
            name = "title",
            description = "The title of your suggestion",
            type = interactions.OptionType.STRING,
            required = True
          ),
          interactions.Option(
            name = "description",
            description = "The description of your suggestion",
            type = interactions.OptionType.STRING,
            required = True
          )
        ]
      ),
      interactions.Option(
        name = "set_status",
        description = "Updates the status of a suggestion",
        type = interactions.OptionType.SUB_COMMAND,
        options = [
          interactions.Option(
            name = "suggestion",
            description = "The suggestion to update the status of",
            type = interactions.OptionType.STRING,
            required = True,
            choices = suggestion_choices
          ),
          interactions.Option(
            name = "status",
            description = "The new status",
            type = interactions.OptionType.STRING,
            required = True, 
            choices = suggestion_status_choices
          )
        ]
      ),
      interactions.Option(
        name = "view",
        description = "See one or all suggestions currently submitted!",
        type = interactions.OptionType.SUB_COMMAND,
        options = [
          interactions.Option(
            name = "suggestion",
            description = "The suggestion to view",
            type = interactions.OptionType.STRING,
            required = True,
            choices = suggestion_choices + [interactions.Choice(name="View all suggestions", value = "all")]
          )
        ]
      )
    ]
  )
  async def suggestion_master_command (self, ctx : interactions.CommandContext, sub_command,**kwargs):
    if sub_command == "suggest":
      await self.suggest(ctx, kwargs)
    elif sub_command == "set_status":
      await self.status(ctx, kwargs)
    elif sub_command == "view":
      await self.view(ctx, kwargs)

def setup(client):
  SuggestionCommands(client)