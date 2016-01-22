# pipgh

A tool to install python packages from Github.

###### Search

Search for individual packages:

    $ pipgh search requests
    (...)
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
    (...)

Or install a list of packages from a file:

    $ cat requirements.txt
    docopt/docopt
    kennethreitz/requests
    $ pipgh show -r requirements.txt
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
