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
## Packages that have to be installed through the package manager.
import discord
from discord.ext import commands
## Packages on this machine.
import config

class Utils(commands.Cog):

    def __init__(self, bot : commands.AutoShardedBot) -> None:
        """Whenever the class gets initialized the following function will be executed.

        Args:
            bot (commands.AutoShardedBot): Our bot.
        """
        
        self.bot = bot

    @commands.command()
    async def invite(self, ctx : commands.Context) -> None:
        f"""Get the link to invite WumpusHack to your server.

        Args:
            ctx (commands.Context): Discord's context object.
        """

        embed = discord.Embed(
            title = "**Invite Me! 🔗**",
            url = f"https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot",
            color = config.maincolor
        )
        await ctx.send(embed = embed)

    @commands.command()
    async def support(self, ctx : commands.Context) -> None:
        """Get the link to the WumpusHack support server.

        Args:
            ctx (commands.Context): Discord's context object.
        """
        
        embed = discord.Embed(
            title = "**Support Server! 🔗**",
            url = "https://discord.gg/GC7Pw9Y",
            color = config.maincolor
        )
        await ctx.send(embed = embed)
    
    @commands.command(aliases = ["source", "sourcecode", "oss"])
    async def github(self, ctx : commands.Context) -> None:
        """Get the link to the WumpusHack GitHub

        Args:
            ctx (commands.Context): Discord's context object.
        """

        embed = discord.Embed(
            title = "**GitHub Repository! 🔗**",
            url = "https://GitHub.com/xPolar/WumpusHack",
            color = config.maincolor
        )
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Utils(bot))
