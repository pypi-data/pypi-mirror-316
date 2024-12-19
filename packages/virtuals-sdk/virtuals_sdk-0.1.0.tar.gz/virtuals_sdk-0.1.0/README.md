# Virtuals Python API Library


## Documentation
For 

## Installation
```bash
pip install virtuals
```

## Usage
```python
from virtuals.game import Agent

# Create agent with just strings for each component
agent = Agent(
		api_key=VIRTUALS_API_KEY,
    goal="Autonomously analyze crypto markets and provide trading insights",
    description="HODL-9000: A meme-loving trading bot powered by hopium and ramen",
    world_info="Virtual crypto trading environment where 1 DOGE = 1 DOGE"
)

# Simulate one step of the full agentic loop on Twitter/X from the HLP -> LLP -> action
response = agent.simulate_twitter()

# deploy agent! (NOTE: supported for Twitter/X only now)
agent.deploy_twitter()
```