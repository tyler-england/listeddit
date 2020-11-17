import praw

def get_comments(r, url, lvl1=True):
    submission = r.submission(None, url)
    comments=[]
    if lvl1:
        comments = list(submission.comments)
    else:
        comments = submission.comments.list()
    return comments  # list of strings

def make_comment(url_reddit, url_link):
    return
    ver = findrev()  # TODO: get rev from README
    if ver is None:
        ver = "???"
    ua = "listeddit v: " + ver + " by /u/StPeteTy, github.com/tyler-england/listeddit/"
    reddit = praw.Reddit("listeddit", user_agent=ua)  # TODO: Trap/prompt auth error
    if url_reddit.find("?")>=0: #URL for comment
        comment=reddit.comment(None,url_reddit)
        comment.reply(url_link)
    else: #URL for post, not comment
        submission = reddit.submission(None, url_reddit)
        submission.reply(url_link)
    #Todo: reply with link (to post, or [if comment_reply] to comment)
    return