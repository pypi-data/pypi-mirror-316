"""
Enerplot Graph
"""

from __future__ import annotations

import array
from typing import Any, Dict, Optional, Tuple, TYPE_CHECKING

from mhi.common.codec import SimpleCodec, CodecMap
from mhi.common.remote import RemoteException

from .command import Command
from .component import Component
from .remote import rmi
from .trace import Trace

if TYPE_CHECKING:
    from .datafile import DataFile, Channel


#===============================================================================
# Enerplot Graph Frames
#===============================================================================

class ZFrame(Component):

    """
    A ZFrame
    """

    @property
    def title(self) -> str:
        """The title of the frame"""

        return self.properties()["title"]


    @title.setter
    def title(self, title: str):

        self.properties(title=title)


    #-----------------------------------------------------------------------
    # Link/Unlink
    #-----------------------------------------------------------------------

    @rmi
    def delink_all(self) -> None:
        """
        Delink all channel data from the frame
        """


    @rmi
    def relink_all(self, datafile: DataFile) -> None:
        """
        Relink the channel data to the given datafile

        Parameters:
            datafile (DataFile): the datafile to link channel data to.
        """


class GraphMixin:
    """
    Functions common to all graphs (GraphFrame, PlotFrame, FFTFrame, GraphPanel)
    """

    def _generic_command(self, cmd: Command):
        raise NotImplementedError("Must be implemented elsewhere", cmd)


    def __setitem__(self, key: str, value: Any):
        raise NotImplementedError("Must be implemented elsewhere", key, value)


    def reset_extents(self) -> None:
        """
        Reset the graph's extents
        """

        self._generic_command(Command.RESET_EXTENTS)


    def reset_limits(self) -> None:
        """
        Reset the graph's limits
        """

        self._generic_command(Command.RESET_LIMITS)


    def zoom_extents(self, x_extents: bool = True, y_extents: bool = True
                     ) -> None:
        """
        Reset the graph's zoom to the X and/or Y extents.
        By default, both X and Y axis zoom is affected.

        Parameters:
            x_extents (bool): set to False to not affect X-axis
            y_extents (bool): set to False to not affect Y-axis
        """

        if x_extents:
            self.zoom_x_extents()
        if y_extents:
            self.zoom_y_extents()


    def zoom_limits(self, x_limits: bool = True, y_limits: bool = True) -> None:
        """
        Reset the graph's zoom to the X and/or Y limits.
        By default, both X and Y axis zoom is affected.

        Parameters:
            x_limits (bool): set to False to not affect X-axis
            y_limits (bool): set to False to not affect Y-axis
        """

        if x_limits:
            self.zoom_x_limits()
        if y_limits:
            self.zoom_y_limits()


    def zoom_x_extents(self) -> None:
        """
        Reset the graph's zoom for the X-axis to the X extents.
        """

        self._generic_command(Command.RESET_EXTENTS_X)


    def zoom_x_limits(self) -> None:
        """
        Reset the graph's zoom for the X-axis to the X limits.
        """

        self._generic_command(Command.RESET_LIMITS_X)


    def zoom_y_extents(self) -> None:
        """
        Reset the graph's zoom for the Y-axis to the Y extents.
        """

        self._generic_command(Command.RESET_EXTENTS_Y)


    def zoom_y_limits(self) -> None:
        """
        Reset the graph's zoom for the Y-axis to the Y limits.
        """

        self._generic_command(Command.RESET_LIMITS_Y)


    @rmi
    def zoom(self,
             xmin=None, xmax=None, ymin=None, ymax=None, *,
             compute_x_grid: bool = True, compute_y_grid: bool = True) -> None:
        """
        Alter the graph's viewport
        """


    def toggle_grid_lines(self) -> None:
        """
        Toggle grid lines on or off
        """

        self._generic_command(Command.TOGGLE_GRID_LINES)


    def show_grid(self, show: bool = True) -> None:
        """
        Set the grid's visibility.

        Parameters:
            show (bool): Set to ``False`` to turn off the grid.
        """

        self['grid'] = show


    def toggle_tick_marks(self) -> None:
        """
        Toggle tick marks on or off
        """

        self._generic_command(Command.TOGGLE_TICK_MARKS)


    def show_ticks(self, show: bool = True) -> None:
        """
        Set the tick visibility.

        Parameters:
            show (bool): Set to ``False`` to turn off the tick markers.
        """

        self['ticks'] = show


    def toggle_curve_glyphs(self) -> None:
        """
        Toggle curve glyphs on or off
        """

        self._generic_command(Command.TOGGLE_CURVE_GLYPHS)


    def show_glyphs(self, show: bool = True) -> None:
        """
        Set the curve glyph visibility.

        Parameters:
            show (bool): Set to ``False`` to turn off the curve glyphs.
        """

        self['glyphs'] = show


    def toggle_x_intercept(self) -> None:
        """
        Toggle X intercept on or off
        """

        self._generic_command(Command.TOGGLE_X_INTERCEPT)


    def show_x_intercept(self, show: bool = True) -> None:
        """
        Set the X intercept visibility on or off
        """

        self['xinter'] = show


    def toggle_y_intercept(self) -> None:
        """
        Toggle Y intercept on or off
        """

        self._generic_command(Command.TOGGLE_Y_INTERCENT)


    def show_y_intercept(self, show: bool = True) -> None:
        """
        Set the Y intercept visibility on or off
        """

        self['yinter'] = show


