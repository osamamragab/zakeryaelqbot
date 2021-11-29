import os
import sys
from datetime import date, datetime
import tweepy


API_KEY = os.getenv("TWITTER_API_KEY")
API_KEY_SECRET = os.getenv("TWITTER_API_KEY_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
DEV_MODE = os.getenv("DEV_MODE") == "1"

EXAMS_DATE = date(2022, 6, 11)


def get_api() -> tweepy.API:
    auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    try:
        api.verify_credentials()
    except Exception as e:
        print("auth failed", file=sys.stderr)
        raise e

    return api


def main() -> int:
    bot = get_api()

    if len(sys.argv) > 1:
        if sys.argv[1] == "checkauth":
            print("auth ok")
            return 0
        elif sys.argv[1] == "tweet":
            if len(sys.argv) == 2:
                return 1
            bot.update_status(sys.argv[2])
            return 0
        else:
            print(f"unknown option {sys.argv[1]}", file=sys.stderr)
            return 1

    if not DEV_MODE:
        delta = (EXAMS_DATE - datetime.now().date()).days
        if delta > 0:
            bot.update_status(f"فاضل على الامتحانات {delta} يوم.")
        elif delta == 0:
            bot.update_status("شروق يوم العملية")

    return 0


if __name__ == "__main__":
    tweepy.debug(DEV_MODE, int(DEV_MODE))
    sys.exit(main())
