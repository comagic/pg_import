import re


class PgObject(object):
    children = []

    def __init__(self, parser, file_name):
        self.parser = parser
        self.items = {i: {} for i in self.children}
        self.depends = []
        self.data = open(file_name).read()
        self.post_data = ''
        self.is_restored_structure = False
        self.is_restored_complite = False

        if '\n--depend on ' in self.data:
            for s in self.data.split('\n'):
                if s.startswith('--depend on '):
                    type, schema, name = re.match(
                        '--depend on (\\w*) (\\w*)\\.(\\w*)', s).groups()
                    self.depends.append(
                        {'type': type+'s', 'schema': schema, 'name': name})

    def restore_structure(self, out_file):
        if not self.is_restored_structure:
            self.is_restored_structure = True
            for d in self.depends:
                self.parser.schemas[d['schema']].items[d['type']][d['name']].\
                    restore_structure(out_file)
            out_file.write(self.data + '\n\n')

    def restore_complite(self, out_file):
        if not self.is_restored_complite:
            self.is_restored_complite = True
            for d in self.depends:
                self.parser.schemas[d['schema']].items[d['type']][d['name']].\
                    restore_complite(out_file)
            if self.post_data:
                out_file.write(self.post_data + '\n\n')


class Schema(PgObject):
    children = ['extensions', 'languages', 'sequences', 'types', 'domains',
                'functions', 'procedures', 'operators', 'casts', 'aggregates',
                'tables', 'views', 'materializedviews', 'triggers', 'servers',
                'usermappings', 'foreigntables']


class Table(PgObject):
    def __init__(self, parser, file_name):
        super(Table, self).__init__(parser, file_name)
        self.post_data = ';\n\n'.join(self.data.split(';\n\n')[1:]) + '\n\n'
        self.data = self.data.split(';\n\n')[0] + ';\n\n'
        pk = re.match('.*(\n?alter table only.*\n    add '
                      'constraint .* primary key[^\n]*;\n).*',
                      self.post_data, flags=re.S)
        if pk:
            pk = pk.groups()[0]
            self.post_data = self.post_data.replace(pk, '')
            self.data += pk

        while 1:
            uni = re.match('.*(\n?create unique index[^\n]*;\n).*',
                           self.post_data, flags=re.S) or \
                  re.match('.*(\n?alter table only[^\n]*\n    '
                           'add constraint [^\n]* unique[^\n]*;\n).*',
                           self.post_data, flags=re.S)
            if uni:
                uni = uni.groups()[0]
                self.post_data = self.post_data.replace(uni, '')
                self.data += uni
            else:
                break


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
    pass


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
