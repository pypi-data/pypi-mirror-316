"""
Enerplot Component
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple, TYPE_CHECKING

from .command import Command
from .remote import Remotable, rmi, rmi_property

if TYPE_CHECKING:
    from .book import Book, Sheet


#===============================================================================
# Enerplot Component
#===============================================================================

class Component(Remotable):

    """
    The base type for all Enerplot components.

    Include graph frames, dividers, and sticky notes
    """

    #---------------------------------------------------------------------------
    # Identity
    #---------------------------------------------------------------------------

    @property
    def id(self) -> str:
        """The id of the component (read-only)"""

        return self._identity['id']


    @property
    def book_name(self) -> str:
        """The book the component belongs to (read-only)"""

        return self._identity['book']


    @property
    def book(self) -> Book:
        """The book the component belongs to (read-only)"""

        return self.main.book(self.book_name)


    @rmi_property
    def classid(self) -> str:                         # type: ignore[empty-body]
        """The classid of the component (read-only)"""


    #---------------------------------------------------------------------------
    # Hierarchy
    #---------------------------------------------------------------------------

    @rmi
    def parent(self) -> Sheet:                        # type: ignore[empty-body]
        """Retrieve the owner of this component"""


    #---------------------------------------------------------------------------
    # Attributes
    #---------------------------------------------------------------------------

    @rmi
    def attributes(self, **kwargs) -> Dict[str, Any]: # type: ignore[empty-body]
        """
        Set or get a component's attributes

        A component's attributes are used to describe the component's
        location and size relative to its parent.

        Parameters:
            **kwargs: key=value arguments

        Returns:
            dict: The component's current attributes.

        See also:
            :meth:`properties`
        """


    def _extents(self, **kwargs):

        args = sum(v is not None for v in kwargs.values())
        if args == 0:
            attr = self.attributes()
            return tuple(attr[key] for key in kwargs)
        if args != len(kwargs):
            raise ValueError("Specify all arguments, or no arguments")
        if any(v <= 0 for v in kwargs.values()):
            raise ValueError("All values must be positive")

        return self.attributes(**kwargs)


    def position(self,
                 x: Optional[int] = None, y: Optional[int] = None
                 ) -> Optional[Tuple[int, int]]:
        """
        Get or set the component's position.

        If the x & y parameters are given, the position is set.
        If they are omitted, the current position is returned.

        Parameters:
            x (int): The component's new x location on the sheet
            y (int): The component's new y location on the sheet

        Returns:
            Tuple[x,y]: The current location of the component
        """

        return self._extents(x=x, y=y)


    def size(self,
             width: Optional[int] = None, height: Optional[int] = None
             ) -> Optional[Tuple[int, int]]:
        """
        Get or set the component's size

        If the width & height parameters are given, the size is set.
        If they are omitted, the current size is returned.

        Parameters:
            width (int): The component's new width
            height (int): The component's new height

        Returns:
            Tuple[width, height]: The current size of the component
        """

        return self._extents(w=width, h=height)


    def extents(self,
                x: Optional[int] = None, y: Optional[int] = None,
                width: Optional[int] = None, height: Optional[int] = None
                ) -> Optional[Tuple[int, int, int, int]]:
        """
        Get or set the component's position and size

        If all parameters are given, the position and size is set.
        If all parameters are omitted, the current extents are returned.

        Parameters:
            x (int): The component's new x location on the sheet
            y (int): The component's new y location on the sheet
            width (int): The component's new width
            height (int): The component's new height

        Returns:
            Tuple[x,y,width,height]: The current extents of the component
        """

        return self._extents(x=x, y=y, w=width, h=height)


    #---------------------------------------------------------------------------
    # Properties
    #---------------------------------------------------------------------------

    @rmi
    def _properties(self, paramlist, **kwargs):
        """Set/Get parameters"""


    @staticmethod
    def _app_val(val):
        if isinstance(val, bool):
            return 'true' if val else 'false'
        return str(val)


    def properties(self, paramlist: str = '', **kwargs) -> Dict[str, Any]:
        """
        Set or get a component's properties

        A component's properties are used to describe the component's
        appearance or control the component's behaviour.

        Parameters:
            **kwargs: key=value arguments

        Returns:
            dict: The component's current property values

        See also:
            :meth:`attributes`
        """

        codecs = self._codecs()

        if kwargs:
            kwargs = { key.replace('̵','-'): val for key, val in kwargs.items()
                       if val is not None }
            for codec in codecs:
                kwargs = codec.encode_all(kwargs)
            kwargs = { key: Component._app_val(val)
                       for key, val in kwargs.items() if val is not None }

            params = self._properties(paramlist, **kwargs)

        else:
            params = self._properties(paramlist)
            for codec in codecs:
                params = codec.decode_all(params)

        return params


    def __setitem__(self, key: str, item):
        self.properties('', **{key: item})


    def __getitem__(self, key: str):
        return self.properties('')[key]


    def _codecs(self):
        return ()


    #---------------------------------------------------------------------------
    # Commands
    #---------------------------------------------------------------------------

    @rmi
    def _command(self, cmd_id: int) -> None:
        """
        Send a generic command to the component

        Parameters:
            cmd_id (int): The command number
        """


    def _generic_command(self, command: Command) -> None:
        """
        Send a generic command to the component

        Parameters:
            command (enum): The enumerated command identifier
        """

        self._command(command.value)


    def copy_as_metafile(self) -> None:
        """
        Copy component to clipboard as a metafile
        """

        self._generic_command(Command.COPY_AS_METAFILE)


    def copy_as_bitmap(self) -> None:
        """
        Copy component to clipboard as a bitmap
        """

        self._generic_command(Command.COPY_AS_BITMAP)


    def cut(self) -> None:
        """
        Remove the component to the clipboard
        """

        self._generic_command(Command.IDZ_CMP_CUT)


    def copy(self) -> None:
        """
        Copy the component to the clipboard
        """

        self._generic_command(Command.IDZ_CMP_COPY)


    def paste(self) -> None:
        """
        Paste the component(s) from the clipboard to this canvas
        """

        self._generic_command(Command.IDZ_CMP_PASTE)


    #---------------------------------------------------------------------------
    # Container functions
    #---------------------------------------------------------------------------

    @rmi
    def list(self,                                    # type: ignore[empty-body]
             classid: Optional[str] = None
             ) -> List[Component]:
        """
        List all the components contained inside this object,
        possibly restricted to a certain classid.

        Parameters:
            classid (str): one of "GraphFrame", "PlotFrame", "FFTFrame",
                "Divider", "Sticky" or "GroupBox".

        Returns:
            List[Component]: the list of components
        """


    def find(self, classid: Optional[str] = None, **properties
             ) -> Optional[Component]:
        """find( [classid,] [key=value, ...])

        Find the (singular) component that matches the given criteria, or None
        if no matching component can be found.  Raises an exception if more
        than one component matches the given criteria.

        Parameters:
            classid (str): one of "GraphFrame", "PlotFrame", "FFTFrame",
                "Divider", "Sticky" or "GroupBox".
            key=value: additional parameters which must be matched.

        Returns:
            Component: the found component or None
        """

        components = self.find_all(classid, **properties)

        if len(components) > 1:
            raise ValueError("Multiple components found")

        return components[0] if components else None


    def find_first(self, classid: Optional[str] = None, **properties
                   ) -> Optional[Component]:
        """find_first( [classid,] [key=value, ...])

        Find a component that matches the given criteria, or None
        if no matching component can be found.

        Parameters:
            classid (str): one of "GraphFrame", "PlotFrame", "FFTFrame",
                "Divider", "Sticky" or "GroupBox".
            key=value: additional parameters which must be matched.

        Returns:
            Component: the found component or None
        """

        components = self.find_all(classid, **properties)

        return components[0] if components else None


    def find_all(self, classid: Optional[str] = None, **properties
                 ) -> List[Component]:
        """find_all( [classid,] [key=value, ...])

        Find all components that matches the given criteria, or None
        if no matching component can be found.

        Parameters:
            classid (str): one of "GraphFrame", "PlotFrame", "FFTFrame",
                "Divider", "Sticky" or "GroupBox".
            key=value: additional parameters which must be matched.

        Returns:
            List[Component]: the list of matching components
        """

        components = self.list(classid) if classid else self.list()

        if properties:
            properties = { key: Component._app_val(val)
                           for key, val in properties.items() }
            components = [ component for component in components
                           if self._match_props(component, properties) ]

        return components


    @staticmethod
    def _match_props(cmp, properties):
        props = cmp.properties()

        return all(props.get(key) == val for key, val in properties.items())
