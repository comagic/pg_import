usage: pg_import [-h] [--section {pre-data,data,post-data}] src_dir [out_file]

Convert object files in plane postgres backup file for restore database

positional arguments:
  src_dir               directory with object files
  out_file              out file

optional arguments:
  -h, --help            show this help message and exit
  --section {pre-data,data,post-data}
