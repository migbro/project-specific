#!/usr/bin/env python

import sys

flist = sys.argv[1]
pval = float(sys.argv[2])
n = int(sys.argv[3])

val_dict = {}
slist = []
for fn in open(flist):
    fn = fn.rstrip('\n')
    slist.append(fn)
    val_dict[fn] = {}
    cur = open(fn)
    next(cur)
    for line in cur:
        info = line.rstrip('\n').split(',')
        if info[-1] != 'NA':
            lfc = float(info[2])
            gene = info[0]
            cpval = float(info[-1])
            if cpval <= pval:
                val_dict[fn][gene] = lfc
    cur.close()
g_dict = {}

for fn in slist:
    x = 1
    for gene, value in sorted(val_dict[fn].iteritems(), key=lambda (k, v): (v, k)):
        if x <= n:
            if gene not in g_dict:
                g_dict[gene] = 0
            g_dict[gene] += 1
        else:
            break
        x += 1
    x = 1
    for gene, value in sorted(val_dict[fn].iteritems(), key=lambda (k, v): (v, k), reverse=True):
        if x <= n:
            if gene not in g_dict:
                g_dict[gene] = 0
            g_dict[gene] += 1
        else:
            break
        x += 1

for gene in g_dict:
    print(gene + '\t' + str(g_dict[gene]))
