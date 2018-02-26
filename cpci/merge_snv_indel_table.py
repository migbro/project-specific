#!/usr/bin/env python2

import sys
import os
import re
import pdb


def process_indel_report(pair, report, indel_head_list, indel_head_dict, pos_gene, alt_vaf, cov, banned_tup, length,
                         vclass):
    cur = open(report)
    next(cur)
    maf = 1.0
    # biotype = 'protein_coding'
    weak_impact = {'MODIFIER': 1, 'LOW': 1}
    # 'gene', 'chr', 'pos', 'ref', 'alt', 'alt_cov', 'vaf', 'snp_ID', 'ExAC_MAF', 'impact', 'effect', 'codon_change',
    #  'amino_acid_change'
    for line in cur:
        if line == '\n':
            continue
        info = line.rstrip('\n').split('\t')
        vtup = '\t'.join((info[indel_head_dict['chr']], info[indel_head_dict['pos']], info[indel_head_dict['ref']],
                          info[indel_head_dict['alt']]))
        chr_pos = info[indel_head_dict['gene']] + '_' + info[indel_head_dict['pos']]
        if chr_pos not in pos_gene:
            # might be repeats in reports, skip if position reported already
            pos_gene[chr_pos] = {}
            pos_gene[chr_pos]['name'] = info[indel_head_dict['gene']]
        if pair in pos_gene[chr_pos]:
            continue
        pos_gene[chr_pos][pair] = 1
        try:
            vap = float(info[indel_head_dict['vaf']]) * 100
        except:
            sys.stderr.write('Could not format vap for ' + info[indel_head_dict['vaf']] + 'in sample ' + report + '\n')
            exit(1)
        if vap < alt_vaf:
            continue
        if len(info[indel_head_dict['ref']]) > length or len(info[indel_head_dict['alt']]) > length:
            continue
        if vtup in banned_tup:
            continue
        if info[indel_head_dict['impact']] in weak_impact:
            continue
        if len(info[indel_head_dict['MAF']]) > 0 and float(info[indel_head_dict['MAF']]) > maf:
            continue
        if int(info[indel_head_dict['alt_cov']])/float(info[indel_head_dict['vaf']]) < cov:
            continue
        sys.stdout.write(pair + '\t' + info[vclass])
        info[indel_head_dict['vaf']] = str(vap) + '%'
        for key in indel_head_list:
            sys.stdout.write('\t' + info[indel_head_dict[key]])
        print
    cur.close()


def process_snv_report(pair, report, snv_head_list, snv_head_dict, tn_ratio, pos_gene, alt_vaf, cov):

    cur = open(report)
    next(cur)
    maf = 1.0
    tn = 2
    # biotype = 'protein_coding'
    weak_impact = {'MODIFIER': 1, 'LOW': 1}
    for line in cur:
        if line == '\n':
            continue
        info = line.rstrip('\n').split('\t')
        if info[-1] == 'OFF':
            continue
        chr_pos = info[snv_head_dict['chr']] + '_' + info[snv_head_dict['pos']]
        if chr_pos not in pos_gene:
            # might be repeats in reports, skip if position reported already
            pos_gene[chr_pos] = {}
            pos_gene[chr_pos]['name'] = info[snv_head_dict['gene']]
        if pair in pos_gene[chr_pos]:
            continue
        pos_gene[chr_pos][pair] = 1
        cur_vaf = info[snv_head_dict['%_tumor_alt']].rstrip('%')

        if float(cur_vaf) < alt_vaf:
            continue
        if float(info[tn_ratio]) <= tn:
            continue
        if info[snv_head_dict['impact']] in weak_impact:
            continue
        if len(info[snv_head_dict['MAF']]) > 0 and float(info[snv_head_dict['MAF']]) > maf:
            continue
        if int(info[snv_head_dict['tumor_alt_count']]) + int(info[(snv_head_dict['tumor_alt_count'] - 1)]) < cov:
            continue
        sys.stdout.write(pair + '\t' + 'SNV')
        for key in snv_head_list:
            sys.stdout.write('\t' + info[snv_head_dict[key]])
        print

    cur.close()


