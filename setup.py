import os
import sys
import shutil
import getpass
import setuptools


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


__label__ = 'pipgh'
__description__ = 'Tool to install python packages from Github.'


if 'clean' in argv:
    shutil.rmtree('%s.egg-info' % __label__, ignore_errors=True)
    shutil.rmtree('build', ignore_errors=True)
    shutil.rmtree('dist', ignore_errors=True)
    shutil.rmtree('%s/__pycache__' % __label__, ignore_errors=True)
    shutil.rmtree('tests/__pycache__', ignore_errors=True)
    def pyclean(path):
        for root, drs, fns in os.walk(path):
            filtered_fns = filter(lambda f: f.endswith('.pyc'), fns)
            for fn in filtered_fns:
                _fn = os.path.join(root, fn)
                os.remove(_fn)
    pyclean(__label__)
    pyclean('tests')
    shutil.rmtree('.tox', ignore_errors=True)


setuptools.setup(
    name=__label__,
    description=__description__,
    author='Filipe Funenga',
    author_email='fmafunenga@gmail.com',
    url='https://github.com/ffunenga/%s' % __label__,
    license='MIT',
    packages=[__label__],
    test_suite = 'tests',
    entry_points = {
        'console_scripts' : [
            '{pkg} = {pkg}:main'.format(pkg=__label__)
        ]
    }
)
