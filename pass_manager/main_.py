import sys
from PyQt6.QtWidgets import QApplication as qapp
from ui_main_ import PasswordManagerWindow

app = qapp(sys.argv)
window = PasswordManagerWindow()
window.show()
sys.exit(app.exec())
