import os
import sys
import shutil
import getpass
import setuptools

import pipgh


argv = ''.join(sys.argv[1:])


if 'test' in argv:
    _q = 'This command will run all test cases. Are you sure? [y/N] '
    try:
        answer = raw_input(_q)
    except NameError:
        answer = input(_q)
    if answer.strip().lower() != 'y':
        exit('')
    try:
        try:
            username = raw_input(u'Username: ')
        except NameError:
            username = input(u'Username: ')
        password = getpass.getpass(u'Password: ')
    except KeyboardInterrupt:
        exit('')
    os.environ['GH_AUTH_USER'] = username
    os.environ['GH_AUTH_PASS'] = password


if 'clean' in argv:
    shutil.rmtree('%s.egg-info' % pipgh.__name__, ignore_errors=True)
    shutil.rmtree('build', ignore_errors=True)
    shutil.rmtree('dist', ignore_errors=True)
    shutil.rmtree('%s/__pycache__' % pipgh.__name__, ignore_errors=True)
    shutil.rmtree('tests/__pycache__', ignore_errors=True)
    def pyclean(path):
        for root, drs, fns in os.walk(path):
            filtered_fns = filter(lambda f: f.endswith('.pyc'), fns)
            for fn in filtered_fns:
                _fn = os.path.join(root, fn)
                os.remove(_fn)
    pyclean(pipgh.__name__)
    pyclean('tests')
    shutil.rmtree('.tox', ignore_errors=True)


setuptools.setup(
    name=pipgh.__name__,
    description=pipgh.__description__,
    long_description=pipgh.__doc__,
    version=pipgh.__version__,
    author='Filipe Funenga',
    author_email='fmafunenga@gmail.com',
    url='https://github.com/ffunenga/%s' % pipgh.__name__,
    license='MIT',
    packages=[pipgh.__name__],
    test_suite = 'tests',
    entry_points = {
        'console_scripts' : [
            '{pkg} = {pkg}:main'.format(pkg=pipgh.__name__)
        ]
    }
)
