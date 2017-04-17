#!/usr/bin/env python
import sys
import json
import subprocess
import pdb

def get_stats_files(bnid, cont, obj):
    cmd = 'swift list ' + cont + ' --prefix ' + obj + '/' + bnid + '/ | grep .qc_stats.json'
    try:
        res = subprocess.check_output(cmd, shell=True)
    except:
        return None
    res = res.rstrip('\n')
    flist = res.split('\n')
    return flist


if len(sys.argv) == 1:
    sys.stderr.write('Usage: ' + sys.argv[0] + '{container}{object}{bnid list}{output file name}\n')
    exit(1)

cont = sys.argv[1]
obj = sys.argv[2]
bid_list = sys.argv[3]
out = sys.argv[4]


bfile = open(bid_list, 'r')
bdict = {}
for bnid in bfile:
    
    bnid = bnid.rstrip('\n')
    bdict[bnid] = {}
    bdict[bnid]['ct'] = 0
    bdict[bnid]['cov'] = 0.0
    qc_list = get_stats_files(bnid, cont, obj)
    if qc_list is not None:
        for fname in qc_list:
            dl_cmd = 'swift download ' + cont + ' ' + fname + ' >> ' + out + '.log'
            # pdb.set_trace()
            sys.stderr.write(dl_cmd + '\n')
            subprocess.call(dl_cmd, shell=True)
            try:
                qc_data = json.loads(open(fname, 'r').read())
            except:
                sys.stderr.write(fname + 'not found, skipping!\n')
                continue
            try:
                cov = qc_data['coverage']['V3_capture_t2']['average']
                bdict[bnid]['cov'] += float(cov)
                bdict[bnid]['ct'] += 1
            except:
                try:
                    cov = qc_data['coverage']['V2_capture_t2']['average']
                    bdict[bnid]['cov'] += float(cov)
                    bdict[bnid]['ct'] += 1
                except:
                    try:
                        cov = qc_data['coverage']['hg19']['average']
                        bdict[bnid]['cov'] += float(cov)
                        bdict[bnid]['ct'] += 1
                    except:
                        sys.stderr.write(bnid +'\t' + fname + '\tcould not nail down dict format to extract info\n')
                        try:
                            del bdict[bnid]
                        except:
                            pass
    else:
        print sys.stderr.write(bnid + '\tno files found!  Try a different object name or container\n')
        try:
            del bdict[bnid]
        except:
            pass
bfile.close()
out_fh = open(out + '.txt', 'w')
out_fh.write('BID\tTotal coverage\tAlign Count\n')
for bnid in bdict:
    out_fh.write('\t'.join((bnid,str(bdict[bnid]['cov']),str(bdict[bnid]['ct']))) + '\n')
