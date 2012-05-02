# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'RedditLink.created_at'
        db.delete_column('redditgraph_redditlink', 'created_at')

        # Deleting field 'RedditLink.modified_at'
        db.delete_column('redditgraph_redditlink', 'modified_at')

        # Adding index on 'RedditLink', fields ['link_id']
        db.create_index('redditgraph_redditlink', ['link_id'])

        # Deleting field 'RedditUser.created_at'
        db.delete_column('redditgraph_reddituser', 'created_at')

        # Deleting field 'RedditUser.modified_at'
        db.delete_column('redditgraph_reddituser', 'modified_at')

        # Adding index on 'RedditUser', fields ['username']
        db.create_index('redditgraph_reddituser', ['username'])

        # Deleting field 'RedditVote.created_at'
        db.delete_column('redditgraph_redditvote', 'created_at')

        # Deleting field 'RedditVote.modified_at'
        db.delete_column('redditgraph_redditvote', 'modified_at')


    def backwards(self, orm):
        
        # Removing index on 'RedditUser', fields ['username']
        db.delete_index('redditgraph_reddituser', ['username'])

        # Removing index on 'RedditLink', fields ['link_id']
        db.delete_index('redditgraph_redditlink', ['link_id'])

        # Adding field 'RedditLink.created_at'
        db.add_column('redditgraph_redditlink', 'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2012, 5, 1, 17, 18, 44, 531689), blank=True), keep_default=False)

        # Adding field 'RedditLink.modified_at'
        db.add_column('redditgraph_redditlink', 'modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, default=datetime.datetime(2012, 5, 1, 17, 18, 53, 43822), blank=True), keep_default=False)

        # Adding field 'RedditUser.created_at'
        db.add_column('redditgraph_reddituser', 'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2012, 5, 1, 17, 19, 7, 163403), blank=True), keep_default=False)

        # Adding field 'RedditUser.modified_at'
        db.add_column('redditgraph_reddituser', 'modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, default=datetime.datetime(2012, 5, 1, 17, 19, 12, 915634), blank=True), keep_default=False)

        # Adding field 'RedditVote.created_at'
        db.add_column('redditgraph_redditvote', 'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2012, 5, 1, 17, 19, 21, 715562), blank=True), keep_default=False)

        # Adding field 'RedditVote.modified_at'
        db.add_column('redditgraph_redditvote', 'modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, default=datetime.datetime(2012, 5, 1, 17, 19, 25, 499751), blank=True), keep_default=False)


    models = {
        'redditgraph.redditlink': {
            'Meta': {'object_name': 'RedditLink'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'})
        },
        'redditgraph.reddituser': {
            'Meta': {'object_name': 'RedditUser'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'})
        },
        'redditgraph.redditvote': {
            'Meta': {'object_name': 'RedditVote'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_upvote': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'link': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['redditgraph.RedditLink']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['redditgraph.RedditUser']"})
        }
    }

    complete_apps = ['redditgraph']
