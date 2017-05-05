#!/usr/bin/python
# helper script to take a custom table from UCSC and create a refseq reference picking a single isoform per gene


import sys
import re


def write_line(fh, line):
    info = line.split('\t')
    fh.write('\t'.join(info))

fh = open(sys.argv[1])
head = next(fh)
filt = open('filtered_tx_list.txt', 'w')
review = open('tx_to_review.txt', 'w')
filt.write(head)
review.write(head)

tx_dict = {}

for line in fh:
    info = line.rstrip('\n').split('\t')
    gene = info[7]
    if gene not in tx_dict:
        tx_dict[gene] = {}
        tx_dict[gene]['flag'] = 999
        tx_dict[gene]['best'] = ''
        tx_dict[gene]['list'] = []
        tx_dict[gene]['id_best'] = ''
        tx_dict[gene]['id_flag'] = 99999999999999999999
    tx_dict[gene]['list'].append(line)
    m = re.search('transcript variant (\d+)', info[-1])
    try:
        n = int(m.group(1))
        if n < tx_dict[gene]['flag']:
            tx_dict[gene]['flag'] = n
            tx_dict[gene]['best'] = line
    except:
        nm_id = info[0].split('_')
        if int(nm_id[1]) < tx_dict[gene]['id_flag']:
            tx_dict[gene]['id_flag'] = int(nm_id[1])
            tx_dict[gene]['id_best'] = line

fh.close()
for gene in tx_dict:
    if len(tx_dict[gene]['list']) == 1:
        # filt.write(tx_dict[gene]['list'][0])
        write_line(filt, tx_dict[gene]['list'][0])
    elif tx_dict[gene]['flag'] < 999:
        # filt.write(tx_dict[gene]['best'])
        write_line(filt, tx_dict[gene]['best'])
    elif tx_dict[gene]['id_flag'] < 99999999999999999999:
        # filt.write(tx_dict[gene]['id_best'])
        write_line(filt, tx_dict[gene]['id_best'])
    else:
        review.write(''.join(tx_dict[gene]['list']))
filt.close()
review.close()

