#!/usr/bin/python
# created index for discordant gene/aa calls from multiple reports using a custom table generated from UCSC table browser
import sys
import pdb


def calc_aa_gene(ref_cur, v_pos, info):
    starts = ref_cur[5].split(',')
    ends = ref_cur[6].split(',')
    gene = ref_cur[7]
    cur_len = 0
    if ref_cur[4] == '+':
        for i in xrange(len(starts)):
            if int(starts[i]) <= v_pos <= int(ends[i]):
                aa_pos = str((v_pos - int(starts[i]) + cur_len)/3)
                print '\t'.join(info) + '\t' + aa_pos + '\t' + gene
                break
            else:
                cur_len += int(ends[i]) - int(starts[i]) + 1
    else:
        for i in xrange(len(starts)-2, 0, -1):
            if int(starts[i]) <= v_pos <= int(ends[i]):
                aa_pos = str((int(ends[i]) - v_pos + cur_len)/3)
                print '\t'.join(info) + '\t' + aa_pos + '\t' + gene
                break
            else:
                cur_len += int(ends[i]) - int(starts[i]) + 1

to_fix = open(sys.argv[1])
ref = open(sys.argv[2])

head = next(ref)
print 'ct\ttype\told gene\tchrom\tpos\tref\talt\taa_pos\tnew_gene'
cur = next(ref)
ref_cur = cur.rstrip('\n').split('\t')
for line in to_fix:
    info = line.rstrip('\n').split('\t')
    s_flag = 0
    while s_flag == 0:
        if info[3] == ref_cur[1]:
            v_pos = int(info[4])
            c_start = int(ref_cur[2])
            c_end = int(ref_cur[3])
            if c_start <= v_pos <= c_end:
                calc_aa_gene(ref_cur, v_pos, info)
                s_flag = 1
        else:
            cur = next(ref)
            ref_cur = cur.rstrip('\n').split('\t')
