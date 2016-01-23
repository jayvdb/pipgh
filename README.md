# pipgh

A tool to install python packages from Github.

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

###### Show

Take a look at a repository metadata and its README file with this:

    $ pipgh show docopt/docopt
    (...)
    $ pipgh show docopt/docopt | less   # also works

###### Install

Finally, install a package:

    $ pipgh install docopt/docopt
    Fetching files from 'docopt/docopt'...
    Installing python package 'docopt-0.6.1'...

Or install a list of packages from a file:

    $ cat requirements.txt
    docopt/docopt
    kennethreitz/requests
    $ pipgh install -r requirements.txt
    (...)

## Usage

    pipgh [--auth] search <query>...
    pipgh [--auth] show <full_name>
    pipgh [--auth] install (<full_name> | -r <requirements.txt>)
    pipgh [-h | --help]

## Commands

* `search` - Search python packages in github.
* `show` - Shows information from github about a repository.
* `install` - Download and install a package (from a github repository).

## Options

* `-h | --help` - Shows this help message.
* `--auth` - Activates the use of HTTP basic authentication. Use this when the rate limit threshold is achieved.
