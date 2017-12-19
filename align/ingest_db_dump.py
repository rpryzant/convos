"""



"""
import pandas as pd
import os
from pyunpack import Archive


DB_ROOT = '../crawl/files'
OUT_ROOT = 'aligned_subs/'

def align(jsrt_path, esrt_path):
    # TODO
    return {
        'alignment': 'hello!', 
        'jid': os.path.basename(jsrt_path), 
        'eid': os.path.basename(esrt_path)
    }

def choose_best_alignment(alignments):
    # TODO
    best = alignments[0]
    return best['alignment'], best['jid'], best['eid']


def get_or_extract_sub_path(row):
    # example path for IDSubtitleFile 12345.gz is 5/4/3/2/12345.gz
    sid = str(row['IDSubtitleFile'])
    path = os.path.join(
        DB_ROOT, 
        '/'.join(sid[-4:][::-1]),
        sid)
    if os.path.exists(path):
        return path

    dest = os.path.dirname(path)
    gz_path = path + '.gz'
    assert os.path.exists(gz_path)
    Archive(gz_path).extractall(dest)

    return os.path.join(dest, sid)

df = pd.read_csv(os.path.join(DB_ROOT, 'export.tsv'), sep='\t')

for mid in df['MovieID'].unique():
    jpn_subs = df[
        (df['MovieID'] == mid) &\
        (df['SubLanguageID'] == 'jpn')]
    eng_subs = df[
        (df['MovieID'] == mid) &\
        (df['SubLanguageID'] == 'eng')]

    alignments = []
    for _, jsub in jpn_subs.iterrows():
        for _, esub in eng_subs.iterrows():
            jsrt_path = get_or_extract_sub_path(jsub)
            esrt_path = get_or_extract_sub_path(esub)
            print jsrt_path, esrt_path
            alignments.append(align(jsrt_path, esrt_path))

    # somehow pick the best pairing..?
    best_alignment, jid, eid = choose_best_alignment(alignments)

    out_dir = os.path.join(OUT_ROOT, str(mid))
    # somehow record stuff




