from PyQt6.QtWidgets import QMainWindow,QApplication,QWidget, QGridLayout,QLabel,QLineEdit,QPushButton,QTableWidget,QTableWidgetItem
from PyQt6.QtGui import QAction
import sys
import sqlite3

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setGeometry(100, 100, 400, 300)

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")

        add_student_action = QAction("Add Student", self)
        file_menu_item.addAction(add_student_action)

        help_action = QAction("About",self)
        help_menu_item.addAction(help_action)

        # create Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        # To hide the extra id col that comes by default
        self.table.verticalHeader().setVisible(False)

        self.setCentralWidget(self.table)

    def load_data(self):
        connection = sqlite3.connect("database.db")
        #The following is a cursor object.. u can cvt it to list and then print to see what its structure looks like
        results = connection.execute("SELECT * FROM students")
        #This line makes sure that ebvery time u run the program, the data is freshly loaded and not stacked upon
        self.table.setRowCount(0)
        for row_num, row_data in enumerate(results):
            self.table.insertRow(row_num)
            for column_num, data in enumerate(row_data):
                self.table.setItem(row_num,column_num, QTableWidgetItem(str(data)))
        connection.close()


app = QApplication(sys.argv)
app_calculator = MainWindow()
app_calculator.show()
app_calculator.load_data()
sys.exit(app.exec())