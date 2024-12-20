"""
Enerplot DataFile
"""

from __future__ import annotations

import array
import os
import math as mth

from pathlib import PurePath
from typing import List, Optional, Tuple, Union

import mhi.common.path

from mhi.common.collection import IndexableDict
from .trace import Trace
from .remote import Remotable, rmi, rmi_property, requires, deprecated


#===============================================================================
# Enerplot DataFile
#===============================================================================

class DataFile(Remotable):          # pylint: disable=too-many-public-methods

    """An Enerplot Data File"""

    #---------------------------------------------------------------------------
    # File Load Types
    #---------------------------------------------------------------------------

    FLT_EMTDC = 1                   # PSCAD/EMTDC
    FLT_CSV = 2                     # Comma Separated Files
    FLT_CSV_UNFORMATTED = 3         # Comma Separated Files (Unformatted)
    FLT_COMTRADE = 4                # COMTRADE Files
    FLT_PSSE = 5                    # PSS/E Files
    FLT_HFS = 6                     # Harmonic Frequency Scanner Files
    FLT_RSCAD = 7                   # RSCAD Files
    FLT_TXT = 8                     # Text Files
    FLT_TXT_UNFORMATTED = 9         # Text Files (Unformatted)
    FLT_ALL_FILES = 10              # All Files
    FLT_ALL_FILES_UNFORMATTED = 11  # All Files(Unformatted)

    #---------------------------------------------------------------------------
    # File Save Types
    #---------------------------------------------------------------------------

    FST_CSV = 1                     # Comma Separated Files
    FST_COMTRADE_1999_ASCII = 2     # COMTRADE
    FST_COMTRADE_1999_BINARY = 3    # COMTRADE
    FST_COMTRADE_1991_ASCII = 4     # COMTRADE
    FST_COMTRADE_1991_BINARY = 5    # COMTRADE
    FST_PSSE = 6                    # PSS/E Files

    _COMTRADE_FST = ((1999, (FST_COMTRADE_1999_ASCII,
                             FST_COMTRADE_1999_BINARY)),
                     (1991, (FST_COMTRADE_1991_ASCII,
                             FST_COMTRADE_1991_BINARY)))


    #---------------------------------------------------------------------------
    # DataFile attributes
    #---------------------------------------------------------------------------

    _channel_dict: IndexableDict[str, Channel]


    #---------------------------------------------------------------------------
    # Identity
    #---------------------------------------------------------------------------

    @property
    def id(self) -> str:
        """The id of the data file (read-only)"""
        return self._identity['id']

    @property
    def name(self) -> str:
        """The name of the data file (read-only)"""
        return os.path.basename(self.filename) if self.filename else None

    @rmi_property
    def label(self) -> str:
        """The label of the data file"""

    @label.setter                                       # type: ignore[no-redef]
    def label(self, value: str):
        pass

    @rmi_property
    def filename(self) -> str:                        # type: ignore[empty-body]
        """The filename of the data file (read-only)"""

    @property
    def modified(self) -> bool:
        """Whether or not this is an Enerplot "modified" datafile"""
        return self.name.endswith(".mod.csv")


    #---------------------------------------------------------------------------
    # Save/Unoad
    #---------------------------------------------------------------------------

    @requires('1.0.1')
    def save(self) -> bool:
        """
        Save an Enerplot-modifiable datafile

        Requires Enerplot 1.0.1 or later

        Returns:
            bool: ``True`` if the file state was dirty and required saving,
            ``False`` otherwise.
        """

        if not self.modified:
            raise ValueError("File is not a Enerplot modified datafile")

        return self._save()

    @rmi
    def _save(self):
        pass

    def save_as(self, filename: Union[str, PurePath],
                file_type: int = FST_CSV,
                folder: Optional[Union[str, PurePath]] = None) -> None:
        """
        Save the datafile to a new path location.

        Parameters:
            filename (str): location to store the new datafile.
            file_type (int): type of file to save (see below)
            folder (str): folder to store saved file in

        .. table:: "File Save Type" Format Codes

            =================================  ==============================
            Format Code                        Description
            =================================  ==============================
            DataFile.FST_CSV                   Comma Separated Values
            DataFile.FST_COMTRADE_1999_ASCII   COMTRADE 1999 (Binary)
            DataFile.FST_COMTRADE_1999_BINARY  COMTRADE 1999 (ASCII)
            DataFile.FST_COMTRADE_1991_ASCII   COMTRADE 1999 (Binary)
            DataFile.FST_COMTRADE_1991_BINARY  COMTRADE 1999 (ASCII)
            DataFile.FST_PSSE                  PSSE
            =================================  ==============================
        """

        if folder:
            filename = os.path.join(folder, filename)
        filename = mhi.common.path.expand_path(filename, abspath=True)

        self._save_as(filename, file_type)


    def save_as_csv(self, filename: Union[str, PurePath], plotted: bool =False,
                    folder: Optional[Union[str, PurePath]]=None) -> None:
        """
        Save a CSV datafile to a new path location.

        Parameters:
            filename (str): location to store the new datafile.
            plotted (bool): If true, only plotted channels, otherwise all channels
            folder (str): folder to store saved file in

        """

        if folder:
            filename = os.path.join(folder, filename)
        filename = mhi.common.path.expand_path(filename, abspath=True)

        self._save_as(filename, DataFile.FST_CSV, plotted=plotted)


    def save_as_comtrade(self,
                         filename: Union[str, PurePath], *channels,
                         folder: Optional[Union[str, PurePath]]=None,
                         plotted: bool = False, year: int = 1999,
                         binary: bool = True, station: Optional[str] = None,
                         header: Optional[str] = None) -> None:
        """
        Save an COMTRADE datafile to a new path location.

        If no channel names are given, and ``plotted`` is not set to ``True``,
        all data will be saved.

        Parameters:
            filename (str): location to store the new datafile.
            *channels (str): list of channel names to store
            folder (str): folder to store saved file in
            plotted (bool): if true, all plotted channels are added to output
            year (int): year-based file format version (eg, 1991 or 1999)
            binary (bool): if true, data is saved in binary format
            station (str): Station text to write to file
            header (str): Header text to write to file

        Example:

            The following code will save channels named A, B, and C, as
            well as any channel used in a plot, in an ASCII COMTRADE file::

                datafile.save_as_comtrade("new_file.cfg", "A", "B", "C",
                                          plotted=True, binary=False)
        """

        if folder:
            filename = os.path.join(folder, filename)
        filename = mhi.common.path.expand_path(filename, abspath=True)

        # Year/Binary to File Save Type
        file_type = next((fst[binary] for start, fst in self._COMTRADE_FST
                          if year >= start), None)
        if not file_type:
            raise ValueError("Unsupported year")

        kwargs = { 'plotted': plotted, 'channels': channels }
        if station:
            kwargs['station'] = station
        if header:
            kwargs['header'] = header

        self._save_as(filename, file_type, **kwargs)


    @rmi
    def _save_as(self, filename, file_type, **kwargs):
        pass


    @rmi
    def remove(self) -> None:
        """
        Remove this data file from the workspace
        """


    #---------------------------------------------------------------------------
    # Domain
    #---------------------------------------------------------------------------

    @property
    def num_samples(self) -> int:
        """
        The number of samples in the data file.

        Returns:
            int: the number of samples
        """

        return len(self.domain)

    @rmi
    def _fetch_domain(self):
        pass

    @property
    def domain(self) -> Trace:
        """
        The domain channel of the data file.

        Returns:
            Trace: the domain values
        """

        if '_domain' not in self.__dict__:
            try:
                self._domain = Trace(self._fetch_domain())
            except ValueError:
                raise AttributeError("Domain not set") from None

            self._domain._read_only = True    # pylint: disable=protected-access
            self._domain._upload_required = False # pylint: disable=protected-access

        return self._domain

    @domain.setter
    def domain(self, domain: Trace):
        try:
            _ = self.domain
            raise RuntimeError("Domain already set")
        except AttributeError:
            pass

        self._domain = Trace(domain)
        self._domain._read_only = True        # pylint: disable=protected-access
        self._domain._upload_required = True  # pylint: disable=protected-access


    def set_domain(self, *, rate: float = 0, samples: int = 0,
                   duration: float = 0) -> Trace:
        """
        Set the domain of the data file

        Parameters:
            rate (float): Difference between successive domain values
            samples (int): Total number of samples
            duration (float): The final or ending domain value (inclusive)

        Returns:
            Trace: the domain channel

        Example:

            To create a time channel, with every millisecond,
            from 0.000 seconds up to and including 2.000 seconds,
            use one of the following statements::

                data_file.set_domain(rate=0.001, samples=2001)
                data_file.set_domain(samples=2001, duration=2.000)
                data_file.set_domain(rate=0.001, duration=2.000)
        """

        if rate > 0 and samples > 0 and duration > 0:
            raise ValueError("Over specified")

        if samples == 0 and rate > 0 and duration > 0:
            samples = mth.floor(duration / rate + 1.5)
        elif rate == 0 and samples > 1 and duration > 0:
            rate = duration / (samples - 1)

        if samples <= 0 or rate <= 0:
            raise ValueError("Under specified")

        domain = self.trace(samples)
        for i in range(samples):
            domain[i] = i * rate

        self.domain = domain

        return domain


    #---------------------------------------------------------------------------
    # Channels
    #---------------------------------------------------------------------------

    @rmi
    def _channels(self):
        pass


    def channels(self, refresh: bool = False) -> IndexableDict[str, Channel]:
        """
        Return an indexable dictionary of channels in the DataFile

        Parameters:
            refresh (bool): forces a reload of the channel cache, if ``True``

        Returns:
            IndexableDict[str,Channel]: channels in the data file
        """

        if refresh or '_channel_dict' not in self.__dict__:
            channels = self._channels()
            for channel in channels:
                channel._journal = self       # pylint: disable=protected-access
            self._channel_dict = IndexableDict((channel.name, channel)
                                               for channel in channels)

        return self._channel_dict


    def channel_names(self, refresh: bool = False) -> List[str]:
        """
        Return a list of channel names in the data file

        Returns:
            List[str]: the list of channel names in the data file.
        """

        channels = self.channels(refresh)

        return list(channels.keys())


    #---------------------------------------------------------------------------
    # Channel
    #---------------------------------------------------------------------------

    @rmi
    def _channel(self, key):
        pass

    def channel(self, key: str) -> Channel:
        """
        Return the channel by name or index

        Parameters:
            key: A name (str) or an index (int) indicating the required channel

        Returns:
            Channel: the indicated channel from the data file
        """

        channel = self._channel(key)
        if channel is not None:
            channel._journal = self           # pylint: disable=protected-access

        return channel


    record = channel # Temporary alias


    def __getitem__(self, key: str):
        return self.channel(key)


    #---------------------------------------------------------------------------
    # Trace
    #---------------------------------------------------------------------------

    def trace(self, n: int = 0) -> Trace:
        """
        Create a new trace for the data file.

        If the number of samples is not specified,
        it defaults to the length of the data file's domain.

        Parameters:
            n (int): number of samples in trace (optional)

        Returns:
            Trace: buffer to store trace in
        """

        if not n:
            n = self.num_samples

        return Trace(n)


    def analog(self, func_or_iterable) -> Trace:
        """
        Create a new analog trace for the data file.

        The length of the trace corresponds to the number of samples
        in the data file's domain channel.

        If given an iterable object, successive values from the
        iterable are copied into the trace.

        If given a callable function, the function is repeatedly called
        with sucessive values from the domain channel, and the resulting
        values are copied into the trace.

        Parameters:
            func_or_iterable: source to generate channel values from

        Returns:
            Trace: the generated trace
        """

        trace = self.trace(self.num_samples)
        if callable(func_or_iterable):
            func = func_or_iterable
            for i, t in enumerate(self.domain):
                trace[i] = func(t)
        else:
            iterable = iter(func_or_iterable)
            for i in range(self.num_samples):
                trace[i] = next(iterable)

        return trace


    @deprecated("Use DataFile.analog() instead")
    def to_trace(self, data, num_samples=None): # pylint: disable=missing-function-docstring
        if not num_samples:
            num_samples = self.num_samples
        if len(data) != num_samples:
            raise ValueError("Incorrect data length")
        buffer = self.trace(num_samples)
        for i in range(num_samples):
            buffer[i] = data[i]
        return buffer


    #---------------------------------------------------------------------------
    # Set (Replace) channel
    #---------------------------------------------------------------------------

    @rmi
    def _set_channel(self, data, name, group):
        pass

    @rmi
    def _add_channel(self, name, data, group, domain):
        pass

    def set_channel(self, data, name: str, group: str = "Data") -> Channel:
        """
        Add or replace a channel of data to this data file

        Parameters:
            data: a series of data values representing a channel
            name (str): name to be given to the channel
            group (str): group to create the channel in

        Returns:
            Channel: the create channel
        """

        if not isinstance(data, Trace):
            data = self.analog(data)

        if len(data) > self.num_samples:
            data = data[:self.num_samples]
        elif len(data) < self.num_samples:
            raise ValueError("Incorrect data length")

        data = bytes(data)
        if self._domain._upload_required:     # pylint: disable=protected-access
            channel = self._add_channel(name, data, group, bytes(self._domain))
            self._domain._upload_required = False # pylint: disable=protected-access
        else:
            channel = self._set_channel(data, name, group)

        channel._journal = self               # pylint: disable=protected-access
        if '_channel_dict' in self.__dict__:
            self._channel_dict[name] = channel

        return channel


    #---------------------------------------------------------------------------
    # Add new channel
    #---------------------------------------------------------------------------

    @deprecated("Use DataFile.set_channel")
    def add_channel(self, data, name, group="Data"): # pylint: disable=missing-function-docstring
        self.set_channel(data, name, group)


