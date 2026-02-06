import sys
from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QLineEdit, QLabel,
                             QPushButton, QWidget, QApplication, QSplashScreen, QHBoxLayout, QGridLayout)
from PyQt6.QtGui import QPixmap, QGuiApplication, QPainter, QBrush, QColor
from PyQt6.QtCore import Qt, QTimer, QSize
# Above are all helper classes needed from PyQt6 for this project, so far.
class MainWindow(QMainWindow):
    # Prototype MainWindow class to test PyQt6 GUI viability.
    def __init__(self):
        super().__init__()
        #Create GUI
        self.setWindowTitle("Player Entry Terminal Screen")
        self.setGeometry(400, 150, 1050, 800)
        # Main Layout
        main_layout = QVBoxLayout()
        # Entries layout
        entry_layout = QHBoxLayout()

        self.red_panel = RedTeamPanel()
        red_entry_box = QVBoxLayout(self.red_panel)

        self.green_panel = GreenTeamPanel()
        green_entry_box = QVBoxLayout(self.green_panel)

        red_label = QLabel("RED TEAM")
        red_label.setStyleSheet("color: red; font-weight: bold; font-size: 18px;")
        red_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        red_entry_box.addWidget(red_label)

        green_label = QLabel("GREEN TEAM")
        green_label.setStyleSheet("color: green; font-weight: bold; font-size: 18px;")
        green_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        green_entry_box.addWidget(green_label)

        entry_layout.addWidget(red_label)
        entry_layout.addWidget(green_label)
        main_layout.addLayout(entry_layout)

        teams_layout = QHBoxLayout()

        # Create red and green grids
        self.red_entries = self.create_player_grid(red_entry_box, "RED")
        self.green_entries = self.create_player_grid(green_entry_box, "GREEN")
        teams_layout.addWidget(self.red_panel)
        teams_layout.addWidget(self.green_panel)
        main_layout.addLayout(teams_layout)

        # Set central Widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def create_player_grid(self, parent_layout, team_name):
        player_entry_grid = QGridLayout()
        entries = []
        id_prompt = QLabel("Player ID")
        eq_prompt = QLabel("Equipment ID")
        id_prompt.setStyleSheet("color: white; font-weight: bold; font-size: 12px;")
        eq_prompt.setStyleSheet("color: white; font-weight: bold; font-size: 12px;")
        id_prompt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        eq_prompt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        action_prompt = QLabel("")
        # Add an item for each prompt necessary
        player_entry_grid.addWidget(id_prompt, 0, 0)
        player_entry_grid.addWidget(eq_prompt, 0, 1)
        player_entry_grid.addWidget(action_prompt, 0, 2)
        cool_font = "font-family: 'Courier New'; font-size: 14px; font-weight: bold; color: black; background-color: #e0e0e0;"
        # Add QLineEdit for each entry and a QPushButton for submission on each entry
        for row in range(1, 16):
            row_data = []
            for col in range(2):
                entry = QLineEdit()
                entry.setFixedSize(80, 20)
                entry.setStyleSheet(cool_font)
                player_entry_grid.addWidget(entry, row, col)
                row_data.append(entry)
            row_btn = QPushButton("⏎")
            row_btn.setFixedSize(30, 20)
            row_btn.setStyleSheet("font-size: 10px; background-color: #FFFFF;")
            row_btn.clicked.connect(lambda checked, r=row_data, t=team_name: self.on_row_submit(r, t))

            player_entry_grid.addWidget(row_btn, row, 2)
            entries.append(row_data)

        parent_layout.addLayout(player_entry_grid)
        return entries

    def on_row_submit(self, row_data, team):
        player_id = row_data[0].text().strip()
        equip_id = row_data[1].text().strip()
        if player_id and equip_id:
            # If both fields are found, run this logic.
            print(f"[{team}] SUCCESS - Player: {player_id}, Equipment: {equip_id}")

            # Reset style in case ERROR correction by user.
            row_data[0].setStyleSheet("color: black;")
            row_data[1].setStyleSheet("color: black;")
        else:
            # If both fields are not found, run error logic and graphically prompt user.
            print(f"[{team}] ERROR: Both fields are required for this row.")
            if not player_id:
                row_data[0].setStyleSheet("border: 1px solid yellow; background-color: #ffcccc; color: black;")
            if not equip_id:
                row_data[1].setStyleSheet("border: 1px solid yellow; background-color: #ffcccc; color: black;")

class RedTeamPanel(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        # Draw a dark red rectangle that fills this specific widget.
        painter.setBrush(QBrush(QColor(150, 0, 0)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(self.rect())

class GreenTeamPanel(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        # Draw a green rectangle that fills this specific widget.
        painter.setBrush(QBrush(QColor(0, 100, 0))) # Dark Green
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(self.rect())

global_main_window = None
# Allows main window reference to stay alive

def show_main_window(splash_screen):
    global global_main_window
    global_main_window = MainWindow()
    global_main_window.show()
    splash_screen.finish(global_main_window)

def main():
    app = QApplication(sys.argv)
    screen_size = QGuiApplication.primaryScreen().size()/2
    # set application to scale according to user screen size
    pixmap = QPixmap("logo.jpg").scaled(QSize(screen_size))
    splash = QSplashScreen(pixmap, Qt.WindowType.WindowStaysOnTopHint)
    # Ensure window splashes on top of all other applications on start up
    splash.show()
    app.processEvents()
    QTimer.singleShot(3000, lambda: show_main_window(splash))
    # After 3 seconds, run show main window.
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

