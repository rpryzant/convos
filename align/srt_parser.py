"""
wrapper class for parsing .srt files

http://stp.lingfil.uu.se/~joerg/paper/ranlp07-subalign.pdf
http://folk.uio.no/plison/pdfs/talks/opensubtitles2016.pdf


"""
import pysrt
import re

class SRT:

    def __init__(self, srt_fp):
        self.fp = srt_fp
        self.srt = pysrt.open(self.fp)
        self.subs = self.parse_srt(self.srt)



    def parse_srt(self, srt):
        # maybe get a pysrt into better format? like join sentences?
        print self.srt




if __name__ == '__main__':
    import sys
    SRT(sys.argv[1])
    




        

    
