#!/usr/bin/env python3

import sys
import os
# from math import log

# cnv_dict = []
rename_dict = []
slist = []

for line in open(sys.argv[1]):
    info = line.rstrip('\n').split('\t')
    rename_dict[info[0]] = info[1]

sys.stdout.write('ID\tchrom\tloc.start\tloc.end\tnum.mark\tseg.mean')
for fn in open(sys.argv[2]):
    fn = fn.rstrip('\n')
    cfn = os.path.basename(fn)
    samp = rename_dict[cfn.split('_')[0]]
    slist.append(samp)
    # cnv_dict[samp] = {}
    cur = open(fn)
    next(cur)
    for data in cur:
        datum = data.rstrip('\n').split(',')
        gene = datum[12]
        cn = datum[1]
        amp = datum[0]
        chrom = datum[2]
        mark = datum[4]
        start = datum[7]
        end = datum[3]
        # if gene not in cnv_dict[samp] and gene != 'None':
        if amp == 'Gain':
            print(samp + '\t' + chrom + '\t' + start + '\t' + end + '\t' + mark + cn)
        else:
            if cn != 2:
                cn = int(cn)
                if cn == 0:
                    cn += 2
                cn = cn * -1
                print(samp + '\t' + chrom + '\t' + start + '\t' + end + '\t' + mark + str(cn))
    cur.close()
