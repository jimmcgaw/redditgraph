from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django import forms  # ModelForm

from tagging.fields import TagField

import datetime, os

class Base(models.Model):
    created_at  = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now=True, auto_now_add=True)

    class Meta:
        abstract = True


class RedditUser(models.Model):
    username = models.CharField(max_length=100, db_index=True)
    
    def get_links(self, upvotes=True):
        """ get links the user has voted on; will be 'Up' votes if upvotes=True (default is True) """
        votes = self.get_votes(upvotes=upvotes)
        links = RedditLink.objects.filter(redditvote__in=votes)
        return links
        
    def get_votes(self, upvotes=True):
        return RedditVote.objects.filter(user=self, is_upvote=upvotes)
        
    def get_similar_users(self):
        """ return list of users who also upvoted with the links this user did """
        links = self.get_links()
        users = []
        for link in links:
            for user in link.get_users():
                if user not in users:
                    users.append(user)
        users = [user for user in users if user != self]
        return users
        
    def get_similar_users_sql(self):
        sql = """ 
        SELECT DISTINCT ru2.username FROM redditgraph_reddituser ru1  
        INNER JOIN redditgraph_redditvote rv1 ON ru1.id = rv1.user_id  
        INNER JOIN redditgraph_redditlink rl1 ON rv1.link_id = rl1.id  
        INNER JOIN redditgraph_redditvote rv2 ON rl1.id = rv2.link_id  
        INNER JOIN redditgraph_reddituser ru2 ON rv2.user_id = ru2.id  
        WHERE rv1.is_upvote = 1 AND rv2.is_upvote = 1 AND ru1.username <> ru2.username AND ru1.username='%s';
        """ % self.username
        
        from django.db import connection, transaction
        cursor = connection.cursor()
        #print sql
        cursor.execute(sql)
        usernames = cursor.fetchall()
        usernames = [username[0] for username in usernames]
        return usernames
        
        
    def get_recommended_links(self):
        """ 'Users who upvoted links you upvoted also upvoted....' """
        similar_users = self.get_similar_users()
        user_link_ids = [link.id for link in self.get_links()]
        recommended_links = RedditLink.objects.filter(redditvote__user__in=similar_users).exclude(id__in=user_link_ids).distinct()
        return recommended_links
        
    def get_recommended_links_sql(self):
        sql = """ 
        SELECT DISTINCT rl2.link_id FROM redditgraph_reddituser ru1  
        INNER JOIN redditgraph_redditvote rv1 ON ru1.id = rv1.user_id  
        INNER JOIN redditgraph_redditlink rl1 ON rv1.link_id = rl1.id  
        INNER JOIN redditgraph_redditvote rv2 ON rl1.id = rv2.link_id  
        INNER JOIN redditgraph_reddituser ru2 ON rv2.user_id = ru2.id  
        INNER JOIN redditgraph_redditvote rv3 ON ru2.id = rv3.user_id
        INNER JOIN redditgraph_redditlink rl2 ON rv3.link_id = rl2.id
        WHERE rv1.is_upvote = 1 AND rv2.is_upvote = 1 AND rv3.is_upvote = 1 AND ru1.username <> ru2.username AND ru1.username='%s' LIMIT 20;
        """ % self.username
        
        from django.db import connection, transaction
        cursor = connection.cursor()
        #print sql
        cursor.execute(sql)
        usernames = cursor.fetchall()
        usernames = [username[0] for username in usernames]
        return usernames
        
    def __unicode__(self):
        return self.username
    
class RedditLink(models.Model):
    link_id = models.CharField(max_length=100, db_index=True)
    
    def get_users(self):
        users = RedditUser.objects.filter(redditvote__link=self)
        return users
    
    def __unicode__(self):
        return self.link_id
    
class RedditVote(models.Model):
    user = models.ForeignKey("redditgraph.RedditUser")
    link = models.ForeignKey("redditgraph.RedditLink")
    is_upvote = models.BooleanField(default=True)
    
    def __unicode__(self):
        direction = u"Up" if self.is_upvote else u"Down"
        return u"Vote %s by %s for %s" % (direction, self.user.username, self.link.link_id)
        
        
class UserEdge(models.Model):
    to_user = models.CharField(max_length=100)
    from_user = models.CharField(max_length=100)
    
        
"""
SELECT ru1.username, rv1.is_upvote, rl1.link_id FROM redditgraph_reddituser ru1 
INNER JOIN redditgraph_redditvote rv1 ON ru1.id = rv1.user_id 
INNER JOIN redditgraph_redditlink rl1 ON rv1.link_id = rl1.id
INNER JOIN redditgraph_redditvote rv2 ON rl1.id = rv2.link_id
INNER JOIN redditgraph_reddituser ru2 ON rv2.user_id = ru2.id LIMIT 10;



SELECT DISTINCT ru2.username FROM redditgraph_reddituser ru1 
INNER JOIN redditgraph_redditvote rv1 ON ru1.id = rv1.user_id 
INNER JOIN redditgraph_redditlink rl1 ON rv1.link_id = rl1.id 
INNER JOIN redditgraph_redditvote rv2 ON rl1.id = rv2.link_id 
INNER JOIN redditgraph_reddituser ru2 ON rv2.user_id = ru2.id 
WHERE rv1.is_upvote = 1 AND rv2.is_upvote = 1 AND ru1.username <> ru2.username AND ru1.username='adoit90';
"""