#!/usr/bin/env python

import sys
import pdb


def summary2aa_vaf(report, min_ct, mode):
    fh = open(report)
    var_dict = {}
    gcol = 2
    aa_col = 14
    samp = 0
    sdict = {}
    g_samp = {}
    min_ct = int(min_ct)
    (chrom, pos, ref, alt) = (3, 4, 5, 6)
    next(fh)
    for line in fh:
        info = line.rstrip('\n').split('\t')
        # pdb.set_trace()
        (cur_samp, cur_gene, cur_aa) = (info[samp], info[gcol], info[aa_col])
        # need to see if there is an aa change, otherwise use genomic position
        if len(cur_aa) < 1:
            cur_aa = '_'.join((info[chrom], info[pos], info[ref], info[alt]))
        if cur_gene not in var_dict:
            var_dict[cur_gene] = {}
            g_samp[cur_gene] = {}
        if cur_aa not in var_dict[cur_gene]:
            var_dict[cur_gene][cur_aa] = {}
        var_dict[cur_gene][cur_aa][cur_samp] = '1'
        sdict[cur_samp] = 1
        g_samp[cur_gene][cur_samp] = '1'
    fh.close()
    slist = []
    for s in sdict:
        slist.append(s)

    if mode == 'aa':
        print 'Sample/AA\t' + '\t'.join(slist)
        for gene in var_dict:
            if len(g_samp[gene]) >= min_ct:
                for aa in var_dict[gene]:
                    sys.stdout.write(gene + '_' + aa)
                    for sample in slist:
                        if sample in var_dict[gene][aa]:
                            sys.stdout.write('\t' + var_dict[gene][aa][sample])
                        else:
                            sys.stdout.write('\t0')
                    print
    else:

        print 'Sample/Gene\t' + '\t'.join(slist)
        for gene in var_dict:
            if len(g_samp[gene]) >= min_ct:
                sys.stdout.write(gene)
                for sample in slist:
                    if sample in g_samp[gene]:
                        sys.stdout.write('\t' + g_samp[gene][sample])
                    else:
                        sys.stdout.write('\t0')
                print

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Creates merged reports and filters on vaf, impact, biotype, '
                                                 't/n ratio, panel of normals, coverage.')
    parser.add_argument('-r', '--report', action='store', dest='report',
                        help='Merged report file.')
    parser.add_argument('-m', '--minimum', action='store', dest='min',
                        help='Min number of samples to see the GENE in')
    parser.add_argument('-t', '--type', action='store', dest='mode',
                        help='Create binary table on \'aa\' or \'gene\'')



    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    inputs = parser.parse_args()
    (report, min_ct, mode) = (inputs.report, inputs.min, inputs.mode)
    summary2aa_vaf(report, min_ct, mode)
