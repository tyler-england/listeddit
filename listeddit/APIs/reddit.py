def get_comments(sub, lvl1=True):  # sub=submission
    if lvl1:
        comments = list(sub.comments)
    else:
        comments = sub.comments.list()
    return comments  # list of strings


def make_comment(c, url_link):
    response = "Here's the link! " + url_link
    c.reply(response)
    return
