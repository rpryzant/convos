"""
=== DESCRIPTION
takes a list of title pages, e.g.
https://subscene.com/subtitles/ben-hur
and downloads all of them

=== USAGE
python title_pages_from_urls.py [title page file] [output dir]

"""
import sys
import os
from tqdm import tqdm
import time

infile = sys.argv[1]
outdir = sys.argv[2]


n = sum(1 for line in open(infile))



for i, l in enumerate(tqdm(open(infile), total=n)):
    l = l.strip()
    title = l.split('/')[-1]
    out_path = os.path.join(outdir, title)
    cmd = 'wget -O %s %s' % (out_path, l)
    os.system(cmd)
    time.sleep(3)

