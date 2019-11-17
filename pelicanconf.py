#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'lumy'
SITENAME = 'Lumy\'s blog'

SITEURL = '' # http://blog.lumy.me'
PATH='content'

LOAD_CONTENT_CACHE = False
CACHE_CONTENT = False

CATEGORY_URL = '{slug}/category'
CATEGORY_SAVE_AS = '{slug}/category.html'

ARTICLE_URL = '{lang}/{category}/{slug}/'
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
    "libravatar",
    "pelicanfly",
    "i18n_subsites",
]

LIBRAVATAR_AUTHOR_EMAIL="lumy@lumy.me"
LIBRAVATAR_SIZE=220

I18N_SUBSITES = {
    'fr': {
        'SITENAME': 'Journal de Lumy',
        'THEME_STATIC_PATHS': ["themes/",],
    }
}

JINJA2CONTENT_TEMPLATES="content"

# Whether to display pages on the menu of the template. Templates may or may not honor this setting.
DISPLAY_PAGES_ON_MENU = True

# Whether to display categories on the menu of the template.
DISPLAY_CATEGORIES_ON_MENU = True

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

def extract_trans(article, lang, url):
  for trans in article.translations:
    if trans.lang == lang:
        return trans.url
    return url

languages_lookup = {
                 'en': 'English',
                 'fr': 'Francais',
                 }
def lookup_lang_name(lang_code):
  return languages_lookup[lang_code]

import os

def generate_url_lang(lang_file):
  lang, filename = lang_file[0], lang_file[1]
  if lang != "en":
    return os.path.join("/", lang, filename)
  else:
    return os.path.join("/", filename)

JINJA_FILTERS = {
    'extract_trans': extract_trans,
    'lookup_lang_name': lookup_lang_name,
  "generate_url_lang": generate_url_lang,
}
TWITTER_USERNAME="lumy4242"
