from PySide2.QtWidgets import QWidget

from ...GUI.WExport.Ui_WExport import Ui_WExport


class WExport(Ui_WExport, QWidget):
    """Widget to select how to export the data"""

    def __init__(self, parent=None):
        """Initialize the GUI according to machine type

        Parameters
        ----------
        self : WExport
            a WExport object
        parent : QWidget
            The parent widget
        """

        # Build the interface according to the .ui file
        QWidget.__init__(self, parent=parent)
        self.setupUi(self)
