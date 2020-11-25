def get_comments(sub, lvl1=True):  # sub=submission
    if lvl1:
        comments = list(sub.comments)
    else:
        comments = sub.comments.list()
    return comments  # list of strings


def get_response(supported, url_link):
    todo = ["movie", "show", "game"]  # Unfinished, but will be supported
    if url_link.lower().find("/") > -1:
        if url_link.lower()[:7] != "http://":
            url_link = "http://" + url_link
        response = "[Here's the link!](" + url_link + ")"
    elif not supported:
        if url_link == "that":
            response = "Sorry, " + url_link + " listing mode is unsupported :("
        else:
            response = "Sorry, " + url_link + "-listing mode is unsupported :("
    elif url_link == "":
        response = "Sorry, something went wrong :("
    else:
        if url_link in todo:
            response = "Sorry, " + url_link + "-listing mode is still in development :("
        else:
            response = "Sorry, I couldn't find any " + url_link + "s in this post :("
    response = response + "\n\nI am a bot"
    return response


def make_comment(c, supported, url_link):
    response = get_response(supported, url_link)
    response = response + "\n(I am a bot)"
    c.reply(response)
    print("replied!")
    return


def send_message(c, supported, url_link, r):  # requires the reddit instance for messaging
    sub = c.submission
    sub_url = sub.url
    link = get_response(supported, url_link)
    y = link.find(")")
    if y > -1:  # hyperlink provided --> markdown won't work with PRAW
        x = link.find("(") + 1
        link = link[x:y]
    response = "You requested a list of the comments on the following post:\n\n"
    response = response + sub_url + "\n\n"
    response = response + "Please see the output below:\n\n\n"
    response = response + link + "\n\n\n"
    response = response + "Please note: I am a bot. If you received this message, it's because I was prevented " \
                          "from commenting.\n(maybe because there have been too many requests, or the subreddit " \
                          "simply doesn't allow bots)"
    user = c.author
    r.redditor(user.name).message("Your ListPlease results", response)
    print("messaged!")
    return
