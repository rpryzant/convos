"""
takes a root directory of title pages,
and converts this into a nested directory, where
the leaves contain sub links

python title_pages_to_nested_srt_urls.py [title_pages root] > output

"""
import sys
import os
from bs4 import BeautifulSoup
from tqdm import tqdm

SUBSCENE_BASE_URL = 'https://subscene.com'


def parse_title_page(html_file):
    try:
        soup = BeautifulSoup(open(html_file).read(), 'html.parser')
        sub_table = soup.find('table').find_all('tr')[1:]
    except:
        return
    for i, td in enumerate(sub_table):
        if i % 2 == 0:
            # language only -- can throw away because in URL
            continue
            print td.td.attrs['id']

        try:
            srt_url = td.td.a.attrs['href']
            srt_url = SUBSCENE_BASE_URL + srt_url

            language = srt_url.split('/')[-2]

            title = html_file.split('/')[-1]

            yield language, srt_url, title
        except:
            pass








if __name__ == '__main__':
    title_page_root = sys.argv[1]
    for filename in tqdm(os.listdir(title_page_root)):
        html_path = os.path.join(title_page_root, filename)
        for language, sub_page_url, title in parse_title_page(html_path):
            print language, sub_page_url, title


