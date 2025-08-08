from PyQt6.QtWidgets import (QWidget, QMessageBox, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
                             QFormLayout, QTableWidget, QTableWidgetItem, QApplication)
from PyQt6.QtGui import QGuiApplication
from utils_ import add_entry, search_entry, generate_pass, load_all_data, delete_data_by_website, edit_data_by_website


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
        self.generate_btn = QPushButton("Gen.")
        self.add_btn = QPushButton("Add")
        self.search_btn = QPushButton("Search")
        self.copy_btn = QPushButton("Copy")
        self.delete_btn = QPushButton("Delete")
        self.edit_btn = QPushButton("Edit")

        # SHOW/HIDE FEATURE
        self.toggle_btn = QPushButton("Show")
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.setFixedWidth(60)
        self.toggle_btn.clicked.connect(self.toggle_password)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.generate_btn)
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.search_btn)
        btn_layout.addWidget(self.copy_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.edit_btn)

        self.add_btn.clicked.connect(self.add_entry)
        self.search_btn.clicked.connect(self.search_entry)
        self.generate_btn.clicked.connect(self.gen_pass)
        self.copy_btn.clicked.connect(self.copy_data)
        self.delete_btn.clicked.connect(self.del_data)
        self.edit_btn.clicked.connect(self.edit_data)

        for btn in [self.generate_btn, self.add_btn, self.search_btn]:
            # btn.setMinimumHeight(40)
            # btn.setMinimumWidth(80)
            btn.setStyleSheet("font-weight: bold")

        # INPUT
        form_layout = QFormLayout()
        form_layout.addRow("Website:", self.website_input)
        form_layout.addRow("username:", self.username_input)
        # form_layout.addRow("Password:", self.password_input)

        self.pw_layout = QHBoxLayout()
        self.pw_layout.addWidget(self.password_input)
        self.pw_layout.addWidget(self.toggle_btn)
        form_layout.addRow("password: ", self.pw_layout)

        # LAYOUTS
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addSpacing(10)
        main_layout.addLayout(btn_layout)
        main_layout.setContentsMargins(20,20,20,20)
        main_layout.setSpacing(15)
        form_layout.setVerticalSpacing(10)

        # PASS TABLE UI
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Website", "Username", "Password"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  # disables editing sells
        self.table.itemSelectionChanged.connect(self.fill_input_from_selection)

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
        # add_entry -> t/f + success or error message

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
            self.table.setItem(row, 0, QTableWidgetItem(str(website)))
            self.table.setItem(row, 1, QTableWidgetItem(str(creds["username"])))
            self.table.setItem(row, 2, QTableWidgetItem(str(creds["password"])))

    def copy_data(self):
        selected_items = self.table.selectedItems()

        if selected_items and len(selected_items) >= 3:
            # username_item = selected_items[1]
            # username = username_item.text()
            password_item = selected_items[2]
            password = password_item.text()

            # QGuiApplication.clipboard().setText(username)
            QGuiApplication.clipboard().setText(password)
            QMessageBox.information(self, "Copied", "Password copied to clipboard.")

        else:
            QMessageBox.warning(self, "Error", "Please select a full row.")

    def del_data(self):
        selected_items = self.table.selectedItems()

        if selected_items and len(selected_items) >= 3:
            website = selected_items[0].text()

            confirm = QMessageBox.question(self, "Confirm delete",
                                           f"Are you sure you want to delete password for {website}",
                                           QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.No)

            if confirm == QMessageBox.StandardButton.Yes:
                success = delete_data_by_website(website)

                if success:
                    QMessageBox.information(self, "Deleted", f"Entry for {website
                    } deleted.")
                    self.load_data()

                else:
                    QMessageBox.warning(self, "Error", "Could not delete entry.")

        else:
            QMessageBox.warning(self, "Error", "Please select a row.")

    def fill_input_from_selection(self):
        selected_items = self.table.selectedItems()
        if selected_items and len(selected_items) >= 3:
            self.website_input.setText(selected_items[0].text())
            self.username_input.setText(selected_items[1].text())
            self.password_input.setText(selected_items[2].text())
            # _.text() >> To get the text inside the cell.

    def edit_data(self):
        selected_items = self.table.selectedItems()
        if selected_items and len(selected_items) >= 3:
            old_website = selected_items[0].text()

            new_website = self.website_input.text()
            new_username = self.username_input.text()
            new_password = self.password_input.text()

            if not new_website or not new_username or not new_password:
                QMessageBox.warning(self, "Error", "All fields are required.")
                return

            success = edit_data_by_website(old_website, new_website, new_username, new_password)
            if success:
                QMessageBox.information(self, "Edit", "Entry updated successfully.")
                self.load_data()
                self.website_input.clear()
                self.username_input.clear()
                self.password_input.clear()

            else:
                QMessageBox.warning(self, "Error", "Could not update entry.")

        else:
            QMessageBox.warning(self, "Error", "Please select a row.")

    def toggle_password(self):
        if self.toggle_btn.isChecked():
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_btn.setText("Hide")

        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_btn.setText("Show")
    