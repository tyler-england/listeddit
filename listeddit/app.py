from listeddit.APIs import reddit, apis
from listeddit.data import data_parse
import praw, os


def findfile(name, ext):
    name = name.lower()
    if ext[:1] is not ".":
        ext = "." + ext
    ext = ext.lower()
    docpath = os.path.dirname(os.getcwd())  # file parent dir
    for file in os.listdir(docpath):
        if file.endswith(ext):
            if file.find(name) >= 0:
                if docpath.find("/") > -1:
                    docpath = docpath + "/" + file
                else:
                    docpath = docpath + "\\" + file
                break
    if docpath.lower().find(name) >= 0 and docpath.lower().endswith(ext):
        return docpath.lower()
    else:
        return


def findver():
    ver = "???"
    try:
        docpath = findfile("readme", ".md")
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
    sub = c.submission
    list_name = data_parse.get_name(sub)
    comments_raw = reddit.get_comments(sub, True)
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
    if item_list == []:
        reddit.make_comment(c, True, item_type)  # failed to find items
        return
    url_link = apis.create_list(list_name, item_type, item_list)  # make list/playlist
    print(url_link)
    reddit.make_comment(c, True, url_link)  # post link to list
    return


ver = findver()  # program revision / version
ua = "listeddit v: " + ver + " by /u/StPeteTy, github.com/tyler-england/listeddit/"
r = praw.Reddit("listeddit", user_agent=ua)  # TODO: Trap/prompt auth error
comment_doc = findfile("comment", "txt")
with open(comment_doc, "r+") as cmt_list:
    done_comments = [line.rstrip() for line in cmt_list]
    cmt_list.truncate(0)
try:
    for comment in r.subreddit('all').stream.comments():  # r.subreddit('all').stream.comments():
        if comment.id not in done_comments:
            if bot_called(comment.body):
                print("called: " + comment.body)
                run(comment)
                done_comments.append(comment.id)
                with open(comment_doc, "a+") as cmt_list:
                    print("id: " + str(comment.id))
                    cmt_list.write(str(comment.id) + "\n")
except Exception as e:
    print("error:" + str(e))
    quit()  # TODO: restart bot?
