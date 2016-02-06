__version__ = '0.0.7a0'
__author__ = 'Filipe Funenga'
__license__ = 'MIT'
__lead__ = 'A tool to install python packages from Github.'
__description__ = __lead__ + """

    Why can't we use Github as a means to share our Python code directly?

*pipgh* searches and installs Python packages from Github. You can further
cite a specific branch, release or commit's hash value. This makes the
deployment of your Python package as simple as a commit to your repository.

It also allows to inspect the metadata of a repository or to
look at a singular field, which is very handy for stuff like this::

    $ git clone `pipgh show --clone-url docopt/docopt`

Pure Python code, without dependencies. 2 and 3 compatible.
"""

from .pipgh import USAGE_MESSAGE, HELP_MESSAGE
__doc__ = __description__+ u'\n' + USAGE_MESSAGE + u'\n' + HELP_MESSAGE
del USAGE_MESSAGE, HELP_MESSAGE

from .pipgh import main
from .pipgh import search
from .pipgh import install
from .pipgh import show
