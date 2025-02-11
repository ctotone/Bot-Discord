import pytest
import discord.ext.test as dpytest
from discord.ext import commands
import asyncio

class TestBotCommands:
    @pytest.mark.asyncio
    async def test_help_command(self, bot):
        """Test that the help command works"""
        await dpytest.message('!help')
        assert dpytest.verify().message().contains().content("Here's a list of available commands:")

    @pytest.mark.asyncio
    async def test_ping_command(self, bot):
        """Test the ping command"""
        @bot.command()
        async def ping(ctx):
            await ctx.send('pong')

        await dpytest.message('!ping')
        assert dpytest.verify().message().contains().content("pong")

    @pytest.mark.asyncio
    async def test_invalid_command(self, bot):
        """Test behavior with invalid command"""
        await dpytest.message('!invalidcommand')
        assert dpytest.verify().message().contains().content("Command not found")

    @pytest.mark.asyncio
    async def test_command_permissions(self, bot, test_member):
        """Test command permissions"""
        @bot.command()
        @commands.has_permissions(administrator=True)
        async def admin_only(ctx):
            await ctx.send('admin command executed')

        await dpytest.message('!admin_only')
        assert dpytest.verify().message().contains().content("You don't have permission")
