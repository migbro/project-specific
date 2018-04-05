#!/usr/bin/env python

import sys
import os

g_dict = {}

for line in open(sys.argv[1]):
    g_dict[line.rstrip('\n')] = {}

s_list = []
vcol = 2
try:
    vcol = int(sys.argv[3])
except:
    vcol = 2

for fn in open(sys.argv[2]):
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
