import os

from distutils.core import setup

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()

def get_packages(dirs):
    packages = []
    for dir in dirs:
        for dirpath, dirnames, filenames in os.walk(dir):
            if '__init__.py' in filenames:
                packages.append(dirpath)
    return packages

setup(name = "pg_import",
      description="repo -> pg_dump",
      license="""uiscom license""",
      version = "0.2",
      maintainer = "Dima Beloborodov",
      maintainer_email = "d.beloborodov@ulab.ru",
      url = "http://uiscom.ru",
      scripts = ['bin/pg_import'],
      packages = get_packages(['pg_import']))
