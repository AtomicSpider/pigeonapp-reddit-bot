import praw
import summarizer
import os


FOOTER = """

-------------------------------------------------------------
This is an automated bot created by u/pigeonapp
Please reach out for any greviences/suggestions :)
-------------------------------------------------------------
"""


def fetch_posts(reddit, subreddit_name):
    combined_text = ""
    subreddit = reddit.subreddit(subreddit_name)

    for post in subreddit.top(time_filter="day", limit=100):
        if post.is_self:
            combined_text += (
                f"Title: {post.title}\n\n{post.selftext}\n\nURL: {post.url}\n\n---\n\n"
            )

    return combined_text


def main():
    # Initialize Reddit instance
    reddit = praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        user_agent="pigeonapp-bot by /u/pigeonapp",
    )

    subreddits = ["BollyBlindsNGossip"]

    for subreddit_name in subreddits:

        # Fetch posts and save to file
        posts = fetch_posts(reddit, subreddit_name)

        # Summarize the combined text file
        summary = summarizer.summarize(posts)

        post_selftext = f"{summary}{FOOTER}"

        print(post_selftext)
        # Post the summary to the subreddit
        # reddit.subreddit(subreddit_name).submit(
        #     title=f"Summary of top posts from the last 24 hours in {subreddit_name}",
        #     selftext=summary,
        # )


if __name__ == "__main__":
    main()
