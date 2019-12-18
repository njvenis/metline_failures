import json
import logging
import os
from datetime import date

import emoji
import tweepy

import secrets

logging.basicConfig(filename="botLog.log", filemode="a",
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')


def authenticate():
    # Authentication
    auth = tweepy.OAuthHandler(secrets.CONSUMER_KEY, secrets.CONSUMER_SECRET)
    auth.set_access_token(secrets.ACCESS_TOKEN, secrets.ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    valid = False

    try:
        api.verify_credentials()
        logging.debug("Successful authentication to twitter")
        valid = True

    except Exception as e:
        logging.error("Unable to authenticate, error: %s", str(e))

    if not valid:
        logging.critical("bot exiting, credential failure")
        exit(1)

    scrape(api)


def scrape(api_object):
    delay = False

    timeline = api_object.user_timeline("metline", count="20")

    today = str(date.today())
    matching_tweets = []

    for tweet in timeline:
        for s in {tweet.created_at}:
            if today in str(s):
                matching_tweets.append(tweet)

    for t in matching_tweets:
        for m in {t.text}:
            if "@" in m.lower():
                continue
            if "severe delay" in m.lower():
                delay = True

    save(today, delay, api_object)


def save(today, delay, api_object):
    out_dict = {
        "date": today,
        "daySince": "0"
    }
    days = None

    if not os.path.exists("delaytrack.json"):
        logging.debug("Written new JSON file")
        with open("delaytrack.json", "w") as outfile:
            json.dump(out_dict, outfile)
    else:
        with open("delaytrack.json", "r") as infile:
            data = json.load(infile)
            for key, value in data.items():
                if value == today and key == "date":
                    if delay:
                        days = 0
                    else:
                        days = data["daySince"]
                elif value != today and key == "date":
                    i = int(data["daySince"])
                    days = i + 1
            infile.close()
        out_dict = {
            "date": today,
            "daySince": days
        }
        with open("delaytrack.json", "w") as outfile:
            json.dump(out_dict, outfile)

        send_tweet(days, api_object)


def send_tweet(days, api):
    string = emoji.emojize("It has been " + days + " day(s) since a severe delay on the @metline :warning:")
    api.update_status(string)


if __name__ == '__main__':
    authenticate()
