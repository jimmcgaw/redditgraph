# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'UserEdge'
        db.create_table('redditgraph_useredge', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('to_user', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('from_user', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('redditgraph', ['UserEdge'])


    def backwards(self, orm):
        
        # Deleting model 'UserEdge'
        db.delete_table('redditgraph_useredge')


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
        },
        'redditgraph.useredge': {
            'Meta': {'object_name': 'UserEdge'},
            'from_user': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'to_user': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['redditgraph']
