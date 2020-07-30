# Author: Michael F Harris Jr and Mark Jones

import sys
import random
import matplotlib

from GUIProject.Seaborntest import MplCanvas

matplotlib.use('Qt5Agg')
from pathlib import Path
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# from PyPWA.libs.file import processor

"""New Import adds down below 10/11/2019"""
import matplotlib as plt
import seaborn as viz
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

viz.set()


# Introduction GUI Window
class IntroductionPWA(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        # Locks Introduction PWA window
        self.setFixedSize(800, 400)
        self.setWindowTitle('PyPWA 3')
        self.open_project_button()
        self.__new_project_button()
        self.__design()

    def __new_project_button(self):
        self.new = QtWidgets.QPushButton('New Project', self)
        self.new.clicked.connect(self.toggle_new_project)
        self.new.move(100, 300)

    def open_project_button(self):
        self.open = QtWidgets.QPushButton('Open Project', self)
        self.open.clicked.connect(self.toggle_open_project)
        self.open.move(600, 300)

    def __design(self):
        pwa = QtWidgets.QLabel(self)
        pwa.setPixmap(QtGui.QPixmap('pypwa.png'))
        pwa.move(125, 50)

        jlab = QtWidgets.QLabel('Thomas Jefferson National Accelerator Facility', self)
        jlab.setFont(QtGui.QFont("Times", 14, QtGui.QFont.Black))
        jlab.move(160, 175)

        nsu = QtWidgets.QLabel('Norfolk State University', self)
        nsu.setFont(QtGui.QFont("Times", 14, QtGui.QFont.Black))
        nsu.move(280, 215)

    def toggle_new_project(self):
        new_project = MagicWizard(self)
        new_project.show()

    def toggle_open_project(self):
        open_project = MainPWA()
        open_project.show()


# Setup Window(Wizard)
class MagicWizard(QtWidgets.QWizard):

    def __init__(self, parent=None):
        super(MagicWizard, self).__init__(parent)
        self.addPage(Page1(self))
        self.addPage(Fitting(self))
        self.addPage(Simulation(self))
        self.addPage(BinSettings(self))
        self.setWindowTitle("PyPWA 3 Wizard ")


class Page1(QtWidgets.QWizardPage):

    def __init__(self, parent=None):
        super(Page1, self).__init__(parent)
        print("Intialized Page 1")
        self.page_one_setup()
        self.page_one_layouts()
        self.toggle_fit()
        self.toggle_fit()

    def page_one_layouts(self):
        pwa = QtWidgets.QLabel(self)
        pwa.setPixmap(QtGui.QPixmap('pypwa.png'))
        information_layout = QtWidgets.QVBoxLayout()
        information_layout.addWidget(pwa)
        information_layout.addWidget(self.setup_box_one)
        self.setLayout(information_layout)

    def page_one_setup(self):
        self.setup_box_one = QtWidgets.QGroupBox()

        # Project Name area here
        project_layout = QtWidgets.QHBoxLayout()
        project_name_label = QtWidgets.QLabel('New Project Name:')
        project_name_label.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Black))
        project_name_text = QtWidgets.QLineEdit()
        project_layout.addWidget(project_name_label)
        project_layout.addWidget(project_name_text)

        # Basis area here
        basis_layout = QtWidgets.QHBoxLayout()
        basis_text = QtWidgets.QLabel('Basis')
        basis_text.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Black))
        basis_drop_box = QtWidgets.QComboBox()
        basis_drop_box.addItem("Basis Test 1")
        basis_drop_box.addItem("Basis Test 2")
        basis_layout.addWidget(basis_text)
        basis_layout.addWidget(basis_drop_box)

        # Frame area here
        frame_layout = QtWidgets.QHBoxLayout()
        frame_text = QtWidgets.QLabel('Frame')
        frame_text.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Black))
        frame_drop_box = QtWidgets.QComboBox()
        frame_drop_box.addItem("Frame Test 1")
        frame_drop_box.addItem("Frame Test 2")
        frame_layout.addWidget(frame_text)
        frame_layout.addWidget(frame_drop_box)

        # Project Types Area here
        project_type_layout = QtWidgets.QHBoxLayout()
        project_types_text = QtWidgets.QLabel('Project Types')
        project_types_text.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Black))
        project_types_drop_box = QtWidgets.QComboBox()
        project_types_drop_box.addItem("Fitting", self.toggle_fit)
        project_types_drop_box.addItem("Simulation", self.toggle_sim)
        project_type_layout.addWidget(project_types_text)
        project_type_layout.addWidget(project_types_drop_box)

        # Setup master Layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(project_layout)
        main_layout.addLayout(basis_layout)
        main_layout.addLayout(frame_layout)
        main_layout.addLayout(project_type_layout)

        self.setup_box_one.setLayout(main_layout)

    def toggle_fit(self):
        fit = Fitting()
        fit.show()

    def toggle_sim(self):
        sim = Simulation()
        sim.show()


