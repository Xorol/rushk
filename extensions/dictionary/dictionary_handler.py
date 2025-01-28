# Contains all the logic for loading and manipulating dictionaries


from .word_paginator import WordPaginator

import csv
import datetime
import enum
import json
import pathlib
import random
import re
import string
from typing import NamedTuple, Optional

import interactions as ipy


# The metadata for the registered dictionaries
dictionary_metadata: dict = None

with open("extensions/dictionary/dictionaries/meta.json", "r") as metadata_file:
        dictionary_metadata = json.load(metadata_file)

# The json schema for a dictionary representation in `meta.json`
# (instances of `Dictionary` have these same properties)
"""
{
    "type":"object",
    "properties": {
        "name": {
            "description": "The name of the dictionary",
            "type": "string"
        },
        "file": {
            "description": "The name of the file where the dictionary's contents are stored",
            "type": "string"
        },
        "owner_id": {
            "description": "The Discord ID of the owner of the dictionary",
            "type": "string"
        },
        "language_description": {
            "description": "A description of the language",
            "type": "string"
        },
        "url": {
            "description": "(optional) Link to the language's documentation",
            "type": "string",
            "format": "uri"
        },
        "display_image_url": {
            "description": "(optional) Link to a display image for the dictionary",
            "type": "string",
            "format": "uri"
        },
        "search_shortcuts": {
            "description": "(optional) Creates an ability to short-circuit a search operation"
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "triggers": {
                        "description": "A list of strings that, when `term` matches them, will trigger the short-circuit",
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "minItems": 1,
                        "uniqueItems": true
                    },
                    "result": {
                        "description": "The result to be given instead of a normal search",
                        "type": "string"
                    }
                },
                required: ["triggers", "action"]
            },
            "minItems": 1
        }
    },
    "required": ["name", "file", "owner_id"]
}
"""


def generate_dictionary_choices() -> list[ipy.SlashCommandChoice]:
    # Dynamically generate a list of `SlashCommandChoice`s for use in 
    # `SlashCommand` definitions, one choice per detected dictionary

    

    # Iterate over all registered dictionaries' names, create a 
    # `SlashCommandChoice` for each one, and return
    return [
        ipy.SlashCommandChoice(
            name=dictionary_name.capitalize(), 
            value=dictionary_name
        ) 
        for dictionary_name in dictionary_metadata
    ]


class Word(NamedTuple):
    # `NamedTuple` to represent an individual Word

    entry: str
    IPA_transcription: Optional[str]
    part_of_speech: str
    definition: str
    notes: Optional[str]

    @classmethod
    def from_list(cls, origin: list[str]) -> "Word":
        # Fill in mising fields with `None`
        if len(origin) < 5:
            origin += [None] * 5

        return cls._make(origin[:5])


class SearchSpecificity(enum.Enum):
    # Enum for representing how narrow a search is
    # Broad succeeds if `word` *contains* `term`
    # Medium succeeds if `word` contains `term` *as a standalone word*
    # Narrow succeeds only if `word` *is equal to* `term`

    BROAD = enum.auto()
    MEDIUM = enum.auto()
    NARROW = enum.auto()

    @classmethod
    async def convert(
        cls, 
        ctx: ipy.BaseContext, 
        argument: str
    ) -> "SearchSpecificity":
        # Helper function to automagically convert `str`-type arguments passed
        # to slash commands into `SearchSpecificity`s as needed 

        return cls[argument.upper()]


class SearchResult(NamedTuple):
    # Represents the result of a search

    result: "WordList | str"
    shortcut_flag: bool # Whether the search resulted in a shortcut


