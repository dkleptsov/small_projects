from instapy import InstaPy
import os

session = InstaPy(username="you_know_me_right_7", password=os.getenv("YT_MP3_DOWNLOAD_BOT_API_KEY"))
# session = InstaPy(username='test', password='test', headless_browser=True)
session.login()
session.set_quota_supervisor(enabled=True, peak_comments_daily=240, peak_comments_hourly=21)
# session.set_relationship_bounds(enabled=True, max_followers=8500)
session.like_by_tags(["bmw", "mercedes"], amount=5)
session.set_dont_like(["naked", "nsfw"])
#session.set_do_follow(True, percentage=50)
session.set_do_comment(True, percentage=100)
session.set_comments(["Nice!", "Sweet!", "Beautiful :heart_eyes:"])
session.end()