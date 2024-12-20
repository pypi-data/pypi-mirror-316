#===============================================================================
# Manitoba Hydro International / Power Technology Center
# Enerplot Automation Library
#===============================================================================
"""
Manitoba Hydro International

Enerplot Python Automation Library

Connect to already running application::

   import mhi.enerplot
   enerplot = mhi.enerplot.connect()
   enerplot.load_files('myproject')

Launch and connect to new application instance::

   import mhi.enerplot
   enerplot = mhi.enerplot.launch()
   enerplot.load_files('myproject')

Connect to application, launching a new instance if necessary::

   import mhi.enerplot
   enerplot = mhi.enerplot.application()
   enerplot.load_files('myproject')
"""

#===============================================================================
# Imports
#===============================================================================

import logging
import os
import sys

from typing import cast, List, Optional, Tuple, Union
from warnings import warn


#-------------------------------------------------------------------------------
# Submodules
#-------------------------------------------------------------------------------

import mhi.common
from mhi.common.remote import Context
from mhi.common import config

from .application import Enerplot
from .progress import Progress
from .trace import Trace
from .component import Component
from .book import Book, Sheet
from .annotation import Line, TextArea, GroupBox
from .graph import GraphFrame, PlotFrame, FFTFrame, GraphPanel, Curve
from .datafile import DataFile, MutableDataFile, Channel

# Enerplot 1.0 compatibility:
sys.modules['mhi.enerplot.common'] = sys.modules['mhi.common']


#===============================================================================
# Version Identifiers
#===============================================================================

_VERSION = (3, 0, 0)

_TYPE = 'f0'

VERSION = '.'.join(map(str, _VERSION)) + ('' if _TYPE == 'f0' else _TYPE)
VERSION_HEX = int.from_bytes((*_VERSION, int(_TYPE, 16)), byteorder='big')


#===============================================================================
# Logging
#===============================================================================

_LOG = logging.getLogger(__name__)


#===============================================================================
# Options
#===============================================================================

OPTIONS = config.fetch("~/.mhi.enerplot.py")


#===============================================================================
# Connection and Application Start
#===============================================================================

def application() -> Enerplot:
    """
    This method will find try to find a currently running Enerplot application,
    and connect to it.  If no running Enerplot application can be found, or
    if it is unable to connect to that application, a new Enerplot application
    will be launched and a connection will be made to it.

    If running inside a Python environment embedded within an Enerplot
    application, the containing application instance is always returned.

    Returns:
        Enerplot: The Enerplot application proxy object

    Example::

        import mhi.enerplot
        enerplot = mhi.enerplot.application()
        enerplot.load_files('myproject')
    """

    app_ = Context._application(connect, launch, 'Enerplot%.exe')   # pylint: disable=protected-access
    app = cast(Enerplot, app_)

    app._initialize()                         # pylint: disable=protected-access

    return app


def connect(host: Optional[str] = None, port: int = 0,
            timeout: int = 5) -> Enerplot:
    """
    This method will find try to find a currently running Enerplot application,
    and connect to it.

    Parameters:
        host (str): The host the Enerplot application is running on
            (defaults to the local host)

        port (int): The port to connect to.  Required if running multiple
            Enerplot instances.

        timeout (int): Seconds to wait for the connection to be accepted.

    Returns:
        Enerplot: The Enerplot application proxy object

    Example::

        import mhi.enerplot
        enerplot = mhi.enerplot.application()
        enerplot.load_files('myproject')
    """

    if port == 0:

        import socket                  # pylint: disable=import-outside-toplevel
        from mhi.common import process # pylint: disable=import-outside-toplevel

        if host is not None and not process.is_local_host(host):
            raise ValueError(f"Cannot autodetect port on foreign host {host!r}")

        listeners = process.listener_ports_by_name('Enerplot%')
        if not listeners:
            raise ProcessLookupError("No available Enerplot processes")

        if host is not None:
            listeners = list(filter(process.host_filter(host), listeners))
            if not listeners:
                raise ProcessLookupError("No matching Enerplot processes")

        host, port, pid, appname = listeners[0]
        _LOG.info("%s [%d] listening on [%s]:%d", appname, pid, host, port)
        if host in {'0.0.0.0', '::'}:
            host = socket.getfqdn()

    _LOG.info("Connecting to %s:%d", host, port)

    app_ = Context._connect(host=host, port=port, timeout=timeout) # pylint: disable=protected-access
    app = cast(Enerplot, app_)

    app._initialize()                         # pylint: disable=protected-access

    return app


