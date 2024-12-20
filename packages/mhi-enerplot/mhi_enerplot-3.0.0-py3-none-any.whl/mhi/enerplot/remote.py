#===============================================================================
# Enerplot Remotable objects
#===============================================================================

"""
Enerplot Remote Proxy
"""


#===============================================================================
# Imports
#===============================================================================

from __future__ import annotations

from typing import TYPE_CHECKING

# Allow modules to import rmi, rmi_property, requires and deprecated from here.
# pylint: disable=unused-import
from mhi.common.remote import Remotable as _Remotable
from mhi.common.remote import rmi, rmi_property, deprecated, requires
# pylint: enable=unused-import

if TYPE_CHECKING:
    from .application import Enerplot


#===============================================================================
# PSCAD Remotable
#===============================================================================

class Remotable(_Remotable):            # pylint: disable=too-few-public-methods
    """
    The Remote Proxy
    """

    # Treat all derived classes as being in the mhi.enerplot module
    _MODULE = "mhi.enerplot"


    @property
    def main(self) -> Enerplot:
        return self._context._main            # pylint: disable=protected-access
