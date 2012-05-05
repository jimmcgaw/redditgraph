from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import loader, RequestContext
from django.views.decorators.csrf import csrf_exempt

from redditgraph_site.redditgraph.models import *
from redditgraph_site.redditgraph.model_forms import *

from celery.decorators import task
import simplejson
import random
import networkx as nx

def index(request, template_name="redditgraph/index.html"):
            
    return render(request, template_name, locals())

def graph_json(request):
    
    data = {}
    data['nodes'] = []
    data['links'] = []
    
    reddit_users = RedditUser.objects.all()[0:30]
    graph = nx.Graph()
    
    for user in reddit_users:
        graph.add_node(user)
        data['nodes'].append({'name': user.username, 'group': 1 })
        similar_users = user.get_similar_users()[0:5]
        for similar_user in similar_users:
            graph.add_node(similar_user)
            data['nodes'].append({'name': similar_user.username, 'group': 2 })
            graph.add_edge(user, similar_user)
        
    nodes = graph.nodes()
    edges = graph.edges()
    for edge in edges:
        source_index = nodes.index(edge[0])
        target_index = nodes.index(edge[1])
        data['links'].append({'source': source_index, 'target': target_index})
        
    
    
    json = simplejson.dumps(data)
    return HttpResponse(json, content_type="application/json")
    






