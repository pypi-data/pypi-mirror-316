#!/usr/bin/env python

# Check that a bigwig file is ready for release

import argparse
import logging


logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('bigwigfile', type=str)
    parser.add_argument('genome', type=str)
    args = parser.parse_args()

    log.info("Checking bigwig file {} against genome {}".format(args.bigwigfile, args.genome))
    log.info("Skipping checks for now")
