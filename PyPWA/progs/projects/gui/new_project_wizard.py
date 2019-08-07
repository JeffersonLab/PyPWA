import enum

from PyQt5 import QtCore, QtWidgets, QtGui


class MagicWizard(QtWidgets.QWizard):

    class _WizardPages(enum.IntEnum):
        Intro = enum.auto()
        Fitting = enum.auto()
        Simulation = enum.auto()
        BinSettings = enum.auto()

    def __init__(self, parent=None):
        super(MagicWizard, self).__init__(parent)
        self.setWindowTitle("PyPWA 3 Wizard ")
        self.setPage(self._WizardPages.Intro, IntroPage(self))
        self.setPage(self._WizardPages.Fitting, FittingPage(self))
        self.setPage(self._WizardPages.Simulation, Simulation(self))
        self.setPage(self._WizardPages.BinSettings, BinSettings(self))

    def nextId(self) -> int:
        if self.currentId() == self._WizardPages.Intro:
            if self.field("Project Type") == 1:
                return self._WizardPages.Simulation
            else:
                return self._WizardPages.Fitting
        elif self.currentId() == self._WizardPages.Fitting:
            return self._WizardPages.BinSettings
        elif self.currentId() == self._WizardPages.BinSettings:
            return -1
        else:
            return self.currentId() + 1


class IntroPage(QtWidgets.QWizardPage):

    def __init__(self, parent=None):
        super(IntroPage, self).__init__(parent)
        self.__setup_page()

    def __setup_page(self):
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.__get_logo_widget())
        layout.addLayout(self.__get_project_name_layout())
        layout.addLayout(self.__get_basis_layout())
        layout.addLayout(self.__get_frame_layout())
        layout.addLayout(self.__get_project_type_layout())
        self.setLayout(layout)

    def __get_logo_widget(self) -> QtWidgets.QLabel:
        pwa = QtWidgets.QLabel(self)
        pwa.setPixmap(QtGui.QPixmap('pypwa.png'))
        return pwa

    def __get_project_name_layout(self) -> QtWidgets.QHBoxLayout:
        project_name_textbox = QtWidgets.QLineEdit()
        self.registerField("Project Name", project_name_textbox)

        project_name_label = QtWidgets.QLabel('New Project Name:')
        project_name_label.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Black))
        project_name_label.setBuddy(project_name_textbox)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(project_name_label)
        layout.addWidget(project_name_textbox)
        return layout

    def __get_basis_layout(self) -> QtWidgets.QHBoxLayout:
        basis_drop_box = QtWidgets.QComboBox()
        basis_drop_box.addItem("Basis Test 1")
        basis_drop_box.addItem("Basis Test 2")
        self.registerField("Basis", basis_drop_box)

        basis_text = QtWidgets.QLabel('Basis')
        basis_text.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Black))
        basis_text.setBuddy(basis_drop_box)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(basis_text)
        layout.addWidget(basis_drop_box)
        return layout

    def __get_frame_layout(self) -> QtWidgets.QHBoxLayout:
        frame_drop_box = QtWidgets.QComboBox()
        frame_drop_box.addItem("Frame Test 1")
        frame_drop_box.addItem("Frame Test 2")
        self.registerField("Frame", frame_drop_box)

        frame_text = QtWidgets.QLabel('Frame')
        frame_text.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Black))
        frame_text.setBuddy(frame_drop_box)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(frame_text)
        layout.addWidget(frame_drop_box)
        return layout

    def __get_project_type_layout(self) -> QtWidgets.QHBoxLayout:
        project_types_drop_box = QtWidgets.QComboBox()
        project_types_drop_box.addItem("Fitting")
        project_types_drop_box.addItem("Simulation")
        self.registerField("Project Type", project_types_drop_box)

        project_types_text = QtWidgets.QLabel('Project Types')
        project_types_text.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Black))
        project_types_text.setBuddy(project_types_drop_box)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(project_types_text)
        layout.addWidget(project_types_drop_box)
        return layout