def filter_merge_reports(reports, panel, length, alt_vaf, cov, vep):
    snv_suffix = {'.subsitutions.vep.prioritized_impact.report.xls': 1, '.subsitutions.vep.curated_reports.xls': 1,
                  '.subsitutions.vep91.prioritized_impact.report.xls': 1}
    # indel_suffix = '.indels.vep.prioritized_impact.report.xls'

    head = 'Sample_pair\tTYPE\tGENE\tCHROM\tPOS\tREF\tALT\tALT_CT\tALT_PCT\tsnp ID\tExAC_MAF\tIMPACT\tEFFECT' \
           '\tCODON_CHANGE\tAMINO_ACID_CHANGE\tTx Isoform Used'
    print head
    snv_head_list = ('gene', 'chr', 'pos', 'ref', 'alt', 'tumor_alt_count', '%_tumor_alt', 'snp_ID', 'MAF',
                     'impact', 'effect', 'codon_change', 'amino_acid_change', 'isoform')
    snv_head_dict = {'gene': 14, 'chr': 0, 'pos': 1, 'ref': 3, 'alt': 4, 'tumor_alt_count': 9, '%_tumor_alt': 10,
                     'snp_ID': 12, 'ExAC_MAF': 13, 'impact': 17, 'effect': 16, 'codon_change': 19,
                     'amino_acid_change': 20, 'isoform': 15}
    tn_ratio = 9
    indel_head_list = ('gene', 'chr', 'pos', 'ref', 'alt', 'alt_cov', 'vaf', 'snp_ID', 'MAF',
                     'impact', 'effect', 'codon_change', 'amino_acid_change', 'isoform')
    indel_head_dict = {'gene': 6, 'chr': 0, 'pos': 1, 'ref': 2, 'alt': 3, 'alt_cov': 14, 'vaf': 16, 'snp_ID': 4,
                       'ExAC_MAF': 5, 'impact': 10, 'effect': 9, 'codon_change': 12, 'amino_acid_change': 13,
                       'isoform': 7}
    if vep == '91':
        snv_head_list = ('gene', 'chr', 'pos', 'ref', 'alt', 'tumor_alt_count', '%_tumor_alt', 'snp_ID', 'MAF',
                         'impact', 'effect', 'codon_change', 'amino_acid_change', 'isoform')
        snv_head_dict = {'gene': 14, 'chr': 0, 'pos': 1, 'ref': 3, 'alt': 4, 'tumor_alt_count': 9, '%_tumor_alt': 10,
                         'snp_ID': 12, 'MAF': 13, 'impact': 18, 'effect': 17, 'codon_change': 20,
                         'amino_acid_change': 21, 'isoform': 16}
        indel_head_list = ('gene', 'chr', 'pos', 'ref', 'alt', 'alt_cov', 'vaf', 'snp_ID', 'gnomAD_AF',
                           'impact', 'effect', 'codon_change', 'amino_acid_change', 'isoform')
        indel_head_dict = {'gene': 6, 'chr': 0, 'pos': 1, 'ref': 2, 'alt': 3, 'alt_cov': 15, 'vaf': 17, 'snp_ID': 4,
                           'MAF': 5, 'impact': 11, 'effect': 10, 'codon_change': 13, 'amino_acid_change': 14,
                           'isoform': 8}

    vclass = 8
    banned_tup = {}
    length = int(length)
    alt_vaf = int(alt_vaf)
    cov = int(cov)
    for line in open(panel):
        info = line.rstrip('\n').split('\t')
        banned_tup['\t'.join(info[0:4])] = 0
    pos_gene = {}
    for report in open(reports):
        report = report.rstrip('\n')
        fn = os.path.basename(report)
        m = re.search('^(\d+-\d+_\d+-\d+)(\S+)', fn)
        (pair, suffix) = (m.group(1), m.group(2))
        if suffix in snv_suffix:
            process_snv_report(pair, report, snv_head_list, snv_head_dict, tn_ratio, pos_gene, alt_vaf, cov)
        else:
            process_indel_report(pair, report, indel_head_list, indel_head_dict, pos_gene, alt_vaf, cov, banned_tup,
                                length, vclass)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Creates merged reports and filters on vaf, impact, biotype, '
                                                 't/n ratio, panel of normals, coverage.')
    parser.add_argument('-r', '--reports', action='store', dest='reports',
                        help='List of report files.')
    parser.add_argument('-p', '--panel', action='store', dest='panel',
                        help='Panel of normals')
    parser.add_argument('-c', '--min_coverage', action='store', dest='cov',
                        help='Min read coverage')

    parser.add_argument('-l', '--length', action='store', dest='length',
                        help='Max indel length')
    parser.add_argument('-v', '--vaf', action='store', dest='vaf',
                        help='Min variant allele frequency')
    parser.add_argument('-s', '--vep', action='store', dest='vep',
                        help='Version of vep used')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    inputs = parser.parse_args()
    (reports, panel, length, avaf, cov, vep) = (inputs.reports, inputs.panel, inputs.length, inputs.vaf, inputs.cov,
                                                inputs.vep)
    filter_merge_reports(reports, panel, length, avaf, cov, vep)