class WordList:
    # Represents some list of words (could be an entire dictionary,
    # could be the results of a search, etc.)
    
    def __init__(self, origin: list[list[str]]):
        # Converts a `list` into a `WordList`

        self.words: list[list[str]] = origin

    def __len__(self) -> int:
        return len(self.words)
    
    def as_words(self):
        # Storing each word as an instance of `Word` would be terribly
        # memory-intensive, so, let's just make the `Word`s when we need them

        output = [Word.from_list(word) for word in self.words]
        return output
    
    @classmethod
    def from_Words(cls, words: list[Word]) -> "WordList":
        # Create a `WordList` from a `list[Word]`

        return WordList(list(map(list, words)))
    
    def format(self, splitlines: bool = False) -> str | list[str]:
        # Converts the `WordList` into a pretty, formatted `str`

        def format_word(word: Word) -> str:
            # Helper function to format an individual `Word`
            output = f"***{word.entry}***"

            if word.IPA_transcription:
                output += f" [{word.IPA_transcription}]"
            
            output += "\n"
            output += f"*{word.part_of_speech}"

            if not word.part_of_speech.endswith("."):
                output += "."
            
            output += "* "
            output += word.definition

            if word.notes:
                output += f"— {word.notes}"
            
            return output

        # Format each of our `Word`s
        formatted_words: list[str] = list(map(format_word, self.as_words()))

        # If `splitlines` was set to `True`, return `formatted_words` as is
        if splitlines:
            return formatted_words
        
        # Otherwise, join `formatted_words` and return
        return "\n".join(formatted_words)

    def choice(self) -> "WordList":
        # Returns a new `WordList` containing a random word from this `WordList`

        return WordList([random.choice(self.words)])

    def search(
        self, 
        term: str | list[str], 
        specificity: SearchSpecificity
    ) -> "WordList":
        # Searches for `term` in this `WordList`, returning a new `WordList`
        # containing the results of the search

        # Helper functions for matching words
        # Only one is used at a time, based on `specificity`
        def broad_check(word: Word) -> bool:
            return term in word.entry or term in word.definition
        
        def medium_check(word: Word) -> bool:
            normalized_definition = ''.join(chr for chr in word.definition if chr not in string.punctuation)
            return term in word.entry.split(" ") or term in normalized_definition.split(" ")
        
        def narrow_check(word: Word) -> bool:
            return term == word.entry or term == word.definition
        
        # Set `check` to whatever the relevant helper function is as dictated
        # by `specificity`
        match specificity:
            case SearchSpecificity.BROAD:
                check = broad_check
            case SearchSpecificity.MEDIUM:
                check = medium_check
            case SearchSpecificity.NARROW:
                check = narrow_check

        # Force `term` to be a `list` and put it into `terms`
        if isinstance(term, str):
            terms = [term]
        else:
            terms = term

        del term # Very important 

        # Filter `self.words` based on if each word passes `check` (returns `True`)
        output: list[Word] = []
        for term in terms:
            # Now the `term` that is referenced in the `broad_check`,
            # `medium_check`, and `narrow_check` definitions above is actually
            # referring to this for-loop's `term`, so we don't need to pass it
            # as an argument to `check` and can still use the `filter` function!
            output += list(filter(check, self.as_words()))

        # Remove duplicate words that matched multiple `term`s
        output = list(set(output))
        
        # Make a new `WordList` and return
        return WordList.from_Words(output)
    
    async def send(self, ctx: ipy.BaseContext, fallback: str, header: str = None, **kwargs):
        # Send this `WordList` as a message to `ctx`

        if len(self) == 0:
            return await ctx.send(fallback, **kwargs)

        # Paginate long `WordList`s
        if len(self) > 5:
            # Instantiate a `WordPaginator`
            paginator = WordPaginator.from_wordlist(ctx.client, self)

            # Send it and return
            return await paginator.send(ctx, content=header, **kwargs)
        
        # Otherwise, just format and send
        output = header + "\n" + self.format()
        return await ctx.send(output, **kwargs)
    
    def regex_search(self, pattern: re.Pattern) -> SearchResult:
        # Return a new `WordList` containing words whose entries match `pattern`

        # Filter `self.words` based on if they match `pattern`
        matches: list[Word] = list(
            filter(
                lambda word: bool(pattern.findall(word.entry)), 
                self.as_words()
            )
        )

        # Process `matches` into a `SearchResult` and return
        result = WordList.from_Words(matches)
        return SearchResult(result, shortcut_flag=False)

    def filter_by_part_of_speech(
        self, 
        part_of_speech: str | list[str]
    ) -> "WordList":
        # Returns a new `WordList` containing all words in this `WordList` that
        # match `part_of_speech`

        if isinstance(part_of_speech, str):
            part_of_speech = [part_of_speech]
        
        def check(word: Word) -> bool:
            # Helper function to check if the parts of speech match

            return word.part_of_speech in part_of_speech
        
        # Filter our `Word`s based on if they pass `check` (returns `True`)
        output: list[Word] = list(filter(check, self.as_words()))

        return WordList.from_Words(output)


class Dictionary:
    def __init__(self, name: str):
        

        # Python trickery
        self.__dict__ = {**self.__dict__, **dictionary_metadata[name]}
        self._words: WordList = None 

    @property
    def display_name(self) -> str:
        return self.name.capitalize()
    
    @property
    def last_updated(self) -> datetime.datetime:
        # The last time the `Dictionary`'s file was modified

        self_file = pathlib.Path(f"extensions/dictionary/dictionaries/{self.file}")
        modified_timestamp = self_file.stat().st_mtime
        modified_time = datetime.datetime.fromtimestamp(modified_timestamp, tz=datetime.UTC)

        return modified_time

    @property
    def words(self) -> WordList:
        # Reads the `Dictionary`'s words from the relevant file and returns
        # them as a WordList

        # Caching system so we're not constantly opening files
        if self._words:
            return self._words
        
        # Open the relevant file and make a reader object
        with open(f"extensions/dictionary/dictionaries/{self.file}", "r") as word_file:
            reader = csv.reader(word_file, dialect="excel-tab")
            raw_words = [word[:5] for word in reader] # We only care about the first 5 columns
        
        # Convert the reader object into a WordList and return
        self._words = WordList(raw_words)
        return self._words

    def search(
        self, 
        term: str | list[str], 
        specificity: SearchSpecificity
    ) -> SearchResult:
        # Search through this `Dictionary` for words matching `term`

        # Check if a search shortcut has been triggered
        if hasattr(self, "search_shortcuts"):
            for shortcut in self.search_shortcuts:
                if term in shortcut["triggers"]:
                    result = shortcut["result"]
                    shortcut_flag = True

                    return SearchResult(result, shortcut_flag)
        
        # If no shortcut was triggered, search normally
        result = self.words.search(term, specificity)
        shortcut_flag = False

        return SearchResult(result, shortcut_flag)

    @classmethod
    async def convert(
        cls, 
        ctx: ipy.BaseContext, 
        argument: str
    ) -> "Dictionary | str":
        # Same as the converter for `SearchSpecificity`, but for `Dictionary`s
        
        # If `argument` isn't a valid dictionary, just return as is
        if argument not in dictionary_metadata.keys():
            return argument
        
        return cls(argument)
