'''
Created on Oct 29, 2015

@author: Kagiu
'''

import sys, inspect
from PySide import QtGui, QtCore
from signin import TimeLogger

def boxToWidget(layout):
    widget = QtGui.QWidget()
    widget.setLayout(layout)
    return widget

class SignGUI(QtGui.QMainWindow):
    def __init__(self):
        super(SignGUI, self).__init__()
        self.logger = TimeLogger()
        self.setWindowTitle("Metrobots Sign-In")
        self.initMain()
        self.initAdmin()
        self.initMenu()
        self.show()
    
    def initMain(self): #Main sign-in code
        self.lineEdit = QtGui.QLineEdit(self)
        self.lineEdit.setPlaceholderText("Your name here")
        self.lineEdit.editingFinished.connect(self.register)
        self.autoComplete()
        
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(QtGui.QLabel("Name:", self))
        hbox.addWidget(self.lineEdit)
        
        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(hbox)
        
        self.tabs = QtGui.QTabWidget()
        self.tabs.addTab(boxToWidget(vbox), "Sign-in")
        self.setCentralWidget(self.tabs)
    
    def initAdmin(self): #Admin code
        self.timelist = QtGui.QTreeWidget(self) #Total time
        self.timelist.setColumnCount(2)
        self.timelist.setHeaderLabels(["Name", "Total time"])
        try: self.populateTotal()
        except Exception as e: print(e)
        refreshBtn = QtGui.QPushButton("Refresh", self)
        refreshBtn.clicked.connect(self.populateTotal)
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.timelist)
        vbox.addWidget(refreshBtn)
        self.tabs.addTab(boxToWidget(vbox), "Total time")
        
        self.lookup = QtGui.QLineEdit()
        self.timetable = QtGui.QTreeWidget()
        self.timetable.setColumnCount(3)
        self.timetable.setHeaderLabels(["Time in", "Time out", "Total time"])
        vbox2 = QtGui.QVBoxLayout()
        vbox2.addWidget(self.lookup)
        vbox2.addWidget(self.timetable)
        self.tabs.addTab(boxToWidget(vbox2), "Individual time")
        self.tabs.setTabEnabled(1, False)
        self.tabs.setTabEnabled(2, False)
    
    def initMenu(self):
        self.admin = QtGui.QAction("&Enable data access", self)
        self.admin.setCheckable(True)
        self.admin.triggered.connect(self.enableAdmin)
        
        filemenu = self.menuBar().addMenu("&File")
        filemenu.addAction(self.admin)
    
    def enableAdmin(self):
        if not self.admin.isChecked():
            self.tabs.setTabEnabled(1, False)
            self.tabs.setTabEnabled(2, False)
        else:
            passwd = QtGui.QInputDialog.getText(self, "Password required", "Enter password",
                                                QtGui.QLineEdit.Password)
            print(passwd)
            if passwd[0] == "3324":
                self.tabs.setTabEnabled(1, True)
                self.tabs.setTabEnabled(2, True)
            else:
                QtGui.QMessageBox.warning(self, "Error", "Wrong password.")
                self.admin.setChecked(False)
    
    def autoComplete(self):
        completer = QtGui.QCompleter(self.logger.names(), self)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        completer.activated.connect(self.register)
        self.lineEdit.setCompleter(completer)
     
    def populateTotal(self):
        self.timelist.clear()
        times = []
        for name in self.logger.names():
            times.append(QtGui.QTreeWidgetItem([name, str(self.logger.getTime(name))]))
        self.timelist.addTopLevelItems(times)
    
    def register(self):
        #print(inspect.stack()[1])
        name = self.lineEdit.text().title()
        if name not in self.logger.names():
            reply = QtGui.QMessageBox.question(self, 'Message', name + " is not in the roster. Would you like to add it?",
                                               QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                               QtGui.QMessageBox.Yes)
            if reply == QtGui.QMessageBox.No:
                QtGui.QMessageBox.information(self, "", "Not adding " + name + ".")
                return
            self.autoComplete()
        
        self.lineEdit.clear()
        self.lineEdit.setText("")
        status = self.logger.register(name)
        self.statusBar().clear()
        self.statusBar().showMessage(name + " has been signed " + ("in." if status else "out."))


def main():
    app = QtGui.QApplication(sys.argv)
    gui = SignGUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()