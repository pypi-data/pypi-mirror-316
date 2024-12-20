"""
Enerplot Status Area Progress Bar
"""

from typing import Optional

from .remote import Remotable, rmi, rmi_property


#===============================================================================
# Progress Bar
#===============================================================================

class Progress(Remotable):

    """
    Progress Bar in the application's Status Bar area

    When finished with a progress bar, it is imperative to call the
    close() method to allow Enerplot to remove the bar from the status window.
    This is easiest done using a ``with`` statement which will automatically
    close the resource, even if an exception or early return occurs::

        with enerplot.progress() as progress_bar:
            progress_bar.update(10)
            progress_bar.update(50)
            progress_bar.update(100)
    """


    @rmi
    def update(self,
               amount: Optional[int] = None, *,
               total: Optional[int] = None,
               status: Optional[int] = None,
               priority: Optional[int] = None,
               text: Optional[str] = None) -> None:
        """
        Update a previously created progress bar

        Parameters:
            amount (int): new amount of progress to display in the bar
            total (int): new maximum value for the progress bar (optional)
            status (int): 0 = running, 1 = waiting, 2 = stopped (optional)
            priority (int): priority for the progress bar (optional)
            text (str): message to display in progress bar (optional)
        """


    amount = rmi_property(fset=True, doc="progress bar amount (write-only)", name='amount')

    total = rmi_property(fset=True, doc="progress bar total (write-only)", name='total')

    status = rmi_property(fset=True, doc="progress bar status code (write-only)", name='status')

    priority = rmi_property(fset=True, doc="progress bar priority (write-only)", name='priority')

    text = rmi_property(fset=True, doc="progress bar text (write-only)", name='text')


    @rmi
    def close(self) -> None:
        """
        Remove the progress bar from the status bar at the bottom of
        the application.

        When finished with a progress bar, it is imperative to call the
        close() method to allow Enerplot to remove the bar from the status window.
        This is easiest done using a ``with`` statement which will automatically
        close the resource, even if an exception or early return occurs::

            with enerplot.progress() as progress_bar:
                progress_bar.update(10)
                progress_bar.update(50)
                progress_bar.update(100)
        """


    def __enter__(self):

        return self


    def __exit__(self, exc_type, exc_value, traceback):

        self.close()
