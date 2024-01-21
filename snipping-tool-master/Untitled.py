import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, pyqtSignal

class CustomWidget(QWidget):
    returnToMainWindowSignal = pyqtSignal()

    def __init__(self):
        super().__init__()

    def mouseReleaseEvent(self, event):
        # This method is called when a mouse button is released
        print("Mouse button released at:", event.pos())

        # Example: Change the background color when the left mouse button is released
        if event.button() == Qt.LeftButton:
            self.change_background_color()

    def change_background_color(self):
        # Change the background color to a random color
        new_color = QColor(255, 0, 0)  # Red color (you can customize this)
        self.setStyleSheet(f"background-color: {new_color.name()};")

        # Emit the custom signal to indicate that the action is completed
        self.returnToMainWindowSignal.emit()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Create an instance of CustomWidget
        self.custom_widget = CustomWidget()

        # Set up the layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.custom_widget)

        # Connect the custom signal to a slot in MainWindow
        self.custom_widget.returnToMainWindowSignal.connect(self.handleReturnToMainWindow)

        self.setWindowTitle('Main Window with Custom Widget')

    def handleReturnToMainWindow(self):
        # Slot to handle the custom signal and perform actions in MainWindow
        print("Returning to MainWindow")

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Create an instance of MainWindow
    main_window = MainWindow()
    main_window.setGeometry(100, 100, 300, 200)
    main_window.show()

    sys.exit(app.exec_())

# 2024/1/14 22:47