class Fitting(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(Fitting, self).__init__(parent)
        self.fitting_setup()
        self.fitting_layout()

        # Simulation

    def fitting_layout(self):
        # pwa = QtWidgets.QLabel(self)
        # pwa.setPixmap(QtGui.QPixmap('pypwa.png'))
        information_layout = QtWidgets.QVBoxLayout()
        fitting_title = QtWidgets.QLabel("Fitting")
        fitting_title.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Black))
        information_layout.addWidget(fitting_title)
        # information_layout.addWidget(pwa)
        information_layout.addWidget(self.setup_box_two)
        self.setLayout(information_layout)

    def fitting_setup(self):
        self.setup_box_two = QtWidgets.QGroupBox()

        # Keyfiles
        keyfiles_layout = QtWidgets.QHBoxLayout()
        keyfiles_name_label = QtWidgets.QLabel('Keyfiles')
        keyfiles_name_label.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Black))
        keyfiles_folder = QtWidgets.QLineEdit()
        keyfiles_layout.addWidget(keyfiles_name_label)
        keyfiles_layout.addWidget(keyfiles_folder)

        # RAW
        fitting_raw_layout = QtWidgets.QHBoxLayout()
        fitting_raw_label = QtWidgets.QLabel('Raw:')
        fitting_raw_label.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Black))
        fitting_raw_files = QtWidgets.QLineEdit()
        fitting_raw_layout.addWidget(fitting_raw_label)
        fitting_raw_layout.addWidget(fitting_raw_files)

        # Data
        fitting_data_layout = QtWidgets.QHBoxLayout()
        fitting_data_label = QtWidgets.QLabel('Data:')
        fitting_data_label.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Black))
        fitting_data_file = QtWidgets.QLineEdit()
        fitting_data_layout.addWidget(fitting_data_label)
        fitting_data_layout.addWidget(fitting_data_file)

        # HCCMC

        # Minuit / Nestle
        minuit_nestle_layout = QtWidgets.QHBoxLayout()
        minuit_nestle_label = QtWidgets.QLabel("Minuit/Nestle:")
        minuit_nestle_label.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Black))

        # Setup master Layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(keyfiles_layout)
        main_layout.addLayout(fitting_raw_layout)

        self.setup_box_two.setLayout(main_layout)


