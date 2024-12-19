#!/usr/bin/env python

import argparse
import logging
import os
import sys

from beauris import Beauris

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


def main():
    """
    Submit a func_annot job with drmaa and wait for it to finish.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=str)
    args = parser.parse_args()

    bo = Beauris()
    org = bo.load_organism(args.infile)

    task_id = "func_annot_orson"

    exit_code_all = 0

    script_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '{}.sh'.format(task_id))

    for ass in org.assemblies:
        for annot in ass.annotations:
            job_args = [annot.get_derived_path('proteins_fa'), annot.get_derived_path('fixed_gff')]

            options = annot.get_task_options(task_id)
            cmd_options = []

            if 'hectar' in options and options['hectar']:
                cmd_options.append("--hectar_enable true")

            if 'hectar_type' in options:
                cmd_options.append("--hectar_type {}".format(options['hectar_type']))

            if cmd_options:
                job_args.append(" ".join(cmd_options))

            runner = bo.get_runner('drmaa', annot, task_id)
            add_script = []
            add_script.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'add_fa_description.py'))
            add_script.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'add_gff_description.py'))
            exit_code, stdout, stderr = runner.run_or_resume_job(script_path=script_path, job_args=job_args, additional_script=add_script)

            exit_code_all += exit_code

    if exit_code_all != 0:
        log.error('Some {} job failed with exit code {} for {}, see log above.'.format(task_id, exit_code_all, org.slug()))
    else:
        log.info('All {} jobs succeeded for {}.'.format(task_id, org.slug()))

    sys.exit(min(exit_code_all, 255))


if __name__ == '__main__':
    main()
