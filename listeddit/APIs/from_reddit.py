import praw


def get_comments(lvl1=True):
    ver = findrev()  # TODO: get rev from README
    if ver is None:
        ver = "???"
    ua = "listeddit v: " + ver + " by /u/StPeteTy, github.com/tyler-england/listeddit/"
    reddit = praw.Reddit("listeddit", user_agent=ua)  # TODO: Trap/prompt auth error
    comments = []
    if lvl1:
    # TODO: Get top level comments from thread
    else:
    # TODO: Get all comments from thread
    return comments  # list of strings


def findrev():
    rev = "???"
    # go to README
    # Find revision
    # return revision
    return rev
