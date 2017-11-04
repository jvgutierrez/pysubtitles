"""
pysubtitles.

Usage:
    pysubtitles [options] <episode>

Options:
    --lang=<lang>           Language [default: English].
    --provider=<provider>   Subtitle provider [default: addic7ed].
"""

import codecs
import importlib
import logging
import os
import sys

import requests

from docopt import docopt
from guessit import guessit

log = logging.getLogger('pysubtitles.pysubtitles')

def extract_episode_data(filename):
    try:
        data = guessit(filename)

        return {
                'show': data['title'],
                'season': data['season'],
                'episode': data['episode'],
            }
    except KeyError as ke:
        raise ValueError(ke)


def persist_subtitle(subtitle, episode):
    filename =  "{0}.srt".format(os.path.splitext(episode)[0])
    f = codecs.open(filename, "w", encoding='utf-8')
    f.write(subtitle)
    f.close()


def main():
    options = docopt(__doc__)
    try:
        provider = importlib.import_module('pysubtitles.providers.{0}'.format(options['--provider']))
    except ImportError:
        log.error("Invalid subtitle provider: %s", options['--provider'])
        sys.exit(1)

    try:
        episode_data = extract_episode_data(options['<episode>'])
    except ValueError as ve:
        log.error("Unable to guess %s from filename", ve)
        sys.exit(1)

    show_list = provider.fetch_show_list()

    if episode_data['show'].lower() in show_list:
        subtitles = provider.list_subtitles(episode_data['show'], episode_data['season'], episode_data['episode'], options['--lang'])
    else:
        log.error("Unable to find show %s in provider %s", episode_data['show'], options['--provider'])
        sys.exit(1)
    if len(subtitles) > 0:
        input = None
        while input != -1:
            try:
                for i, subtitle in enumerate(subtitles):
                    print "{0}. {1}".format(i, subtitle['file'])
                input = int(raw_input('--> '))
                subtitle = provider.fetch_subtitle(subtitles[input]['link'])
                persist_subtitle(subtitle, options['<episode>'])
                sys.exit(0)
            except KeyboardInterrupt:
                sys.exit(0)
            except (IndexError, ValueError) as ive:
                log.error("Unable to fetch and store subtitle: %s", ive)


if __name__ == '__main__':
    logging.getLogger('pysubtitles').addHandler(logging.StreamHandler())
    main()
