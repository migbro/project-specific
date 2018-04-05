#!/usr/bin/env python
import sys
flist = sys.argv[1]
strip = sys.argv[2]
study = sys.argv[3]

# xargs -IFN aws s3 cp FN s3://tm-uchicago-pan/CPCI_Retrospective_Study --sse --profile tempus

out = open('flist.txt', 'w')
for line in open(flist):
        line = line.rstrip('\n')
        fn = line.replace(strip, '')
        output = line + ' s3://tm-uchicago-pan/' + study + '/' + fn
        out.write(output + '\n')
out.close()