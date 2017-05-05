#!/usr/bin/python
# created index for discordant gene/aa calls from multiple reports using a custom table generated from UCSC table browser
import sys
from math import ceil
import pdb


def calc_aa_gene(ref_cur, v_pos, info):
    starts = ref_cur[5].split(',')
    ends = ref_cur[6].split(',')
    gene = ref_cur[7]
    cur_aa_len = 0
    cds_start = ref_cur[3]
    cds_end = ref_cur[4]
    if ref_cur[2] == '+':
        # start could be farther or shorter in
        f = 0
        j = 0

        while f == 0:
            if int(starts[j]) <= int(cds_start) <= int(ends[j]):
                f = 1
            else:
                j += 1
        starts[j] = cds_start
        for i in xrange(j, len(starts)-1, 1):
            # starts[i] = str(int(starts[i]) + 1)
            if int(starts[i]) <= v_pos <= int(ends[i]):
                # pdb.set_trace()
                aa_pos = str(int((ceil(v_pos - int(starts[i]))/3.0)) + cur_aa_len)
                print '\t'.join(info) + '\t' + aa_pos + '\t' + gene
                break
            else:
                temp = (int(ends[i]) - int(starts[i]))
                cur_aa_len += int(ceil(temp/3.0))

    else:
        # start could be farther or shorter in
        f = 0
        j = -2
        # pdb.set_trace()
        while f == 0:
            if int(starts[j]) < int(cds_end):
                f = 1
            else:
                j -= 1
        ends[j] = cds_end
        for i in xrange(len(ends)+j, 0, -1):
            # starts[i] = str(int(starts[i]) + 1)

            if int(starts[i]) <= v_pos <= int(ends[i]):
                aa_pos = str(int(round((int(ends[i]) - v_pos)/3.0)) + cur_aa_len)
                print '\t'.join(info) + '\t' + aa_pos + '\t' + gene
                break
            else:
                temp = (int(ends[i]) - int(starts[i]))
                cur_aa_len += int(round(temp / 3.0))

to_fix = open(sys.argv[1])
ref = open(sys.argv[2])

head = next(ref)
print 'ct\ttype\told gene\tchrom\tpos\tref\talt\taa_pos\tnew_gene'
cur = next(ref)
ref_cur = cur.rstrip('\n').split('\t')
for line in to_fix:
    sys.stderr.write('Processing ' + line)
    info = line.rstrip('\n').split('\t')
    s_flag = 0
    while s_flag == 0:
        v_chr = info[3].replace('chr', '')
        r_chr = ref_cur[1].replace('chr', '')
        r = 0
        v = 0
        try:
            v = int(v_chr)
        except:
            v = ord(v_chr)
        try:
            r = int(r_chr)
        except:
            r = ord(r_chr)

        if r > v:
            # pdb.set_trace()
            sys.stderr.write('Not in predominant transcript coding region:\n' + line)
            s_flag = 1
        elif v_chr == r_chr:
            v_pos = int(info[4])
            c_start = int(ref_cur[3])
            c_end = int(ref_cur[4])
            if c_start <= v_pos <= c_end:
                calc_aa_gene(ref_cur, v_pos, info)
                s_flag = 1
            elif c_start > v_pos:
                sys.stderr.write('Not in predominant transcript coding region:\n' + line)
                s_flag = 1
            else:
                cur = next(ref)
                ref_cur = cur.rstrip('\n').split('\t')
        else:
            cur = next(ref)
            ref_cur = cur.rstrip('\n').split('\t')
