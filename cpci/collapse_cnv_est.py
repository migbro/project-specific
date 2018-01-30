#!/usr/bin/env python2

import sys
import os


def collapse_mega(flist):
    head = 'Pair\tCHROM\tGENE\tTier\tTum Read ct\tNorm Read ct\tT/N ratio\tlog2 ratio'
    print head
    for fname in open(flist):
        sys.stderr.write('Processing ' + fname)
        fname = fname.rstrip('\n')
        pair = os.path.basename(fname).replace('_cnv_estimate.txt', '')
        fh = open(fname)
        next(fh)
        for line in fh:
            sys.stdout.write(pair + '\t' + line)
        fh.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Collapses per-sample cnv estimates into one mega-file')
    parser.add_argument('-l', '--list', action='store', dest='flist', help='List of cnv est files')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    inputs = parser.parse_args()
    flist = inputs.flist
    collapse_mega(flist)
