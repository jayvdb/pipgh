from __future__ import print_function
import os
import platform
import sys
import json
import datetime
import getpass
import base64
import shutil
import zipfile
import subprocess
try:
    from urllib.parse import urlencode
    from urllib.request import urlopen, urlretrieve
except ImportError:
    from urllib import urlencode, urlretrieve
    from urllib2 import urlopen


__version__ = '0.0.2'
__description__ = 'A tool to install python packages from Github.'
__author__ = 'Filipe Funenga'
__license__ = 'MIT'


def authenticate(top_level_url=u'https://api.github.com'):
    try:
        if 'GH_AUTH_USER' not in os.environ:
            try:
                username =  raw_input(u'Username: ')
            except NameError:
                username =  input(u'Username: ')
        else:
            username = os.environ['GH_AUTH_USER']
        if 'GH_AUTH_PASS' not in os.environ:
            password = getpass.getpass(u'Password: ')
        else:
            password = os.environ['GH_AUTH_USER']
    except KeyboardInterrupt:
        sys.exit(u'')
    try:
        import urllib.request as urllib_alias
    except ImportError:
        import urllib2 as urllib_alias
    password_mgr = urllib_alias.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, top_level_url, username, password)
    handler = urllib_alias.HTTPBasicAuthHandler(password_mgr)
    opener = urllib_alias.build_opener(handler)
    urllib_alias.install_opener(opener)


def test_color_support():
    is_ansi = os.environ.get('TERM', '') == 'ANSI'
    for handle in [sys.stdout, sys.stderr]:
        isatty = hasattr(handle, 'isatty') and handle.isatty()
        if isatty or is_ansi:
            is_windows = platform.system() == 'Windows'
            if is_windows and not is_ansi:
                return False
            else:
                return True
        return False


def force_unicode(s):
    try:
        return unicode(s)
    except NameError:
        return str(s)
normalize = lambda s: u'' if s == None else force_unicode(s)
color_support = test_color_support()
colorize = lambda i, s: (normalize(s) if not color_support
                                      else (i + normalize(s) + u'\033[0m'))
header = lambda s: colorize(u'\033[95m', s)
okblue = lambda s: colorize(u'\033[94m', s)
okgreen = lambda s: colorize(u'\033[92m', s)
warning = lambda s: colorize(u'\033[93m', s)
fail = lambda s: colorize(u'\033[91m', s)
bold = lambda s: colorize(u'\033[1m', s)
underline = lambda s: colorize(u'\033[4m', s)


class URLOpenContext:

    def __init__(self, url):
        self.url = url

    def __enter__(self):
        self.f = urlopen(self.url)
        return self.f

    def __exit__(self, *args):
        self.f.close()


def search(auth_flag, argv, output=True):
    if len(argv) < 2 or argv[0] != 'search':
        sys.exit('usage: pipgh search <query>...')
    params = {u'q': u' '.join(argv[1:]) + u' language:python',
              u'stars': u'stars'}
    url = u'https://api.github.com/search/repositories'
    if auth_flag:
        authenticate(url)
    url += u'?' + urlencode(params)
    if output:
        print(u"Searching github.com for '%s'..." % header(params[u'q']))
    with URLOpenContext(url) as conn:
        try:
            headers = conn.getheaders()
        except AttributeError:
            headers = conn.headers.dict
        response = conn.read().decode('utf-8')
        response = json.loads(response)
    #print(json.dumps(response['items'][0], indent=4))
    maxlen = 0
    description_lens = []
    lines = []
    for item in response['items']:
        label = normalize(item['full_name'])
        description = normalize(item['description'])
        nstars = item['stargazers_count']
        nforks = item['forks_count']
        last_update = datetime.datetime.strptime(
                item['pushed_at'], u'%Y-%m-%dT%H:%M:%SZ')
        last_update = last_update.strftime(u'%Y %b %d')
        stats = u'(\u2605:{} f:{} u:{})'
        stats = stats.format(nstars, nforks, last_update)
        line = (label, description, stats)
        lines.append(line)
        maxlen = max(maxlen, len(" ".join(line)))
        description_lens.append(len(" ".join([label, stats])))
    maxlen = min(maxlen, 76)
    for line, dlen in zip(lines, description_lens):
        label, description, stats = line
        dlen = maxlen - dlen
        description = (description if len(description) < dlen
                                   else (description[:dlen] + u'...'))
        if output:
            print(okblue(label), bold(description), stats)
    total_count = response['total_count']
    phrase = {1: u'repository was'}.get(total_count, u'repositories were')
    nitems = len(response['items'])
    showing = {nitems: u''}.get(total_count, u', showing the first %d' % nitems)
    if output:
        print(u'[%d %s found%s]' % (total_count, phrase, showing))
    return total_count, lines


