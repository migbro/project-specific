#!/usr/bin/env python

import sys
import os
import subprocess


def get_bnid(csv, names_ind):
    parts = csv.split('/')
    for part in parts:
        if part in names_ind:
            return names_ind[part]


def process_sample_sheet(csv, fparts):
    flow_id = ''
    lane = ''
    cur_id = fparts[0] + '_' + fparts[1]
    fh = open(csv)
    f = 0
    for info in fh:
        if f == 1:
            break
        stuff = info.rstrip('\n').split(',')
        if stuff[0] == 'Experiment Name':
            flow_id = stuff[1]
        elif stuff[0] == '[Data]':
            check = next(fh)
            test = check.split(',')
            if test[0] == 'Sample_ID':
                sys.stderr.write('No lane info for ' + csv + ', using default of 1\n')
                f = 1
                lane = '1'
            else:
                for lanes in fh:
                    check = lanes.split(',')
                    if check[1] == cur_id:
                        lane = check[0]
                        f = 1
                        break
    fh.close()
    return flow_id, lane


def create_links(names, flist, dest, dry):
    name_ind = {}
    if dry == 'y':
        sys.stderr.write('Dry run flag indicated, no links will be made\n')
    for line in open(names):
        info = line.rstrip('\n').split('\t')
        name_ind[info[0]] = info[1]
    for csv in open(flist):
        csv = csv.rstrip('\n')
        fn = os.path.basename(csv)
        fd = os.path.dirname(csv)
        fparts = fn.split('.')[1].split('_')
        bnid = get_bnid(csv, name_ind)
        dest_dir = dest + bnid
        # make dir to hold fastqs for current sample
        if not os.path.isdir(dest_dir):
            sys.stderr.write('Making destination dir ' + dest_dir + '\n')
            os.mkdir(dest_dir)
        (flow_id, lane) = process_sample_sheet(csv, fparts)
        fq1f = fd + '/' + '_'.join(fparts) + '_T_1.fastq.gz'
        if not os.path.isfile(fq1f):
            sys.stderr.write('Sample for ' + bnid + ' sheet ' + csv + ' does not conform. Check desired path ' + fq1f
                             + ' SKIPPING\n')
            continue
        fq1l = dest_dir + '/' + bnid + '_' + flow_id + '_' + lane + '_1_sequence.txt.gz'
        fq2f = fd + '/' + '_'.join(fparts) + '_T_2.fastq.gz'
        if not os.path.isfile(fq2f):
            sys.stderr.write('Sample for ' + bnid + ' sheet ' + csv + ' does not conform. Check desired path ' + fq1f
                             + ' SKIPPING\n')
            continue
        fq2l = dest_dir + '/' + bnid + '_' + flow_id + '_' + lane + '_2_sequence.txt.gz'
        link_file = 'ln ' + fq1f + ' ' + fq1l + '; sleep 2'
        sys.stderr.write('Creating hard link\n' + link_file + '\n')
        if dry != 'y':
            subprocess.call(link_file, shell=True)
        link_file = 'ln ' + fq2f + ' ' + fq2l
        sys.stderr.write('Creating hard link\n' + link_file + '\n')
        if dry != 'y':
            subprocess.call(link_file)
    sys.stderr.write('Fin!\n')


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Creates panel of normals for vcf, use somatic .')
    parser.add_argument('-i', '--index', action='store', dest='index',
                        help='List of sample conversion names: study\tbnid')
    parser.add_argument('-l', '--flist', action='store', dest='flist',
                        help='List of sample sheet with sample name in dir name')
    parser.add_argument('-d', '--dest', action='store', dest='dest',
                        help='Destination dir for hard links, like /cephfs/PROJECTS/PANCAN/RAW/')
    parser.add_argument('-f', '--dry', action='store', dest='dry',
                        help='Flag to do a dry run \'y\', use error output to determine if it would have worked')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    inputs = parser.parse_args()
    create_links(inputs.index, inputs.flist, inputs.dest, inputs.dry)