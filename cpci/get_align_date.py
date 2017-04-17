#!/usr/bin/env python
import sys
import json
import subprocess
import pdb
import os

def get_stats_files(bnid, cont, obj, cont2):
    cmd = 'swift list ' + cont + ' --prefix ' + obj + '/' + bnid + '/ | grep .qc_stats.json'
    try:
        res = subprocess.check_output(cmd, shell=True)
    except:
        try:
            cmd = 'swift list ' + cont2 + ' --prefix ' + obj + '/' + bnid + '/ | grep .qc_stats.json'
            res = subprocess.check_output(cmd, shell=True)
        except:
            return None
    res = res.rstrip('\n')
    flist = res.split('\n')
    return flist

if len(sys.argv) != 5:
    sys.stderr.write('Usage: ' + sys.argv[0] + ' {container} {object} {bnid list} {cont2}\n')
    exit(1)

cont = sys.argv[1]
obj = sys.argv[2]
bid_list = sys.argv[3]
cont2 = sys.argv[4]

bfile = open(bid_list, 'r')
bdict = {}
for bnid in bfile:
    bnid = bnid.rstrip('\n')
    qc_list = get_stats_files(bnid, cont, obj, cont2)
    if qc_list is not  None:
        for fname in qc_list:
            dl_cmd = 'swift download ' + cont + ' ' + fname + ' >> errs.log 2>> errs.log'
            sys.stderr.write(dl_cmd + '\n')
            subprocess.call(dl_cmd, shell=True)
            if not os.path.isfile(fname):
                dl_cmd = 'swift download ' + cont2 + ' ' + fname + ' >> errs.log 2>> errs.log'
                sys.stderr.write('File in first container not found.  Trying another.\n' + dl_cmd + '\n')
                subprocess.call(dl_cmd, shell=True)
            try:
                qc_data = json.loads(open(fname, 'r').read())
                bdict[bnid] = qc_data['date_aligned']
            except:
                try:
                    bdict[bnid] = qc_data['align_date']
                except:
                    sys.stderr.write('No valid json found for bnid ' + bnid + ' file ' + fname + '\n')
    else:
        print sys.stderr.write(bnid + '\tno files found!  Try a different object name or container\n')
bfile.close()

print 'BID\tDate aligned'
for bnid in bdict:
    sys.stdout.write('\t'.join((bnid,bdict[bnid])) + '\n')
