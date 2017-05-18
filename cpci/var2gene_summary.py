#!/usr/bin/env python
# quick script to summarize categories of variants for eah gene

import sys
import re


def mk_list(fn):
    temp = []
    for line in open(fn):
        temp.append(line.rstrip('\n'))
    return temp

def print_vals(g_dict, p_list):
    for item in p_list:
        sys.stdout.write('\t' + str(g_dict[item]))

fh = open(sys.argv[1])
type_list = mk_list(sys.argv[2])
impact_list = mk_list(sys.argv[3])
effect_list = mk_list(sys.argv[4])
head = next(fh)

gene_dict = {}
for line in fh:
    line = line.rstrip('\n').split('\t')
    tup = '\t'.join(line[3:7])
    gene = line[2]
    if gene not in gene_dict:
        gene_dict[gene] = {}
        gene_dict[gene] = {'impact': {}, 'effect': {}, 'type': {}}
        for ty in type_list:
            gene_dict[gene]['type'][ty] = 0
        for eff in effect_list:
            gene_dict[gene]['effect'][eff] = 0
        for imp in impact_list:
            gene_dict[gene]['impact'][imp] = 0
    (effect, impact, vtype) = (line[12], line[11], line[1])
    eff = effect.split('&')
    gene_dict[gene]['type'][vtype] += 1
    gene_dict[gene]['effect'][eff[0]] += 1
    gene_dict[gene]['impact'][impact] += 1

fh.close()

print 'Gene\t' + '\t'.join(type_list) + '\t' + '\t'.join(impact_list) + '\t' + '\t'.join(effect_list)
for gene in gene_dict:
    sys.stdout.write(gene)
    cur = gene_dict[gene]
    print_vals(cur['type'], type_list)
    print_vals(cur['impact'], impact_list)
    print_vals(cur['effect'], effect_list)
    print


