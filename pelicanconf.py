#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'lumy'
SITENAME = 'Lumy\'s Hobbies'

SITEURL = '' # http://blog.lumy.me'
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

ABOUT_ME={
  "en":"a little about me",
  "fr":"un peu plus sur moi",
}

# Other themes
# plumage
# pelican-themes -l
THEME = "pelican-themes/pelican-bootstrap3"
#"pelican-themes/pelican-blue"

PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = [
    # "jinja2content",
    "libravatar",
    # "pelicanfly",
    "i18n_subsites",
  "image_process.pelican_image_process",
  "better_figures_and_images",
]

RESPONSIVE_IMAGE = True
FIGURE_NUMBERS = True

LIBRAVATAR_AUTHOR_EMAIL="lumy@lumy.me"
LIBRAVATAR_SIZE=220
SITELOGO_SIZE=220
MENUITEMS=()
AVATAR=True

I18N_SUBSITES = {
    'fr': {
        'SITENAME': 'Lumy\'s Hobbies',
        'THEME_STATIC_PATHS': ["themes/",],
    }
}

IMAGE_PROCESS = {
  # 'crisp': {'type': 'responsive-image',
  #           'srcset': [('1x', ["scale_in 800 600 True"]),
  #                      ('2x', ["scale_in 1600 1200 True"]),
  #                      ('4x', ["scale_in 3200 2400 True"]),
  #           ],
  #           'default': '1x',
  # },
  'large-photo': {'type': 'responsive-image',
                  'sizes': '(min-width: 1200px) 800px, (min-width: 992px) 650px, \
                  (min-width: 768px) 718px, 100vw',
                  'srcset': [('600w', ["scale_in 600 450 True"]),
                             ('800w', ["scale_in 800 600 True"]),
                             ('1600w', ["scale_in 1600 1200 True"]),
                  ],
                  'default': '800w',
  },
      }
JINJA2CONTENT_TEMPLATES="content"

# Whether to display pages on the menu of the template. Templates may or may not honor this setting.
DISPLAY_PAGES_ON_MENU = True

# Whether to display categories on the menu of the template.
DISPLAY_CATEGORIES_ON_MENU = True

DISPLAY_TAGS_ON_MENU = False

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
TYPOGRIFY = True
# Blogroll
LINKS = (("Lta's Blog", 'http://blog.lta.io/'),
         ("Lumy's website", 'https://www.lumy.me'),
         ("Lumy's cv", 'http://cv.lumy.me/'),
        ("Rohja's Blog", "https://blog.rohja.com/"),
) 

# Social widget
MSOCIAL = (
    ('Twitter', 'https://twitter.com/Lumy4242', "fab fa-2x fa-twitter"),
    ('Github', 'https://github.com/lumy', "fab fa-2x fa-github"),
    ('Music', 'https://soundcloud.com/lumyi', "fab fa-2x fa-soundcloud"),
)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = False

DELETE_OUTPUT_DIRECTORY = True

import os

def get_about(lang):
  return ABOUT_ME[lang]

JINJA_FILTERS = {
  "get_about": get_about,
}
TWITTER_USERNAME="lumy4242"


