from APIs import reddit, apis
from data import data_parse
from datetime import datetime
import praw


def findver():
    ver = "???"
    try:
        docpath = apis.findfile("readme", ".md")
        if docpath.endswith(".md"):
            with open(docpath) as doc:  # go to README
                linelist = [line.rstrip() for line in doc]
            for line in linelist:
                if line.lower().find("version") > -1:  # Find rev/ver
                    first, *middle, last = line.split()
                    ver = last
    except Exception:
        pass
    return ver  # return revision


def bot_called(ctxt):
    response = False
    if ctxt.lower().find("listplease!") >= 0:
        response = True
    return response


def run(c, r):  # c is the comment which called the script
    no_prob_subs = ["music", "stonerrock", "techno"]
    item_type = data_parse.get_type(c)  # song, movie, etc.
    lvl1 = True
    if c.body.lower().find("all") > -1:
        lvl1 = False
    sub = c.submission
    subreddit = c.subreddit
    list_name = data_parse.get_name(sub)
    comments_raw = reddit.get_comments(sub, lvl1)

    if item_type == "song":
        item_list = data_parse.get_songs(comments_raw)  # handle comments (songs is default mode)
    elif item_type == "movie":
        item_list = data_parse.get_movies(comments_raw)  # handle comments -> movies
    elif item_type == "show":
        item_list = data_parse.get_shows(comments_raw)  # handle comments -> shows
    elif item_type == "game":  # TODO: Figure out if APIs exist for these
        item_list = data_parse.get_games(comments_raw)  # handle comments -> games
    else:
        reddit.make_comment(c, False, item_type)  # item type not supported
        return
    if not item_list:
        reddit.make_comment(c, True, item_type)  # failed to find items
        return
    url_link = apis.create_list(list_name, sub.id, item_type, item_list)  # make list/playlist
    if not url_link == "":
        if subreddit in no_prob_subs:  # bots can comment -> no msg necessary
            reddit.make_comment(c, True, url_link)
        else:
            reddit.send_message(c, True, url_link, r)
            reddit.make_comment(c, True, url_link)  # post link to list
    return


def mainfunc():
    try:
        x = 5
        ver = findver()  # program revision / version
        ua = "listeddit v: " + ver + " by /u/StPeteTy, github.com/tyler-england/listeddit/"
        r = praw.Reddit("listeddit", user_agent=ua)  # TODO: Trap/prompt auth error
        comment_doc = apis.findfile("comment", "txt")
        with open(comment_doc, "r+") as cmt_list:
            done_comments = [line.rstrip() for line in cmt_list]
            cmt_list.truncate(0)

        for comment in r.subreddit('all').stream.comments():
            if comment.id not in done_comments:
                if bot_called(comment.body):
                    time = datetime.now().strftime("%-d %b %Y, %H:%M:%S")
                    print(
                        "called: " + time + " -- " + comment.body + " - " + comment.author.name + ", " + comment.permalink)
                    run(comment, r)
                    done_comments.append(comment.id)
                    with open(comment_doc, "a+") as cmt_list:
                        cmt_list.write(str(comment.id) + "\n")
    except Exception as e:
        print("\n" + str(e))
        x = 0
    return x