#===============================================================================
# Enerplot Mutable DataFile
#===============================================================================

class MutableDataFile(DataFile):
    """
    Mutable Data Files

    A datafile whose domain can be set from Python.

    Deprecated.
    """


#===============================================================================
# Enerplot Channel
#===============================================================================

class Channel(Remotable, Trace):

    """An Enerplot Channel from a Data File"""

    _journal: DataFile


    @property
    def datafile(self) -> DataFile:
        """The data file which this channel is a member of (read-only)"""
        if '_journal' not in self.__dict__:
            journal_id = self._identity['journal']
            self._journal = self.main._datafile(id=journal_id) # pylint: disable=protected-access
        return self._journal


    @rmi_property
    def name(self) -> str:                            # type: ignore[empty-body]
        """Channel name (read only)"""


    @rmi
    def copy(self) -> None:
        """Copy the channel to the clipboard"""

    @rmi
    def _fetch_data(self, i=0):
        pass


    @property
    def domain(self) -> Trace:
        """The domain for this channel"""

        return self.datafile.domain


    def points(self) -> int:
        """The number of samples in this channel"""

        return len(self.domain)


    def __len__(self):
        return self.points()


    @property
    def data(self) -> array.array:
        """The samples of this channel (read-only)"""

        if '_data' not in self.__dict__:
            data = self._fetch_data(0)
#            self._data = memoryview(data).cast('d')
            self._data = array.array('d', memoryview(data).cast('d'))
        return self._data


    @property
    def read_only(self) -> bool:

        return True


    def extents(self) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        """
        The domain and range of this channel's sample values

        Returns:
            Tuple[Tuple]: (minimum x, maximum x), (minimum y, maximum y)
        """

        x_min = self.domain[0]
        x_max = self.domain[-1]
        y_min = min(self.data)
        y_max = max(self.data)

        return ((x_min, x_max),(y_min, y_max))
