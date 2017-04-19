#!/usr/bin/env python
import sys
import os
from utilities.date_time import date_time


def cov_hole_matrix(hlist):
    cov_dict = {}
    low = 30
    slist = []
    for floc in open(hlist):
        floc = floc.rstrip('\n')
        samp = os.path.basename(floc).replace('.hist', '')
        sys.stderr.write(date_time() + 'Processing file ' + floc + 'sample name ' + samp + '\n')
        slist.append(samp)
        fh = open(floc)
        for line in fh:
            if line[0:3] != 'all':
                info = line.rstrip('\n').split('\t')
                if int(info[4]) < low:
                    if info[3] not in cov_dict:
                        cov_dict[info[3]] = {}
                    cov_dict[info[3]][samp] = info[4]
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

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    inputs = parser.parse_args()
    hlist = inputs.hlist
    cov_hole_matrix(hlist)