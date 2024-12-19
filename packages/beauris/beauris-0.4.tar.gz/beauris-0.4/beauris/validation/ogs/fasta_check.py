#!/usr/bin/env python

# Check that a genome fasta file is ready for release

import argparse
import logging
import re

from Bio import SeqIO

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=str)
    parser.add_argument('--max_contigs', type=int, help="Raise a warning if fasta has more thant given number of contigs/scaffolds")
    args = parser.parse_args()

    log.info("Checking fasta {}".format(args.infile))

    pattern = re.compile("^[A-Za-z0-9-_.]+$")

    fragments = 0

    for record in SeqIO.parse(args.infile, "fasta"):
        if not pattern.match(record.id):
            raise RuntimeError("Invalid fasta header: {}".format(record.id))
        if args.max_contigs:
            fragments += 1

    if args.max_contigs and fragments > args.max_contigs:
        raise RuntimeError("Fragmented assembly, sequence number >{}".format(args.max_contigs))

    with open(args.infile, 'r') as f:
        for line in f:
            if len(line) > 200:
                raise RuntimeError("Fasta line contains more than 200 characters:")
