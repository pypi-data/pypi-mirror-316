"""
Enerplot Book
"""

from __future__ import annotations

import os
from pathlib import PurePath
from typing import Optional, Union, TYPE_CHECKING

import mhi.common.path
from mhi.common.collection import IndexableDict
from mhi.common.codec import SimpleCodec
from .command import Command
from .component import Component
from .remote import Remotable, rmi, rmi_property, requires

if TYPE_CHECKING:
    from .annotation import GroupBox, Line, TextArea
    from .datafile import DataFile
    from .graph import FFTFrame, GraphFrame, PlotFrame


#===============================================================================
# Codecs
#===============================================================================

_pagesize = SimpleCodec({'A/A4': 0, 'B/A3': 1, 'C/A2': 2, 'D/A1': 3,
                         'Oversize':4})
_pagesize.alternates({'A': 0, 'B': 1, 'C': 2, 'D': 3,
                      'A4': 0, 'A3': 1, 'A2': 2, 'A1': 3,
                      '8.5x11':0, '11x17':1, '17x22':2, '22x34':3, '34x44': 4})

_orient = SimpleCodec(Portrait=0, Landscape=1)


#===============================================================================
# Enerplot Books
#===============================================================================

class Book(Remotable):

    """
    An Enerplot Book holds one or more sheets, which in turn will hold
    graph frames for viewing curve data.
    """

    @property
    def name(self) -> str:
        """
        The name of the book (read-only)
        """

        return self._identity['name']


    @rmi_property
    def file(self) -> str:                            # type: ignore[empty-body]
        """
        The book's filename (read-only)
        """


    @rmi_property
    def description(self) -> str:                     # type: ignore[empty-body]
        """
        The book's description (read-only)
        """


    header = rmi_property(True, True, doc="Header Text", name='header')

    title = rmi_property(True, True, doc="Header Title", name='title')

    footer_left = rmi_property(True, True, doc="Left footer",
                               name='footer_left')
    footer_center = rmi_property(True, True, doc="Centre footer",
                                 name='footer_center')
    footer_right = rmi_property(True, True, doc="Right footer",
                                name='footer_right')

    _page_numbers = rmi_property(True, True, doc="Right footer",
                                 name='_page_numbers')

    _PAGE_NUM_LOCS = ('none', 'top-left', 'top-centre', 'top-right',
                      'bottom-left', 'bottom-centre', 'bottom-right')


    @property
    def page_numbers(self) -> str:
        """
        Return the location the page numbers will be drawn.
        """

        idx = int(self._page_numbers or "0")
        return self._PAGE_NUM_LOCS[idx]


    @page_numbers.setter
    def page_numbers(self, loc) -> None:

        try:
            self._page_numbers = str(self._PAGE_NUM_LOCS.index(loc.lower()))
        except ValueError:
            raise ValueError(f"Invalid page number location: {loc!r}") from None


    @rmi
    def unload(self) -> None:
        """
        Unload this book

        The book is unloaded from the Enerplot workspace.

        Warning:

            Any changes made to the book, which have not explicitly been
            saved, will be lost.  Call :meth:`save` or :meth:`save_as`
            before unloading to preserve changes.
        """


    @requires('1.1')
    @rmi
    def reload(self) -> None:
        """
        Reload this book

        The book is reloaded into the Enerplot workspace.

        Warning:

            Any changes made to the book, which have not explicitly been
            saved, will be lost.  Call :meth:`save` or :meth:`save_as`
            before reloading to preserve changes.

        .. versionadded:: 2.3
        """


    @requires('1.1')
    @rmi
    def focus(self) -> None:
        """
        Focus on this book.

        .. versionadded:: 2.5
        """


    @requires('1.1')
    def print(self) -> None:
        """
        Print this book to the default printer

        .. versionadded:: 2.5
        """

        self.focus()
        self.main.print()


    @rmi_property
    def dirty(self) -> bool:                          # type: ignore[empty-body]
        """
        Has the book been modified since it was last saved (read-only)

        .. versionadded:: 2.3
        """


    @requires('1.1')
    def is_dirty(self) -> bool:
        """
        Check if the project contains unsaved changes

        Returns:
            `True`, if unsaved changes exist, `False` otherwise.

        .. versionadded:: 2.3
        """

        return self.dirty


    #-----------------------------------------------------------------------
    # Save / Save as
    #-----------------------------------------------------------------------

    @rmi
    def _save(self, path=None):
        pass


    def save(self) -> None:
        """
        Save all changes in book
        """

        self._save()


    def save_as(self,
                path: Union[str, PurePath],
                folder: Optional[Union[str, PurePath]] = None) -> None:
        """
        Save book to a new path location

        Parameters:
            path (str): location to store the book.
                The extension .epbx is appended if not present.

            folder (str): If provided, the path to the book is resolved
                relative to this folder.
        """

        if isinstance(path, PurePath):
            path = str(path)

        if not path.endswith(".epbx"):
            path += '.epbx'

        if folder:
            path = os.path.join(folder, path)

        path = mhi.common.path.expand_path(path, abspath=True)

        name = os.path.splitext(os.path.basename(path))[0]

        enerplot = self._context._main        # pylint: disable=protected-access

        book = enerplot.book(name)

        # Ok to save to the same name in a new location;
        # not ok to save to the name of an existing book, otherwise.
        if self._identity != book._identity:  # pylint: disable=protected-access
            raise ValueError(f"Book {name!r} already exists")

        self._save(path)

        book = enerplot.book(name)
        if self._identity != book._identity:  # pylint: disable=protected-access
            self._identity = book._identity   # pylint: disable=protected-access


    #-----------------------------------------------------------------------
    # Sheets
    #-----------------------------------------------------------------------

    @rmi
    def _sheets(self):
        """
        List all of the sheets in this book

        Returns:
            List[Sheet]: the list of sheets.
        """


    def sheets(self) -> IndexableDict[str, Sheet]:
        """
        List all of the sheets in this book.

        Returns:
            IndexableDict[str,Sheet]: An indexable dictionary of sheets.
        """

        sheets = self._sheets()
        return IndexableDict((sheet.name, sheet) for sheet in sheets)


    @rmi
    def sheet(self, name: str) -> Optional[Sheet]:
        """
        Retrieve a sheet reference, by name

        Parameters:
            name (str): the name of the sheet

        Returns:
            Sheet: the named sheet (if present)
        """


    @rmi
    def _new_sheet(self, name, description):
        """Create a new sheet"""


    def new_sheet(self, name: str = "", description: str = ""):
        """
        Create a new sheet

        Parameters:
            name (str): The desired sheet name; if not provided, "Sheet#" will
                be used.

            description (str): a description to be given to the sheet.

        Returns:
            Sheet: the created sheet.
        """

        return self._new_sheet(name, description)


    #-----------------------------------------------------------------------
    # Components
    #-----------------------------------------------------------------------

    @rmi
    def _find(self, _id, classid=None):
        """
        Find a component in a book by id number and classid.

        This function exists for backward compatibility only.
        Other find functions are easier to use.

        Parameters:
            _id (int): The component's ID number
            classid (str): The component's class-id

        Returns:
            Component: the identified component
        """

    #-----------------------------------------------------------------------
    # Link/Unlink
    #-----------------------------------------------------------------------

    @rmi
    def delink_all(self) -> None:
        """
        Delink all channel data from book
        """

    @rmi
    def relink_all(self, datafile: DataFile) -> None:
        """
        Relink the channel data to the given datafile

        Parameters:
            datafile (DataFile): the datafile to link channel data to.
        """

    @rmi
    def relink(self, from_datafile: DataFile, to_datafile: DataFile) -> None:
        """
        Relink channels to the referenced in one datafile to the other

        Parameters:
            from_datafile (DataFile): the datafile to unlink channel data from.
            to_datafile (DataFile): the datafile to link channel data to.
        """



