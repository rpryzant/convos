import sys

for l in open(sys.argv[1]):
    print l.strip().lower()