class ShowNode(object):

    def __init__(self, node, level=0):
        self.level = level
        def is_str(s):
            try:
                return type(s) == unicode
            except NameError:
                return type(s) == str
        _test = lambda i: (type(i[1]) == dict or
                           (type(i[1]) != dict and
                            not normalize(i[1]).startswith('http')))
        self.children = [n for n in node.items()]  # if _test(n)]
        self.children.sort(key=lambda i: i[0])

    def __str__(self):
        indent = self.level * u' '
        items = []
        for key, value in self.children:
            if type(value) == dict:
                value = ShowNode(value, self.level + 4)
                items.append(u'%s%s:\n%s\n' % (indent, okblue(key), value))
            else:
                items.append(u'%s%s: %s\n' % (indent, okblue(key), value))
        rst = u''.join(items).strip()
        return rst


def show(auth_flag, argv, output=True):
    if len(argv) != 2 or argv[0] != 'show':
        sys.exit('usage: pipgh show <full_name>...')
    url = u'https://api.github.com/repos'
    if auth_flag:
        authenticate(url)
    url += '/' + argv[1]
    if output:
        print(u"Fetching '%s' information..." % header(argv[1]), file=sys.stderr)
    with URLOpenContext(url) as conn:
        try:
            headers = conn.getheaders()
        except AttributeError:
            headers = conn.headers.dict
        response = conn.read().decode('utf-8')
        response = json.loads(response)
    url += '/readme'
    if output:
        print(u"Fetching %s..." % header('readme'), file=sys.stderr)
    try:
        with URLOpenContext(url) as conn:
            readme = conn.read().decode('utf-8')
            readme = json.loads(readme)['content']
    except:
        readme = u''
    root = ShowNode(response)
    try:
        if output:
            print(root)
    except UnicodeEncodeError:
        if output:
            print(root.__str__().encode('utf-8'))
    if sys.version_info < (3, 0, 0):
        readme = base64.decodestring(readme)
    else:
        readme = base64.decodebytes(readme.encode('utf-8')).decode('utf-8')
    if output:
        print(readme)
    return response, readme


class TempDirContext:

    def __init__(self, path):
        self.path = path
        self.parent_dir = os.getcwd()

    def __enter__(self):
        try:
            os.mkdir(self.path)
        except OSError as e:
            if e.errno != 17:  # File exists
                raise
            shutil.rmtree(self.path)
            os.mkdir(self.path)
        finally:
            os.chdir(self.path)
        return self

    def __exit__(self, *args):
        os.chdir(self.parent_dir)
        try:
            shutil.rmtree(self.path)
        except:
            pass


def unzip(zipfilename, destination):
    with zipfile.ZipFile(zipfilename) as zf:
        zf.extractall(destination)
    for root, ds, fs in os.walk('.'):
        if root == '.':
            root_dir = os.path.join(root, ds[0])
            ini_strip = len(root_dir) + 1
            continue
        target = root[ini_strip:]
        for d in ds:
            source = os.path.join(root, d)
            destination = os.path.join(target, d)
            shutil.move(source, destination)
        for f in fs:
            source = os.path.join(root, f)
            destination = os.path.join(target, f)
            shutil.move(source, destination)
        if root != root_dir:
            break
    shutil.rmtree(root_dir)


def install_one_package(repo_label, ref=None):
    ref = ref if ref != None else 'master'
    url = "https://github.com/{}/archive/{}.zip".format(repo_label, ref)
    with TempDirContext(".pygh") as cwd:
        _info = u"Fetching files from '%s'..." % header(repo_label)
        print(_info, file=sys.stderr)
        urlretrieve(url, 'distro.zip')
        unzip('distro.zip', '.')
        args = ['python', 'setup.py', '--fullname']
        full_name = subprocess.check_output(args).decode('utf-8').strip()
        _info = u"Installing python package '%s'..." % header(full_name)
        print(_info, file=sys.stderr)
        args = ['python', 'setup.py', 'install']
        with open(os.devnull, 'wb') as shutup:
            return_code = subprocess.check_call(
                    args, stdout=shutup, stderr=shutup)
        if return_code != 0:
            _fmt = u'%s: installation failed with code %d'
            sys.exit(_fmt % (fail('Error'), return_code))


