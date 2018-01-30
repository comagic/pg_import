# -*- coding:utf-8 -*-

import os


class DataRestore:

    def __init__(self, src_dir):
        self.src_dir = src_dir

    def restore_all(self, out_file):
        src_dir = os.path.join(self.src_dir, 'data')
        for root, dirs, files in os.walk(src_dir):
            for f in files:
                out_file.write(open(os.path.join(root, f)).read()+'\n')
