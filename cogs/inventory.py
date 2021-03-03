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
from bson.int64 import Int64
## Packages that have to be installed through the package manager.
import discord
from discord.ext import commands
## Packages on this machine.
import config

class Inventory(commands.Cog):

    def __init__(self, bot : commands.AutoShardedBot) -> None:
        """Whenever the class gets initialized the following function will be executed.

        Args:
            bot (commands.AutoShardedBot): Our bot.
        """
        
        self.bot = bot
    
    async def prefix(self, message : discord.Message) -> str:
        """Get the prefix for a message.

        Args:
            message (discord.Message): The message to get the prefix for.

        Returns:
            str: The prefix that works for the server.
        """

        document = config.prefix.clusters.find_one({"_id": Int64(message.guild.id)})
        if message.guild:
            return config.prefix
        else:
            return document['prefix'] if document else config.prefix

    @commands.command(aliases = ["i", "inv"])
    async def inventory(self, ctx : commands.Context) -> None:
        """View all of the items in your inventory.

        Args:
            ctx (commands.Context): Discord's context object.
        """

        if not ctx.invoked_subcommand:
            if not ctx.guild:
                await ctx.message.delete()
        document = config.cluster.data.users.find_one({"_id": Int64(ctx.author.id)})
        if not document:
            return await ctx.author.send(f"You don't have a computer, please do `{await self.get_prefix(ctx.message)}login` to start your adventure!")
        elif document["online"] == False:
            return await ctx.author.send(f"Your computer is currently offline, please do `{await self.get_prefix(ctx.message)}login` to turn it on!")
        else:
            inventory = []
            index = 0
            for item in document["inventory"]:
                inventory.append(f"**{item['type'].upper()}** - `{item['name']}`\n{item['system']} GHz | {item['cost']} MSRP\nID: `{index}`")
                index += 1
            embed = discord.Embed(
                title = "Inventory",
                description = "\n\n".join(inventory) if inventory != [] else "**You have no items in your inventory!**",
                color = config.maincolor
            )
            await ctx.author.send(embed = embed)

def setup(bot):
    bot.add_cog(Inventory(bot))
