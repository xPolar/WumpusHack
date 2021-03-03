"""
MIT License

Copyright (c) 2019 xPolar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# Packages.
## Packages default to Python.
import datetime
from asyncio import sleep
## Packages that have to be installed through the package manager.
import aiohttp, discord
from colorama import Fore, Style, init
from discord.ext import commands
## Packages on this machine.
import config

# Initialize colorama
init()

def get_prefix(bot : commands.AutoShardedBot, message : discord.Message) -> list:
    """Returns the bot's prefix.

    Args:
        bot (commands.AutoShardedBot): The bot object.
        message (discord.Message): Message object.

    Returns:
        list: The prefixes the bot will accept.
    """

    return commands.when_mentioned_or(">")(bot, message)

intents = discord.Intents.default()
intents.members = True
bot = commands.AutoShardedBot(activity = discord.Game(f"with {config.prefix}help"), command_prefix = get_prefix, case_insensitive = True, intents = intents, status = discord.Status.dnd)

bot.load_extension("jishaku")

# Loads all of our cogs.
for cog in config.cogs:
    bot.load_extension(f"cogs.{cog}")
    print(f"{Style.BRIGHT}{Fore.GREEN}[SUCCESS]{Fore.WHITE} Loaded Cog: {cog}")

async def owner(ctx) -> bool:
    """Checks if a user is allowed to run the restart.

    Args:
        ctx (discord.py's context object): Context object.

    Returns:
        bool: Wether the user is one of the bot's owners.
    """

    return ctx.author.id in config.ownerids

@bot.event
async def on_command_error(ctx : commands.Context, error : Exception) -> None:
    """Bot wide error handler.

    Args:
        ctx (commands.Context): Discord's context object.
        error (Exception): The error that was raised.
    """

    if isinstance(error, (commands.CommandNotFound, commands.CheckFailure, commands.BadUnionArgument, commands.BotMissingPermissions)):
        return
    else:
        try:
            embed = discord.Embed(
                title = "Error",
                description = f"**```\n{error}\n```**".replace(config.token, "[ R E D A C T E D ]"),
                color = config.errorcolor
            )
            embed.set_footer(text = "Please report this to Polar#6880")
            await ctx.send(embed = embed)
        finally:
            raise error

@bot.event
async def on_guild_join(guild : discord.Guild) -> None:
    """When the bot joins a server send a webhook with detailed information as well as print out some basic information.


    Args:
        guild (discord.Guild): The guild we joined.discord
    """

    embed = discord.Embed(
        title = "Joined a server!",
        timestamp = datetime.datetime.utcnow(),
        color = 0x77DD77
    )
    embed.add_field(name = "Server Name", value = guild.name)
    embed.add_field(name = "Server Members", value = len(guild.members) - 1)
    embed.add_field(name = "Server ID", value = guild.id)
    embed.add_field(name = "Server Owner ID", value = guild.owner.id)
    embed.set_footer(text = f"I am now in {len(bot.guilds)} servers", icon_url = guild.icon_url)
    owner = bot.get_user(guild.owner_id)
    if owner:
        embed.add_field(name = "Server Owner", value = f"{owner}")
    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(config.webhook, adapter = discord.AsyncWebhookAdapter(session))
        await webhook.send(embed = embed, username = "Joined a server")
    print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}[JOINED-SERVER]{Fore.WHITE} Joined {Fore.YELLOW}{guild.name}{Fore.WHITE} with {Fore.YELLOW}{len(guild.members) - 1}{Fore.WHITE} members.")

@bot.event
async def on_guild_remove(guild : discord.Guild) -> None:
    """When the bot leaves a server send a webhook with detailed information as well as print out some basic information.


    Args:
        guild (discord.Guild): The guild we joined.discord
    """

    embed = discord.Embed(
        title = "Left a server!",
        timestamp = datetime.datetime.utcnow(),
        color = 0xFF6961
    )
    embed.add_field(name = "Server Name", value = guild.name)
    embed.add_field(name = "Server Members", value = len(guild.members))
    embed.add_field(name = "Server ID", value = guild.id)
    embed.add_field(name = "Server Owner ID", value = guild.owner.id)
    embed.set_footer(text = f"I am now in {len(bot.guilds)} servers", icon_url = guild.icon_url)
    owner = bot.get_user(guild.owner_id)
    if owner:
        embed.add_field(name = "Server Owner", value = f"{owner}")
    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(config.webhook, adapter = discord.AsyncWebhookAdapter(session))
        await webhook.send(embed = embed, username = "Left a server")
    print(f"{Style.BRIGHT}{Fore.LIGHTRED_EX}[LEFT-SERVER]{Fore.WHITE} Left {Fore.YELLOW}{guild.name}{Fore.WHITE} with {Fore.YELLOW}{len(guild.members)}{Fore.WHITE} members.")

@bot.event
async def on_shard_ready(shard_id : int) -> None:
    """When a shard starts print out that the shard has started.

    Args:
        shard_id (int): The ID of the shard that has started. (Starts from 0).
    """

    print(f"{Style.BRIGHT}{Fore.CYAN}[SHARD-STARTED]{Fore.WHITE} Shard {Fore.YELLOW}{shard_id}{Fore.WHITE} has started!")

@bot.event
async def on_ready() -> None:
    """When the bot fully starts print out that the bot has started and set the status."""

    print(f"{Style.BRIGHT}{Fore.CYAN}[BOT-STARTED]{Fore.WHITE} I'm currently in {len(bot.guilds)} servers with {len(bot.users)} users!")
    while True:
        await bot.change_presence(status = discord.Status.dnd, activity = discord.Game(f"with {config.prefix}help"))
        await sleep(1800)

# Start the bot.
bot.run(config.token)