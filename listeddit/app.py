from listeddit.APIs import reddit, apis
from listeddit.data import data_parse
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


def run(c):  # c is the comment which called the script
    item_type = data_parse.get_type(c)  # song, movie, etc.
    lvl1 = True
    if c.body.lower.find("all") > -1:
        lvl1 = False
    sub = c.submission
    subreddit = c.subreddit
    list_name = data_parse.get_name(sub)
    comments_raw = reddit.get_comments(sub, lvl1)
    item_list = []
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
    url_link = apis.create_list(list_name, item_type, item_list)  # make list/playlist
    if subreddit in no_bot_subs:  # bots aren't allowed to comment
        reddit.send_message(c, True, url_link, r)
    else:
        try:
            reddit.make_comment(c, True, url_link)  # post link to list
        except Exception as e:
            if not url_link == "":  # link was okay --> try different method
                if str(e)[:9] == "RATELIMIT":  # must wait before submitting another comment
                    reddit.send_message(c, True, url_link, r)
    return


ver = findver()  # program revision / version
ua = "listeddit v: " + ver + " by /u/StPeteTy, github.com/tyler-england/listeddit/"
r = praw.Reddit("listeddit", user_agent=ua)  # TODO: Trap/prompt auth error
comment_doc = apis.findfile("comment", "txt")
with open(comment_doc, "r+") as cmt_list:
    done_comments = [line.rstrip() for line in cmt_list]
    cmt_list.truncate(0)
no_bot_subs = ["askreddit"]
try:
    for comment in r.subreddit('all').stream.comments():  # r.subreddit('all').stream.comments():
        if comment.id not in done_comments:
            if bot_called(comment.body):
                print("called: " + comment.body)
                run(comment)
                done_comments.append(comment.id)
                with open(comment_doc, "a+") as cmt_list:
                    cmt_list.write(str(comment.id) + "\n")
except Exception as e:
    quit()  # TODO: restart bot?
