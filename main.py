from PyQt6.QtWidgets import QMainWindow,QApplication,QWidget, QGridLayout,QLabel,QLineEdit,QPushButton,QTableWidget,QTableWidgetItem,\
    QDialog,QVBoxLayout,QComboBox,QToolBar, QStatusBar,QMessageBox
from PyQt6.QtGui import QAction,QIcon
from PyQt6.QtCore import Qt
import sys
import sqlite3

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(600,600)

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction(QIcon("icons/add.png"),"Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About",self)
        help_menu_item.addAction(about_action)
        about_action.triggered.connect(self.about)

        search_action = QAction(QIcon("icons/search.png"),"Search", self)
        edit_menu_item.addAction(search_action)
        search_action.triggered.connect(self.search)
        # create Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        # To hide the extra id col that comes by default
        self.table.verticalHeader().setVisible(False)

        self.setCentralWidget(self.table)

        #create a toolbar and add toolbar elements
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        #Create a Status Bar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        #Detect a Click
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        #fixing multiple edit and del button
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

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

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
        dialog.exec()

class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        self.setText("This app is created by Arpan Swain"\
                     "as a part of his project to gain better understanding"\
                     "of OOPs as well working with SQL")

class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        #Can also use a grid but vbox will be easy here
        layout = QVBoxLayout()


        #Get the name of student on the row on which user clicked
        row_num = main_window.table.currentRow()
        student_name = main_window.table.item(row_num,1).text()

        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        #Get the Id of student
        self.student_id = main_window.table.item(row_num,0).text()

        #Get the course name
        student_course_name = main_window.table.item(row_num, 2).text()
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Physics", "Astronomy"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(student_course_name)
        layout.addWidget(self.course_name)

        # Same for mob
        mob = main_window.table.item(row_num, 3).text()
        self.mobile_num = QLineEdit(mob)
        self.mobile_num.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile_num)

        button =QPushButton("Update")
        button.clicked.connect(self.update_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def update_student(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",
                       (self.student_name.text(),self.course_name.itemText(self.course_name.currentIndex()),
                        self.mobile_num.text(), self.student_id))
        connection.commit()
        cursor.close()
        connection.close()

        #Refresh the data
        main_window.load_data()

class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student Data")

        layout = QGridLayout()
        confirmation = QLabel("Are you sure?")
        yes = QPushButton("Yes")
        no = QPushButton("No")

        layout.addWidget(confirmation,0,0,1,2)
        layout.addWidget(yes,1,0)
        layout.addWidget(no,1,1)

        self.setLayout(layout)

        yes.clicked.connect(self.del_student)
        no.clicked.connect(self.close)

    def del_student(self):
        #Get selected row and studnt id
        row_num = main_window.table.currentRow()
        student_id = main_window.table.item(row_num, 0).text()

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("DELETE from students WHERE id = ?",(student_id,))

        connection.commit()
        cursor.close()
        connection.close()

        main_window.load_data()

        self.close()

        confirmation = QMessageBox()
        confirmation.setWindowTitle("Success")
        confirmation.setText("The record was deleted successfully !")
        # Execute Necessary
        confirmation.exec()


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


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        button = QPushButton("Search")
        button.clicked.connect(self.search)
        layout.addWidget(button)

        self.setLayout(layout)

    def search(self):
        name = self.student_name.text()

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name = ?",(name,))
        rows = list(result)
        print(rows)

        #The below is a generator
        items = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            main_window.table.item(item.row(),1).setSelected(True)

        cursor.close()
        connection.close()




app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())