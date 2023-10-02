from PyQt6.QtWidgets import QMainWindow,QApplication,QWidget, QGridLayout,QLabel,QLineEdit,QPushButton,QTableWidget,QTableWidgetItem,\
    QDialog,QVBoxLayout,QComboBox
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
        add_student_action.triggered.connect(self.insert)
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

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        #Can also use a grid but vbox will be easy here
        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Physics", "Astronomy"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        self.mobile_num = QLineEdit()
        self.mobile_num.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile_num)

        button =QPushButton("Register")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        name, course, mobile = (self.student_name.text(),
                                self.course_name.itemText(self.course_name.currentIndex()),
                                self.mobile_num.text())

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?,?,?)", (name, course, mobile))

        connection.commit()
        cursor.close()
        connection.close()

        main_window.load_data()

app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())