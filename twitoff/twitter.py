from os import getenv
import not_tweepy as tweepy
import spacy
from .models import DB, Tweet, User

# Get API Key from environment vars.
key = getenv('TWITTER_API_KEY')
secret = getenv('TWITTER_API_KEY_SECRET')

# Connect to the Twitter API
TWITTER_AUTH = tweepy.OAuthHandler(key, secret)
TWITTER = tweepy.API(TWITTER_AUTH)

# Load our pretrained SpaCy Word Embeddings model
nlp = spacy.load('my_model/')

# Turn tweet text into word embeddings.
def vectorize_tweets(tweet_text):
    return nlp(tweet_text).vector

def add_or_update_user(username):
    """
    Gets twitter user and tweets from Twitter.
    Gets user by "username" parameter.
    """
    try:
        # gets back Twitter user object
        twitter_user = TWITTER.get_user(screen_name=username)
        
        # Either updates or adds user to our DB
        db_user = User.query.filter_by(username=username).first()
        if db_user is None:
            db_user = User(username=username)
            DB.session.add(db_user)
        
        # Update the newest_tweet_id if needed
        if db_user.newest_tweet_id is None:
            db_user.newest_tweet_id = twitter_user.status.id
        elif db_user.newest_tweet_id < twitter_user.status.id:
            db_user.newest_tweet_id = twitter_user.status.id

        DB.session.commit()

    except Exception as e:
        print(f"Error processing {username}: {e}")
        raise e

def update_all_users():
    """
    Updates all users in the database.
    """
    try:
        users = User.query.all()
        for user in users:
            add_or_update_user(user.username)
    except Exception as e:
        print(f"Error updating users: {e}")
        raise e