class MarkerMixin:
    """
    Functions common to GraphFrame and FFTFrame
    """

    def _generic_command(self, cmd: Command):
        raise NotImplementedError("Must be implemented elsewhere", cmd)


    def __getitem__(self, key: str) -> Any:
        raise NotImplementedError("Must be implemented elsewhere", key)


    def __setitem__(self, key: str, value: Any):
        raise NotImplementedError("Must be implemented elsewhere", key, value)


    def properties(self, **kwargs) -> Dict[str, Any]: # pylint: disable=missing-function-docstring
        raise NotImplementedError("Must be implemented elsewhere", kwargs)


    def toggle_markers(self) -> None:
        """
        Toggle X/O markers
        """

        self._generic_command(Command.TOGGLE_MARKERS)


    def show_markers(self, show: bool = True) -> None:
        """
        Show (or hide) the X/O markers
        """

        self['markers'] = show


    def set_markers(self, x: Optional[float] = None, o: Optional[float] = None,
                    *, delta: Optional[float] = None) -> None:
        """
        Set the X and/or O marker positions.

        If both ``x`` and ``o`` are specified, ``delta`` cannot be given.

        If ``delta`` is given, the O-marker is positioned the specified
        distance after the X-marker, unless the ``o`` value is specified
        in which case the X-marker is positioned the specified distance
        before the O-marker.

        If the markers were hidden, they will automatically be shown.

        If the markers are "locked together", they will remain locked together,
        but with their relative offset defined by their new positions.

        Parameters:
            x (float): new x-marker position
            o (float): new o-marker position
            delta (float): distance between x & o markers

        Examples:

            The following are equivalent, and set the markers 1 cycle apart,
            assuming a 60Hz waveform::

                graph_frame.set_markers(0.1, 0.11666667)
                graph_frame.set_markers(0.1, delta=0.01666667)
                graph_frame.set_markers(0.1, delta=1/60)
                graph_frame.set_markers(delta=1/60, x=0.1)
                graph_frame.set_markers(delta=1/60, o=0.11666667)
        """

        if x is not None and o is not None and delta is not None:
            raise ValueError("Cannot specify delta if both x & o are given")

        props: Dict[str, Any] = {'markers': True}

        if delta is not None:
            if o is None:
                o = (x if x is not None else float(self['xmarker'])) + delta
            else:
                x = o - delta

        if x is not None:
            props['xmarker'] = x
        if o is not None:
            props['omarker'] = o

        self.properties(**props)


    def lock_markers(self, lock: bool = True, *,
                     delta: Optional[float] = None) -> None:
        """
        Lock (or unlock) markers to a fixed offset from each other.

        Parameters:
            lock (bool): set to ``False`` to unlock the marker
            delta (float): used to specify lock offset (optional)

        Examples::

            fft.lock_markers()
            fft.lock_markers(delta=1/50)
            fft.lock_markers(False)
        """

        props: Dict[str, Any] = { 'lockmarkers': lock }

        if lock:
            props['markers'] = 'true'
            if delta is not None:
                props['omarker'] = float(self['xmarker']) + delta
        elif delta is not None:
            raise ValueError("Cannot specify delta when unlocking")

        self.properties(**props)


class SubGraphsMixin:
    """
    Functions common to graph frames with panels (GraphFrame & FFTFrame)
    """

    def list(self):                 # pylint: disable=missing-function-docstring
        raise NotImplementedError("Must be implemented elsewhere")


    def panels(self) -> int:
        """
        Return the number of panels in a the Frame
        """

        return len(self.list())


    def panel(self, index: int) -> GraphPanel:
        """
        Return the indexed panel
        """

        return self.list()[index]


