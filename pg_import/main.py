import os
import sys
import argparse
from . import executor


def main():
    arg_parser = argparse.ArgumentParser(
                     description='Convert object files in plane postgres '
                                 'backup file for restore database',
                     epilog='Report bugs to <a.chernyakov@comagic.dev>.')
    section_def = \
        arg_parser.add_argument('--section',
                                action='append',
                                choices=['pre-data', 'data', 'post-data'])
    arg_parser.add_argument('src_dir',
                            help='directory with object files')
    arg_parser.add_argument('out_file',
                            nargs='?',
                            type=argparse.FileType('w'),
                            help='out file')
    args = arg_parser.parse_args()

    args.section = set(args.section or section_def.choices)
    args.out_file = args.out_file or sys.stdout

    if not os.access(args.src_dir, os.F_OK):
        arg_parser.error("Can not access to directory '%s'" % args.src_dir)

    executor.Executor(args.section, args.src_dir, args.out_file)()
