from PyQt6.QtWidgets import (QWidget, QMessageBox, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
                             QFormLayout, QTableWidget, QTableWidgetItem)
from PyQt6.QtCore import Qt
from utils_ import add_entry, search_entry, generate_pass, load_all_data


class PasswordManagerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Password Manager")
        self.setFixedSize(400, 400)
        self.setup_ui()

    def setup_ui(self):
        # ENTRIES
        self.website_input = QLineEdit()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()

        # BUTTONS
        self.generate_btn = QPushButton("Generate")
        self.add_btn = QPushButton("Add")
        self.search_btn = QPushButton("search")

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.generate_btn)
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.search_btn)

        self.add_btn.clicked.connect(self.add_entry)
        self.search_btn.clicked.connect(self.search_entry)
        self.generate_btn.clicked.connect(self.gen_pass)

        # INPUT
        form_layout = QFormLayout()
        form_layout.addRow("Website:", self.website_input)
        form_layout.addRow("username:", self.username_input)
        form_layout.addRow("Password:", self.password_input)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addSpacing(10)
        main_layout.addLayout(btn_layout)

        # PASS TABLE UI
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Website", "Username", "Password"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  # disables editing sells

        self.setLayout(main_layout)
        main_layout.addSpacing(15)
        main_layout.addWidget(self.table)
        self.load_data()

    def add_entry(self):
        web = self.website_input.text()
        user = self.username_input.text()
        pswd = self.password_input.text()

        print("⏳ Trying to save entry...")

        success, message = add_entry(web, user, pswd)
        # save_entry -> t/f + success or error message

        if success:
            print("✅ Entry saved. Showing message...")
            QMessageBox.information(self, "Success", message)
            self.website_input.clear()
            self.username_input.clear()
            self.password_input.clear()

            print("📥 Loading data into table...")
            self.load_data()
        else:
            QMessageBox.warning(self, "Error", message)

    def gen_pass(self):
        pswd = generate_pass()
        self.password_input.setText(pswd)

    def search_entry(self):
        web = self.website_input.text()
        success, result = search_entry(web)

        if success:
            username, password = result
            self.username_input.setText(username)
            self.password_input.setText(password)

        else:
            QMessageBox.warning(self, "Not found", result)

    def load_data(self):
        data = load_all_data()
        self.table.setRowCount(0)

        for row, (website, creds) in enumerate(data.items()):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(website))
            self.table.setItem(row, 1, QTableWidgetItem(creds["username"]))
            self.table.setItem(row, 2, QTableWidgetItem(creds["password"]))