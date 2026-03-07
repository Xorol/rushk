# A `Paginator` for long search results


import uuid

from interactions.ext.paginators import Paginator
import interactions as ipy


class WordPaginator(Paginator):
    # The main show

    wordlist: "WordList" = None

    @classmethod
    def from_wordlist(
            self, 
            client: ipy.Client, 
            wordlist: "WordList", 
            page_size: int = 500, # How many chars per page
            timeout: int = 300 # Timeout duration in seconds
        ):
        # Create a `WordPaginator` from a `WordList`

        word_paginator = super().create_from_list(
            client=client, 
            content=wordlist.format(splitlines=True),
            page_size=page_size,
            timeout=timeout
        )

        word_paginator.wordlist = wordlist
        word_paginator.show_callback_button = False

        # Register a callback for the filter dropdown
        client.add_component_callback(
            ipy.ComponentCommand(
                name=f"WordPaginator:{word_paginator._uuid}",
                callback=word_paginator._on_button,
                listeners=[
                    f"{word_paginator._uuid}|filter",
                ],
            )
        )

        return word_paginator
    
    def create_components(self, disable = False) -> list[ipy.ActionRow]:
        # Method override of `Paginator` to account for filtering

        output = super().create_components(disable)

        # Create the part-of-speech filter dropdown
        unique_parts_of_speech: set[str] = {word.part_of_speech for word in self.wordlist.as_words()}
        filter_dropdown = ipy.StringSelectMenu(
            *unique_parts_of_speech,
            custom_id=f"{self._uuid}|filter",
            placeholder="Filter by parts of speech…",
            max_values=len(unique_parts_of_speech)
        )

        output.insert(0, ipy.ActionRow(filter_dropdown))

        return output
    
    async def _on_button(self, ctx: ipy.ComponentContext, *args, **kwargs):
        # Method override of `Paginator` to account for filtering

        # Check if the filter was used
        if ctx.custom_id.endswith("filter"):
            # Filter the wordlist by the selected parts of speech
            filtered_wordlist = self.wordlist.filter_by_part_of_speech(ctx.values)

            # Substitute those filtered words in
            filtered_pages = WordPaginator.from_wordlist(self.client, filtered_wordlist).pages
            self.pages = filtered_pages
            self.page_index = 0

        await super()._on_button(ctx, *args, **kwargs)