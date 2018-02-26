#!/usr/bin/env python2

import sys
import os


def filt_var(tn_ratio, maf, target):
    if (maf == '' or float(maf) <= 0.1) and float(tn_ratio) >= 2 and target == 'ON':
        return 1
    else:
        return 0


def gen_snv_maf(flist, vep):

    class_dict = {'3_Prime_UTR_Variant': '3\'UTR', '5_Prime_UTR_Variant': '5\'UTR', 'Downstream_Gene_Variant': '3\'Flank',
                  'Inframe_Deletion': 'In_Frame_Del', 'Inframe_Insertion': 'In_Frame_Ins', 'Intergenic_Variant': 'IGR',
                  'Intron_Variant': 'Intron', 'Missense_Variant': 'Missense_Mutation',
                  'Non_Coding_Transcript_Exon_Variant': 'Targeted_Region', 'Splice_Acceptor_Variant': 'Splice_Site',
                  'Splice_Donor_Variant': 'Splice_Site', 'Splice_Region_Variant': 'Splice_Site',
                  'Start_Lost': 'Translation_Start_Site', 'Stop_Gained': 'Nonsense_Mutation',
                  'Stop_Retained_Variant': 'Nonsense_Mutation', 'Synonymous_Variant': 'Silent',
                  'Upstream_Gene_Variant': '5\'Flank', 'Stop_Lost': 'Nonstop_Mutation'}
    header = '#version 2.4\nHugo_Symbol\tTumor_Sample_Barcode\tVariant_Classification\tHGVSp_Short\tNCBI_Build' \
             '\tChromosome\tStart_Position\tStrand\tVariant_Type\tReference_Allele\tTumor_Seq_Allele1\tdbSNP_RS' \
             '\tMutation_Status\tt_alt_count\tt_ref_count'
    print header
    shift = 0
    if vep != '84':
        shift = 1
    for fn in open(flist):
        fn = fn.rstrip('\n')
        parts = os.path.basename(fn).split('.')
        (tum_bnid, norm_bnids) = parts[0].split('_')
        fh = open(fn)
        next(fh)
        for line in fh:
            data = line.rstrip('\n').split('\t')
            if data[(17 + shift)] != 'MODIFIER':
                (gene, tum_bnid, var_class, aa, build, chrom, start, strand, var_type, ref, alt, dbsnp, status, alt_ct,
                 ref_ct) = (data[14], tum_bnid, data[(16 + shift)], data[(20 + shift)], '37', data[0], data[1], '+',
                            'SNV', data[3], data[4], data[12], 'somatic', data[8], data[9])
                (tn_ratio, maf, target) = (data[11], data[13], data[-1])
                flag = filt_var(tn_ratio, maf, target)
                if flag == 1:
                    repl_var_class = var_class.split('&')
                    to_cap = repl_var_class[0].split('_')
                    for i in xrange(len(to_cap)):
                        if to_cap[i][0].islower():
                            to_cap[i] = to_cap[i][0].upper() + to_cap[i][1:]
                    var_class = '_'.join(to_cap)
                    var_class = class_dict[var_class]
                    # if var_class != 'Frameshift_Variant':
                    #     var_class = class_dict[var_class]
                    # else:
                    #     if var_type == 'insertion':
                    #         var_class = 'Frame_Shift_Ins'
                    #     else:
                    #         var_class = 'Frame_Shift_Del'
                    repl_dbsnp = dbsnp.split('&')
                    f = 0
                    for i in xrange(len(repl_dbsnp)):
                        if repl_dbsnp[i][0:2] == 'rs':
                            dbsnp = repl_dbsnp[i]
                            f = 1
                            break
                    if f == 0:
                        dbsnp = ''
                    alt_ct_fix = alt_ct.split(',')
                    # if len(alt_ct_fix) > 1:
                    #     alt_ct = alt_ct_fix[0].replace('(', '')
                    # ref_ct = str(int(ref_ct) - int(alt_ct))
                    print '\t'.join((gene, tum_bnid, var_class, aa, build, chrom, start, strand, var_type, ref, alt, dbsnp,
                                     status, alt_ct, ref_ct))
        fh.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Converts snv report files into single mag file compatible with '
                                                 'cbioportal.')
    parser.add_argument('-l', '--list', action='store', dest='flist', help='List of snv report files')
    parser.add_argument('-v', '--vep', action='store', dest='vep', help='Version of vep used')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    inputs = parser.parse_args()
    flist = inputs.flist
    vep = inputs.vep
    gen_snv_maf(flist, vep)
