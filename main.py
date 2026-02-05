import sys
import signal

# UI framework
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QPixmap, QGuiApplication
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QSplashScreen


# TODO:
# 1. use QSlpashScren and implement a transient from that to the main screen
# 2. figure out the widget necessity and design the UI
class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()

    self.title = "Photon Main - team 20"
    self.setWindowTitle(self.title)

    # Set the size to the half of the full screen (only while development)
    screen_size=QGuiApplication.primaryScreen().size()/2

    self.setFixedSize(screen_size)

    label=QLabel(self)
    pixmap=QPixmap('UI_images/logo.jpg').scaled(QSize(screen_size))
    label.setPixmap(pixmap)
    self.setCentralWidget(label)

    self.statusBar().showMessage("splashscreen")

def main():
  print("---main.py is called---")

  # Make the program
  app = QApplication([])

  # Open the GUI window
  window = MainWindow()
  window.show()

  # Availability to quit the program with Ctrl + C
  signal.signal(signal.SIGINT, lambda *_: app.quit())
  timer=QTimer()
  timer.timeout.connect(lambda: None)
  timer.start(100)
  sys.exit(app.exec())

  print("---exited main.py---")
  pass

if __name__ == '__main__':
  main()
