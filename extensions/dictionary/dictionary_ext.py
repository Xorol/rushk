from random import choice
import re
from typing import Annotated
import uuid

from .dictionary_handler import (
    Dictionary, 
    SearchSpecificity, 
    generate_dictionary_choices, 
    SearchResult,
    dictionary_metadata,
)
from .word_paginator import WordPaginator
from extensions.base_ext import RushkExtension, SERVER_SCOPES

import interactions as ipy


DICTIONARY_CHOICES: list[ipy.SlashCommandChoice] = generate_dictionary_choices()


class PatternConverter(ipy.Converter):
    # Used to automagically convert slash command arguments to a `re.Pattern`
    # if needed

    async def convert(ctx: ipy.SlashContext, argument: str) -> re.Pattern:
        return re.compile(argument)


class DictionaryExtension(RushkExtension):

    @ipy.slash_command(
        name="dictionary",
        sub_cmd_name="regexsearch",
        sub_cmd_description="Search a dictionary using Regex!",
        scopes=SERVER_SCOPES
    )
    @ipy.slash_option(
        name="pattern",
        description="The Regex pattern to search with",
        opt_type=ipy.OptionType.STRING,
        required=True
    )
    @ipy.slash_option(
        name="dictionary",
        description="(default Tsevhu)",
        opt_type=ipy.OptionType.STRING,
        choices=DICTIONARY_CHOICES,
        required=False
    )
    async def dictionary_regexsearch(
        self, 
        ctx: ipy.SlashContext, 
        pattern: PatternConverter, 
        dictionary: Dictionary = Dictionary("tsevhu")
    ):
        # /dictionary regexsearch <pattern> [dictionary]

        result: SearchResult = dictionary.words.regex_search(pattern)

        await result.result.send(
            ctx,
            "No results",
            f"### Results for `/{pattern.pattern}/` in {dictionary.display_name}:"
        )

    @ipy.slash_command(
        name="dictionary",
        sub_cmd_name="search",
        sub_cmd_description="Search a dictionary!",
        scopes=SERVER_SCOPES
    )
    @ipy.slash_option(
        name="term",
        description="The term to search for (can use commas as delimiters)",
        opt_type=ipy.OptionType.STRING,
        required=True,
    )
    @ipy.slash_option(
        name="dictionary_to_search",
        description="(default Tsevhu)",
        choices=DICTIONARY_CHOICES + [
            ipy.SlashCommandChoice(name="All dictionaries", value="all")
        ],
        opt_type=ipy.OptionType.STRING,
        required=False,
    )
    @ipy.slash_option(
        name="specificity",
        description="Defines how strict the search is (default Contains word)",
        opt_type=ipy.OptionType.STRING,
        required=False,
        choices=[
            ipy.SlashCommandChoice(name="Contains", value="BROAD"),
            ipy.SlashCommandChoice(name="Contains word", value="MEDIUM"),
            ipy.SlashCommandChoice(name="Exact match", value="NARROW"),
        ],
    )
    async def search(
        self, 
        ctx: ipy.SlashContext, 
        term: str, 
        # (`Annotated` is here to activate i.py's automagical type conversion)
        dictionary_to_search: Dictionary = Dictionary("tsevhu"),
        specificity: SearchSpecificity = SearchSpecificity.MEDIUM,
    ):
        # /dictionary search <term> [dictionary_to_search] [specificity]

        # Search the dictionary
        terms: list[str] = [i.strip() for i in term.lower().split(",")]
        result: SearchResult = dictionary_to_search.search(terms, specificity)

        # Check if the search triggered a shortcut, and, if so, send it instead
        if result.shortcut_flag:
            await ctx.send(result.result)
            return
        
        await result.result.send(
            ctx,
            "No results",
            f"### Results for '{term}' in {dictionary_to_search.name.capitalize()}:"
        )


    @ipy.slash_command(
        name="dictionary",
        sub_cmd_name="random",
        sub_cmd_description="Get a random word stored in Rushk!",
        scopes=SERVER_SCOPES
    )
    @ipy.slash_option(
        name="dictionary",
        description="(default is random)",
        choices=DICTIONARY_CHOICES,
        opt_type=ipy.OptionType.STRING,
        required=False,
    )
    async def dictionary_random(self, ctx: ipy.SlashContext, dictionary: Dictionary = None):
        # /dictionary random [dictionary]

        # If no dictionary was provided, choose one randomly
        if dictionary is None:
            dictionary = Dictionary(choice(list(dictionary_metadata.keys())))

        random_word = dictionary.words.choice()

        # A button to generate another random word from the same dictionary
        another_button = ipy.Button(
            style=ipy.ButtonStyle.BLUE,
            label="Another!",
            custom_id=f"another|{uuid.uuid4()}|{dictionary.name}"
        )

        # Send the word and button
        await random_word.send(
            ctx, 
            "Uhh something's gone wrong",
            f"### A random word from {dictionary.display_name}:\n",
            components=another_button
        ) 
        
    # Add a callback for the another button from `/dictionary random`
    @ipy.component_callback(re.compile(r"^another.*"))
    async def another_button_callback(self, ctx: ipy.ComponentContext):
        # Extract the dictionary from the custom id
        dictionary = Dictionary(ctx.custom_id.split("|")[2])

        # Get a random word and edit the original msg with it
        random_word = dictionary.words.choice()
        output = f"## A random word from {dictionary.display_name}:\n"
        output += random_word.format()

        await ctx.edit_origin(content=output)
    
    @ipy.slash_command(
        name="dictionary",
        sub_cmd_name="info",
        sub_cmd_description="Find out more about a dictionary!",
        scopes=SERVER_SCOPES
    )
    @ipy.slash_option(
        name="dictionary",
        description="The dictionary to look at",
        choices=DICTIONARY_CHOICES,
        opt_type=ipy.OptionType.STRING,
        required=True,
    )
    async def dictionary_info(self, ctx: ipy.SlashContext, dictionary: Dictionary):
        # /dictionary info <dictionary>

        # stupid python 3.11
        last_updated_text=dictionary.last_updated.strftime(r"%B %d, %Y")

        output = ipy.Embed(
            title=dictionary.display_name,
            description=dictionary.language_description,
            thumbnail=dictionary.display_image_url,
            url=dictionary.url,
            footer=ipy.EmbedFooter(
                text=f"Last updated {last_updated_text}"
            ),
            fields=[
                ipy.EmbedField(
                    name="Owner",
                    value=f"<@{dictionary.owner_id}>",
                    inline=True
                ),
                ipy.EmbedField(
                    name="Length",
                    value=f"{len(dictionary.words)} words",
                    inline=True
                ),
                ipy.EmbedField(
                    name="Sample Word",
                    value=dictionary.words.choice().format(),
                    inline=True
                )
            ]
        )

        await ctx.send(embeds=output)


def setup(bot):
    DictionaryExtension(bot)