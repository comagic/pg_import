## installation

```
pip install pg-import
```

## usage

```
usage: pg_import [--help] [--section {pre-data,data,post-data}] [--schema SCHEMA] [-d DATABASE] [-h HOST] [-p PORT] [-U USER] [-W PASSWORD] [-r ROLES] [--rebuild] [--refresh-sequence] src_dir [out_file]

Convert object files (pg-export format) in sequence of commands for restore database

positional arguments:
  src_dir               directory with object files
  out_file              out file

options:
  --help                show this help message and exit
  --section {pre-data,data,post-data}
  --schema SCHEMA
  -d DATABASE, --database DATABASE
                        database name for build
  -h HOST, --host HOST  host for connect db (env variable PG_HOST=<host>)
  -p PORT, --port PORT  port for connect db (env variable PG_PORT=<port>)
  -U USER, --user USER  user for connect db (env variable PG_USER=<user>)
  -W PASSWORD, --password PASSWORD
                        password for connect db (env variable PG_PASSWORD=<password>)
  -r ROLES, --roles ROLES
  --rebuild             drop if exists / create database
  --refresh-sequence    do setval() for all sequences by max(column)

Report bugs: https://github.com/comagic/pg_import/issues
```
