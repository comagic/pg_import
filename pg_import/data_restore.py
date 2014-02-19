# -*- coding:utf-8 -*-

import os
import psycopg2
import psycopg2.extras


class DataRestore:

    def __init__(self, db_connect):
        self.db_connect = db_connect

    def restore_all(self, root_dir):
        pass
