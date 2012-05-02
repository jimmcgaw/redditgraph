#!/usr/bin/python
from redditgraph.models import *

import csv

csv_file_path = "/Users/smoochy/aptana/redditgraph_site/publicvotes.csv"

def run_import():
    f = open(csv_file_path)

    csv_reader = csv.reader(f)

    for row in csv_reader:
        username = row[0]
        link_id = row[1]
        vote_direction = row[2]
        vote_int = int(vote_direction)
        is_upvote = vote_int > 0

        reddit_user, created = RedditUser.objects.get_or_create(username=username)
        if created:
            print "Saved reddituser %s" % username

        reddit_link, created = RedditLink.objects.get_or_create(link_id=link_id)
        if created:
            print "Saved redditlink %s" % link_id

        reddit_vote, created = RedditVote.objects.get_or_create(link=reddit_link, user=reddit_user, is_upvote=is_upvote)
        if created:
            print "Saved reddit_vote"

    f.close()
    