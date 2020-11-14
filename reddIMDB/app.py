from reddIMDB.APIs import from_reddit
from reddIMDB.data import data_parse


def run():
    url_reddit = ""  # get link (if not given in terminal?)
    comments_raw = from_reddit.get_comments_lvl1(url_reddit)  # retrieve comments
    movie_list = data_parse.get_movies(comments_raw)  # handle comments
    # connect to IMDB --> APIs
    # make playlist --> APIs
    # for each movie, figure out best & add it --> data?/APIs
    # return success message / link?