class _ProjectTypeBase(QtWidgets.QWizardPage):

    def __init__(self, parent=None):
        super(_ProjectTypeBase, self).__init__(parent)

    def _get_keyfiles_layout(self) -> QtWidgets.QHBoxLayout:
        keyfiles_folder = QtWidgets.QLineEdit()
        self.setField("keyfiles folder", keyfiles_folder)

        keyfiles_name_label = QtWidgets.QLabel('Keyfiles')
        keyfiles_name_label.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Black))
        keyfiles_name_label.setBuddy(keyfiles_folder)

        keyfiles_layout = QtWidgets.QHBoxLayout()
        keyfiles_layout.addWidget(keyfiles_name_label)
        keyfiles_layout.addWidget(keyfiles_folder)
        return keyfiles_layout

    def _get_raw_layout(self) -> QtWidgets.QHBoxLayout:
        fitting_raw_files = QtWidgets.QLineEdit()
        self.setField("raw files", fitting_raw_files)

        fitting_raw_label = QtWidgets.QLabel('Raw:')
        fitting_raw_label.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Black))
        fitting_raw_label.setBuddy(fitting_raw_files)

        fitting_raw_layout = QtWidgets.QHBoxLayout()
        fitting_raw_layout.addWidget(fitting_raw_label)
        fitting_raw_layout.addWidget(fitting_raw_files)
        return fitting_raw_layout

    def _get_data_layout(self) -> QtWidgets.QHBoxLayout:
        fitting_data_file = QtWidgets.QLineEdit()
        self.setField("data file", fitting_data_file)

        fitting_data_label = QtWidgets.QLabel('Data:')
        fitting_data_label.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Black))
        fitting_data_label.setBuddy(fitting_data_file)

        fitting_data_layout = QtWidgets.QHBoxLayout()
        fitting_data_layout.addWidget(fitting_data_label)
        fitting_data_layout.addWidget(fitting_data_file)
        return fitting_data_layout


class FittingPage(_ProjectTypeBase):
    def __init__(self, parent=None):
        super(FittingPage, self).__init__(parent)
        self.setTitle("Fitting")
        self.__setup_page()

    def __setup_page(self):
        information_layout = QtWidgets.QVBoxLayout()
        information_layout.addLayout(self._get_keyfiles_layout())
        information_layout.addLayout(self._get_raw_layout())
        information_layout.addLayout(self._get_data_layout())
        information_layout.addLayout(self.__get_minimization_layout())
        self.setLayout(information_layout)

    def __get_minimization_layout(self) -> QtWidgets.QHBoxLayout:
        optimizer_box = QtWidgets.QComboBox()
        optimizer_box.addItem("Minuit")
        optimizer_box.addItem("Nestle")
        self.setField("optimizer", optimizer_box)

        minuit_nestle_label = QtWidgets.QLabel("Optimizer:")
        minuit_nestle_label.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Black))
        minuit_nestle_label.setBuddy(optimizer_box)

        minuit_nestle_layout = QtWidgets.QHBoxLayout()
        minuit_nestle_layout.addWidget(minuit_nestle_label)
        minuit_nestle_layout.addWidget(optimizer_box)
        return minuit_nestle_layout


class Simulation(_ProjectTypeBase):
    def __init__(self, parent=None):
        super(Simulation, self).__init__(parent)
        self.setTitle("Simulation")
        self.__setup_page()

        self.__vs_checkbox.clicked.connect(self.__toggle_hide_vs_location)
        self.__toggle_hide_vs_location()

    def __setup_page(self):
        information_V_layout = QtWidgets.QVBoxLayout()
        information_V_layout.addLayout(self._get_keyfiles_layout())
        information_V_layout.addLayout(self._get_raw_layout())
        information_V_layout.addLayout(self.__get_vs_checkbox_layout())
        information_V_layout.addLayout(self.__get_vs_location_layout())
        self.setLayout(information_V_layout)

    def __get_vs_checkbox_layout(self) -> QtWidgets.QHBoxLayout:
        self.__vs_checkbox = QtWidgets.QCheckBox(self)
        self.setField("use vs", self.__vs_checkbox)

        simulation_vs = QtWidgets.QLabel('Use VS:')
        simulation_vs.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Black))
        simulation_vs.setBuddy(self.__vs_checkbox)

        simulation_vs_layout = QtWidgets.QHBoxLayout()
        simulation_vs_layout.setAlignment(QtCore.Qt.AlignLeft)
        simulation_vs_layout.addWidget(simulation_vs)
        simulation_vs_layout.addWidget(self.__vs_checkbox)
        return simulation_vs_layout

    def __get_vs_location_layout(self) -> QtWidgets.QHBoxLayout:
        self.__vs_location_textbox = QtWidgets.QLineEdit(self)
        self.setField("vs location", self.__vs_location_textbox)

        self.__vs_location_label = QtWidgets.QLabel('VS Location:')
        self.__vs_location_label.setFont(
            QtGui.QFont("Times", 12, QtGui.QFont.Black)
        )
        self.__vs_location_label.setBuddy(self.__vs_location_textbox)

        simulation_vs_location_layout = QtWidgets.QHBoxLayout()
        simulation_vs_location_layout.addWidget(self.__vs_location_label)
        simulation_vs_location_layout.addWidget(self.__vs_location_textbox)
        return simulation_vs_location_layout

    def __toggle_hide_vs_location(self):
        if self.__vs_checkbox.isChecked():
            self.__vs_location_textbox.setEnabled(True)
        else:
            self.__vs_location_textbox.setEnabled(False)


class BinSettings(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(BinSettings, self).__init__(parent)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    w = MagicWizard()
    w.show()
    app.exec_()
