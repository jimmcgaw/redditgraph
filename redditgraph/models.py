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
        
    def get_recommended_links(self):
        """ 'Users who upvoted links you upvoted also upvoted....' """
        similar_users = self.get_similar_users()
        user_link_ids = [link.id for link in self.get_links()]
        recommended_links = RedditLink.objects.filter(redditvote__user__in=similar_users).exclude(id__in=user_link_ids).distinct()
        return recommended_links
        
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