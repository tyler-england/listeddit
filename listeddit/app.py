from listeddit.APIs import reddit
from listeddit.data import data_parse


def run():
    qtype = "song"
    qtype = qtype.lower()
    url_reddit = "https://www.reddit.com/r/AskReddit/comments/julars/who_still_plans_on_having_holidays_with_family/"  # get link (if not given in terminal?)
    comments_raw = reddit.get_comments(url_reddit, False)  # retrieve comments
    apis = []
    if qtype is "song":
        item_list = data_parse.get_songs(comments_raw)  # handle comments
        apis.append("spotify")
    elif qtype is "movie":
        item_list = data_parse.get_movies(comments_raw)  # handle comments
        apis.append("imdb")
    # connect to API(s) --> APIs
    # make list/playlist --> APIs
    # for each item, figure out best & add it --> data?/APIs
    url_link = ""  # return success message / link
    reddit.make_comment(url_reddit, url_link)
