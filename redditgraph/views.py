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

import simplejson
import random
import networkx as nx
#import matplotlib.pyplot as plt


def index(request, template_name="redditgraph/index.html"):
            
    return render(request, template_name, locals())

def graph_json(request):
    data = build_data()
    #data, graph = get_graph_and_data()
    
    json = simplejson.dumps(data)
    return HttpResponse(json, content_type="application/json")
    
def get_graph_and_data():
    data = {}
    data['nodes'] = []
    data['links'] = []
    
    reddit_users = RedditUser.objects.all()[0:10]
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
        
    return data, graph

def build_graph():
    graph = nx.Graph()
    
    user_edges = UserEdge.objects.all()[0:500]
    usernames = []
    for user_edge in user_edges:
        graph.add_node(user_edge.to_user)
        graph.add_node(user_edge.from_user)
        
    usernames = list(set(usernames))
    [graph.add_node(username) for username in usernames]
    
    nodes = graph.nodes()
    for user_edge in user_edges:
        try:
            to_index = nodes.index(user_edge.to_user)
            from_index = nodes.index(user_edge.from_user)
            graph.add_edge(to_index, from_index)
        except:
            pass
            
    nodes = graph.nodes()
    for node in nodes:
        if not graph.neighbors(node):
            graph.remove_node(node)
    
    return graph
    
def build_data():
    data = {}
    data['nodes'] = []
    data['links'] = []
    graph = build_graph()
    
    for node in graph.nodes():
        node_data = {}
        node_data['name'] = node
        node_data['group'] = 1
        data['nodes'].append(node_data)
        
    for edge in graph.edges():
        print "Loading data for edge with %s & %s " % (edge[0], edge[1])
        link_data = {}
        link_data['source'] = edge[0]
        link_data['target'] = edge[1]
        data['links'].append(link_data)
        
    return data



