import pytest
import discord.ext.test as dpytest

class TestBotEvents:
    @pytest.mark.asyncio
    async def test_member_join(self, bot, test_guild):
        """Test member join event"""
        @bot.event
        async def on_member_join(member):
            channel = member.guild.system_channel
            if channel is not None:
                await channel.send(f'Welcome {member.mention}!')

        await dpytest.member_join()
        assert dpytest.verify().message().contains().content("Welcome")

    @pytest.mark.asyncio
    async def test_message_delete(self, bot, test_channel):
        """Test message delete event"""
        @bot.event
        async def on_message_delete(message):
            await message.channel.send(f'Message deleted: {message.content}')

        message = await dpytest.message('Test message')
        await dpytest.delete_message(message)
        assert dpytest.verify().message().contains().content("Message deleted")
