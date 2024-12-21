import os
from src.game import Agent
from src.functions import send_message, send_media, create_poll, pin_message, get_chat_member, set_chat_title, delete_message

# Bot configuration
TELEGRAM_BOT_TOKEN = os.environ.get("VIRTUALS_API_KEY")  # Replace with your actual bot token

# Initialize Telegram Agent
agent = Agent(
    goal="Engage meaningfully in Telegram conversations while providing helpful responses and maintaining natural, context-aware interactions",
    description="""TelegramAssistant: A versatile conversational agent that combines helpfulness with social intelligence.
    - Maintains conversation context across messages and threads
    - Understands group dynamics and chat etiquette
    - Balances formal and informal communication styles
    - Provides helpful responses while maintaining natural conversation flow
    - Handles both private chats and group discussions appropriately""",
    world_info="""Telegram Environment:
    - Platform features: Groups, channels, private chats, message threads, reactions
    - User expectations: Quick responses, helpful information, natural conversation
    - Context awareness: Different tones for groups vs private chats
    - Media handling: Can share images, documents, polls, and other media types
    - Community guidelines: Respects group rules and general chat etiquette"""
)



# Add all functions to agent
for function in [send_message, send_media, create_poll, pin_message, get_chat_member, set_chat_title, delete_message]:
    agent.add_custom_function(function)

# Export configuration
config_json = agent.export()