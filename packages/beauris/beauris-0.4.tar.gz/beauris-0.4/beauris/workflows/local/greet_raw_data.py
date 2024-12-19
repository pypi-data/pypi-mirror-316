#!/usr/bin/env python

# Greet raw data from yml files
#   - download data if urls is specified
#   - unzip is needed
#   - check hash if needed

import argparse
import logging

from beauris import Beauris

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=str)
    args = parser.parse_args()

    bo = Beauris()
    org = bo.load_organism(args.infile)
    log.info("Greet raw data for %s" % org.slug())

    org.greet_raw_data(bo.downloaders)
