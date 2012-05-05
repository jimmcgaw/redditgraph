import os, site, sys

# From http://jmoiron.net/blog/deploying-django-mod-wsgi-virtualenv/

vepath = '/home/smoochy/redditgraph_site/lib/python2.7/site-packages'

prev_sys_path = list(sys.path)

site.addsitedir(vepath)

wsgi_dir = os.path.abspath(os.path.dirname(__file__))
project_dir = os.path.dirname(wsgi_dir)
sys.path.append(project_dir)
parent_dir = os.path.dirname(project_dir)
sys.path.append(parent_dir)

# reorder sys.path so new directories from the addsitedir show up first
new_sys_path = [p for p in sys.path if p not in prev_sys_path]
for item in new_sys_path:
    sys.path.remove(item)
sys.path[:0] = new_sys_path

from django.core.handlers.wsgi import WSGIHandler
os.environ['DJANGO_SETTINGS_MODULE'] = 'redditgraph_site.settings'
application = WSGIHandler()