class Simulation(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(Simulation, self).__init__(parent)
        self.simulation_setup()
        self.simulation_layout()

    # Simulation
    def simulation_layout(self):
        information_V_layout = QtWidgets.QVBoxLayout()
        simulation_title = QtWidgets.QLabel("Simulation")
        simulation_title.setFont(QtGui.QFont("Times", 14, QtGui.QFont.Black))
        information_V_layout.addWidget(simulation_title)
        information_V_layout.addWidget(self.setup_box_two)
        self.setLayout(information_V_layout)

    def simulation_setup(self):
        self.setup_box_two = QtWidgets.QGroupBox()

        # Keyfiles
        keyfiles_name_layout = QtWidgets.QHBoxLayout()
        keyfiles_name_label = QtWidgets.QLabel('Keyfiles:')
        keyfiles_name_label.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Black))
        keyfiles_folders = QtWidgets.QLineEdit()
        keyfiles_name_layout.addWidget(keyfiles_name_label)
        keyfiles_name_layout.addWidget(keyfiles_folders)

        # RAW
        simulation_raw_layout = QtWidgets.QHBoxLayout()
        simulation_raw_label = QtWidgets.QLabel('Raw:')
        simulation_raw_label.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Black))
        simulation_raw_files = QtWidgets.QLineEdit()
        simulation_raw_layout.addWidget(simulation_raw_label)
        simulation_raw_layout.addWidget(simulation_raw_files)

        # Use VS
        simulation_vs_layout = QtWidgets.QHBoxLayout()
        simulation_vs = QtWidgets.QLabel('Use VS:')  # Check Box would go beside it
        simulation_vs.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Black))
        simulation_vs_checkbox = QtWidgets.QCheckBox()
        simulation_vs_layout.addWidget(simulation_vs)
        simulation_vs_layout.addWidget(simulation_vs_checkbox)

        # VS Location
        simulation_vs_location_layout = QtWidgets.QHBoxLayout()
        simulation_vs_location = QtWidgets.QLabel('VS Location:')
        simulation_vs_location.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Black))
        simulation_vs_location_dict = QtWidgets.QLineEdit()
        simulation_vs_location_layout.addWidget(simulation_vs_location)
        simulation_vs_location_layout.addWidget(simulation_vs_location_dict)

        # Setup master Layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(keyfiles_name_layout)
        main_layout.addLayout(simulation_raw_layout)
        main_layout.addLayout(simulation_vs_layout)
        main_layout.addLayout(simulation_vs_location_layout)

        self.setup_box_two.setLayout(main_layout)

    # def VS_Checkbox(self):
    #   if state == QtCore.Qt.Checked:
    #       print('Checked')
    #   else:
    #       print('Unchecked')


