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
    gene = info[5]
    if gene not in tx_dict:
        tx_dict[gene] = {}
        tx_dict[gene]['flag'] = 999
        tx_dict[gene]['best'] = ''
        tx_dict[gene]['list'] = []
        tx_dict[gene]['id_best'] = ''
        tx_dict[gene]['id_flag'] = 99999999999999999999
    tx_dict[gene]['list'].append(line)
    m = re.search('transcript variant (\w+),', info[-5])
    try:
        try:
            n = int(m.group(1))
        except:
            n = ord(m.group(1))
        if n < tx_dict[gene]['flag']:
            tx_dict[gene]['flag'] = n
            tx_dict[gene]['best'] = line
    except:
        nm_id = info[0].split('_')
        if int(nm_id[1]) < tx_dict[gene]['id_flag'] and nm_id[0] == 'NM':
            tx_dict[gene]['id_flag'] = int(nm_id[1])
            tx_dict[gene]['id_best'] = line

fh.close()
sum_dict = {'single': 0, 'id': 0}
for gene in tx_dict:
    if len(tx_dict[gene]['list']) == 1:
        # filt.write(tx_dict[gene]['list'][0])
        sum_dict['single'] += 1
        write_line(filt, tx_dict[gene]['list'][0])
    elif tx_dict[gene]['flag'] < 999:
        # filt.write(tx_dict[gene]['best'])
        if tx_dict[gene]['flag'] not in sum_dict:
            sum_dict[tx_dict[gene]['flag']] = 0
        sum_dict[tx_dict[gene]['flag']] += 1
        write_line(filt, tx_dict[gene]['best'])
        if tx_dict[gene]['flag'] != 1:
            sys.stderr.write(gene + '\t' + str(tx_dict[gene]['flag']) + '\n')
    elif tx_dict[gene]['id_flag'] < 99999999999999999999:
        # filt.write(tx_dict[gene]['id_best'])
        write_line(filt, tx_dict[gene]['id_best'])
        sum_dict['id'] += 1
    else:
        review.write(''.join(tx_dict[gene]['list']))
filt.close()
review.close()
for key in sum_dict:
    sys.stderr.write(str(key) + '\t' + str(sum_dict[key]) + '\n')

