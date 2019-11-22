#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'lumy'

# BLOG_AUTHORS = {
#   'Lumy': {
#     'description':"""A little mor about me""",
#     'short_description': """short version""",
#     'image': "https://cdn.libravatar.org/avatar/aba70c130633876489a562cc6f686e42?s=220",
#     'links': (("Lumy's website", 'https://www.lumy.me'),
#               ("Lumy's cv", 'http://cv.lumy.me/'))
#   }
# }
SITENAME = 'Lumy\'s Hobbies'
SITESUBTITLE = "My roads"

PATH='content'

LOAD_CONTENT_CACHE = False
CACHE_CONTENT = False

CATEGORY_URL = '{slug}/category'
CATEGORY_SAVE_AS = '{slug}/category.html'

ARTICLE_URL = '{category}/{slug}/'
ARTICLE_SAVE_AS = '{category}/{slug}.html'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'en'
JINJA_ENVIRONMENT = {'extensions': ['jinja2.ext.i18n']}

THEME='clean-blog'

PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = [
  # "libravatar",
  # "i18n_subsites",
]

# LIBRAVATAR_AUTHOR_EMAIL="lumy@lumy.me"
# LIBRAVATAR_SIZE=220

I18N_SUBSITES = {
    'fr': {
        'SITENAME': 'Les passions de Lumy',
        'THEME_STATIC_PATHS': ["themes/",],
    }
}

JINJA2CONTENT_TEMPLATES="content"

# Whether to display pages on the menu of the template. Templates may or may not honor this setting.
DISPLAY_PAGES_ON_MENU = True

# Whether to display categories on the menu of the template.
DISPLAY_CATEGORIES_ON_MENU = False

DISPLAY_TAGS_ON_MENU = False

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
TYPOGRIFY = True

SHOW_SITESUBTITLE_IN_HTML = True
SHOW_SOCIAL_ON_INDEX_PAGE_HEADER = True

SHOW_FULL_ARTICLE = False
COLOR_SCHEME_CSS="tomorrow_night.css"

# Social widget
SOCIAL = (
  ('twitter', 'https://twitter.com/Lumy4242'),
  ('github', 'https://github.com/lumy'),
  ('music', 'https://soundcloud.com/lumyi'),
  ('envelope', 'mailto:contact@lumy.me'),
  ("home", 'https://www.lumy.me'),
  ("id-card", 'https://cv.lumy.me/'),
  ("users", 'https://blog.lta.io/'),
  ("users", "https://blog.rohja.com/"),
)

# Blogroll
# Unused for now
# LINKS = (("Lta's Blog", 'http://blog.lta.io/'),
#         ("Rohja's Blog", "https://blog.rohja.com/"),
# )

HEADER_COVER = '/images/banner_default.jpg'

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = False

DELETE_OUTPUT_DIRECTORY = True

HEADER_COVERS = {
  "van": "/images/van_back.jpg",
  "juggling":"",
  "cs":"/images/chef-run.gif",
  "misc":"",
}

def output_header(header):
  return HEADER_COVERS[header]

JINJA_FILTERS = {
  'header': output_header,
}


STATIC_PATHS = ["images", "favicon.ico"]

INTRO_CONTENTO_CONTENT = "welcome on my road"