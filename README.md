# pipgh

> Why can't we use Github as a means to share our Python code directly?

*pipgh* searches and installs Python packages from Github. You can further
cite a specific branch, release or commit's hash value. This makes the
deployment of your Python package as simple as a commit to your repository.

It also allows to inspect the metadata of a repository or to
look at a singular field, which is very handy for stuff like this:

    $ git clone `pipgh show --clone-url docopt/docopt`

Pure Python code, without dependencies. 2 and 3 compatible.

###### Search

Search for individual packages:

    $ pipgh search requests
    Searching github.com for 'requests language:python'...
    kennethreitz/requests Python HTTP Requests for... (★:17198 f:2998 u:2016 Jan 22)
    requests/requests-oauthlib OAuthlib support for P... (★:517 f:146 u:2016 Jan 12)
    kennethreitz/grequests Requests + Gevent = <3 (★:1246 f:153 u:2015 Nov 21)
    requests/requests-ntlm NTLM authentication support ... (★:65 f:32 u:2015 Oct 31)
    bulkan/robotframework-requests Robot Framework keyw... (★:81 f:58 u:2016 Jan 13)
    (...)
    [2226 repositories were found, showing the first 30]
    $ pipgh search docopt
    (...)

Searching like this:

    $ pipgh search http async server

is equivalent to search

    http async server language:python

with your web-browser on github.com/search.

###### Install

Install a package from the latest commit on the master branch:

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

###### Show

Show a repository metadata and its README file with this:

    $ pipgh show docopt/docopt
    (...)
    $ pipgh show docopt/docopt | less   # also works

Or show a specific metadata field with:

    $ pipgh show --clone-url docopt/docopt

Which is useful to, for example, shortcut the git clone command:

    $ git clone `pipgh show --clone-url docopt/docopt`

## Usage

    pipgh [--auth] search <query>...
    pipgh [--auth] show [--<key>...] <full_name>
    pipgh install ( (<full_name> [<ref>]) | (-r <requirements.txt>) )
    pipgh [-h | --help | --version]

## Commands

* `search` - Search Python packages in github.
* `install` - Download and install a package.
* `show` - Shows information from github about a repository.

## Options

* `-h | --help` - Shows this help message.
* `--version` - Shows the current version number.
* `--auth` - Activates the use of HTTP basic authentication. Use this if the rate limit threshold is achieved.
