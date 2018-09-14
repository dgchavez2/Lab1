import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import praw

reddit = praw.Reddit(client_id='FMuuISYIcednXA',
                     client_secret='gbNLmZhK0Ywr4VQyGnaSCLWFAbM',
                     user_agent='StretchTucker'
                     )


nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()
neutral_comment_list = []
negative_comment_list = []
positive_comment_list = []
def get_text_negative_proba(text):
   return sid.polarity_scores(text)['neg']


def get_text_neutral_proba(text):
   return sid.polarity_scores(text)['neu']


def get_text_positive_proba(text):
   return sid.polarity_scores(text)['pos']


def get_submission_comments(url):
    submission = reddit.submission(url=url)
    submission.comments.replace_more()

    return submission.comments
#pos_or_neg tests to see if the comment in question is
    #positive or negative using the neutral index to calculate the odds.
def pos_or_neg(comment, c):
    a = get_text_negative_proba(comment.body)
    b = get_text_positive_proba(comment.body)
    if a-c > b-c:
        positive_comment_list.append(comment.id)
    else:
        negative_comment_list.append(comment.id)

def process_comments(comments):
    for parentcomment in comments.list():
        #if there is no replies, it will begin calculating sentiment
        if len(parentcomment.replies) < 1:
            c = get_text_neutral_proba(parentcomment.body)
    #if the neutrality of a comment is at least 51
    #it is listed as a neutral comment. 
            if c >= 0.51:
                neutral_comment_list.append(parentcomment.id)
            else:
                pos_or_neg(parentcomment, c)
    #here's the recursive call for replies to a comment. 
            for second_level_comment in parentcomment.replies.list():
                process_comments(second_level_comment.replies)


def main():
    comments = get_submission_comments('https://www.reddit.com/r/learnprogramming/comments/5w50g5/eli5_what_is_recursion/')
    print(comments[0].body)
    print(comments[0].replies[0].body)
    process_comments(comments)
    neg = get_text_negative_proba(comments[0].replies[0].body)
    print(negative_comment_list)
    print(20*'-')
    print('negative')
    print(positive_comment_list)
    print(20*'-')
    print('positive')
    print(neutral_comment_list)
    print(20*'-')
    print('neutral')

    print(neg)

main()