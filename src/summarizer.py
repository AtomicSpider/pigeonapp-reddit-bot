import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)

ASSISTANT_DIRECTIVE = """
You are a Subreddit summary assistant. You will be provided with the top posts of a subreddit. Please create a summary of the collective posts and also append relevant post urls at the end.
Your response should always be like this:

Summary:
<Summary in bullet points> 

Refrences: 
<Post URLs>
"""


def summarize(posts):
    message = client.messages.create(
        max_tokens=1024,
        system=ASSISTANT_DIRECTIVE,
        messages=[
            {
                "role": "user",
                "content": posts,
            },
            {"role": "assistant", "content": "Summary:"},
        ],
        model="claude-instant-1.2",
    )
    return message.content[0].text
