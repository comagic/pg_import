import sys
import re


system_types = set([
    'integer',
    'bigint',
    'text',
    'character',
    'boolean',
    'timestamp',
    'date',
    'interval',
    'numeric',
    'float',
    'inet',
])


class PgObject(object):
    def __init__(self, parser, file_name):
        self.parser = parser
        self.depends = []
        self.data = open(file_name).read()
        self.post_data = ''
        self.is_restored_structure = False
        self.is_restored_complite = False

    def restore_structure(self, out_file):
        if not self.is_restored_structure:
            self.is_restored_structure = True
            for d in self.get_dependency():
                item = self.parser.items[d['type']].get(
                                                    (d['schema'], d['name']))
                if item is None:
                    print('WARNING: Resolve dependency: item not found:',
                          d, file=sys.stderr)
                    continue
                item.restore_structure(out_file)
            out_file.write(self.data + '\n\n')

    def get_dependency(self):
        res = []
        if '\n--depend on ' in self.data:
            for s in self.data.split('\n'):
                if s.startswith('--depend on '):
                    type, schema, name = re.match(
                        '--depend on (\\w*) (\\w*)\\.(\\w*)', s).groups()
                    res.append(
                        {'type': type+'s', 'schema': schema, 'name': name})
        return res


class Schema(PgObject):
    pass


class Table(PgObject):
    def __init__(self, parser, file_name):
        super(Table, self).__init__(parser, file_name)
        self.post_data = ';\n\n'.join(self.data.split(';\n\n')[1:]) + '\n\n'
        self.data = self.data.split(';\n\n')[0] + ';\n\n'
        self.unique = ''

        while 1:
            m = (re.match('.*(\n?alter table .* add constraint .*\n'
                          '  primary key[^\n]*;\n).*',
                          self.post_data, flags=re.S)
                 or
                 re.match('.*(\n?alter table .* add constraint .*\n'
                          '  unique[^\n]*;\n).*',
                          self.post_data, flags=re.S)
                 or
                 re.match('.*(\n?create unique index[^\n]*;\n).*',
                          self.post_data, flags=re.S))
            if m:
                m = m.groups()[0]
                self.post_data = self.post_data.replace(m, '')
                self.unique += m
            else:
                break

        table_name = (re.match('^create table (.*) \\(', self.data) or
                      re.match('^create unlogged table (.*) \\(', self.data)
                      ).groups()[0]
        for column in self.data.split('\n'):
            m = re.match('^  ([^ ]+) .* default (.*\\(.*\\)),?$', column)
            if m:
                column_name, func_def = m.groups()
                if (func_def != 'now()' and
                   not func_def.startswith('nextval')):
                    self.post_data += ('\n\nalter table %s alter column %s '
                                       'set default %s;' % (table_name,
                                                            column_name,
                                                            func_def))
                    self.data = self.data.replace('default %s' % func_def, '')

    def restore_unique(self, out_file):
        out_file.write(self.unique + '\n\n')

    def restore_post_data(self, out_file):
        out_file.write(self.post_data + '\n\n')

    def get_dependency(self):
        res = super(Table, self).get_dependency()
        parent = re.match('.*inherits \\(([^)]+)\\).*', self.data, flags=re.S)
        if parent:
            parent = parent.groups()[0]
            if '.' not in parent:
                parent = 'public.' + parent
            res.append({'type': 'tables',
                        'schema': parent.split('.')[0],
                        'name': parent.split('.')[1]})
        return res


class Aggregate(PgObject):
    pass


class Function(PgObject):
    pass


class Procedure(PgObject):
    pass


class Operator(PgObject):
    pass


class Sequence(PgObject):
    pass


class Type(PgObject):
    def get_dependency(self):
        res = []
        if re.match('^create type \S+ as \($', self.data.split('\n')[0]):
            for c in self.data.split('\n')[1:]:
                if c == ');':
                    break
                att_type = re.match('^  \S+ (\S+?)(\[.*|\(.*|,.*| with.*'
                                    '| varying.*)?$', c)
                if att_type:
                    att_type = att_type.groups()[0]
                else:
                    print('WARNING: cannot determine attribute type:', c,
                          file=sys.stderr)
                    continue
                if att_type in system_types:
                    continue
                if '.' in att_type:
                    att_schema, att_type = att_type.split('.')
                else:
                    att_schema = 'public'
                res.append({
                    'type': 'types',
                    'schema': att_schema,
                    'name': att_type,
                })
        return res


class Domain(PgObject):
    pass


class View(PgObject):
    pass


class MaterializedViews(PgObject):
    pass


class ForeignTable(PgObject):
    pass


class Cast(PgObject):
    pass


class Extension(PgObject):
    pass


class Language(PgObject):
    pass


class Server(PgObject):
    pass


class UserMapping(PgObject):
    pass
