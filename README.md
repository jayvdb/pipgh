# pipgh

*pipgh* allows searching for Python packages on Github (GH) and installing
them directly. It further allows to specify a reference to a branch, a
release or a commit's hash value.

*pipgh* works with common HTTP GET requests. This simplicity makes it a
great solution to deploy software with dependencies available on github,
whithout the need to install a Version Control System client on the users'
system.

Pure Python code (2 and 3 compatible). No dependencies.

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

## Usage

    pipgh [--auth] search <query>...
    pipgh [--auth] show <full_name>
    pipgh install ( (<full_name> [<ref>]) | (-r <requirements.txt>) )
    pipgh [-h | --help]

## Commands

* `search` - Search Python packages in github.
* `install` - Download and install a package.
* `show` - Shows information from github about a repository.

## Options

* `-h | --help` - Shows this help message.
* `--auth` - Activates the use of HTTP basic authentication. Use this if the rate limit threshold is achieved.
