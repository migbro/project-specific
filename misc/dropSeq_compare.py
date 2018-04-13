#!/usr/bin/env python

import sys
import os
g_file = open(sys.argv[1])
g_track = {}
g_dict = {}
s_list = []
for line in g_file:
    g_dict[line.rstrip('\n')] = {}
    g_track[line.rstrip('\n')] = 0
g_file.close()
pval = float(sys.argv[3])

fn = open(sys.argv[2])

for deseq in fn:
    deseq = deseq.rstrip('\n')
    samp = os.path.basename(deseq).split('_')[1]
    s_list.append(samp)
    cur = open(deseq)
    next(cur)
    for de in cur:
        data = de.rstrip('\n').split(',')
        gene = data[0]
        if gene in g_dict:
            lfc = float(data[2])
            g_track[gene] = 1
            cur_pval = data[-1]
            if cur_pval == 'NA':
                cur_pval = 1.0
            else:
                cur_pval = float(cur_pval)
            if cur_pval <= pval:
                g_dict[gene][samp] = lfc
            else:
                g_dict[gene][samp] = 0
    cur.close()
fn.close()
for gene in g_track:
    if g_track[gene] == 0:
        sys.stderr.write('Warning ' + gene + ' not found!\n')

print('Gene' + '\t' + '\t'.join(s_list))
for gene in g_dict:
    sys.stdout.write(gene)
    for samp in s_list:
        if samp in g_dict[gene]:
            sys.stdout.write('\t' + str(g_dict[gene][samp]))
        else:
            sys.stdout.write('\t0')
    sys.stdout.write('\n')
