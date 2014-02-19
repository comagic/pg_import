# -*- coding:utf-8 -*-

import re
import os
import psycopg2
import psycopg2.extras

from pg_items import *

item_types = {
    'aggregates': Aggregate,
    'casts': Cast,
    'extensions': Extension,
    'foreigntables': ForeignTable,
    'functions': Function,
    'triggers': Function,
    'operators': Operator,
    'languages': Language,
    'SCHEMA': Schema,
    'servers': Server,
    'tables': Table,
    'types': Type,
    'usermappings': UserMapping,
    'views': View,
    'sequences': Sequence
}

class Distributor:
    def __init__(self):
        self.schemas = {}

    def parse(self, src_dir):
        src_dir = os.path.join(src_dir, 'schema')
        for root, dirs, files in os.walk(src_dir):
            rel_dir = os.path.relpath(root, src_dir)
            dir_name = os.path.basename(root)
            if os.path.relpath(root, src_dir) == '.':
                continue
            for f in files:
                if rel_dir == dir_name == f.split('.')[0]:
                    self.schemas[dir_name] = Schema(self, os.path.join(root, f))
                else:
                    item_name = f.split('.')[0]
                    item_type = dir_name
                    schema_name = rel_dir.split('/')[0]
                    self.schemas[schema_name].items[item_type][item_name] = item_types[item_type](self, os.path.join(root, f))
#        print self.schemas['public'].items['casts'].values()[0].data

    def restore_structure(self, out_file):
        out_file.write('set check_function_bodies=off;\n')
        for s in self.schemas.values():
            s.restore_structure(out_file)
        for c in self.schemas['public'].children:
            for s in self.schemas.values():
                for i in s.items[c].values():
                    i.restore_structure(out_file)

    def restore_complite(self, out_file):
        for s in self.schemas.values():
            s.restore_complite(out_file)
        for c in self.schemas['public'].children:
            for s in self.schemas.values():
                for i in s.items[c].values():
                    i.restore_complite(out_file)