import requests
import json
from typing import Optional, List, Dict
import time
import os

# Replace with your bot token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Will be populated by get_chat_id()
TEST_CHAT_ID: Optional[str] = None

def create_url(endpoint):
    """Create full API URL with token"""
    return f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/{endpoint}"

def delete_webhook() -> Dict:
    """
    Delete the active webhook if one exists.
    Returns:
        Dict containing the response from Telegram
    """
    url = create_url("deleteWebhook")
    response = requests.get(url)
    result = response.json()
    if result.get("ok"):
        print("Successfully deleted webhook")
    else:
        print(f"Error deleting webhook: {result.get('description')}")
    return result

def get_webhook_info() -> Dict:
    """
    Get information about the current webhook status.
    Returns:
        Dict containing webhook information
    """
    url = create_url("getWebhookInfo")
    response = requests.get(url)
    result = response.json()
    if result.get("ok"):
        webhook_info = result.get("result", {})
        if webhook_info.get("url"):
            print(f"Current webhook URL: {webhook_info['url']}")
        else:
            print("No webhook currently set")
    else:
        print(f"Error getting webhook info: {result.get('description')}")
    return result


def get_updates(offset: Optional[int] = None) -> Dict:
    """
    Get updates (new messages) from Telegram
    Args:
        offset: Optional ID of last update received
    """
    url = create_url("getUpdates")
    params = {
        "timeout": 30,
        "allowed_updates": json.dumps(["message", "channel_post"])
    }
    if offset:
        params["offset"] = offset
    response = requests.get(url, params=params)
    return response.json()

def get_chat_id(timeout: int = 30) -> Optional[str]:
    """
    Get chat ID by waiting for a new message.
    
    Instructions will be printed for the user to send a message to the bot.
    The function will wait up to timeout seconds for a message.
    
    Args:
        timeout: How many seconds to wait for a message
    
    Returns:
        Chat ID if found, None otherwise
    """
    print(f"\nTo get your chat ID:")
    print(f"1. Start a chat with your bot")
    print(f"2. Send any message to the bot")
    print(f"Waiting {timeout} seconds for a message...")
    
    start_time = time.time()
    last_update_id = None
    
    while time.time() - start_time < timeout:
        updates = get_updates(last_update_id)
        if updates.get("ok") and updates["result"]:
            for update in updates["result"]:
                if "message" in update:
                    chat_id = str(update["message"]["chat"]["id"])
                    user_data = update["message"]["from"]
                    from_user = user_data.get("username") or user_data.get("first_name") or user_data.get("id", "Unknown")
                    print(f"\nFound chat ID: {chat_id} from user: {from_user}")
                    return chat_id
                elif "channel_post" in update:
                    chat_id = str(update["channel_post"]["chat"]["id"])
                    chat_title = update["channel_post"]["chat"].get("title", "Unknown channel")
                    print(f"\nFound channel ID: {chat_id} from channel: {chat_title}")
                    return chat_id
            
            # Update the offset to avoid getting the same updates again
            last_update_id = updates["result"][-1]["update_id"] + 1
        
        time.sleep(1)  # Avoid hammering the API
    
    print("\nNo new messages received. Please try again.")
    return None

# Check and handle webhook before attempting to get updates
def setup_for_getting_updates():
    """
    Prepare the bot for getting updates by checking and removing any webhook
    """
    print("\nChecking webhook status...")
    webhook_info = get_webhook_info()
    if webhook_info.get("ok") and webhook_info["result"].get("url"):
        print("Found active webhook, deleting...")
        delete_webhook()
    else:
        print("No active webhook found")

# Try to get chat ID if not manually set
if TEST_CHAT_ID is None:
    print("\nNo TEST_CHAT_ID set. Attempting to get it automatically...")
    setup_for_getting_updates()


def test_send_message(chat_id=TEST_CHAT_ID, text="Test message"):
    """
    Test sending a simple message
    Basic usage: test_send_message(chat_id="123456", text="Hello world")
    """
    url = create_url("sendMessage")
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    response = requests.post(url, json=payload)
    print(f"Send Message Response: {json.dumps(response.json(), indent=2)}")
    return response.json()

def test_send_media(chat_id=TEST_CHAT_ID, media_url="https://example.com/image.jpg", media_type="photo", caption="Test media"):
    """
    Test sending media (photo/document/video/audio)
    Basic usage: test_send_media(chat_id="123456", media_url="https://example.com/image.jpg", media_type="photo")
    """
    url = create_url(f"send{media_type.capitalize()}")
    payload = {
        "chat_id": chat_id,
        media_type: media_url,
        "caption": caption
    }
    response = requests.post(url, json=payload)
    print(f"Send Media Response: {json.dumps(response.json(), indent=2)}")
    return response.json()

def test_create_poll(chat_id=TEST_CHAT_ID, question="Test poll?", options=["Option 1", "Option 2"]):
    """
    Test creating a poll
    Basic usage: test_create_poll(chat_id="123456", question="Favorite color?", options=["Red", "Blue", "Green"])
    """
    url = create_url("sendPoll")
    payload = {
        "chat_id": chat_id,
        "question": question,
        "options": json.dumps(options),
        "is_anonymous": True
    }
    response = requests.post(url, json=payload)
    print(f"Create Poll Response: {json.dumps(response.json(), indent=2)}")
    return response.json()