def launch(port: Union[int,range] = 0,         # pylint: disable=too-many-locals
           silence: bool = True, timeout: int = 5,
           version: Optional[str] = None,
           minimum: Optional[str]='1.0', maximum: Optional[str] = None,
           address: Optional[str] = None,
           allow_alpha: Optional[bool] = None, allow_beta: bool = False,
           x64: bool = True,
           **options) -> Enerplot:

    """
    Launch a new Enerplot instance and return a connection to it.

    Parameters:
        port (int|range): The port to connect to.  Required if running multiple
            Enerplot instances.

        silence (bool): Suppresses dialogs which can block automation.

        timeout (int): Time (seconds) to wait for the connection to be
            accepted.

        version (str): Specific version to launch if multiple versions present.

        minimum (str): Minimum allowed version to run (default '1.0')

        maximum (str): Maximum allowed  version to run (default: unlimited)

        address (str): Interface address to bind PSCAD's automation server on

        **options: Additional keyword=value options

    Returns:
        Enerplot: The Enerplot application proxy object

    Example::

        import mhi.enerplot
        enerplot = mhi.enerplot.launch()
        enerplot.load_files('myproject')

    .. versionchanged:: 2.2.1
        added ``minimum``, ``maximum``, ``allow_alpha``, ``allow_beta``,
        ``x64`` parameters.
    .. versionchanged:: 2.6.1
        ``allow_alpha``, ``allow_beta`` parameters are no longer supported.
    .. versionchanged:: 3.0.0
        ``allow_beta`` parameter is supported again.
    """

    if allow_alpha is not None:
        warn("allow_alpha is no longer supported and will be removed",
             DeprecationWarning, stacklevel=2)


    from mhi.common import process     # pylint: disable=import-outside-toplevel

    options = dict(OPTIONS, **options) if OPTIONS else options

    args = ["{exe}", "/nologo", "/port:{port}"]

    if address is not None:
        args.append(f"/address:{address}")

    if not options.get('exe', None):
        options['exe'] = process.find_exe('Enerplot', version, x64, minimum,
                                          maximum, allow_beta=allow_beta)
        if not options['exe']:
            raise ValueError("Unable to find required version")

    if not port:
        port = options.get('port_range', None)
    if port is None or isinstance(port, range):
        port = process.unused_tcp_port(port)
        _LOG.info("Automation server port: %d", port)

    process.launch(*args, port=port, **options)

    host = None
    #connect_opts = {'port': port, 'timeout': timeout}
    if address is not None:
        from socket import getaddrinfo # pylint: disable=import-outside-toplevel

        for addr_info in getaddrinfo(address, port):
            addr = addr_info[4][0]
            if addr not in {'0.0.0.0', '::'}:
                #connect_opts['host'] = address
                host = address

    app = connect(host=host, port=port, timeout=timeout)

    if app and silence:
        app.silence = True

    return cast(Enerplot, app)



#===============================================================================
# Enerplot Versions
#===============================================================================

def versions() -> List[Tuple[str, bool]]:
    """
    Find the installed versions of Enerplot

    Returns:
        List[Tuple[str, bool]]: List of tuples of version string and 64-bit flag
    """

    from mhi.common import process     # pylint: disable=import-outside-toplevel

    return process.versions('Enerplot')
