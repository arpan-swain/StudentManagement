from PyQt6.QtWidgets import QMainWindow,QApplication,QWidget, QGridLayout,QLabel,QLineEdit,QPushButton
from PyQt6.QtGui import QAction
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")

        add_student_action = QAction("Add Student", self)
        file_menu_item.addAction(add_student_action)

        help_action = QAction("About",self)
        help_menu_item.addAction(help_action)




app = QApplication(sys.argv)
app_calculator = MainWindow()
app_calculator.show()
sys.exit(app.exec())