import sys
from PySide6.QtWidgets import QApplication
from widget import Widget

issue_list = list()

app = QApplication(sys.argv)

widget = Widget()
widget.resize(650, 50)

widget.show()

app.exec()