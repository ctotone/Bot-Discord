import discord
from typing import Optional

def create_mock_message(content: str, author_name: str = "TestUser", 
                       channel_name: str = "test-channel") -> discord.Message:
    """Create a mock discord message for testing"""
    mock_message = discord.Message(state=None, channel=None, data={
        "id": "123456789",
        "content": content,
        "author": {
            "id": "987654321",
            "username": author_name,
            "discriminator": "0000"
        },
        "channel_id": "111222333",
        "guild_id": "444555666"
    })
    return mock_message

def verify_command_response(response: Optional[str], expected: str) -> bool:
    """Verify if a command response matches expected output"""
    if response is None:
        return False
    return expected.lower() in response.lower()

def simulate_bot_permissions(guild_id: str, user_id: str, 
                           permissions: discord.Permissions) -> discord.Member:
    """Create a mock member with specific permissions"""
    mock_member = discord.Member(state=None, data={
        "id": user_id,
        "guild_id": guild_id,
        "roles": []
    })
    mock_member._permissions = permissions
    return mock_member