class BinSettings(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(BinSettings, self).__init__(parent)


# Main GUI Window
class MainPWA(QtWidgets.QMainWindow, QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        # Set the size of window box
        self.Width = 1060
        self.height = int(0.618 * self.Width)
        self.resize(self.Width, self.height)
        self.setWindowTitle("PyPWA")
        self.__menu_bar = self.menuBar()
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)
        table = TableWidget(self, True)
        grid_layout = QtWidgets.QGridLayout(self)
        grid_layout.addWidget(table)
        central_widget.setLayout(grid_layout)

        self.__file_menu()
        self.__edit_menu()

    def __file_menu(self):
        file_menu = self.__menu_bar.addMenu("File")
        new_project = QtWidgets.QAction(QtGui.QIcon(), 'New Project', self)
        new_project.setStatusTip('Created A New Project name: ')
        # Need works for saving project
        new_project.triggered.connect(self.saveState)
        file_menu.addAction(new_project)

        # Create New File
        new_file = QtWidgets.QAction(QtGui.QIcon(), 'New File', self)
        new_file.setStatusTip('Created A New File: ')
        file_menu.addAction(new_file)

        # Save Files
        save_file_buttom = QtWidgets.QAction(QtGui.QIcon(), 'Save', self)
        save_file_buttom.setShortcut('Ctrl+S')
        # Note: Make sure to link File Path to status bar!!!!
        save_file_buttom.setStatusTip('File Saved: ')
        save_file_buttom.triggered.connect(self.close)
        file_menu.addAction(save_file_buttom)
        # Set an algorithm to Save files and SaveAs

        # Save As Files
        save_as_file_file_button = QtWidgets.QAction(QtGui.QIcon(), 'Save As', self)
        save_as_file_file_button.setShortcut('Ctrl+Shift+S')
        # Note: Make sure to link File Path to status bar!!!!
        save_as_file_file_button.setStatusTip('File Save As: ')
        save_as_file_file_button.triggered.connect(self.close)
        file_menu.addAction(save_as_file_file_button)

        # Exit Out from the program
        exit_button = QtWidgets.QAction(QtGui.QIcon(), 'Exit', self)
        exit_button.setShortcut('Ctrl+Q')
        exit_button.setStatusTip('Exit application')
        exit_button.triggered.connect(self.close)
        file_menu.addAction(exit_button)

    def __edit_menu(self):
        edit_menu = self.__menu_bar.addMenu("Edit")
        # Undo
        undo = QtWidgets.QAction(QtGui.QIcon(), 'Undo', self)
        undo.setShortcut('Ctrl+Z')
        undo.setStatusTip('Undo')
        edit_menu.addAction(undo)

        # Redo
        redo = QtWidgets.QAction(QtGui.QIcon(), 'Redo', self)
        redo.setShortcut('Ctrl+X')
        redo.setStatusTip('Redo')
        edit_menu.addAction(redo)

        self.__view_menu()

    def __view_menu(self):
        view_menu = self.__menu_bar.addMenu("View")

        # Maximize Screen
        maximize_screen = QtWidgets.QAction(QtGui.QIcon(), 'Maximize Screen', self)
        maximize_screen.setShortcut('Shift+F9')
        maximize_screen.setStatusTip('Minimize Screen')
        maximize_screen.triggered.connect(self.showMaximized)
        view_menu.addAction(maximize_screen)

        # Minimize Screen
        minimize_screen = QtWidgets.QAction(QtGui.QIcon(), 'Minimize Screen', self)
        minimize_screen.setShortcut('Shift+F9')
        minimize_screen.setStatusTip('Minimize Screen')
        minimize_screen.triggered.connect(self.showMinimized)
        view_menu.addAction(minimize_screen)

        # FullScreen
        fullscreen = QtWidgets.QAction(QtGui.QIcon(), 'FullScreen', self)
        fullscreen.setShortcut('Shift+F10')
        fullscreen.setStatusTip('Enabled Fullscreen Window')
        fullscreen.triggered.connect(self.showFullScreen)
        view_menu.addAction(fullscreen)

        self.__help_menu()

    def __help_menu(self):
        help_menu = self.__menu_bar.addMenu("Help")
        _help = QtWidgets.QAction(QtGui.QIcon(), 'Help', self)
        _help.setStatusTip('Help')
        # Help.triggered.connect(self.)
        help_menu.addAction(_help)

        report = QtWidgets.QAction(QtGui.QIcon(), 'Report', self)
        report.setStatusTip('Enabled Fullscreen Window')
        # Report.triggered.connect(self.)
        help_menu.addAction(report)

        about = QtWidgets.QAction(QtGui.QIcon(), 'About', self)
        about.setStatusTip('About')
        # About.triggered.connect(self.)
        help_menu.addAction(about)

        self.__subproject_menu()

    def __subproject_menu(self):
        subproject_menu = self.__menu_bar.addMenu("Subproject")
        mc = QtWidgets.QAction(QtGui.QIcon(), 'MC', self)
        mc.setStatusTip('MC')
        subproject_menu.addAction(mc)

        cha = QtWidgets.QAction(QtGui.QIcon(), 'CHA', self)
        cha.setStatusTip('CHA')
        subproject_menu.addAction(cha)

        new_subproject = QtWidgets.QAction(QtGui.QIcon(), 'New Subproject', self)
        new_subproject.setStatusTip('New Subproject')
        subproject_menu.addAction(new_subproject)

        self.status_bar()

    def status_bar(self):
        # Set the status bar
        self.statusBar().showMessage("Status Bar: ")

        self.__file_browser_side_bar()

        self.__jobs_side_bar()

    def __jobs_side_bar(self):
        # Set the Filling SideBar layout
        self.job_bar = QtWidgets.QDockWidget("Jobs", self)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.job_bar)
        self.dockedWidget = QtWidgets.QWidget(self)
        self.job_bar.setWidget(self.dockedWidget)
        self.dockedWidget.setLayout(QtWidgets.QVBoxLayout())

        self.__project_side_bar()

    def __project_side_bar(self):
        # Set the Filling SideBar layout
        self.project_side_bar = QtWidgets.QDockWidget("Projects", self)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.project_side_bar)
        self.dockedWidget = QtWidgets.QWidget(self)
        self.project_side_bar.setWidget(self.dockedWidget)
        self.dockedWidget.setLayout(QtWidgets.QVBoxLayout())

        self.__log_side_bar()

    def __log_side_bar(self):
        # Set the Bottom SideBar layout
        self.log_side_bar = QtWidgets.QDockWidget("Log", self)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.log_side_bar)
        self.dockedWidget = QtWidgets.QWidget(self)
        self.log_side_bar.setWidget(self.dockedWidget)

    def __file_browser_side_bar(self):
        self.file_browser_side_bar = QtWidgets.QDockWidget("File Browser", self)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.file_browser_side_bar)
        self.dockedWidget = FileBrowser()
        self.file_browser_side_bar.setWidget(self.dockedWidget)


