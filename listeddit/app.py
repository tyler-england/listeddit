from listeddit.APIs import reddit
from listeddit.data import data_parse
import praw, os


def findrev():
    rev = "???"
    try:
        docpath = os.path.dirname(os.getcwd())  # README parent
        for file in os.listdir(docpath):
            if file.endswith(".md"):
                print(file)
                if file.find("README"):
                    if docpath.find("/") > -1:
                        docpath = docpath + "/" + file
                    else:
                        docpath = docpath + "\\" + file
                    break
        print(docpath)
        if docpath.endswith(".md"):
            with open(docpath) as doc:  # go to README
                linelist = [line.rstrip() for line in doc]
            for line in linelist:
                if line.lower().find("version") > -1:  # Find rev/ver
                    first, *middle, last = line.split()
                    rev = last
    except Exception: pass
    return rev  # return revision


ver = findrev()
if ver is None:
    ver = "???"
ua = "listeddit v: " + ver + " by /u/StPeteTy, github.com/tyler-england/listeddit/"
r = praw.Reddit("listeddit", user_agent=ua)  # TODO: Trap/prompt auth error
print(ua)


def run(c):  # c is the comment which called the script
    qtype = "songs"  # data_parse.get_type(c)
    qtype = qtype.lower()
    url_reddit = "reddit.com" + c.permalink  # get link (if not given in terminal?)
    print(url_reddit)
    quit()
    comments_raw = reddit.get_comments(url_reddit, True)  # retrieve comments
    apis = []
    if qtype is "song":
        item_list = data_parse.get_songs(comments_raw)  # handle comments
        apis.append("spotify")
    elif qtype is "movie":
        item_list = data_parse.get_movies(comments_raw)  # handle comments
        apis.append("imdb")
    # connect to API(s) --> APIs
    # make list/playlist --> APIs
    # for each item, figure out best & add it --> data?/APIs
    url_link = ""  # return success message / link
    reddit.make_comment(url_reddit, url_link)


def bot_called(c):
    response = False
    if c.body.lower().find("listplease!") >= 0:
        response = True
    return response


test_c = [r.comment(None,
                    "https://www.reddit.com/r/AskReddit/comments/julars/who_still_plans_on_having_holidays_with_family/gcduwiz")]
for c in test_c:  # praw.helpers.comment_stream(r, 'all'):
    run(c)
    # if bot_called(c):
    #     run(c)
