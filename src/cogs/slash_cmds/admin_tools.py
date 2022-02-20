import asyncio

import discord
from discord.ext import commands

from cogs.useful_decoration import only_admin_debug
from src.cogs.better_response import response


class DebugTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def debug(self, ctx):
        """ debug cmd group """
        if ctx.invoked_subcommand is None:
            # command response
            title = "Wrong argument"
            asyncio.create_task(response(ctx, title))

    @debug.group()
    async def doro(self, ctx):
        """ doro cmd group """
        if ctx.invoked_subcommand is None:
            # command response
            title = "Wrong argument"
            asyncio.create_task(response(ctx, title))

    @doro.command()
    @only_admin_debug
    async def running_sessions(self, ctx):
        msg = discord.Embed(title="Run Information")
        active_sessions = 0
        active_members = 0
        for dojo in self.bot.dojos.values():
            for session in dojo.sessions.values():
                active_members += session.member_count
                if session.timer.is_active:
                    active_sessions += 1

        msg.description = f"""
            Active sessions: {active_sessions}
            Active members : {active_members} 
        """
        await ctx.send(embed=msg)

    @debug.group()
    async def delete(self, ctx):
        """ delete cmd group """
        if ctx.invoked_subcommand is None:
            # command response
            title = "Wrong argument"
            asyncio.create_task(response(ctx, title))

    @delete.command()
    async def envs(self, ctx):
        """ Removes all environments from the bot. """
        # cmd only for me
        if ctx.author.id == 302:
            title = "Okay sir I'll clean your room!"
            asyncio.create_task(response(ctx, title))
            # get dojo reference
            for category in ctx.guild.categories:
                if "🍅" in category.name:
                    # delete all channels inside category
                    for vc in category.voice_channels:
                        await vc.delete()
                    for tc in category.text_channels:
                        await tc.delete()
                    # delete category
                    await category.delete()

    @delete.command()
    async def messages(self, ctx):
        """ Removes all messages from the channel. """
        # cmd only for me
        if ctx.author.id == 302:
            # delete all messages inside message.channel
            async for msg in ctx.channel.history():
                asyncio.create_task(msg.delete())
            # command response
            title = "Okay sir I'll delete your messages!"
            asyncio.create_task(response(ctx, title))

    @delete.command()
    async def sessions(self, ctx):
        """ Removes all Session environments from the bot. """
        # cmd only for me
        if ctx.author.id == 302:
            # command response
            title = "Okay sir I'll delete your sessions!"
            asyncio.create_task(response(ctx, title))
            # get dojo reference
            dojo = self.bot.dojos[ctx.guild.id]
            # delete all sessions in ctx.guild
            for session in dojo.sessions.values():
                asyncio.create_task(session.dispose())