def test_pin_message(chat_id=TEST_CHAT_ID, message_id=""):
    """
    Test pinning a message
    Basic usage: test_pin_message(chat_id="123456", message_id="789")
    Note: message_id can be obtained from the response of test_send_message
    """
    url = create_url("pinChatMessage")
    payload = {
        "chat_id": chat_id,
        "message_id": message_id
    }
    response = requests.post(url, json=payload)
    print(f"Pin Message Response: {json.dumps(response.json(), indent=2)}")
    return response.json()

def test_get_chat_member(chat_id=TEST_CHAT_ID, user_id=""):
    """
    Test getting chat member info
    Basic usage: test_get_chat_member(chat_id="123456", user_id="789")
    """
    url = create_url("getChatMember")
    payload = {
        "chat_id": chat_id,
        "user_id": user_id
    }
    response = requests.get(url, params=payload)
    print(f"Get Chat Member Response: {json.dumps(response.json(), indent=2)}")
    return response.json()

def test_delete_message(chat_id=TEST_CHAT_ID, message_id=""):
    """
    Test deleting a message
    Basic usage: test_delete_message(chat_id="123456", message_id="789")
    Note: message_id can be obtained from the response of test_send_message
    """
    url = create_url("deleteMessage")
    payload = {
        "chat_id": chat_id,
        "message_id": message_id
    }
    response = requests.post(url, json=payload)
    print(f"Delete Message Response: {json.dumps(response.json(), indent=2)}")
    return response.json()

def test_get_chat_history(chat_id=TEST_CHAT_ID, limit=50):
    """
    Test retrieving chat history
    Basic usage: test_get_chat_history(chat_id="123456", limit=50)
    """
    url = create_url("getUpdates")
    payload = {
        "offset": -100,  # Get recent messages
        "limit": limit,
        "allowed_updates": ["message"]
    }
    
    response = requests.get(url, params=payload)
    result = response.json()
    
    if result.get("ok"):
        messages = [update["message"] for update in result.get("result", []) 
                   if "message" in update and str(update["message"]["chat"]["id"]) == str(chat_id)]
        print(f"Retrieved {len(messages)} messages from chat")
        for msg in messages[:20]:  # Show first 3 messages as preview
            sender = msg.get("from", {}).get("first_name", "Unknown")
            text = msg.get("text", "[non-text message]")
            print(f"- {sender}: {text[:50]}...")
    else:
        print(f"Failed to get chat history: {result.get('description')}")
    return result

def test_get_message_context(chat_id=TEST_CHAT_ID):
    """
    Test getting message context
    Basic usage: test_get_message_context(chat_id="123456", message_id="789")
    """
    url = create_url("getChat")
    payload = {
        "chat_id": chat_id
    }
    response = requests.get(url, params=payload)
    result = response.json()
    
    if result.get("ok"):
        chat_info = result["result"]
        print(f"Chat type: {chat_info.get('type')}")
        print(f"Chat title: {chat_info.get('title', 'Private chat')}")
        print(chat_info)
        print(result)
    else:
        print(f"Failed to get message context: {result.get('description')}")
    
    return result


# Example usage and testing sequence
if __name__ == "__main__":
    # Try to get chat ID if not set
    if TEST_CHAT_ID is None:
        TEST_CHAT_ID = get_chat_id(timeout=30)
        if TEST_CHAT_ID is None:
            print("Could not get chat ID. Please either:")
            print("1. Run the script again and send a message to your bot within 30 seconds, or")
            print("2. Set TEST_CHAT_ID manually at the top of the script")
            exit(1)
    
    CHAT_ID = TEST_CHAT_ID
    USER_ID = "TEST_USER_ID"  # For testing get_chat_member
    
    # Test 1: Send a message
    print("\n=== Testing Send Message ===")
    message_response = test_send_message(
        chat_id=CHAT_ID,
        text="Hello! This is a test message."
    )
    
    if "result" in message_response:
        message_id = message_response["result"]["message_id"]
        
        # Test 2: Pin the message we just sent
        print("\n=== Testing Pin Message ===")
        test_pin_message(
            chat_id=CHAT_ID,
            message_id=str(message_id)
        )
        
        # Test 3: Delete the message
        # print("\n=== Testing Delete Message ===")
        # test_delete_message(
        #     chat_id=CHAT_ID,
        #     message_id=str(message_id)
        # )
    
    # Test 4: Create a poll
    print("\n=== Testing Create Poll ===")
    test_create_poll(
        chat_id=CHAT_ID,
        question="How's this test poll?",
        options=["Great!", "Works fine", "Needs improvement"]
    )
    
    # Test 5: Send media
    print("\n=== Testing Send Media ===")
    test_send_media(
        chat_id=CHAT_ID,
        media_url="https://pbs.twimg.com/media/GOQRcbhbIAAofos.jpg",
        media_type="photo",
        caption="Test image"
    )

    # Test 5: Get chat history
    print("\n=== Testing Get Chat History ===")
    test_get_chat_history(chat_id=CHAT_ID)

    # Test 6: Get message context
    if "result" in message_response and "message_id" in message_response["result"]:
        print("\n=== Testing Get Message Context ===")
        test_get_message_context(
            chat_id=CHAT_ID
        )

    # # Test 6: Get chat member info
    # print("\n=== Testing Get Chat Member ===")
    # test_get_chat_member(
    #     chat_id=CHAT_ID,
    #     user_id=USER_ID
    # )

