#!/usr/bin/env python2
import re
import sys

from date_time import date_time


def create_pon(vlist):
    banned_tup = {}
    norm_flag = {}
    print 'chr\tpos\tref\talt\tct'
    banned_filt = {'HighVafNormal': 0, 'HighAltCountNormal': 0}

    for fn in open(vlist):
        sys.stderr.write(date_time() + 'Processing ' + fn)
        fn = fn.rstrip('\n')
        bnids = re.search('(\d+-\d+)_(\d+-\d+)', fn)
        norm = bnids.group(2)
        vcf = open(fn)
        if norm not in norm_flag:
            norm_flag[norm] = {}
        for line in vcf:
            if line[0] != '#':
                info = line.rstrip('\n').split('\t')
                filt = info[6].split(';')
                for state in filt:
                    if state in banned_filt:
                        cur = '\t'.join((info[0], info[1], info[3], info[4]))
                        if cur not in banned_tup:
                            banned_tup[cur] = 1
                            norm_flag[norm][cur] = 1
                        elif cur not in norm_flag[norm]:
                            norm_flag[norm][cur] = 1
                            banned_tup[cur] += 1
                        break
        vcf.close()
    sys.stderr.write(date_time() + 'Outputting results\n')
    for tup in banned_tup:
        sys.stdout.write(tup + '\t' + str(banned_tup[tup]) + '\n')


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Creates panel of normals for vcf, use somatic .')
    parser.add_argument('-l', '--list', action='store', dest='vlist',
                        help='List of vcf files')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    inputs = parser.parse_args()
    vlist = inputs.vlist
    create_pon(vlist)
