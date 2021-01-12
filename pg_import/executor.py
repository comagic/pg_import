from pg_import.distributor import Distributor
from pg_import.data_restore import DataRestore


class Executor():
    '''
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

    '''

    def __init__(self, section, src_dir, output):
        assert section.issubset({'pre-data', 'data', 'post-data'})

        self.section = section
        self.output = output
        self.src_dir = src_dir

    def __call__(self):
        if set(['pre-data', 'post-data']) & self.section:
            d = Distributor()
            d.parse(self.src_dir)

        if 'pre-data' in self.section:
            d.restore_pre_data(self.output)

        if 'data' in self.section:
            r = DataRestore(self.src_dir)
            r.restore_all(self.output)

        if 'post-data' in self.section:
            d.restore_post_data(self.output)