# class MyDialog(QtWidgets.QPlainTextEdit):
#   def __init__(self, parent=None):
#      super(MyDialog, self).__init__(parent)
#
#       log_text_box = QPlainTextEdit()
# You can format what is printed to text box
#   log_text_box.setFormatter(
#        logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
#   logging.getLogger().addHandler(log_text_box)
# You can control the logging level
#  logging.getLogger().setLevel(logging.DEBUG)

# l = logging.getLogger()

# for index in range(0, 10):
#   l.info(f"At place{index}")
#    def test(self):
#       logging.debug('damn, a bug')
#      logging.info('something to remember')
#     logging.warning('that\'s not right')
#    logging.error('foobar')


class FileBrowser(QtWidgets.QTreeWidget):

    def __init__(self, dir: Path = Path("."), include_hidden: bool = False):
        super(FileBrowser, self).__init__()
        self.__root_dir = dir
        self.__include_hidden = include_hidden
        self.__populate_directory_tree(dir, self)

    def __repr__(self):
        return f"FileBrowser({self.__root_dir}, {self.__include_hidden})"

    def __populate_directory_tree(self, root_folder, parent):
        for element in root_folder.glob("*"):
            if not str(element.stem)[0] == "." or self.__include_hidden:

                new_parent = QtWidgets.QTreeWidgetItem(parent, [str(element.stem)])
                if element.is_dir():
                    self.__populate_directory_tree(element, new_parent)
                    new_parent.setIcon(0, QtGui.QIcon().fromTheme("folder"))
                else:
                    new_parent.setIcon(0, QtGui.QIcon().fromTheme("text-x-generic"))


class TableWidget(QtWidgets.QWidget):

    def __init__(self, parent, is_simulation=False):
        super(QtWidgets.QWidget, self).__init__(parent)
        self.layout = QtWidgets.QVBoxLayout(self)
        # Initialize tab screen
        self.tabs = QtWidgets.QTabWidget()
        self.simulation = QtWidgets.QWidget()
        self.fitting = QtWidgets.QWidget()
        self.resonance = Resonance(self)
        self.data = QtWidgets.QWidget()
        self.data_box()
        self.grid = QtWidgets.QGridLayout()

        self.plots = Plots(self)

        self.tabs.resize(300, 200)
        self.lbl = QtWidgets.QLabel("", self)

        # Add tabs
        if is_simulation:
            self.tabs.addTab(self.simulation, "Simulation")
        else:
            self.tabs.addTab(self.fitting, "Fitting")
        self.tabs.addTab(self.resonance, "Resonance")
        self.tabs.addTab(self.data, "Data")
        self.tabs.addTab(self.plots, "Plots")

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def data_box(self):
        self.data_table = QtWidgets.QTableWidget()
        self.data_table.setRowCount(4)
        self.data_table.setColumnCount(3)
        self.data_table.setHorizontalHeaderLabels(["X", "Y", "Z"])
        self.data_table.setItem(0, 0, QtWidgets.QTableWidgetItem("TEST"))
        self.data_table.setItem(0, 1, QtWidgets.QTableWidgetItem("TEST"))
        self.data_table.setItem(1, 0, QtWidgets.QTableWidgetItem())
        self.data_table.setItem(1, 1, QtWidgets.QTableWidgetItem())
        self.data_table.setItem(2, 0, QtWidgets.QTableWidgetItem())
        self.data_table.setItem(2, 1, QtWidgets.QTableWidgetItem())
        self.data_table.setItem(3, 0, QtWidgets.QTableWidgetItem())
        self.data_table.setItem(3, 1, QtWidgets.QTableWidgetItem())

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.data_table)
        self.data.setLayout(layout)


