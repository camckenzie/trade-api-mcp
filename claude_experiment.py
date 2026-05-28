from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()

trade_data = [
    {"symbol": "AAPL", "price": 189.50, "timestamp": "2025-05-10T09:30:00"},
    {"symbol": "MSFT", "price": 415.20, "timestamp": "2025-05-10T09:30:01"},
    {"symbol": "TSLA", "price": 177.38, "timestamp": "2025-05-10T09:30:03"},
]

# System prompt gives Claude its role and context
system_prompt = f"""You are a trading assistant with access to the following trade data:

{trade_data}

Answer questions about this data clearly and concisely. 
If asked about a symbol not in the data, say so."""

# Conversation history
# Utilizes multi-turn
conversation = []

print("Trading Assistant ready. Type 'quit' to exit.\n")

while True:
    user_input = input("You: ")
    
    if user_input.lower() == "quit":
        break
    
    # Add user message to history
    conversation.append({
        "role": "user",
        "content": user_input
    })
    
    # Call Claude with the full conversation history
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=system_prompt,
        messages=conversation
    )
    
    assistant_message = response.content[0].text
    
    # Add Claude's response to history so it remembers the conversation
    conversation.append({
        "role": "assistant", 
        "content": assistant_message
    })
    
    print(f"\nClaude: {assistant_message}\n")