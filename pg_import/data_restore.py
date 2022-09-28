# -*- coding:utf-8 -*-

import os


class DataRestore:

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
                out_file.write(open(os.path.join(root, f)).read()+'\n')
