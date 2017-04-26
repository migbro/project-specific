#!/usr/bin/env python
import sys
import os
from date_time import date_time


def cov_hole_matrix(hlist, aflag):
    cov_dict = {}
    low = 30
    slist = []
    # coverage column is 4th unless bedfile wasn't annotated
    c = 4
    if aflag == 'n':
        c = 3
    for floc in open(hlist):
        floc = floc.rstrip('\n')
        samp = os.path.basename(floc).replace('.hist', '')
        sys.stderr.write(date_time() + 'Processing file ' + floc + ' sample name ' + samp + '\n')
        slist.append(samp)
        fh = open(floc)
        for line in fh:
            if line[0:3] != 'all':
                info = line.rstrip('\n').split('\t')
                if int(info[c]) < low:
                    reg = info[3]
                    if aflag == 'n':
                        reg = info[0] + ':' + info[1] + '-' + info[2]
                    if reg not in cov_dict:
                        cov_dict[reg] = {}
                    cov_dict[reg][samp] = info[c]
            else:
                fh.close()
                break
    sys.stderr.write(date_time() + 'Outputting matrix\n')
    print 'Sample/Region\t' + '\t'.join(slist)
    for region in cov_dict:
        sys.stdout.write(region)
        for samp in slist:
            if samp in cov_dict[region]:
                sys.stdout.write('\t' + cov_dict[region][samp])
            else:
                sys.stdout.write('\t30')
        print

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Create table with sample and regions on low coverage.')
    parser.add_argument('-l', '--list', action='store', dest='hlist',
                        help='bedtools hist table list')
    parser.add_argument('-a', '--annot_flag', action='store', dest='aflag',
                        help='y or n flag if bedtools file was annotated')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    inputs = parser.parse_args()
    hlist = inputs.hlist
    aflag = inputs.aflag
    cov_hole_matrix(hlist, aflag)