class GraphFrame(ZFrame, GraphMixin, SubGraphsMixin, MarkerMixin):
    """
    Graph Frame

    A container which can hold one or more Graph Panels, stacked vertically,
    with a common x-axis.
    """

    def add_overlay_graph(self) -> GraphPanel:
        """
        Add a new overly graph panel to the Graph Frame.

        Returns:
            GraphPanel: the newly added graph panel.
        """

        num_panels = len(self.list())

        self._generic_command(Command.ADD_OVERLAY_GRAPH)

        panels = self.list()
        if num_panels == len(panels):
            raise RemoteException("Too many graph panels")

        return panels[-1]


    def add_poly_graph(self) -> GraphPanel:
        """
        Add a new poly-graph panel to the Graph Frame.

        Returns:
            GraphPanel: the newly added graph panel.
        """

        num_panels = len(self.list())

        self._generic_command(Command.ADD_POLY_GRAPH)

        panels = self.list()
        if num_panels == len(panels):
            raise RemoteException("Too many graph panels")

        return panels[-1]


    @rmi
    def remove(self, *graphs) -> None:
        """
        Remove graphs from the Graph Frame
        """


    def zoom(self,                            # pylint: disable=arguments-differ
             xmin: Optional[float] = None, xmax: Optional[float] = None,
             *, compute_x_grid: bool = True) -> None:
        """
        Alter the x-axis viewport for all graph panels in this graph frame

        .. versionadded:: 2.2.1
        """

        self.panel(0).zoom(xmin=xmin, xmax=xmax, compute_x_grid=compute_x_grid)


class PlotFrame(ZFrame, GraphMixin):
    """
    Plot Frame

    A container which holds a X-Y plot graph containing 1 or more curves.
    """


    def add_curves(self, *channels: Channel):
        """
        Add one or more channels to the X-Y plot.

        For every pair of channels added, one X-Y curve is created.

        Parameters:
            *channels (Channel): curves to add to X-Y plot frame
        """

        if not channels:
            raise ValueError("Expected one or more channels")

        for channel in channels:
            channel.copy()
            self.paste_curve()


    def paste_curve(self) -> None:
        """
        Paste a curve from the clipboard into the graph
        """

        self._generic_command(Command.IDZ_CMP_PASTE)


    def polar(self) -> PlotFrame:
        """
        Switch the plot to Polar mode (magnitude & phase)
        """

        self.properties(mode=1)

        return self


    def rectangular(self) -> PlotFrame:
        """
        Switch the plot to Rectangular mode (X-Y)
        """

        self.properties(mode=0)

        return self


class FFTFrame(ZFrame, GraphMixin, SubGraphsMixin, MarkerMixin):
    """
    FFT Graph Frame

    A container which holds an overlay graph, as well as a magnitude and
    phase graph for automatic harmonic analysis of the curve(s) in the
    overlay graph.
    """

    def add_curves(self, *channels: Channel) -> None:
        """
        Add one or more channels to the FFT Graph

        Parameters:
            *channels (Channel): curves to add to graph
        """

        self.panel(0).add_curves(*channels)


    def paste_curve(self) -> None:
        """
        Paste a curve from the clipboard into the top graph
        """

        self.panel(0).paste_curve()



#===============================================================================
# Enerplot Graphs
#===============================================================================

class GraphPanel(Component, GraphMixin):
    """
    Graph Panel
    """

    def add_curves(self, *channels: Channel) -> None:
        """
        Add one or more channels to a graph

        Parameters:
            *channels (Channel): curves to add to graph
        """

        if not channels:
            raise ValueError("Expected one or more channels")

        for channel in channels:
            channel.copy()
            self.paste_curve()


    def paste_curve(self) -> None:
        """
        Paste a curve from the clipboard into the graph
        """
        self._generic_command(Command.IDZ_CMP_PASTE)


    @rmi
    def remove(self, *curves: Curve):
        """
        Remove curves from the Graph Panel
        """


#===============================================================================
# Enerplot Curves
#===============================================================================

_curve_codec = CodecMap(
    mode=SimpleCodec(ANALOG=0, DIGITAL=1),
    style=SimpleCodec(LINE=0, SCATTER=1, AREA=2),
    )


class Curve(Component, Trace):
    """
    Graph Curve
    """

    @rmi
    def channel(self) -> Channel:                     # type: ignore[empty-body]
        """
        Retrieve the channel associated with a curve
        """


    @property
    def data(self) -> array.array:
        return self.channel().data


    def extents(self) -> Tuple[Tuple[float, float], Tuple[float, float]]: # type: ignore[override] # pylint: disable=arguments-differ
        """
        The domain and range of this Curve

        Returns:
            Tuple[Tuple]: (minimum x, maximum x), (minimum y, maximum y)
        """

        return self.channel().extents()


    def generate_new_record(self) -> None:
        """
        Your description here
        """

        self._generic_command(Command.ID_CURVE_GENERATENEWRECORD)


    def _codecs(self):
        return (_curve_codec,)


    def properties(self, **kwargs):           # pylint: disable=arguments-differ
        if kwargs:
            kwargs = _curve_codec.encode_all(kwargs)
        kwargs = self._context.call(self, 'properties', **kwargs)
        if kwargs:
            kwargs = _curve_codec.decode_all(kwargs)
        return kwargs


    def range(self, keyword: str):
        """
        Return the allowable values for the given property name
        """

        return _curve_codec.range(keyword)
