import sys
import os


class DataRestore:
    ignore_files = {
        '.DS_Store'
    }

    def __init__(self, src_dir, schema):
        self.src_dir = src_dir
        self.schema = schema

    def restore_all(self, out_file):
        src_dir = os.path.join(self.src_dir, 'data')
        if self.schema:
            src_dir = os.path.join(src_dir, self.schema)
        for root, dirs, files in os.walk(src_dir):
            dirs.sort()
            files.sort()
            for f in files:
                if f in self.ignore_files:
                    continue
                file_name = os.path.join(root, f)
                try:
                    body = open(file_name).read()+'\n'
                except Exception:
                    print(
                        f'ERROR: Cannot read file {file_name}',
                        file=sys.stderr
                    )
                    raise
                out_file.write(body)
