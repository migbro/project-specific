#!/usr/bin/env python

import sys
import pdb

fh = open(sys.argv[1])
next(fh)
var_dict = {}
gene_dict = {}

var_out = open('var_summary.txt', 'w')
var_out.write('gene\tchr\tpos\tref\talt\ttype\timpact\teffect\teffect_ct\n')

gene_out = open('gene_summary.txt', 'w')
eff_dict = {}
vtype_list = ('SNV', 'insertion', 'deletion')
impact_list = ('HIGH', 'MODERATE')
gene_out.write('gene\t' + '_ct\t'.join(impact_list) + '_ct\t' + '_ct\t'.join(vtype_list))
for line in fh:
    info = line.rstrip('\n').split('\t')
    tup = '\t'.join(info[3:7])
    # pdb.set_trace()
    gene = info[2]
    vtype = info[1]
    impact = info[11]
    eff = info[12].split('&')
    effect = eff[0]
    if effect not in eff_dict:
        eff_dict[effect] = 0
    eff_dict[effect] += 1
    if tup not in var_dict:
        var_dict[tup] = []
        var_dict[tup].append(impact)
        var_dict[tup].append(effect)
        var_dict[tup].append(0)
        var_dict[tup].append(gene)
        var_dict[tup].append(vtype)
    var_dict[tup][2] += 1

    if gene not in gene_dict:
        gene_dict[gene] = {}
        gene_dict[gene]['impact'] = {}
        gene_dict[gene]['effect'] = {}
        gene_dict[gene]['vtype'] = {}
    if impact not in  gene_dict[gene]['impact']:
        gene_dict[gene]['impact'][impact] = 0
    if effect not in gene_dict[gene]['effect']:
        gene_dict[gene]['effect'][effect] = 0
    if vtype not in gene_dict[gene]['vtype']:
        gene_dict[gene]['vtype'][vtype] = 0
        
    gene_dict[gene]['impact'][impact] += 1
    gene_dict[gene]['effect'][effect] += 1
    gene_dict[gene]['vtype'][vtype] += 1
fh.close()

eff_list = []
for e in sorted(eff_dict, key = eff_dict.get, reverse=True):
    eff_list.append(e)
    gene_out.write('\t' + e + '_ct')
gene_out.write('\n')

for tup in var_dict:
    var_out.write(var_dict[tup][3] + '\t' + tup + '\t' + var_dict[tup][4] + '\t' + var_dict[tup][0] + '\t' + var_dict[tup][1] + '\t' + str(var_dict[tup][2]) + '\n')
var_out.close()

for gene in gene_dict:
    gene_out.write(gene)
    for impact in impact_list:
        if impact in gene_dict[gene]['impact']:
            gene_out.write('\t' + str(gene_dict[gene]['impact'][impact]))
        else:
            gene_out.write('\t0')
    for vtype in vtype_list:
        if vtype in gene_dict[gene]['vtype']:
            gene_out.write('\t' + str(gene_dict[gene]['vtype'][vtype]))
        else:
            gene_out.write('\t0')
    for effect in eff_list:
        if effect in gene_dict[gene]['effect']:
            gene_out.write('\t' + str(gene_dict[gene]['effect'][effect]))
        else:
            gene_out.write('\t0')
    gene_out.write('\n')
gene_out.close()

            
