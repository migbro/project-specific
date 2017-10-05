#!/usr/bin/env python
import os
import sys
import subprocess
import re
import time
import pdb


def date_time():
    cur = ">" + time.strftime("%c") + '\n'
    return cur


def source_novarc(novarc):
    with open(novarc, 'r') as f:
        for line in f:
            k, v = line.rstrip().split('=')
            k = k.replace('export ', '')
            v = v.replace('"', '')
            os.environ[k] = v


def build_segs(cont):
    seg_cmd = 'swift list ' + cont + '_segments '
    temp = {}
    try:
        segs = subprocess.check_output(seg_cmd, shell=True)
        for seg in re.findall('(.*)\n', segs):
            parts = seg.split('/')
            cur = '/'.join(parts[0:(len(parts) - 4)])
            if cur not in temp:
                temp[cur] = parts[-3]
        return temp
    except:
        sys.stderr.write(date_time() + 'No segments found for container ' + cont + 'skipping!\n')
        return 0


def content_compare(novarc, cont, ldir, odir):
    fdict = {}
    source_novarc(novarc)
    list_cmd = 'swift list ' + cont + ' --long'
    sys.stderr.write(date_time() + 'Getting object list for container ' + cont + '\n')
    obj_list = subprocess.check_output(list_cmd, shell=True)
    i = 1
    mod = 1000
    res_out = open(odir + '/' + cont + '_results.txt', 'w')
    sys.stderr.write(date_time() + 'Building segments dict\n')
    big_obj_dict = build_segs(cont)
    sys.stderr.write(date_time() + 'Segments processed, parsing object data\n')
    for fn in re.findall('(.*)\n', obj_list):
        try:
            # added extra space grouping since version 3.3 has it, would have to remove for v2.6
            m = re.search('\s*(\S+)\s+(\S+)\s+(\S+)\s+\S+\s+(\S+)', fn)
            (osize, odate, otime, oname) = (m.group(1), m.group(2), m.group(3), m.group(4))
            if i % mod == 0:
                sys.stderr.write(date_time() + 'Processing object ' + str(i) + ' ' + oname + '\n')
            if int(osize) == 0 and isinstance(big_obj_dict, dict):
                try:
                    osize = big_obj_dict[oname]
                except:
                    sys.stderr.write('File ' + oname + ' appears to be actually empty.  Leaving size as 0!\n')
            fdict[oname] = {}
            fdict[oname]['obj'] = osize
        except:
            sys.stderr.write('Encountered an error processing object ' + fn + ' skipped!\n')
    sys.stderr.write(date_time() + 'Completed processing object data for ' + cont + ' checking local\n')
    i += 1
    flist_cmd = 'find ' + ldir + ' -type f -print0 | xargs -0 stat -c "%s %n"'
    file_list = subprocess.check_output(flist_cmd, shell=True)
    i = 1
    mod = 1000
    for fn in re.findall('(.*)\n', file_list):
        m = re.search('\s*(\S+)\s+(\S+)', fn)
        (fsize, fname) = (m.group(1), m.group(2))
        fname = fname.lstrip(ldir + '/')
        if i % mod == 0:
            sys.stderr.write(date_time() + 'Processing file ' + str(i) + ' ' + fname + '\n')
        if fname not in fdict:
            fdict[fname] = {}
        fdict[fname]['fs'] = fsize
        i += 1
    sys.stderr.write(date_time() + 'Completed gathering file information, outputting results\n')
    res_out.write('File\tObject store size\tFile system size\tComment\n')
    for fn in fdict:
        res_out.write(fn)

        (osize, fsize) = ('0', '0')
        if 'obj' not in fdict[fn]:
            res_out.write('\tNA')
        else:
            osize = fdict[fn]['obj']
            res_out.write('\t' + osize)
        if 'fs' not in fdict[fn]:
            res_out.write('\tNA')
        else:
            fsize = fdict[fn]['fs']
            res_out.write('\t' + fsize)
        if osize != fsize:
            res_out.write('\tWarning! File size/existence mismatch!\n')
        else:
            res_out.write('\tOK')
    res_out.close()
    sys.stderr.write('Fin!\n')


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Compares object store container contents versus local copy.')
    parser.add_argument('-n', '--novarc', action='store', dest='novarc',
                        help='.novarc file to use for swift')
    parser.add_argument('-c', '--container', action='store', dest='cont',
                        help='Object store container to check')
    parser.add_argument('-d', '--directory', action='store', dest='ldir',
                        help='Local directory to check against')
    parser.add_argument('-o', '--output', action='store', dest='odir',
                        help='Output directory to put result table and warning log')

    if len(sys.argv) == 1:
        parser.print_help()
        exit(1)

    inputs = parser.parse_args()
    (novarc, cont, ldir, odir) = (inputs.novarc, inputs.cont, inputs.ldir, inputs.odir)
    content_compare(novarc, cont, ldir, odir)
