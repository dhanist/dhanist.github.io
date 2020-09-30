#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Dhani Setiawan'
SITENAME = u'DevNull'
SITEURL = '//devnull.web.id'

PATH = 'content'

TIMEZONE = 'Asia/Makassar'

DEFAULT_LANG = u'id'

# Feed generation is usually not desired when developing
FEED_ATOM = 'feed/atom.xml'
#FEED_RSS = 'feeds/rss.xml'
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
                ('Transkon-Net', 'http://www.transkon.net.id', '_blank'),
                ('Debian', 'https://www.debian.org/', '_blank'),
                ('OpenStack', 'https://www.openstack.org', '_blank'),
        )

# Social widget
SOCIAL = (
                ("GitHub", "https://github.com/dhanist", "_blank"),
                ('Google+', 'https://plus.google.com/+DhaniSetiawanYoda', '_blank')
         )

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing

ARTICLE_URL = '{category}/{slug}.html'
ARTICLE_SAVE_AS = '{category}/{slug}.html'

PLUGIN_PATHS = ['./plugins']
PLUGINS = ['extract_toc', 'share_post']
MARKDOWN = {
    'extensions': ['codehilite','extra','smarty', 'toc'],
    'extension_configs': {
            'markdown.extensions.codehilite': {'css_class': 'codehilite'},
        },
}
OUTPUT_PATH = 'output/'
THEME = 'themes/me'

COLOPHON = False
COLOPHON_TITLE = 'About'
COLOPHON_CONTENT = "Mainly...."

STATIC_PATHS = ['pages', 'images', 'extra', 'google', 'github']
ARTICLE_EXCLUDES = ['google']
EXTRA_PATH_METADATA = {
        'extra/robots.txt': {'path': 'robots.txt'},
        'extra/favicon.png': {'path': 'favicon.png'},
        'google/google4478290915ecfc37.html': {'path': 'google4478290915ecfc37.html'},
        'google/google0e26f84e56c7d460.html': {'path': 'google0e26f84e56c7d460.html'},
        'github/CNAME': {'path': 'CNAME'}
}

DELETE_OUTPUT_DIRECTORY = True
RELATIVE_URLS = False
FOOTER_TEXT = ('&copy; Dhani Setiawan. '
                '<a href="//devnull.web.id">devnull.web.id</a> '
                'is powered by <a href="http://getpelican.com" target="_blank">Pelican</a> and '
                '<a href="https://github.com/getpelican/pelican-themes/tree/master/dev-random2" target="_blank">'
                'dev-random2</a> theme')

DISQUS_SITENAME = "dhani-devnull"
