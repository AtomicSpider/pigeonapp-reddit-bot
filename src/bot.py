import praw
import summarizer
import os
from datetime import datetime, timedelta
import pytz


FOOTER = """

-------------------------------------------------------------
This post is created by an automated bot from: u/pigeonapp

Please reach out for any greviences/suggestions :)
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


def get_yesterday_ist():
    # Define IST timezone
    ist = pytz.timezone("Asia/Kolkata")

    # Get current time in UTC and convert to IST
    now_utc = datetime.now(pytz.utc)
    now_ist = now_utc.astimezone(ist)

    # Calculate yesterday's date
    yesterday_ist = now_ist - timedelta(days=1)
    return yesterday_ist.strftime("%Y-%m-%d")


def main():
    # Initialize Reddit instance
    reddit = praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        username=os.environ["REDDIT_USERNAME"],
        password=os.environ["REDDIT_PASSWORD"],
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
        _post = reddit.subreddit(subreddit_name).submit(
            title=f"[Daily Digest] {get_yesterday_ist()}: Top Posts from {subreddit_name}",
            selftext=post_selftext,
        )

        print(f"Submitted to {_post.permalink}")


if __name__ == "__main__":
    main()
