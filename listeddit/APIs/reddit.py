def get_comments(sub, lvl1=True):  # sub=submission
    if lvl1:
        comments = list(sub.comments)
    else:
        comments = sub.comments.list()
    return comments  # list of strings


def make_comment(c, supported, url_link):
    todo = ["movie", "show", "game"]  # Unfinished, but will be supported
    if url_link.lower().find("/") > -1:
        response = "Here's the link! " + url_link
    elif not supported:
        if url_link == "that":
            response = "Sorry, " + url_link + " listing mode is unsupported :("
        else:
            response = "Sorry, " + url_link + "-listing mode is unsupported :("
    else:
        print(url_link)
        print(url_link in todo)
        if url_link in todo:
            response = "Sorry, " + url_link + "-listing mode is still in development :("
        else:
            response = "Sorry, I couldn't find any " + url_link + "s in this post :("
    c.reply(response)
    print("replied!")
    return
