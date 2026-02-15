import sys
import time
import database
from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QLineEdit,
    QLabel,
    QWidget,
    QApplication,
    QSplashScreen,
    QHBoxLayout,
    QGridLayout,
    QGraphicsDropShadowEffect,
)
from PyQt6.QtGui import QPixmap, QGuiApplication, QPainter, QBrush, QColor
from PyQt6.QtCore import Qt, QTimer, QSize
from constants import (
    LOGO,
    BLURRED_LOGO
)
from util import (
    isDevMode
)
from udp_server import UDPServer


# TODO:
# using a class for each UI element for its declarative nature and data binding


# Above are all helper classes needed from PyQt6 for this project, so far.
class MainWindow(QMainWindow):
    # TODO: fix a direct assignment as View and Model should be separated
    # should be resolved by passing a data reference to udp_server from the main function
    def __init__(self, udp_server):
        super().__init__()
        self.udp = udp_server

        self.setWindowTitle("PHOTON")
        self.setGeometry(400, 150, 1050, 800)

        # Central widget with background image
        central_widget = QWidget()
        central_widget.setObjectName("MainWindowWidget")
        central_widget.setStyleSheet(f"""
            #MainWindowWidget {{
                border-image: url('{BLURRED_LOGO}');
                background-position: center;
            }}
        """)
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Left side container
        self.left_container = QWidget()
        left_layout = QVBoxLayout(self.left_container)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)

        # Red team panel
        self.red_panel = RedTeamPanel()
        self.red_panel.setLayout(QVBoxLayout())

        # Right side container
        self.right_container = QWidget()
        right_layout = QVBoxLayout(self.right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        # Green team panel
        self.green_panel = GreenTeamPanel()
        self.green_panel.setLayout(QVBoxLayout())

        self.red_label = QLabel("RED TEAM")
        self.green_label = QLabel("GREEN TEAM")

        # Style for red label
        red_label_style = """
            color: white;
            font-weight: bold;
            font-size: 36px;
            font-family: 'Orbitron', 'Courier New', sans-serif;
            background-color: rgba(100, 0, 0, 150);
            border-radius: 20px;
            padding: 10px 20px;
            margin: 10px;
        """
        self.red_label.setStyleSheet(red_label_style)
        self.red_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Style for green label
        green_label_style = red_label_style.replace("rgba(100, 0, 0, 150)", "rgba(0, 100, 0, 150)")
        self.green_label.setStyleSheet(green_label_style)
        self.green_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(0, 5)
        shadow.setColor(QColor(0, 0, 0, 160))
        self.red_label.setGraphicsEffect(shadow)
        self.green_label.setGraphicsEffect(shadow)

        left_layout.addStretch(2)                     # Push label down
        left_layout.addWidget(self.red_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        left_layout.addStretch(1)                     # Space between label and panel
        left_layout.addWidget(self.red_panel, alignment=Qt.AlignmentFlag.AlignHCenter)

        right_layout.addStretch(2)
        right_layout.addWidget(self.green_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        right_layout.addStretch(1)
        right_layout.addWidget(self.green_panel, alignment=Qt.AlignmentFlag.AlignHCenter)

        main_layout.addWidget(self.left_container, 1)
        main_layout.addWidget(self.right_container, 1)

        self.red_index_labels = []
        self.green_index_labels = []

        self.create_player_grid(self.red_panel.layout(), "RED", self.red_index_labels)
        self.create_player_grid(self.green_panel.layout(), "GREEN", self.green_index_labels)

        # Apply initial dimension ruling
        self.update_panel_sizes()

    def update_panel_sizes(self):
        w = self.width()
        h = self.height()
        panel_width = int(w * 0.48) # 0.48 seems to give ideal width
        panel_height = int(h * 0.5)
        self.red_panel.setFixedSize(panel_width, panel_height)
        self.green_panel.setFixedSize(panel_width, panel_height)

    def resizeEvent(self, event):
        # Called when window is resized, update panel sizes.
        super().resizeEvent(event)
        self.update_panel_sizes()

    def create_player_grid(self, parent_layout, team_name, index_label_list):
        player_entry_grid = QGridLayout()
        entries = []
        id_prompt = QLabel("Player ID")
        eq_prompt = QLabel("Equipment ID")
        codename_prompt = QLabel("Codename")
        for lbl in (id_prompt, codename_prompt, eq_prompt):
            lbl.setStyleSheet("color: white; font-weight: bold; font-size: 12px;")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Add an item for each prompt necessary
        player_entry_grid.addWidget(id_prompt, 0, 1)
        player_entry_grid.addWidget(codename_prompt, 0, 2)
        player_entry_grid.addWidget(eq_prompt, 0, 3)
        cool_font = "font-family: 'Courier New'; font-size: 14px; font-weight: bold; color: black; background-color: transparent;"
        # Add QLineEdits for each entry
        for row in range(1, 16):
            # Player number label (initially empty)
            player_index_label = QLabel("")
            player_index_label.setStyleSheet("color: black; font-weight: bold;")
            player_index_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            player_entry_grid.addWidget(player_index_label, row, 0)
            index_label_list.append(player_index_label)   # store for later updates

            row_data = []
            player_id_edit = QLineEdit()
            codename_edit = QLineEdit()
            equipment_id_edit = QLineEdit()
            codename_edit.setReadOnly(True)
            for entry in (player_id_edit, codename_edit, equipment_id_edit):
                entry.setFixedSize(80, 20)
                entry.setStyleSheet(cool_font)
            player_entry_grid.addWidget(player_id_edit, row, 1)
            player_entry_grid.addWidget(codename_edit, row, 2)
            player_entry_grid.addWidget(equipment_id_edit, row, 3)
            row_data = [player_id_edit, codename_edit, equipment_id_edit]
            entries.append(row_data)
            # Player ID entry
            player_id_edit.returnPressed.connect(
                lambda r=row_data, t=team_name, idx=row-1: self.on_player_id_enter(r, t, idx)
            )
            # Codename entry
            codename_edit.returnPressed.connect(
                lambda r=row_data, t=team_name, idx=row-1: self.on_codename_enter(r, t, idx)
            )
            # Equipment ID entry
            equipment_id_edit.returnPressed.connect(
                lambda r=row_data, t=team_name, idx=row-1: self.on_row_submit(r, t, idx)
            )
            # The code above creates anonymous functions that create anonymous variables to quickly grab the row
            # that was clicked and the team name of that grid. This then is passed to our MainWindow functions
            # on_row_submit on_player_id_enter that takes the row and team name, this will then allow precise parsing on submission.
        parent_layout.addLayout(player_entry_grid)
        return entries

    def on_player_id_enter(self, row_data, team, index):
        # Called when Enter is pressed in a Player ID field.
        # Looks up the codename from the database and fills the Codename field.
        player_id = row_data[0].text().strip()

        if team == "RED":
            index_labels = self.red_index_labels
        else:
            index_labels = self.green_index_labels

        if player_id:
            # Show player number
            index_labels[index].setText(f"Player #{index+1}")

            # Convert to int as database expects integer
            try:
                player_id = int(player_id)
            except ValueError:
                return

            # Query the database
            codename = database.get_player_codename(player_id)

            if codename is not None and codename is not False:
                # fill the codename and move to equipment
                row_data[1].setText(codename)
                row_data[1].setReadOnly(True)
                row_data[1].setStyleSheet("color: black;")
                row_data[1].setPlaceholderText("")
                row_data[2].setFocus()
            else:
                # Player not found, new player entry
                row_data[1].clear()
                row_data[1].setReadOnly(False)
                row_data[1].setPlaceholderText("Enter codename for new player")
                row_data[1].setStyleSheet("color: gray;")
                row_data[1].setFocus()
        else:
            # Clear the number label and codename field
            index_labels[index].setText("")
            row_data[1].clear()
            row_data[1].setReadOnly(True)
            row_data[1].setPlaceholderText("")

    def on_codename_enter(self, row_data, team, index):
        # Called when Enter is pressed in the codename field
        # If both Player ID and codename are non‑empty, attempts to add the player to the database.
        # If successful, moves focus to Equipment ID.
        # If the player already exists return false
        if row_data[1].isReadOnly():
            return

        player_id_text = row_data[0].text().strip()
        codename = row_data[1].text().strip()

        if not player_id_text or not codename:
            return

        try:
            player_id = int(player_id_text)
        except ValueError:
            return  # Invalid ID – ignore

        # Attempt to add the new player
        success = database.add_player(player_id, codename)

        if success:
            # Player added – update style and move to equipment
            row_data[1].setReadOnly(True)
            row_data[1].setStyleSheet("color: black;")
            row_data[1].setPlaceholderText("")
            row_data[2].setFocus()
        else:
            # Addition failed (likely because player already exists) – indicate error
            row_data[1].setStyleSheet("border: 1px solid red; background-color: #ffcccc;")

    def on_row_submit(self, row_data, team, index):
        # Called when Enter is pressed in Equipment ID field.
        player_id = row_data[0].text().strip()
        equip_id = row_data[2].text().strip()
        if player_id and equip_id:
            # If both fields are found, run this logic.
            print(f"[{team}] SUCCESS - Player: {player_id}, Equipment: {equip_id}, Player Index: {index}")

            # TODO: fix the direct assignment
            self.udp.broadcast_equipment_id(equip_id)
            
        else:
            # If both fields are not found, run error logic and graphically prompt user.
            print(f"[{team}] ERROR: Both fields are required for this row.")
            if not player_id:
                row_data[0].setStyleSheet("border: 1px solid red; background-color: #ffcccc; color: black;")
            if not equip_id:
                row_data[2].setStyleSheet("border: 1px solid red; background-color: #ffcccc; color: black;")

class RedTeamPanel(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        # Draw a dark red rectangle that fills this specific widget.
        painter.setBrush(QBrush(QColor(100, 0, 0, 127)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 20, 20)

class GreenTeamPanel(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        # Draw a dark green rectangle that fills this specific widget.
        painter.setBrush(QBrush(QColor(0, 100, 0, 127)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 20, 20)

global_main_window = None
# Allows main window reference to stay alive

def show_main_window(splash_screen, udp):
    global global_main_window
    global_main_window = MainWindow(udp)
    global_main_window.show()
    splash_screen.finish(global_main_window)

def main():
    # Fetching UDP info
    # TODO: make a query to the operator on the user interface instead
    receive_ip = "0.0.0.0" if isDevMode() else input("Enter UDP receive IP (default 0.0.0.0): ") or "0.0.0.0"
    broadcast_ip = "255.255.255.255" if isDevMode() else  input("Enter UDP broadcast IP (default 255.255.255.255): ") or "255.255.255.255"


    udp = UDPServer(
        receive_ip=receive_ip,
        broadcast_ip=broadcast_ip
    )

    app = QApplication(sys.argv)
    screen_size = QGuiApplication.primaryScreen().size()/2
    # set application to scale according to user screen size
    pixmap = QPixmap(f"{LOGO}").scaled(QSize(screen_size))
    splash = QSplashScreen(pixmap, Qt.WindowType.WindowStaysOnTopHint)
    # Ensure window splashes on top of all other applications on start up
    splash.show()
    app.processEvents()
    # TODO: fix a direct assignment of UDP
    QTimer.singleShot(0 if isDevMode() else 3000, lambda: show_main_window(splash, udp))
    # After 3 seconds, run show main window.
    sys.exit(app.exec())

if __name__ == "__main__":
    main()