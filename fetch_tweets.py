import tweepy
import requests
import os
import yaml
import cv2 as cv
from skimage import io
import find_palette


with open("settings.conf", "r") as ymlfile:
    cfg = yaml.full_load(ymlfile)

auth = tweepy.OAuth1UserHandler(cfg["twitter_auth"]["CONSUMER_KEY"], cfg["twitter_auth"]["CONSUMER_SECRET"])
auth.set_access_token(cfg["twitter_auth"]["ACCESS_TOKEN"], cfg["twitter_auth"]["ACCESS_TOKEN_SECRET"])

api = tweepy.API(auth, wait_on_rate_limit=True)

def save_last_response(last_id):
    cfg["stats"]["last_response"] = last_id
    with open("settings.conf", "w") as ymlfile:
        yaml.dump(cfg, ymlfile, default_flow_style=False)

def get_new_reply_mentions():
    new_mentions = []
    last_id = cfg["stats"]["last_response"]
    print("Last ID : " + str(last_id))
    mentions = api.mentions_timeline(count=20, since_id=last_id)
    print("Number of mentions found: " + str(len(mentions)))
    for mention in mentions:
        if mention.in_reply_to_status_id is not None:
            print("Found mention in reply to " + str(mention.in_reply_to_status_id))
            print("Reply ID: " + str(mention.id))
            print("New request by " + str(mention.user.name))
            new_mentions.append(mention)
        else:
            print("Not attached to image")

    return new_mentions


def get_concat_images(tweet):
    images = []
    media = tweet.entities["media"]
    for m in media:
        link = m["media_url"]
        print(link)
        img = io.imread(link)
        images.append(img)

    return cv.vconcat(images)

def tweet_response_with_link(tweet, url):
    id = tweet.id
    username = tweet.user.screen_name
    payload = "@" + username + "\n" + url
    api.update_status(status=payload, in_reply_to_status_id=id)

def tweet_palette(filename, message):
    post_result = api.update_status(status=message, media_ids=[media.media_id])

def run_bot():
    print("Checking for new replies...")
    new = get_new_reply_mentions()

    if(len(new) == 0):
        print("Nothing new, exiting... ")
        return

    for tweet in new:
        try:
            original_tweet = api.get_status(tweet.in_reply_to_status_id) # first get the tweet that it was in reply to.
            concat_image = get_concat_images(original_tweet)
            url = find_palette.url_from_image(concat_image)
            tweet_response_with_link(tweet, url)
            print("Responded to " + str(tweet.id))
            save_last_response(tweet.id)
        except:
            print("Could not generate palette for tweet " + str(tweet.id))

run_bot();
