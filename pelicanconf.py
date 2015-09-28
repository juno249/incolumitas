#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Nikolai Tschacher'
SITEURL = 'http://localhost:8000'
SITENAME = 'Coding, Learning and IT Security'
SITETITLE = 'Coding, Learning and IT Security'
SITESUBTITLE = ''
SITEDESCRIPTION = 'Nikolai Tschacher\'s ideas and programming around security and computer science'
SITELOGO = 'http://incolumitas.com/uploads/2012/07/IMG_43211.png'

# The same as I used with wordpress to not brake stuff
ARTICLE_URL = '{date:%Y}/{date:%m}/{date:%d}/{slug}/'
# ... while the file is index.html to be auto-served from the dir location
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'

# page urls
PAGE_URL = 'pages/{slug}/'
PAGE_SAVE_AS = 'pages/{slug}/index.html'

PATH = 'content'

TIMEZONE = 'Europe/Berlin'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing

ROBOTS = 'index, follow'
SUMMARY_MAX_LENGTH = 70
SHOW_SUMMARY_ON_INDEX = True

# Social widget
SOCIAL = (('twitter', 'https://twitter.com/incolumitas_'),
          ('github', 'https://github.com/NikolaiT'),
          ('rss', '//incolumitas.com/feeds/all.atom.xml'),
          ('stack-overflow', 'http://stackoverflow.com/users/1052496/nikolai-tschacher'))

DEFAULT_PAGINATION = 5

PIWIK_URL = 'piwik.incolumitas.com/'
PIWIK_SITE_ID = 1

STATIC_PATHS = ['uploads/', 'images/']

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True


THEME = '/home/nikolai/Projects/private/incolumitas/incolumitas/Flex'

MENUITEMS = (('Archives', '/archives.html'),
             ('Categories', '/categories.html'),
             ('Tags', '/tags.html'),)

COPYRIGHT_YEAR = 2015
MAIN_MENU = True
USE_FOLDER_AS_CATEGORY = True
LOAD_CONTENT_CACHE = False

DISQUS_SITENAME = 'incolumitas'

COMMENTS_PAGES = ('about', 'contact')
COMMENTS_IN_PAGES = True