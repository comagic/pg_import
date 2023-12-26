import os
import sys
import argparse
from . import executor


def main():
    arg_parser = argparse.ArgumentParser(
        description='Convert object files in plane postgres '
                    'backup file for restore database',
        epilog='Report bugs to <a.chernyakov@comagic.dev>.',
        conflict_handler='resolve'
    )
    section_def = arg_parser.add_argument('--section',
                                          action='append',
                                          choices=['pre-data', 'data', 'post-data'])
    arg_parser.add_argument('--schema')
    arg_parser.add_argument('-d', '--database',
                            type=str,
                            help='database name for build')
    arg_parser.add_argument('-h', '--host',
                            type=str,
                            help='host for connect db '
                                 '(env variable PG_HOST=<host>)')
    arg_parser.add_argument('-p', '--port',
                            type=str,
                            help='port for connect db '
                                 '(env variable PG_PORT=<port>)')
    arg_parser.add_argument('-U', '--user',
                            type=str,
                            help='user for connect db '
                                 '(env variable PG_USER=<user>)')
    arg_parser.add_argument('-W', '--password',
                            type=str,
                            help='password for connect db '
                                 '(env variable PG_PASSWORD=<password>)')
    arg_parser.add_argument('--rebuild',
                            action="store_true",
                            help='drop if exists / create database')
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

    executor.Executor(
        args.section, args.schema, args.src_dir, args.out_file,
        database=args.database,
        host=args.host,
        port=args.port,
        user=args.user,
        password=args.password,
        rebuild=args.rebuild
    )()
