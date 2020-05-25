# -*- coding:utf-8 -*-

import os
import pg_import.pg_items as pi

item_types = {
    'aggregates': pi.Aggregate,
    'casts': pi.Cast,
    'extensions': pi.Extension,
    'foreigntables': pi.ForeignTable,
    'functions': pi.Function,
    'procedures': pi.Procedure,
    'triggers': pi.Function,
    'operators': pi.Operator,
    'languages': pi.Language,
    'SCHEMA': pi.Schema,
    'servers': pi.Server,
    'tables': pi.Table,
    'types': pi.Type,
    'domains': pi.Domain,
    'usermappings': pi.UserMapping,
    'views': pi.View,
    'materializedviews': pi.MaterializedViews,
    'sequences': pi.Sequence
}


class Distributor:
    def __init__(self):
        self.schemas = {}

    def parse(self, src_dir):
        src_dir = os.path.join(src_dir, 'schema')
        for root, dirs, files in os.walk(src_dir):
            rel_dir = os.path.relpath(root, src_dir)
            dir_name = os.path.basename(root)
            if rel_dir == '.':
                continue
            for f in files:
                if rel_dir == dir_name == f.split('.')[0]:
                    self.schemas[dir_name] = pi.Schema(self,
                                                       os.path.join(root, f))
                else:
                    item_type = dir_name
                    if item_type == 'functions':
                        item_name = f
                    else:
                        item_name = f.split('.')[0]
                    schema_name = rel_dir.split('/')[0]
                    self.schemas[schema_name].items[item_type][item_name] = \
                        item_types[item_type](self, os.path.join(root, f))

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
