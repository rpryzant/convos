"""
downloads a subtitle for a language

python dl_subs_for_lang.py ../data/subtitle_pages/sub_pages.txt [out_dir] [lang1] [lang2] ..
"""
import time
from collections import defaultdict
import sys
from tqdm import tqdm
import os
import uuid
from ffmpy import FFmpeg
from pyunpack import Archive
import re
sub_pages = sys.argv[1]
out_root = sys.argv[2]
langs = sys.argv[3:]


def download_subfile(url, dest):
    """ download a subscene file at url "url" to                                       
        the location specified by "dest"                                                 
    """
    # download file                                                                   
    dl_id = str(uuid.uuid4())
    target_html = os.path.join(dest, 'html-%s' % dl_id)
    target_file = os.path.join(dest, 'file-%s' % dl_id)

    os.system('wget -nc -P %s %s -O %s' % (dest, url, target_html))
    time.sleep(2)
    
    dl_line = next(l for l in open(target_html) if 'id="downloadButton"' in l)
    dl_link = 'https://subscene.com/' + re.findall('href=\"(.*?)\"', dl_line)[0]

    os.system('wget -nc -P %s %s -O %s' % (dest, dl_link, target_file))

    return target_file



def convert_all_to_srt(dir):
    """ converts all the files in a dir to srt format                                      
    """
    def convert_to_srt(target, dest):
        ff = FFmpeg(
            inputs={target: None},
            outputs={dest: None})
        ff.run()

    for f in os.listdir(dir):
        try:
            f = os.path.join(dir, f)
            if '.srt' not in f:
                convert_to_srt(f, f + '.srt')
        except:
            print 'ERROR: CONVERSION FAILURE ON', f



def extract_archive(target, dest):
    """ tries to extract an archive                                                            
    """
    try:
        Archive(target).extractall(dest)
    except:
        pass


def rm_exclude(dir, suffix):
    os.system("find %s -type f ! -name '*%s' -delete" % (dir, suffix))


def download(url, dest):
    """ downloads a file from url "url" into destination "dest",
            and then converts it to srt format
    """
    dlded_filepath = download_subfile(url, dest)
    if dlded_filepath:
        output = extract_archive(dlded_filepath, dest)
        convert_all_to_srt(dest)
        rm_exclude(dest, '.srt')
        return True
    else:
        return False





d = defaultdict(list)
urls = defaultdict(list)
for l in open(sub_pages):
    [lan, url, title] = l.strip().split()
    d[title].append(lan)
    urls[(title, lan)].append(url)

titles_to_dl = [t for t in d if all([l in d[t] for l in langs]) ]

i = 0
title_gen = ((l, t) for l in langs for t in titles_to_dl)
for l, t in tqdm(title_gen, total=len(langs)*len(titles_to_dl)):
        dl_dir = os.path.join(out_root, l, t)
        if not os.path.exists(dl_dir):
            os.makedirs(dl_dir)
        for url in urls[t, l]:
            time.sleep(2)
            try:
                if download(url, dl_dir):
                    pass
                else:
                    print 'failure!', url
            except KeyboardInterrupt:
                print 'QUITTING'
                quit()
            except Exception as e:
                print 'ERROR on ', url, 'exception ', e
        i += 1

