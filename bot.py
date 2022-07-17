"""
NewsBot

Track RSS feeds and display them in chat messages on Discord
"""

import os
import logging
import argparse
import configparser

from discord.ext import commands

bot = commands.Bot(command_prefix="!")
LOGGER = logging.getLogger(__name__)


def configure_logger(logger: logging.Logger) -> None:
    """
    Setup a logger with a StreamHandler in DEBUG with a custom format

    :param logger: The logger to configure
    :type logger: logging.Logger
    """
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s",
        "%m-%d %H:%M:%S",
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)


def parse_args() -> argparse.Namespace:
    """
    Parse CLI arguments

    :return: The parsed CLI arguments
    :rtype: argparse.Namespace
    """
    LOGGER.debug("Parsing CLI arguments")
    parser = argparse.ArgumentParser(
        description="Bot to subscribe to RSS feeds and have them displayed to you in chat"
    )
    parser.add_argument(
        "--config_file",
        type=str,
        required=True,
        help="INI file containing connection information",
    )
    args = parser.parse_args()

    if not os.path.isfile(args.config_file):
        raise FileNotFoundError(f"Invalid config file: {args.config_file}")

    LOGGER.debug("Finished parsing CLI arguments")
    return args


def parse_config_file(config_file: str) -> configparser.ConfigParser:
    """
    Parse the bot credentials config INI file

    :param config_file: The config file to parse
    :type config_file: str

    :return: The parsed config file
    :rtype: configparser.ConfigParser
    """
    LOGGER.debug(f"Parsing file at {config_file}")
    parser = configparser.ConfigParser()
    parser.read(config_file)
    return parser


@bot.event
async def on_ready():
    LOGGER.info(f"{bot.user} is connected to Discord!")
    for guild in bot.guilds:
        LOGGER.debug(f"{bot.user} is a member of {guild.name} -- {guild.id}")


@bot.command(name="register")
async def register(ctx, *args, **kwargs) -> None:
    """
    Register a new feed to keep track of
    """
    if len(args) != 1:
        await ctx.send("Require a single argument of an RSS feed to subscribe to")
        return
    LOGGER.debug(f"Registering a new feed")
    feed_url = args[0]
    # Do more here to actually register that feed


@bot.command(name="display")
async def display(ctx, *args, **kwargs) -> None:
    """
    Display the current top item of each feed
    """
    raise NotImplementedError("Implement display method")


def main() -> None:
    """
    Main entrypoint
    """
    configure_logger(LOGGER)
    args = parse_args()
    config = parse_config_file(args.config_file)
    bot.run(config["NewsBot"]["DISCORD_TOKEN"])


if __name__ == "__main__":
    main()