class Controls(QtWidgets.QWidget):

    def __int__(self, parent=None):
        super(Controls, self).__int__(parent)


class Resonance(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(Resonance, self).__init__(parent)
        self.__create_layouts()

    def __create_layouts(self):
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(self.__create_main_layout())
        main_layout.addLayout(self.__create_button_layout())
        self.setLayout(main_layout)

    def __create_main_layout(self):
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.__check_list())
        layout.addWidget(self.__resonance_table())
        return layout

    @staticmethod
    def __check_list():
        check_list = QtWidgets.QListWidget()
        str_list = ["Test", "Test", "Test"]
        check_list.addItems(str_list)

        for index in range(check_list.count()):
            item = check_list.item(index)
            item.setFlags(
                QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled
            )
            item.setCheckState(QtCore.Qt.Unchecked)

        return check_list

    @staticmethod
    def __resonance_table():
        table = QtWidgets.QTableWidget()
        table.setRowCount(4)
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["X", "Y", "Z"])
        table.setItem(0, 0, QtWidgets.QTableWidgetItem("TEST"))
        table.setItem(0, 1, QtWidgets.QTableWidgetItem("TEST"))
        table.setItem(1, 0, QtWidgets.QTableWidgetItem())
        table.setItem(1, 1, QtWidgets.QTableWidgetItem())
        table.setItem(2, 0, QtWidgets.QTableWidgetItem())
        table.setItem(2, 1, QtWidgets.QTableWidgetItem())
        table.setItem(3, 0, QtWidgets.QTableWidgetItem())
        table.setItem(3, 1, QtWidgets.QTableWidgetItem())
        return table

    def __create_button_layout(self):
        save_button = QtWidgets.QPushButton("SAVE")
        restore_button = QtWidgets.QPushButton("Restore")
        save_button.clicked.connect(self.__save_toggle_resonance_window)
        restore_button.clicked.connect(self.__restore_toggle_resonance_window)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(save_button)
        layout.addWidget(restore_button)
        layout.setAlignment(QtCore.Qt.AlignRight)
        return layout

    def __save_toggle_resonance_window(self):
        new_window = ResonanceSaveWindow(self)
        new_window.show()

    def __restore_toggle_resonance_window(self):
        new_window = ResonanceRestoreWindow(self)
        new_window.show()


class ResonanceSaveWindow(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(ResonanceSaveWindow, self).__init__(parent)

        options = QtWidgets.QFileDialog.Option()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save File", "", "All Files (*);;Text Files (*.txt)", options=options
        )
        if fileName:
            print(fileName)


class ResonanceRestoreWindow(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(ResonanceRestoreWindow, self).__init__(parent)
        # ISSUE: whenever file dialog is open, if you push cancel it'll close out the whole window
        options = QtWidgets.QFileDialog.Option()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        filename, = QtWidgets.QFileDialog.getSaveFileName(
            self, "Restore File", "", "All Files (*);;Text Files (*.txt)", options=options
        )
        if filename:
            print(filename)


class Plots(FigureCanvas):
    """Design: top box would have tabs for display controls, middle box is plotting, and bottom box would be
   main controls.
   Imports: seaborn, matplotlib"""

    def __init__(self, parent=None, width=5, height=5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

    #     self.plot()
    #
    # def plot(self):
    #
    #     x = np.array([50, 30, 40])
    #     labels = ["TESTING", "TESTING", "TESTING"]
    #     ax = self.figure.add_subplot(111)
    #     ax.pie(x, labels=labels)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('pypwaicon1.png'))
    gui = IntroductionPWA()
    gui.show()
    app.exec_()

