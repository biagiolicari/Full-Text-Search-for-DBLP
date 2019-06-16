from distutils.core import setup
import platform
import sys

if platform.python_version() < '3.6':
    sys.exit("Sorry, only Python 3.6 or > are supported (yet)")


setup(name='DBLP Full Text Search',
        version='1.0.0',
        description='GAVI',
        author='Gabriele Felici & Biagio Licari',
        license='MIT',
        packages=['index', 'query', 'ranking'],
        data_files=[('requirements', ['requirements.txt'])],
          )