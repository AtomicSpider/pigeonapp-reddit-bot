import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)


def summarize(posts):
    message = client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"You are a Subreddit post summary assistant. Here are the top posts of past 24 hours. Please provide a summary. \n\n {posts}",
            }
        ],
        model="claude-3-opus-20240229",
    )
    return str(message.content)
