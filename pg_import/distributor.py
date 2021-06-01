# -*- coding:utf-8 -*-

import os
import pg_import.pg_items as pi


class Distributor:
    item_types = {
        'extensions': pi.Extension,
        'languages': pi.Language,
        'servers': pi.Server,
        'schemas': pi.Schema,
        'types': pi.Type,
        'domains': pi.Domain,
        'sequences': pi.Sequence,
        'tables': pi.Table,
        'foreigntables': pi.ForeignTable,
        'functions': pi.Function,
        'procedures': pi.Procedure,
        'triggers': pi.Function,
        'operators': pi.Operator,
        'casts': pi.Cast,
        'aggregates': pi.Aggregate,
        'views': pi.View,
        'materializedviews': pi.MaterializedViews,
    }

    valid_top_dirs = [
        'casts',
        'extensions',
        'languages',
        'servers',
        'schemas'
    ]

    def __init__(self):
        self.items = {i: {} for i in self.item_types}

    def parse(self, src_dir):
        for abs_dir, dirs, files in os.walk(src_dir):
            dirs.sort()
            files.sort()
            rel_dir = os.path.relpath(abs_dir, src_dir)
            if not any(rel_dir.startswith(d) for d in self.valid_top_dirs):
                continue
            item_type = os.path.basename(rel_dir)
            if rel_dir.startswith('schemas/'):
                schema = rel_dir.split('/')[1]
            else:
                schema = None
            for f in files:
                item_name = os.path.splitext(f)[0]
                file_name = os.path.join(abs_dir, f)
                if (os.path.join('schemas', item_name) in rel_dir and
                   item_type == item_name):
                    item_type = 'schemas'
                if item_type in ['functions', 'triggers']:
                    item_name = f  # the same name and different languages
                self.items[item_type][(schema, item_name)] = \
                    self.item_types[item_type](self, file_name)

    def restore_pre_data(self, out_file):
        out_file.write('set check_function_bodies=off;\n')
        for item_type in self.item_types:
            for i in self.items[item_type].values():
                i.restore_structure(out_file)

    def restore_post_data(self, out_file):
        for i in self.items['tables'].values():
            i.restore_unique(out_file)
        for i in self.items['tables'].values():
            i.restore_post_data(out_file)
