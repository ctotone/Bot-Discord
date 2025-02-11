import pytest
import discord
from discord.ext import commands
import os

class TestBotConnection:
    @pytest.mark.asyncio
    async def test_bot_token_validity(self):
        """Test that the bot token is valid"""
        intents = discord.Intents.default()
        bot = commands.Bot(command_prefix='!', intents=intents)
        
        try:
            await bot.login(os.getenv('DISCORD_TOKEN'))
            token_valid = True
        except discord.LoginFailure:
            token_valid = False
        finally:
            await bot.close()
        
        assert token_valid, "Bot token is invalid"

    @pytest.mark.asyncio
    async def test_bot_connection_status(self, bot):
        """Test that the bot can connect and shows online status"""
        @bot.event
        async def on_ready():
            assert bot.is_ready()
            assert bot.user is not None
            assert bot.user.status == discord.Status.online

        await bot.start(os.getenv('DISCORD_TOKEN'))
        await asyncio.sleep(2)
        await bot.close()
