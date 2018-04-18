#!/usr/bin/env python

import sys
import os


def merge_lfc_by_filter(lfc, padj, flist):
    s_list = []
    g_dict = {}
    padj = float(padj)
    lfc = float(lfc)
    g = 0
    d = 2
    p = 6
    for fn in open(flist):
        fn = fn.rstrip('\n')
        samp = os.path.basename(fn)
        s_list.append(samp)
        fh = open(fn)
        next(fh)
        for data in fh:
            info = data.rstrip('\n').split(',')
            if info[p] != 'NA' and float(info[p]) < padj:
                cur = float(info[d])
                if info[g] not in g_dict:
                    g_dict[info[g]] = {}
                if abs(cur) >= lfc:
                    g_dict[info[g]][samp] = cur
                else:
                    g_dict[info[g]][samp] = 0
        fh.close()

    print('Gene' + '\t' + '\t'.join(s_list))
    for gene in g_dict:
        temp_sum = 0
        temp_string = gene
        for samp in s_list:
            if samp in g_dict[gene]:
                temp_sum += abs(g_dict[gene][samp])
                temp_string += ('\t' + str(g_dict[gene][samp]))
            else:
                temp_string += '\t0'
        if temp_sum > 0:
            sys.stdout.write(temp_string + '\n')
        else:
            sys.stderr.write('Gene ' + gene + ' skipped, statistically significant but not meeting ' + str(lfc)
                             + ' threshold' + '\n')


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Filter DESeq2 output and merge into single table')
    parser.add_argument('-l', '--lfc', action='store', dest='lfc',
                        help='absolute lfc value to filter on')
    parser.add_argument('-p', '--padj', action='store', dest='padj',
                        help='Maximum Adjusted P Value')
    parser.add_argument('-f', '--flist', action='store', dest='flist',
                        help='List of diff exp files from deseq')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    inputs = parser.parse_args()
    merge_lfc_by_filter(inputs.lfc, inputs.padj, inputs.flist)