#===============================================================================
# Enerplot Sheet
#===============================================================================

class Sheet(Component):

    """
    An Enerplot Sheet
    """

    name = rmi_property(True, True, "The name of the sheet", "name")

    description = rmi_property(True, True, "The description of the sheet",
                               "description")

    @rmi
    def focus(self) -> None:
        """
        Switches the currently focused sheet to become this sheet.
        """


    #---------------------------------------------------------------------------
    # Properties (Grid, Orientation, Size)
    #---------------------------------------------------------------------------

    @property
    def grid(self) -> bool:
        """
        Set to `True` to show a grid on the canvas, `False` otherwise.
        """

        return self['show_grid'] != '0'


    @grid.setter
    def grid(self, value):
        self['show_grid'] = 1 if value else 0


    #---------------------------------------------------------------------------

    @property
    def orientation(self) -> str:
        """
        Set to `"Landscape"` to orient the paper horizontally,
        `"Portrait"` to orient vertically.
        """

        return _orient.decode(self['orient'])


    @orientation.setter
    def orientation(self, value: str):

        self['orient'] = _orient.encode(value)


    @property
    def portrait(self) -> bool:
        """
        `True` if the sheet is oriented vertically, `False` otherwise.
        """

        return self['orient'] == '0'


    @property
    def landscape(self) -> bool:
        """
        `True` if the sheet is oriented horizontally, `False` otherwise.
        """

        return self['orient'] != '0'


    #---------------------------------------------------------------------------

    @property
    def pagesize(self) -> str:
        """
        The size of the canvas.

        The size may be set by US name `"A"` or metric name `"A4"`, or by
        dimension in inches `"8.5x11"`.  The following statements all set the
        same canvas size::

            >>> sheet.pagesize = 'A/A4'
            >>> sheet.pagesize = 'A4'
            >>> sheet.pagesize = 'A'
            >>> sheet.pagesize = '8.5x11'
            >>> sheet.pagesize
            'A/A4'
        """

        return _pagesize.decode(self['size'])


    @pagesize.setter
    def pagesize(self, value: str):
        self['size'] = _pagesize.encode(value)


    #---------------------------------------------------------------------------
    # Select All
    #---------------------------------------------------------------------------

    def select_all(self) -> None:
        """
        Select all components on the sheet
        """

        self._generic_command(Command.IDM_SELECTALL)


    #---------------------------------------------------------------------------
    # Removing components
    #---------------------------------------------------------------------------

    @rmi
    def remove(self, *components) -> None:
        """
        Remove components from the sheet
        """


    #---------------------------------------------------------------------------
    # Create child components
    #---------------------------------------------------------------------------

    @rmi
    def _create(self, classid, **attrs) -> Component: # type: ignore[empty-body]
        pass


    def sticky(self,
               x=None, y=None, w=None, h=None, text=None,
               **kwargs) -> TextArea:
        """
        Create a "Sticky Note" styled TextArea

        Parameters:
            x (int): x location for the Sticky Note
            y (int): y-location for the Sticky Note
            w (int): width of the Sticky Note
            h (int): height of the Sticky Note
            text (str): the contents of the sticky note
            **kwargs: Additional key=value properties for the TextArea.

        Returns:
            TextArea: the sticky note

        Example::

            note = sheet.sticky(1, 1, 8, 3, "Hello world", arrows="NE E SE",
                                fg_color='yellow', bg_color='black')
        """

        sticky = self._create("Sticky", x=x, y=y, w=w, h=h)
        sticky.properties(**kwargs)
        if text is not None:
            sticky.text = text

        return sticky


    def caption(self,
                x=None, y=None, w=20, h=2, text="Caption",
                **kwargs) -> TextArea:
        """
        Create a "Caption" styled TextArea

        Parameters:
            x (int): x location for the Caption
            y (int): y-location for the Caption
            w (int): width of the Caption
            h (int): height of the Caption
            text (str): the contents of the Caption
            **kwargs: Additional key=value properties for the TextArea.

        Returns:
            TextArea: the caption

        Example::

            caption = sheet.caption(1, 5, 8, 2, "Output", fg_color='red')
        """

        options = {'style': 0, 'align': 1, 'full_font': 'Tahoma, 16pt'}
        options.update(kwargs)

        caption = self._create("Sticky", x=x, y=y, w=w, h=h)
        caption.properties(**options)
        if text is not None:
            caption.text = text

        return caption


    def divider(self, x=None, y=None, w=None, h=None,
                **kwargs) -> Line:
        """
        Create a "Divider"

        Parameters:
            x (int): x location for the start of Divider
            y (int): y-location for the start of Divider
            w (int): width of the Divider (if horizontal)
            h (int): height of the Divider (if vertical)
            **kwargs: Additional key=value properties for the note.

        Returns:
            Line: the divider

        Example::

            divider = sheet.divider(1, 10, 6, 0, state=0, style='Dash')
        """

        if w and (h is None):
            h = 0
        elif h and (w is None):
            w = 0
        elif w and h:
            raise ValueError("Width and height must not both be given")

        divider = self._create("Divider", x=x, y=y, w=w, h=h)
        if kwargs:
            divider.properties(**kwargs)

        return divider


    @requires('1.1')
    def group_box(self,
                  x=None, y=None, w=11, h=6, name="Groupbox",
                  **kwargs) -> GroupBox:
        """
        Create a "Group Box"

        Parameters:
            x (int): x-location for the start of Group Box
            y (int): y-location for the start of Group Box
            w (int): width of the Group Box
            h (int): height of the Group Box
            name (str): the title of the Group Box
            **kwargs: Additional key=value properties for the Group Box.

        Returns:
            GroupBox: the group box
        """

        group_box = self._create("GroupBox", x=x, y=y, w=w, h=h)
        if name is not None or kwargs:
            group_box.properties(name=name, **kwargs)

        return group_box


    def graph_frame(self,
                    x=None, y=None, w=None, h=None, *,
                    polygraph=False, **kwargs) -> GraphFrame:
        """
        Create a "Graph Frame"

        Parameters:
            x (int): x location for the start of Frame
            y (int): y-location for the start of Frame
            w (int): width of the Frame
            h (int): height of the Frame
            polygraph (bool): First panel is overlay-graph or polygraph
            **kwargs: Additional key=value properties for the frame.

        Returns:
            GraphFrame: the graph frame

        .. versionchanged:: 2.3
            Added `polygraph` parameter
        """

        classid = "GraphFrame+Poly" if polygraph else "GraphFrame"
        graph_frame = self._create(classid, x=x, y=y, w=w, h=h)
        if kwargs:
            graph_frame.properties(**kwargs)

        return graph_frame


    def plot_frame(self, x=None, y=None, w=None, h=None,
                   **kwargs) -> PlotFrame:
        """
        Create a "Plot Frame" for X-Y plots

        Parameters:
            x (int): x location for the start of Frame
            y (int): y-location for the start of Frame
            w (int): width of the Frame
            h (int): height of the Frame
            **kwargs: Additional key=value properties for the frame.

        Returns:
            PlotFrame: the x-y plot frame
        """

        plot_frame = self._create("PlotFrame", x=x, y=y, w=w, h=h)
        if kwargs:
            plot_frame.properties(**kwargs)

        return plot_frame


    def fft_frame(self, x=None, y=None, w=None, h=None,
                  **kwargs) -> FFTFrame:
        """
        Create a "FFT Frame" for FFT Graphs

        Parameters:
            x (int): x location for the start of Frame
            y (int): y-location for the start of Frame
            w (int): width of the Frame
            h (int): height of the Frame
            **kwargs: Additional key=value properties for the frame.

        Returns:
            FFTFrame: the FFT graph frame
        """

        fft_frame = self._create("FFTFrame", x=x, y=y, w=w, h=h)
        if kwargs:
            fft_frame.properties(**kwargs)

        return fft_frame


    @rmi
    def relink(self, from_datafile: DataFile, to_datafile: DataFile) -> None:
        """
        Relink channels to the referenced in one datafile to the other

        Parameters:
            from_datafile (DataFile): the datafile to unlink channel data from.
            to_datafile (DataFile): the datafile to link channel data to.
        """
