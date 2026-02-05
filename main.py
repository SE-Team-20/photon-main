import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap, QGuiApplication
from PyQt6.QtCore import Qt, QTimer, QSize
class MainWindow(QMainWindow):
    def __init__(self):
        self.label = QLabel("Enter Player 1 codename:", self)
        self.codename_input = QLineEdit(self)
        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.on_submit)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.codename_input)
        layout.addWidget(self.submit_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def on_submit(self):
        codename = self.codename_input.text()
        print(f"User input: {codename}")
        self.label.setText(f"Hello, {codename}!")

def show_main_window(splash_screen):
    main_window = MainWindow()
    main_window.show()
    splash_screen.finish(main_window)
def main():
    app = QApplication(sys.argv)
    screen_size = QGuiApplication.primaryScreen().size()/2
    pixmap = QPixmap("logo.jpg").scaled(QSize(screen_size))
    splash = QSplashScreen(pixmap, Qt.WindowType.WindowStaysOnTopHint)
    splash.show()
    app.processEvents()
    QTimer.singleShot(2000, lambda: show_main_window(splash))
    sys.exit(app.exec())

if __name__ == "__main__":
    main()


