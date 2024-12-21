from virtuals_sdk.game import Agent
from virtuals_sdk.functions.telegram import TelegramClient

# Create agent with just strings for each component
agent = Agent(
	api_key="985f75776b45337f0a9c2c11ddf7bd795950ee13b4e5074af604762f449114bd",
    goal="Autonomously analyze crypto markets and provide trading insights",
    description="HODL-9000: A meme-loving trading bot powered by hopium and ramen",
    world_info="Virtual crypto trading environment where 1 DOGE = 1 DOGE"
)

# list available functions that can be added to agent
# print(agent.list_available_default_twitter_functions()) 
# agent.list_available_default_twitter_functions()
# agent.use_default_twitter_functions(["wait", "reply_tweet"])

print("here")
# response = agent.simulate_twitter(session_id="session-twitter")
# print(response)

# get telegram custom functions through client
tg_client = TelegramClient(bot_token="7210003118:AAGDgu4PgMJEwY892B_U0wyfZ0xCm-sMOGk")

print(tg_client.available_functions)

reply_message_fn = tg_client.get_function("send_message")
create_poll_fn = tg_client.get_function("create_poll")
# set_chat_title_fn = tg_client.get_function("set_chat_title")
pin_message_fn = tg_client.get_function("pin_message")

reply_message_fn("5394289251", "Hello World")
create_poll_fn("5394289251", "What is your favorite color?", ["Red", "Blue", "Green"], "True")
pin_message_fn("5394289251", "82", "True")
# set_chat_title_fn("5394289251", "New Chat Title")
