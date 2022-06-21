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


# To support multilingual text
import gettext

# To find running time
from time import perf_counter

JSON_FILE_LOCATION = "/etc/lscmd/commands.json"


def get_commands():
    """
        Reads the commands from the JSON file and returns it as a dictionary
    :return:
        data (dict): Commands in respected language as a nested dictionary (data[command][language])
    """
    with open(JSON_FILE_LOCATION, "r") as file:
        # reads json and writes into dictionary
        data = json.load(file)
    return data


def get_system_language():
    """
        If the default environment's language is turkish set locales lang to turkish
        and sets it to english otherwise, then returns the language
    :return:
        locale_lang (str): locale language (en or tr)
    """

    locale_lang = (locale.getdefaultlocale()[0] or "en-US")[:2]
    if locale_lang != "tr":
        locale_lang = "en"
    return locale_lang


if __name__ == "__main__":

    # starts the time counter
    start = perf_counter()

    logging.basicConfig(filename=None, level=logging.ERROR)

    logger = logging.getLogger('main')

    system_lang = get_system_language()

    # gets the optional argument language to decide the final language to use
    parser = ArgumentParser()
    parser.add_argument("-l", "--language", nargs="?", type=str, choices=["tr", "en"],
                        default=system_lang, help="Selects the language")
    parser.add_argument("-v", "--verbose", action="count", help="Shows the running time")

    args = parser.parse_args()
    lang = args.language

    # loads the selected language's language file lcmd.mo
    translation = gettext.translation('lscmd',localedir="/usr/local/share/locale", languages=[args.language])
    translation.install()
    _ = translation.gettext
    logger.debug("Locale language is " + system_lang + " and chosen language is: " + lang)

    footerMsg = _("You can send mail to grid-teknik@ulakbim.gov.tr for you comments and suggestions.")

    # styles
    title_style = Style(bold=True)
    col1_footer_style = Style(color="red", bold=False)
    col2_footer_style = Style(bold=False)

    # Creates table in the final language
    table = Table(title=_("TRUBA Commands"), show_lines=True, show_footer=True, title_style=title_style)
    table.add_column(_("Command"), style="red", footer="Hint:", footer_style=col1_footer_style)
    table.add_column(_("Explanation"), footer=footerMsg, footer_style=col2_footer_style)

    data = get_commands()
    logger.debug("dictionary is created using the JSON file with size", len(data))

    # Adds commands with their explanations in final language
    for command in data:
        explanation = data[command][lang]
        table.add_row(command+":", explanation)
        logger.debug("Command " + command + " with explanation " + explanation)

    table.box = box.SIMPLE_HEAVY

    # Prints the result to the console
    console = Console()
    console.print(table)

    # ends the time counter and reports if asked
    end = perf_counter()
    if args.verbose:
        print("Time elapsed:", end - start)
