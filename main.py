# To read json file which stores the commands and their explanation
import json

# To write log messages
import logging

# To offer optional arguments
from argparse import ArgumentParser

# To get the language of the user's default environment
import locale

# To print information neatly to the console
from rich.console import Console
from rich.table import Table
from rich.style import Style
from rich import box

from pathlib import Path

JSON_FILE_LOCATION = Path().resolve() / "commands.json"


def get_commands():
    with open(JSON_FILE_LOCATION, "r") as file:
        # reads json and writes into dictionary
        data = json.load(file)
    return data


def get_system_language():
    """If the default environment's language is turkish set locale lang to turkish
    and sets it to english otherwise
    """
    locale_lang = (locale.getdefaultlocale()[0] or "en-US")[:2]
    if locale_lang != "tr":
        locale_lang = "en"
    return locale_lang


if __name__ == "__main__":
    logging.basicConfig(filename=None, level=logging.ERROR)

    logger = logging.getLogger('main')

    system_lang = get_system_language()
    # gets the optional argument language to decide the final language to use
    parser = ArgumentParser()
    parser.add_argument("-l", "--language", nargs="?", type=str, default=system_lang, help="Selects the language")

    args = parser.parse_args()
    lang = args.language
    logger.debug("Locale language is " + system_lang + " and chosen language is: " + lang)

    # Table elements in turkish and english
    tableElements = {"title": {"en": "TRUBA Commands", "tr": "TRUBA Komutları"},
                     "firstCol": {"en": "Command", "tr": "Komut"},
                     "secondCol": {"en": "Explanation", "tr": "Açıklama"}}

    footerDesc = "Görüş ve önerileriniz için grid-teknik@ulakbim.gov.tr adresine mail atabilirsiniz" \
        if lang == "tr" else "You can send mail to grid-teknik@ulakbim.gov.tr for you comments and suggestions"

    # styles
    title_style = Style(bold=True)
    col1_footer_style = Style(color="red", bold=False)
    col2_footer_style = Style(bold=False)

    # Creates table in the final language
    table = Table(title=tableElements["title"][lang], show_lines=True, show_footer=True, title_style=title_style)
    table.add_column(tableElements["firstCol"][lang], style="red", footer="Hint:", footer_style=col1_footer_style)
    table.add_column(tableElements["secondCol"][lang], footer=footerDesc, footer_style=col2_footer_style)

    data = get_commands()

    # Adds commands with their explanations in final language
    for command in data:
        explanation = data[command][lang]
        table.add_row(command+":", explanation)
        logger.debug("Command " + command + " with explanation " + explanation)

    table.box = box.SIMPLE_HEAVY

    # Prints the result to the console
    console = Console()
    console.print(table)
