import interactions as ipy
import cairosvg

from extensions.base_ext import RushkExtension, SERVER_SCOPES
from .koiwriter import koiwriter

import io
import json
import re


with open("extensions/tsevhu/topics.json", "r") as topics_file:
    TOPICS: dict[str, dict[str, str]] = json.load(topics_file)

def generate_tsevhu_topic_choices() -> list[ipy.SlashCommandChoice]:
    # Make a list of choices for all the registered topics
    # Used for `/tsevhu help`

    global TOPICS

    choices = [
        ipy.SlashCommandChoice(
            name=TOPICS[topic]["display_name"], 
            value=topic
        ) 
        for topic in TOPICS
    ]

    return choices


class TsevhuExtension(RushkExtension):

    @ipy.slash_command(
        name="tsevhu",
        sub_cmd_name="ipa",
        sub_cmd_description="Transcribe Tsevhu text in the IPA!",
        scopes=SERVER_SCOPES
    )
    @ipy.slash_option(
        name="text",
        description="The Tsevhu text to IPA-fy",
        opt_type=ipy.OptionType.STRING,
        required=True
    )
    async def tsevhu_ipa(self, ctx: ipy.SlashContext, text: str):
        # /tsevhu ipa <text>

        consonants = r"[pbtdkgqʔɸβfvθszʃʒçxhmnwlrj ]"
        vowels = r"[ɑeɛɪiuʊɔoœəy]"

        text += "⍀"
        ipa = ""

        skip = False
        for i, letter in enumerate(text):
            if skip:
                skip = False
                continue
            
            if letter == "⍀":
                break

            next_letter = text[i+1]
            
            match letter:
                case "a":
                    match next_letter:
                        case "e":
                            ipa += "e"
                            skip = True
                        case "i":
                            ipa += "ai"
                            skip = True
                        case "u":
                            ipa += "ɑʊ"
                            skip = True
                        case _:
                            ipa += "ɑ"
                case "e":
                    match next_letter:
                        case "u":
                            ipa += "œ"
                            skip = True
                        case _:
                            ipa += "ɛ"
                case "i":
                    match next_letter:
                        case "e":
                            ipa += "ijɛ"
                            skip = True
                        case "o":
                            ipa += "ijo"
                            skip = True
                        case "i":
                            ipa += "ɪ"
                            skip = True
                        case _:
                            ipa += "i"
                case "o":
                    match next_letter:
                        case "i":
                            ipa += "ɔi"
                            skip = True
                        case "e":
                           ipa += "owɛ"
                           skip = True
                        case _:
                           ipa += "o"
                case "u":
                    match next_letter:
                        case "e":
                            ipa += "uwɛ"
                            skip = True
                        case _:
                            ipa += "u"
                case "p" if next_letter == "h":
                    ipa += "ɸ"
                    skip = True
                case "v" if next_letter == "h":
                    ipa += "β"
                    skip = True
                case "t" if next_letter == "h":
                    ipa += "θ"
                    skip = True
                case "t" if next_letter == "z":
                    ipa += "dz"
                    skip = True
                case "t" | "d" if next_letter == "j":
                    ipa += "dʒ"
                    skip = True
                case "c" if next_letter == "h":
                    ipa += "tʃ"
                    skip = True
                case "s" if next_letter == "h":
                    ipa += "ʃ"
                    skip = True
                case "r" if next_letter == "h":
                    ipa += "ɾʰ"
                    skip = True
                case "k" if next_letter == "h":
                    ipa += "kʰ"
                    skip = True
                case "r":
                    ipa += "ɾ"
                case "j":
                    ipa += "ʒ"
                case "c":
                    ipa += "ç"
                case "'":
                    ipa += "ʔ"
                case "b" | "g" | "f" | "s" | "z" | "x" | "h" | "m" | "n" | "l" | "p" | "v" | "t" | "d" | "q" | "k" | "w" | "y" | " ":
                    ipa += letter

        ipa = re.sub(rf"^w(?={consonants})|(?<={consonants})w(?={consonants})", "ʍu", ipa)
        ipa = re.sub(rf"y(?={vowels})", "j", ipa)
        ipa = ipa.replace("y", "ə")

        await ctx.send(f"/{ipa}/")
    
    @ipy.slash_command(
        name="tsevhu",
        sub_cmd_name="help",
        sub_cmd_description="Learn about Tsevhu topics!",
        scopes=SERVER_SCOPES
    )
    @ipy.slash_option(
        name="topic",
        description="The topic to learn about",
        required=True,
        opt_type=ipy.OptionType.STRING,
        choices=generate_tsevhu_topic_choices()
    )
    async def tsevhu_help(self, ctx: ipy.BaseContext, topic: str):
        # /tsevhu help <topic>

        topic = TOPICS[topic]

        output = "### " + topic["display_name"] + "\n" + topic["text"]
        await ctx.send(output)
    
    @ipy.slash_command(
        name="tsevhu",
        sub_cmd_name="ripple",
        sub_cmd_description="Turn a Tsevhu word into ripples!",
        scopes=SERVER_SCOPES
    )
    @ipy.slash_option(
        name="word",
        description="The word to ripple-fy. Up to 10 can be provided, separated by commas",
        opt_type=ipy.OptionType.STRING,
        required=True
    )
    async def tsevhu_ripple(self, ctx: ipy.SlashContext, word: str):
        # /tsevhu ripple <word>

        words = word.split(",")
        del word

        if len(words) > 5:
            await ctx.send("Too many words! (max 10)")
            return
        
        pngs: list[ipy.File] = []

        for word in words:
            # Ripple-fy the word
            try:
                koiwriter.rippler(word.lower().strip())
            except KeyError as e:
                # Generate an error message pointing out the bad character
                err_msg = f"Oops! I don't know how to write this character:\n```\n{word}\n"
                bad_char_index = word.index(e.args[0])
                err_msg += (" "*bad_char_index) + "^\n```"

                await ctx.send(err_msg)
                return


            # Turn the outputted .svg into a .png and send
            with open("extensions/tsevhu/koiwriter/output.svg") as svg_file:
                png_bytes: bytes = cairosvg.svg2png(
                    file_obj=svg_file, 
                    output_height=750, 
                    output_width=750,
                    negate_colors=True
                )

            pngs.append(ipy.File(file=io.BytesIO(png_bytes), file_name="ripple.png"))

        await ctx.send(files=pngs)


def setup(bot):
    TsevhuExtension(bot)