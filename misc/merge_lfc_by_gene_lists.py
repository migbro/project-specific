#!/usr/bin/env python

import sys
import os


def merge_lfc_by_gene_lists(g_list, f_list, vcol):
    g_dict = {}

    for line in open(g_list):
        g_dict[line.rstrip('\n')] = {}

    s_list = []
    try:
        vcol = int(vcol)
    except:
        vcol = 2

    for fn in open(f_list):
        fn = fn.rstrip('\n')
        samp = os.path.basename(fn)
        s_list.append(samp)
        fh = open(fn)
        next(fh)
        for data in fh:
            info = data.rstrip('\n').split(',')
            if info[0] in g_dict:
                g_dict[info[0]][samp] = info[vcol]
        fh.close()

    print('Gene' + '\t' + '\t'.join(s_list))
    for gene in g_dict:
        sys.stdout.write(gene)
        for samp in s_list:
            sys.stdout.write('\t' + g_dict[gene][samp])
        sys.stdout.write('\n')


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Creates panel of normals for vcf, use somatic .')
    parser.add_argument('-g', '--gene-list', action='store', dest='g_list',
                        help='List of genes to combine on')
    parser.add_argument('-f', '--flist', action='store', dest='flist',
                        help='List of diff exp files from deseq')
    parser.add_argument('-v', '--value-column', action='store', dest='vcol',
                        help='Column to get values for, 0-based')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    inputs = parser.parse_args()
    merge_lfc_by_gene_lists(inputs.g_list, inputs.flist, inputs.vcol)
