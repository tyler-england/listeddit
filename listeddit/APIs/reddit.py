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
        if url_link.lower().find("spotify") > -1:
            response = "As requested, I've created a playlist of the songs in this comment thread." \
                       "\n\n[Here's the link!](" + url_link + ")"
        else:
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
    response = response + "\n\nNote: I am a bot"
    return response


def make_comment(c, supported, url_link):
    response = get_response(supported, url_link)
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
    response = response + "Note: I am a bot. I replied to your comment with this same link, but I'm " \
                          "messaging you as well because some subreddits simply don't allow bot activity."
    user = c.author
    r.redditor(user.name).message("Your ListPlease results", response)
    print("messaged!")
    return
