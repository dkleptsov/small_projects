from instapy import InstaPy
import os

session = InstaPy(username="you_know_me_right_7", password=os.getenv("PASS")) # YT_MP3_DOWNLOAD_BOT_API_KEY
 # session = InstaPy(username='test', password='test', headless_browser=True)
session.login()

followers = session.grab_followers(username="olgaberek", amount="full", live_match=True, store_locally=True)
print(followers)
##now, `popeye_followers` variable which is a list- holds the `Followers` data of "Popeye" at requested time

# session.set_quota_supervisor(enabled=True, peak_comments_daily=240, peak_comments_hourly=21)
# # session.set_relationship_bounds(enabled=True, max_followers=8500)
# session.like_by_tags(['likelikes', 'likelikeback', 'likelikealways', 'likelikesback',
#                       'likelikers', 'likelikesfromme', 'likeliketeam', 'likelikesbackandfollow',
#                       'likelikebackandfollow', 'likelikebacks', 'likelikesformme', 'likelikey',
#                       'likelikelike', 'likelikee', 'likelikesbackandfollowfollow', 'likelikefromme',
#                       'likelikelike', 'likelikesy', 'likelikefollowforfollow', 'likelikea',
#                       'likeforlike', 'instalike', 'likeforfollow', 'likeforlikes',
#                       'lfl', 'followback', 'followforfollowback', 'likeback'], amount=2)
# session.set_dont_like(["naked", "nsfw"])
# #session.set_do_follow(True, percentage=50)
# session.set_do_comment(True, percentage=100)
# session.set_comments(["Nice!", "Sweet!", "Beautiful :heart_eyes:"])
# session.set_do_story(enabled = True, percentage = 100, simulate = True)
session.end()


# popartmarketing, gurovdigital, irina_brykova, vikavetra, shuvaeva_tani, setters.me, dimmano, bukva.blog, denominant
#+79855082865