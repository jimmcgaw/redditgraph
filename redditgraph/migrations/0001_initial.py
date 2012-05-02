# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'RedditUser'
        db.create_table('redditgraph_reddituser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('redditgraph', ['RedditUser'])

        # Adding model 'RedditLink'
        db.create_table('redditgraph_redditlink', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('link_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('redditgraph', ['RedditLink'])

        # Adding model 'RedditVote'
        db.create_table('redditgraph_redditvote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['redditgraph.RedditUser'])),
            ('link', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['redditgraph.RedditLink'])),
            ('is_upvote', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('redditgraph', ['RedditVote'])


    def backwards(self, orm):
        
        # Deleting model 'RedditUser'
        db.delete_table('redditgraph_reddituser')

        # Deleting model 'RedditLink'
        db.delete_table('redditgraph_redditlink')

        # Deleting model 'RedditVote'
        db.delete_table('redditgraph_redditvote')


    models = {
        'redditgraph.redditlink': {
            'Meta': {'object_name': 'RedditLink'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        'redditgraph.reddituser': {
            'Meta': {'object_name': 'RedditUser'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'redditgraph.redditvote': {
            'Meta': {'object_name': 'RedditVote'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_upvote': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'link': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['redditgraph.RedditLink']"}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['redditgraph.RedditUser']"})
        }
    }

    complete_apps = ['redditgraph']
