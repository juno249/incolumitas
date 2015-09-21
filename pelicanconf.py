#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Nikolai Tschacher'
SITEUR = 'http://localhost:8000'
SITENAME = 'Coding, Learning and IT Security'
SITETITLE = 'Coding, Learning and IT Security'
SITESUBTITLE = ''
SITEDESCRIPTION = 'Nikolai Tschacher\'s ideas and programming around security and computer science'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/Berlin'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

ROBOTS = 'index, follow'
SUMMARY_MAX_LENGTH = 50

# Social widget
SOCIAL = (('twitter', 'https://twitter.com/incolumitas_'),
          ('github', 'https://github.com/NikolaiT'),
          ('rss', '//incolumitas/feeds/all.atom.xml'),
          ('stack-overflow', 'http://stackoverflow.com/users/1052496/nikolai-tschacher'))

DEFAULT_PAGINATION = 5

PIWIK_URL = 'piwik.incolumitas.com/'
PIWIK_SITE_ID = 1

STATIC_PATHS = ['uploads/']

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True


THEME = '/home/nikolai/Projects/private/incolumitas/pelican-themes/Flex'

MENUITEMS = (('Archives', '/archives.html'),
             ('Categories', '/categories.html'),
             ('Tags', '/tags.html'),)

COPYRIGHT_YEAR = 2015
MAIN_MENU = True
USE_FOLDER_AS_CATEGORY = True
LOAD_CONTENT_CACHE = False