def install(auth_flag, argv, dry_run=False):
    # pipgh install <full_name>             2
    # pipgh install <full_name> <ref>       3
    # pipgh install -r <requirements.txt>   3
    _err = ('usage: pipgh install '
            '( (<full_name> [<ref>]) | (-r <requirements.txt>) )')
    if len(argv) not in [2, 3] or argv[0] != 'install' or auth_flag != False:
        sys.exit(_err)
    if argv[1] == '-r' and len(argv) != 3:
        sys.exit(_err)
    if len(argv) == 3:
        if argv[1] == '-r':
            try:
                with open(argv[2]) as f:
                    lines = [l.strip() for l in f.readlines()]
            except FileNotFoundError as e:
                sys.exit(e)
            else:
                lines = [l.split() for l in lines if l != '']
                lines = [(l if len(l) == 2 else (l[0], None)) for l in lines]
                repo_labels, refs = zip(*lines)
                repo_labels, refs = list(repo_labels), list(refs)
        else:
            repo_labels = [argv[1]]
            refs = [argv[2]]
    elif len(argv) == 2:
        if argv[0] != 'install' or argv[1] == '-r':
            sys.exit(_err)
        repo_labels = [argv[1]]
        refs = [None]

    if dry_run:
        return repo_labels, refs
    for repo_label, ref in zip(repo_labels, refs):
        install_one_package(repo_label, ref)


USAGE_MESSAGE = u"""\
Usage: pipgh [--auth] search <query>...
       pipgh [--auth] show <full_name>
       pipgh install ( (<full_name> [<ref>]) | (-r <requirements.txt>) )
       pipgh [-h | --help]
""".format(file=__file__)


HELP_MESSAGE = u"""\
A tool to install python packages from Github.

Commands:
    search   Search Python packages in github.
    install  Download and install a package.
    show     Shows information from github about a repository.

Options:
    -h | --help  Shows this help message.
    --auth       Activates the use of HTTP basic authentication when
                 communicating with api.github.com. Use this if the rate
                 limit threshold is achieved.

Examples:
    SEARCH for individual packages:

        $ pipgh search requests
        (...)
        $ pipgh search docopt
        (...)

    Searching like this:

        $ pipgh search http async server

    is equivalent to search

        http async server language:python

    with your web-browser on github.com/search.

    INSTALL a package from the latest commit on the master branch:

        $ pipgh install docopt/docopt
        Fetching files from 'docopt/docopt'...
        Installing python package 'docopt-0.6.1'...

    Install a specific version of the code using a reference (e.g. release,
    commit's hash value or branch):

        $ pipgh install kennethreitz/requests v2.9.1
        $ pipgh install mitsuhiko/flask 23cf923c7c2e4a3808e6c71b6faa34d1749d4cb6
        $ pipgh install tornadoweb/tornado stable

    Or install a list of packages from a file:

        $ cat requirements.txt
        docopt/docopt 0.6.2
        kennethreitz/requests
        $ pipgh install -r requirements.txt
        (...)

    SHOW a repository metadata and its README file with this:

        $ pipgh show docopt/docopt
        (...)
        $ pipgh show docopt/docopt | less   # also works
""".format(file=__file__)


__doc__ = USAGE_MESSAGE + u'\n' + HELP_MESSAGE


def main(argv=sys.argv[1:], dry_run=False):
    commands = {'search': search, 'show': show, 'install': install}
    def _abort(unknown_cmd=None):
        if unknown_cmd != None:
            help_msg = u'error: command "%s" is unknown.' % unknown_cmd
            help_msg += '\n' + USAGE_MESSAGE.rstrip()
        else:
            help_msg = __doc__
        sys.exit(help_msg)
    # pipgh
    # pipgh -h
    # pipgh --help
    no_args = len(argv) == 0
    get_help = len(argv) == 1 and argv[0] in ['-h', '--help']
    if no_args or get_help:
        _abort()
    # pipgh show <full_name>                2
    # pipgh install <full_name>             2
    # pipgh search <query>...               2+
    # pipgh install <full_name> <ref>       3
    # pipgh install -r <requirements.txt>   3
    # pipgh --auth show <full_name>         3
    # pipgh --auth search <query>...        3+
    if len(argv) < 2 or argv[0] not in ['show', 'install', 'search', '--auth']:
        _abort(unknown_cmd=argv[0])
    if argv[0] == '--auth':
        if len(argv) < 3 or argv[1] not in ['show', 'search']:
            _abort(unknown_cmd=argv[1])
        key = argv[1]
        auth_flag = True
        argv = argv[1:]
    else:
        key = argv[0]
        auth_flag = False
        argv = argv
    if dry_run:
        return key, auth_flag, argv
    commands[key](auth_flag, argv)


if __name__ == "__main__":
    main()
