#!/usr/bin/env python
import os
import sys
import subprocess
import re
import time


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


def get_total_size(cont, oname):
    stat_cmd = 'swift stat ' + cont + ' ' + oname + ' | grep Length'
    res = subprocess.check_output(stat_cmd, shell=True)
    res = res.rstrip('\n')
    m = re.search('(\d+$)', res)
    return m.group(1)


def content_compare(novarc, cont, ldir, odir):
    fdict = {}
    source_novarc(novarc)
    list_cmd = 'swift list ' + cont + ' --long'
    sys.stderr.write(date_time() + 'Getting object list for container ' + cont + '\n')
    obj_list = subprocess.check_output(list_cmd, shell=True)
    i = 1
    mod = 1000
    res_out = odir + '/' + cont + '_results.txt'
    for fn in re.findall('(.*)\n', obj_list):
        m = re.search('\s*(\S+)\s+(\S+)\s+(\S+)\s+(\S+)', fn)
        (osize, odate, otime, oname) = (m.group(1), m.group(2), m.group(3), m.group(4))
        if i % mod == 0:
            sys.stderr.write(date_time() + 'Processing object ' + str(i) + ' ' + oname + '\n')
        if int(osize) == 0:
            osize = get_total_size(cont, oname)
        fdict[oname] = {}
        fdict[oname]['obj'] = osize
    sys.stderr.write(date_time() + 'Completed processing object data for ' + cont + ' checking local\n')
    i += 1
    flist_cmd = 'find ' + ldir + ' -type f -print0 | xargs -0 stat -c "%y %s %n"'
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
    sys.stderr.write(date_time() + 'Completed gathering file information, outputtting results\n')
    print 'File\tObject store size\tFile system size\tComment'
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
            print '\tWarning! File size/existence mismatch!'
        else:
            print '\tOK'


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
