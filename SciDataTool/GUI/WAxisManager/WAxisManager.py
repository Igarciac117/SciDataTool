from PySide2.QtCore import QSize
from PySide2.QtWidgets import QSizePolicy, QSpacerItem, QWidget

from ...GUI.WAxisManager.Ui_WAxisManager import Ui_WAxisManager
from ...GUI.WDataExtractor.WDataExtractor import WDataExtractor
from ...Functions.Plot import fft_dict,ifft_dict,axes_dict

class WAxisManager(Ui_WAxisManager, QWidget):
    """Widget that will handle the selection of the axis as well as generating WDataExtractor"""

    def __init__(self, parent=None):
        """Initialize the GUI according to machine type

        Parameters
        ----------
        self : WAxisManager
            a WAxisManager object
        parent : QWidget
            The parent widget
        """

        # Build the interface according to the .ui file
        QWidget.__init__(self, parent=parent)
        self.setupUi(self)

        self.w_axis_1.axisChanged.connect(self.axes_updated)
        self.w_axis_2.axisChanged.connect(self.gen_data_selec)

        # self.w_axis_1.opeChanged.connect(self.ope_sync)
        # self.w_axis_2.opeChanged.connect(self.ope_updated)



    def axes_updated(self):
        """Method that will check if the axes chosen are correct and if true it will update the comboboxes
        Parameters
        ----------
        self : WAxisManager
            a WAxisManager object
        data : DataND
            the DataND object that we want to plot
        
        """
         
        axis_selected = self.w_axis_1.get_current_axis_name()   #Recovering the axis selected by the user
        self.w_axis_2.remove_axis(axis_selected)                #Removing the axis selected from the the second axis combobox

        self.gen_data_selec()                                   #Generating the DataSelection GroupBox

        
    def gen_data_selec(self):
        """Method that gen the right WDataExtrator widget according to axes_list 
        Parameters
        ----------
        self : WAxisManager
            a WAxisManager object
        data : axes_list
            list of the axes that should be shown inside DataSelection
        """

        #Step 1 : Recovering the axis to generate (those that are not selected)
        axes_list = self.w_axis_1.get_axes_name()[:]

        axes_selected = list()
        axes_selected.append(self.w_axis_1.get_current_quantity())
        axes_selected.append(self.w_axis_2.get_current_quantity())

        for ax in reversed(axes_list):
            if ax in axes_selected:
                axes_list.remove(ax)

        #Step 2 : Deleting items in the layout currently
        if isinstance(self.lay_data_extract.takeAt(self.lay_data_extract.count()-1),QSpacerItem):
            self.lay_data_extract.takeAt(self.lay_data_extract.count()-1).widget().deleteLater()       

        for i in reversed(range (self.lay_data_extract.count())):
            self.lay_data_extract.takeAt(i).widget().deleteLater()
       
        #Step  3: Adding a WDataExtractor widget for each axis inside the layout 
        for axis in axes_list:
            self.w_data_sel = WDataExtractor(self.layoutWidget)
            self.w_data_sel.setObjectName(axis)
            self.w_data_sel.setMinimumSize(QSize(0, 80))
            self.w_data_sel.setMaximumSize(QSize(280, 80))

            self.lay_data_extract.addWidget(self.w_data_sel)

            if axis in axes_dict:
                self.w_data_sel.update(axes_dict[axis])
            else:
                self.w_data_sel.update(axis)

        #Step 4 : Adding a spacer to improve the UI visually 
        self.verticalSpacer = QSpacerItem(296, 50, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.lay_data_extract.addItem(self.verticalSpacer)

    # def ope_sync(self):
    #     """Method that will check the operation chosen and that update the other operation combobox.
    #     So that, by default, we have FFT and FFT or "" and ""
    #     Parameters
    #     ----------
    #     self : WAxisManager
    #         a WAxisManager object
        
    #     """
        
    #     operation_selected = (self.w_axis_1.get_current_ope_name())
    #     self.w_axis_2.set_operation(operation_selected)
    #     self.ope_updated()


    # def ope_updated(self):
    #     """Method that will check the operation chosen and that update the unit combobox
    #     Parameters
    #     ----------
    #     self : WAxisManager
    #         a WAxisManager object
        
    #     """

    #     #Changing the units available if the operation is an FFT or not
    #     if self.w_axis_1.get_current_ope_name() == "FFT" and self.w_axis_1.get_current_quantity() in fft_dict:
    #         self.w_axis_1.set_quantity(fft_dict[self.w_axis_1.get_current_quantity()])
            
    #     elif self.w_axis_1.get_current_ope_name() == "" and self.w_axis_1.get_current_quantity in ifft_dict:
    #         self.w_axis_1.set_quantity(ifft_dict[self.w_axis_1.get_current_quantity()])

    #     #Changing the units available if the operation is an FFT or not
    #     if self.w_axis_2.get_current_ope_name() == "FFT" and self.w_axis_2.get_current_quantity() in fft_dict:
    #         self.w_axis_2.set_quantity(fft_dict[self.w_axis_2.get_current_quantity()])
            
    #     elif self.w_axis_2.get_current_ope_name() == "" and self.w_axis_2.get_current_quantity in ifft_dict:
    #         self.w_axis_2.set_quantity(ifft_dict[self.w_axis_2.get_current_quantity()])
           

    def set_axes(self,data):
        """Method used to set the axes of the Axes group box as well as setting the widgets of the DataSelection groupbox
        Parameters
        ----------
        self : WAxisManager
            a WAxisManager object
        data : DataND
            The DataND object that we want to plot
        """
        self.w_axis_1.blockSignals(True)
        self.w_axis_2.blockSignals(True)
        self.w_axis_1.update(data)
        self.w_axis_2.update(data,axis_name="Y")
        self.w_axis_1.blockSignals(False)
        self.w_axis_2.blockSignals(False)
        self.axes_updated()

