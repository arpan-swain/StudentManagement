from PyQt6.QtWidgets import QApplication,QWidget, QGridLayout,QLabel,QLineEdit,QPushButton
import sys
from datetime import datetime

class AgeCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Age Calculator")

        #Createdgrid obj
        grid = QGridLayout()

        #Create Widgets
        self.name_label = QLabel("Name : ")
        self.name_line_edit =QLineEdit()

        dob_label = QLabel("Enter DOB in MM/DD/YYYY format : ")
        self.dob_line_edit = QLineEdit()

        calc_btn = QPushButton("Calculate Age")
        calc_btn.clicked.connect(self.calculate_age)

        self.output_label = QLabel("")

        #add widgets to grid
        grid.addWidget(self.name_label,0,0)
        grid.addWidget(self.name_line_edit,0,1)
        grid.addWidget(dob_label,1,0)
        grid.addWidget(self.dob_line_edit,1,1)
        grid.addWidget(calc_btn,2,0,1,2)
        grid.addWidget(self.output_label,3,0,1,2)

        self.setLayout(grid)

    def calculate_age(self):
        current_year = datetime.now().year
        date_of_birth = self.dob_line_edit.text()
        year_of_birth = datetime.strptime(date_of_birth, "%m/%d/%Y").date().year
        age = current_year - year_of_birth
        self.output_label.setText(f"{self.name_line_edit.text()} is {age} years old")



app = QApplication(sys.argv)
app_calculator = AgeCalculator()
app_calculator.show()
sys.exit(app.exec())