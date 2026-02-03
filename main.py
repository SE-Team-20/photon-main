import sys

# UI framework
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QSplashScreen

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()

    self.title = "Photon Main - team 20"
    self.setWindowTitle(self.title)

    # self.setGeometry(0, 0, 300, 300)

    self.setFixedSize(300, 300)


    label=QLabel(self)
    pixmap=QPixmap('UI_images/logo.jpg').scaled(QSize(300, 300))
    label.setPixmap(pixmap)
    self.setCentralWidget(label)

    self.statusBar().showMessage("splashscreen(" + self.title + ")")

def main():
  print("---main.py is called---")

  app = QApplication([])

  window = MainWindow()
  window.show()

  sys.exit(app.exec())

  print("---exited main.py---")
  pass

if __name__ == '__main__':
  main()