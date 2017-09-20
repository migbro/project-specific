#!/usr/bin/python

import sys
import os

maf1 = open(sys.argv[1])
maf2 = open(sys.argv[2])

head_dict = {}
h2_dict = {}
default = next(maf1)
sys.stdout.write(default)
head = next(maf1)
header = head.rstrip('\n').split('\t')
# track length on first file header to create a spacer for unused fields
m1_len = len(header)
# will track positions of header in first maf, tack on other values at end for second maf
i = 0
for entry in header:
    head_dict[entry] = i
    i += 1
next(maf2)
head2 = next(maf2)
header2 = head2.rstrip('\n').split('\t')
j = 0
for entry in header2:
    if entry not in head_dict:
        header.append(entry)
    h2_dict[entry] = j
    j += 1
sys.stdout.write('\t'.join(header) + '\n')

spacer = ''
for i in xrange(0, len(header)-m1_len, 1):
    spacer = spacer + '\t'
for line in maf1:
    line = line.rstrip('\n')
    sys.stdout.write(line + spacer + '\n')
maf1.close()

for line in maf2:
    info = line.rstrip('\n').split('\t')
    diff = []
    sys.stdout.write(info[0])
    for i in xrange(1, len(header), 1):
        if header[i] in h2_dict:
            sys.stdout.write('\t' + info[h2_dict[header[i]]])
        else:
            sys.stdout.write('\t')
    #for i in xrange(1, len(header2), 1):
    #    if header2[i] not in head_dict:
    #        sys.stdout.write('\t' + info[i])
    print
maf2.close()