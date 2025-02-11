import pytest
import discord.ext.test as dpytest
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

@pytest.fixture
def bot():
    """Create a bot instance for testing"""
    load_dotenv('.env.test')
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='!', intents=intents)
    return bot

@pytest.fixture
def test_guild():
    """Create a test guild"""
    return dpytest.backend.make_guild("Test Guild")

@pytest.fixture
def test_channel():
    """Create a test channel"""
    return dpytest.backend.make_text_channel("test-channel")

@pytest.fixture
def test_member():
    """Create a test member"""
    return dpytest.backend.make_member("TestUser")

@pytest.fixture(autouse=True)
def setup_teardown():
    """Setup and teardown for each test"""
    dpytest.configure()
    yield
    dpytest.empty_queue()
