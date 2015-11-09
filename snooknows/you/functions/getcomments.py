import praw
import json
import codecs
import re

USER_AGENT = "PSOSM Script by u/shubham03"

def extractComments(userName):
    print "Fetching comments from Reddit for username : " + userName
    r = praw.Reddit(user_agent=USER_AGENT)
    user = r.get_redditor(userName)

    ### Set limit = None to get all the comments
    comments = user.get_comments(limit=100, sort="top")
    commentsDict = {}
    for thing in comments:
        if thing.body:
            body = thing.body.replace('\n','')+'\n'
            try:
                body = body.replace(re.search("(?P<url>https?://[^\s]+)", body).group("url"),"")
            except AttributeError:
                print "..............."
        commentsDict[thing] = body
    # pprint(commentsDict)
    print "Fetched comments from Reddit"
    return commentsDict

if __name__ == '__main__':
	extractComments('maxwellhill')

