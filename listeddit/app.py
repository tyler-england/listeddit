from listeddit.APIs import reddit
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


def findrev():
    rev = "???"
    try:
        docpath = findfile("readme", ".md")
        if docpath.endswith(".md"):
            with open(docpath) as doc:  # go to README
                linelist = [line.rstrip() for line in doc]
            for line in linelist:
                if line.lower().find("version") > -1:  # Find rev/ver
                    first, *middle, last = line.split()
                    rev = last
    except Exception:
        pass
    return rev  # return revision


def bot_called(ctxt):
    response = False
    if ctxt.lower().find("listplease!") >= 0:
        response = True
    return response


def run(c):  # c is the comment which called the script
    item_type = data_parse.get_type(c)  # song, movie, etc.
    item_type = "songs"
    sub = c.submission
    comments_raw = reddit.get_comments(sub, True)
    print(sub.url)
    print(item_type)
    quit()
    apis = []
    if item_type is "movie":
        item_list = data_parse.get_movies(comments_raw)  # handle comments -> movies
        apis.append("imdb")
    elif item_type is "show":
        item_list = data_parse.get_shows(comments_raw)  # handle comments -> shows
        apis.append("netflix")
        apis.append("hulu")
        apis.append("disney+")
    elif item_type is "game":  # TODO: Figure out if APIs exist for these 
        item_list = data_parse.get_games(comments_raw)  # handle comments -> games
        apis.append("playstation")
        apis.append("xbox")
        apis.append("nintendo")
        apis.append("pc")
    else:
        item_list = data_parse.get_songs(comments_raw)  # handle comments (songs is default mode)
        apis.append("spotify")
    # connect to API(s) --> APIs
    # make list/playlist --> APIs
    url_link = "test url"  # return success message / link
    reddit.make_comment(c, url_link)


ver = findrev()  # program revision / version
ua = "listeddit v: " + ver + " by /u/StPeteTy, github.com/tyler-england/listeddit/"
r = praw.Reddit("listeddit", user_agent=ua)  # TODO: Trap/prompt auth error
comment_doc = findfile("comment", "txt")
with open(comment_doc, "r+") as cmt_list:
    done_comments = [line.rstrip() for line in cmt_list]
    cmt_list.truncate(0)
try:
    for comment in r.subreddit('test').stream.comments():  # r.subreddit('all').stream.comments():
        if comment.id not in done_comments:
            check = comment.body
            print(check)
            if bot_called(check):
                run(comment)
                done_comments.append(comment.id)
                with open(comment_doc, "a+") as cmt_list:
                    print("id: " + comment.id)
                    cmt_list.write(comment.id + "\n")
except Exception:
    print("error!")
    quit()  # TODO: restart bot?
