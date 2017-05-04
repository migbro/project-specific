#!/usr/bin/python
# helper script to take a custom table from UCSC and create a refseq reference picking a single isoform per gene


import sys
import re


def write_line(fh, line):
    info = line.split('\t')
    starts = info[3].split(',')
    ends = info[4].split(',')
    info.insert(2, starts[0])
    info.insert(3, ends[-2])
    fh.write('\t'.join(info))

fh = open(sys.argv[1])
head = next(fh)
filt = open('filtered_tx_list.txt', 'w')
review = open('tx_to_review.txt', 'w')
new_head = head.rstrip('\n').split('\t')
new_head.insert(2, 'tx_start')
new_head.insert(3, 'tx_end')
filt.write('\t'.join(new_head) + '\n')
review.write(head)

tx_dict = {}

for line in fh:
    info = line.rstrip('\n').split('\t')
    if info[5] not in tx_dict:
        tx_dict[info[5]] = {}
        tx_dict[info[5]]['flag'] = 999
        tx_dict[info[5]]['best'] = ''
        tx_dict[info[5]]['list'] = []
        tx_dict[info[5]]['id_best'] = ''
        tx_dict[info[5]]['id_flag'] = 99999999999999999999
    tx_dict[info[5]]['list'].append(line)
    m = re.search('transcript variant (\d+)', info[6])
    try:
        n = int(m.group(1))
        if n < tx_dict[info[5]]['flag']:
            tx_dict[info[5]]['flag'] = n
        tx_dict[info[5]]['best'] = line
    except:
        nm_id = info[0].split('_')
        if int(nm_id[1]) < tx_dict[info[5]]['id_flag']:
            tx_dict[info[5]]['id_flag'] = int(nm_id[1])
            tx_dict[info[5]]['id_best'] = line

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

