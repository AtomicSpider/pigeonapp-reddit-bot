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
                "content": f"You are a Subreddit summary assistant. You will be provided with the top posts of subreddit. Please create a summary of the collective posts and also attach relevant post urls along with the summary at the end. Your response should be like this: <Summary> \n\n Links: <Post URLs> \n\n Posts: \n\n {posts}",
            }
        ],
        model="claude-instant-1.2",
    )
    return message.content[0].text
