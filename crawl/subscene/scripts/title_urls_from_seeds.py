"""
=== DESCRIPTION
gets title urls, e.g.
https://subscene.com/subtitles/the-avengers/
from a bunch of subscene search result pages 
that are passed as cli args

=== USAGE
python title_urls_from_seeds.py [search page 1] [search page 2] ...


"""
import sys
import re

TITLE_URL_RE = "http[s]?://subscene.com/subtitles/[//\w-]+"

s = set()

for fp in sys.argv[1:]:
    ftext = open(fp).read()
    for url in re.findall(TITLE_URL_RE, ftext):
        if url.endswith('subtitles/title'):
            continue
        base = '/'.join(url.split('/')[:-2])
        s.add(base)

for x in s:
    print x


