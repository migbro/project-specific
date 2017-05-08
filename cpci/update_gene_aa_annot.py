#!/usr/bin/python
# Uses conversion table to update and standardized variant summary table gene/aa position calls
import sys
import re
import pdb

c_ind = {}
c_fh = open(sys.argv[1])

next(c_fh)

for line in c_fh:
    info = line.rstrip('\n').split('\t')
    tup = '\t'.join(info[3:7])
    c_ind[tup] = {}
    c_ind[tup]['gene'] = info[-1]
    c_ind[tup]['aa_pos'] = info[-2]
c_fh.close()

v_fh = open(sys.argv[2])
head = next(v_fh)
sys.stdout.write(head)

g_col = 2
aa_col = 14

sys.stdout.write('tup\told_gene\tnew_gene\told_aa_pos\tnew_aa_pos\tmulti-flag\n')

for line in v_fh:
    var = line.rstrip('\n').split('\t')
    tup = '\t'.join(var[3:7])
    # pdb.set_trace()
    if tup in c_ind:
        flag = 0
        cand = tup + '\t' + var[g_col]
        if var[g_col] != c_ind[tup]['gene']:
            var[g_col] = c_ind[tup]['gene']
            cand += '\t' + c_ind[tup]['gene']
            flag = 1
        else:
            cand += '\tNA'
        cand += '\t' + var[aa_col]
        new_pos = c_ind[tup]['aa_pos']
        m = re.match('([A-Z|-])(\d+)([A-Z|-]+)', var[aa_col])
        n = re.match('([A-Z|-]+)(\d+)-(\d+)([A-Z|-]+)', var[aa_col])
        if m:
            aa_r = m.group(1)
            old_pos = m.group(2)
            aa_a = m.group(3)
            # pdb.set_trace()
            if old_pos != new_pos:
                flag = 1
                new_aa = aa_r + new_pos + aa_a
                var[aa_col] = new_aa
                cand += '\t' + new_aa + '\tN\n'
        elif n:
            aa_r = n.group(1)
            old_pos = n.group(2)
            old_pos2 = n.group(3)
            aa_a = n.group(4)
            # pdb.set_trace()
            if new_pos != old_pos:
                flag = 1
                new_aa = aa_r + new_pos + '-' + str(int(new_pos) - int(old_pos) + int(old_pos2)) + aa_a
                cand += '\t' + new_aa + '\tY\n'

            else:
                cand += '\tNA\tN\n'
        if flag == 1:
            sys.stderr.write(cand)
    sys.stdout.write('\t'.join(var) + '\n')
