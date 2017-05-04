#!/usr/bin/env python

import sys
import os
import re
import pdb


def process_germ_report(bnid, report, germ_head_list, germ_head_dict, cadd, cov, length, pos_gene):
    cur = open(report)
    next(cur)
    maf = 0.01
    # biotype = 'protein_coding'
    weak_impact = {'MODIFIER': 1, 'LOW': 1}
    # 'gene', 'chr', 'pos', 'ref', 'alt', 'alt_cov', 'cadd', 'snp_ID', 'ExAC_MAF', 'impact', 'effect', 'codon_change', 'amino_acid_change'
    for line in cur:
        if line == '\n':
            continue
        info = line.rstrip('\n').split('\t')
        # vtup = '\t'.join((info[germ_head_dict['chr']], info[germ_head_dict['pos']], info[germ_head_dict['ref']],
        #                  info[germ_head_dict['alt']]))
        chr_pos = info[germ_head_dict['gene']] + '_' + info[germ_head_dict['pos']]
        if chr_pos not in pos_gene:
            # might be repeats in reports, skip if position reported already
            pos_gene[chr_pos] = {}
            pos_gene[chr_pos]['name'] = info[germ_head_dict['gene']]
        if bnid in pos_gene[chr_pos]:
            continue
        pos_gene[chr_pos][bnid] = 1
        if cadd != 0:
            if len(info[germ_head_dict['cadd']]) < 1 or (len(info[germ_head_dict['cadd']]) > 1 and
                                                                 float(info[germ_head_dict['cadd']]) < cadd):
                continue
        if len(info[germ_head_dict['ref']]) > length or len(info[germ_head_dict['alt']]) > length:
            continue
        if info[germ_head_dict['impact']] in weak_impact:
            continue
        if len(info[germ_head_dict['ExAC_MAF']]) > 0 and float(info[germ_head_dict['ExAC_MAF']]) > maf:
            continue
        # pdb.set_trace()
        if int(info[germ_head_dict['cov']]) < cov:
            continue
        sys.stdout.write(bnid)
        try:
            info[germ_head_dict['alt_ct']] = \
            "{0:.0f}%".format(int(info[germ_head_dict['alt_ct']])/float(info[germ_head_dict['cov']]) * 100)
        except:
            sys.stderr.write('Format failure for line:\n' + line)
            # exit(1)
        for key in germ_head_list:
            sys.stdout.write('\t' + info[germ_head_dict[key]])
        print
    cur.close()


def filter_merge_reports(reports, length, cadd, cov):
    snv_suffix = '.subsitutions.vep.prioritized_impact.report.xls'
    # indel_suffix = '.indels.vep.prioritized_impact.report.xls'

    head = 'Sample\tTYPE\tGENE\tCHROM\tPOS\tREF\tALT\tAllele_pct\tPosition coverage\tsnp ID\tExAC_MAF\tIMPACT\tEFFECT' \
           '\tCODON_CHANGE\tAMINO_ACID_CHANGE\tCADD'
    print head
    germ_head_list = ('VARIANT_CLASS', 'gene', 'chr', 'pos', 'ref', 'alt', 'alt_ct', 'cov', 'snp_ID', 'ExAC_MAF',
                     'impact', 'effect', 'codon_change', 'amino_acid_change', 'cadd')
    germ_head_dict = {'gene': 6, 'chr': 0, 'pos': 1, 'ref': 2, 'alt': 3, 'alt_ct': 4, 'cov': 5, 'snp_ID': 13,
                       'VARIANT_CLASS': 14, 'ExAC_MAF': 16, 'impact': 9, 'effect': 8, 'codon_change': 11,
                      'amino_acid_change': 12, 'cadd': 18}
    # banned_tup = {}
    length = int(length)
    cadd = int(cadd)
    cov = int(cov)
    # cov = int(cov)
    # for line in open(panel):
    #     info = line.rstrip('\n').split('\t')
    #     banned_tup['\t'.join(info[0:4])] = 0
    pos_gene = {}
    for report in open(reports):
        report = report.rstrip('\n')
        fn = os.path.basename(report)
        m = re.search('^(\d+-\d+)(.\S+)', fn)
        (bnid, suffix) = (m.group(1), m.group(2))

        process_germ_report(bnid, report, germ_head_list, germ_head_dict, cadd, cov, length, pos_gene)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Creates merged reports and filters on impact, ExaC MAF, '
                                                 'coverage, CADD score.')
    parser.add_argument('-r', '--reports', action='store', dest='reports',
                        help='List of report files.')
    # parser.add_argument('-p', '--panel', action='store', dest='panel',
    #                     help='Panel of normals')
    parser.add_argument('-c', '--min_coverage', action='store', dest='cov',
                        help='Min number of samples to see a variant to report it')

    parser.add_argument('-l', '--length', action='store', dest='length',
                        help='Max indel length')
    parser.add_argument('-p', '--phred', action='store', dest='cadd',
                        help='Min CADD phred score')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    inputs = parser.parse_args()
    (reports, length, cadd, cov) = (inputs.reports, inputs.length, inputs.cadd, inputs.cov)
    filter_merge_reports(reports, length, cadd, cov)
