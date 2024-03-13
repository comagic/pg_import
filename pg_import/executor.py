import asyncio
import io
import re

import asyncpg

from pg_import.distributor import Distributor
from pg_import.data_restore import DataRestore


class Executor:
    """
    Class for running pg_import execution

    The aim of this class is to provide interface for re-using pg_import from
    other pyython code wihtout calling in directly from Shell

    section param: set of specificators for data processing. Available options:
        'pre-data', 'data', 'post-data'.
        * pre-data - process data for preparing DB for running
        * data - process default data for testing. (Can be skipped)
        * post-data - process data with constraints which will be applied after
                first two steps
    output param: way for output data of the exection pg_import. Possible
        options: File or stdout.
    src_dir param: directory with source files (i.e. repository with DB
        related data)
    """

    def __init__(self, section, schema, src_dir, output=None,
                 database=None, host=None, port=None, user=None, password=None,
                 rebuild=False, roles=None):
        assert section.issubset({'pre-data', 'data', 'post-data'})

        self.section = section
        self.src_dir = src_dir
        self.schema = schema
        self.database = database
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.rebuild = rebuild
        self.roles = roles
        if database:
            self.output = io.StringIO()
        else:
            self.output = output

    def __call__(self):
        if {'pre-data', 'post-data'} & self.section:
            d = Distributor()
            d.parse(self.src_dir, self.schema)

        if 'pre-data' in self.section:
            d.restore_pre_data(self.output)

        if 'data' in self.section:
            r = DataRestore(self.src_dir, self.schema)
            r.restore_all(self.output)

        if 'post-data' in self.section:
            d.restore_post_data(self.output)

        if self.database:
            self.build_database()

    def build_database(self):
        asyncio.run(self._build_database())

    @staticmethod
    def split_long_copy_command(src):
        def build_copy_cmd(header, strs):
            if strs:
                return header + '\n'.join(strs) + "\nEeOoFf$program$;"
            return ''

        start_copy_pattern = re.compile('^copy (.*) from stdin;$')
        cmds = []
        copy_data = []
        copy_data_within = False
        copy_header = None
        cur_len = 0
        for s in src.split('\n'):
            if copy_data_within:
                if s == '\\.':
                    copy_data_within = False
                    cmds.append(build_copy_cmd(copy_header, copy_data))
                    copy_data = []
                else:
                    s_len = len(s.encode('utf-8'))
                    if cur_len + s_len < 126 * 1024:
                        copy_data.append(s)
                        cur_len += s_len
                    else:
                        cmds.append(build_copy_cmd(copy_header, copy_data))
                        copy_data = [s]
                        cur_len = s_len

            elif start_copy_pattern.match(s):
                copy_header = s.replace(
                    "from stdin;",
                    'from program $program$cat <<"EeOoFf"\n'
                )
                copy_data_within = True
                cur_len = 0

            else:
                cmds.append(s)
        return '\n'.join(cmds)

    def get_sql(self):
        sql = self.output.getvalue()
        if 'data' in self.section:
            sql = self.split_long_copy_command(sql)
        return sql

    async def _connect(self, database=None) -> asyncpg.Connection:
        return await asyncpg.connect(
            database=database or self.database,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )

    async def _build_database(self):
        if self.rebuild:
            con = await self._connect('postgres')
            await con.execute(f'drop database if exists "{self.database}" (force)')
            await con.execute(f'create database "{self.database}"')
            if self.roles:
                await con.execute(self.roles.read())
            await con.close()

        sql = self.get_sql().strip()
        if sql:
            con = await self._connect()
            await con.execute(sql)
            await con.close()
