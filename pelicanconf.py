#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'lumy'
#SITENAME = 'Lumy\'s blog'

SITEURL = '' # http://blog.lumy.me'
PATH='content'

LOAD_CONTENT_CACHE = False
CACHE_CONTENT = False

CATEGORY_URL = '{slug}/'
CATEGORY_SAVE_AS = '{slug}/index.html'

ARTICLE_URL = '{category}/{slug}/'
ARTICLE_SAVE_AS = '{category}/{slug}/index.html'


TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'en'

# Other themes
# plumage
# pelican-themes -l
THEME = "pelican-themes/brownstone"

PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = [
    "jinja2content",
    "i18n_subsites"
]
I18N_SUBSITES = {
    'en': {
        'SITENAME': 'Lumy\'s blog',
        'THEME_STATIC_PATHS': ["themes/",]
    },
    'fr': {
        'SITENAME': 'Journal de Lumy',
        'THEME_STATIC_PATHS': ["themes/",]
    }
}

JINJA2CONTENT_TEMPLATES="content"

# Whether to display pages on the menu of the template. Templates may or may not honor this setting.
DISPLAY_PAGES_ON_MENU = True

# Whether to display categories on the menu of the template.
DISPLAY_CATEGORIES_ON_MENU = True

# DEFAULT_METADATA = {
#   'description': 'A brief description of your site',
#   'status': 'draft'
# }

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
TYPOGRIFY = True
# Blogroll
LINKS = (('www.lumy.me', 'http://www.lumy.me/'),
         ('cv.lumy.me', 'http://cv.lumy.me/'),
         ('github', 'https://github.com/lumy'),
         ('Music', ''),
)

# Social widget
SOCIAL = (
    ('Twitter', 'https://twitter.com/Lumy4242'),
)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = False

DELETE_OUTPUT_DIRECTORY = True

def extract_trans(article, lang, url):
    for trans in article.translations:
        if trans.lang == lang:
            return trans.url
        return url

JINJA_FILTERS = {'extract_trans': extract_trans}
