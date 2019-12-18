import logging

import tweepy

logging.basicConfig(filename="/var/log/botLog.log", filemode="a",
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')


def authenticate():
    # Authentication
    auth = tweepy.OAuthHandler("")

    auth.set_access_token("")

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
    None
