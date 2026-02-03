import sys

# UI framework
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QLabel

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.title = "Photon Main (team 20)"
    self.setWindowTitle(self.title)

    label=QLabel(self)
    pixmap=QPixmap('UI_images/logo.jpg')
    label.setPixmap(pixmap)
    self.setCentralWidget(label)
    self.resize(pixmap.width(), pixmap.height())

    self.statusBar().showMessage("Welcome to " + self.title)

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