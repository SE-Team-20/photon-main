import sys
import time
from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QLineEdit,
    QLabel,
    QPushButton,
    QWidget,
    QApplication,
    QSplashScreen,
    QHBoxLayout,
    QGridLayout,
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


        self.setWindowTitle("Player Entry Terminal Screen")
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


        # Main layout (fills the whole central widget)
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
        self.red_panel.setLayout(QVBoxLayout())  # internal layout for label + grid
        left_layout.addStretch()
        left_layout.addWidget(self.red_panel, alignment=Qt.AlignmentFlag.AlignHCenter)


        # Right side container
        self.right_container = QWidget()
        right_layout = QVBoxLayout(self.right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)


        # Green team panel
        self.green_panel = GreenTeamPanel()
        self.green_panel.setLayout(QVBoxLayout())
        right_layout.addStretch()
        right_layout.addWidget(self.green_panel, alignment=Qt.AlignmentFlag.AlignHCenter)


        # Add containers to main layout with equal stretch
        main_layout.addWidget(self.left_container, 1)
        main_layout.addWidget(self.right_container, 1)


        # Now build the content inside each panel
        self.setup_panel_content(self.red_panel, "RED")
        self.setup_panel_content(self.green_panel, "GREEN")


        # Apply initial sizing
        self.update_panel_sizes()


    def setup_panel_content(self, panel, team_name):
        #Add the team label and player grid to a panel.
        layout = panel.layout()
        # Team label
        label = QLabel(f"{team_name} TEAM")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(f"""
            color: {team_name.lower()};
            font-weight: bold;
            font-size: 36px;
            font-family: 'Orbitron', 'Courier New', sans-serif;
            background-color: rgba(100, 0, 0, 150);
            border-radius: 20px;
            padding: 10px 20px;
            margin: 10px;
            """)
            # Adjust background color for green
        if team_name == "GREEN":
            label.setStyleSheet(label.styleSheet().replace("rgba(100, 0, 0, 150)", "rgba(0, 100, 0, 150)"))
        layout.addWidget(label)


        # Player grid
        self.create_player_grid(layout, team_name)


    def update_panel_sizes(self):
        #Set panel size to 25% width, 50% height of the current window.
        w = self.width()
        h = self.height()
        panel_width = int(w * 0.48)
        panel_height = int(h * 0.5)
        self.red_panel.setFixedSize(panel_width, panel_height)
        self.green_panel.setFixedSize(panel_width, panel_height)


    def resizeEvent(self, event):
        # Called when window is resized, update panel sizes.
        super().resizeEvent(event)
        self.update_panel_sizes()


    def create_player_grid(self, parent_layout, team_name):
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
        cool_font = "font-family: 'Courier New'; font-size: 14px; font-weight: bold; color: black; background-color: #e0e0e0;"
        # Add QLineEdit for each entry and a QPushButton for submission on each entry
        for row in range(1, 16):
            player_index_label = QLabel(str(row-1))
            player_index_label.setStyleSheet("color: black; font-weight: bold;")
            player_index_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            player_entry_grid.addWidget(player_index_label, row, 0)
            row_data = []
            player_id_edit = QLineEdit()
            codename_edit = QLineEdit()
            equipment_id_edit = QLineEdit()
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
                lambda r=row_data, t=team_name, index= row-1: self.on_player_id_enter((r, t, index))
            )
            # Equipment ID entry
            equipment_id_edit.returnPressed.connect(
                lambda r=row_data, t=team_name, index=row-1: self.on_row_submit(r, t, index)
            )
            # The code above creates an anonymous function that creates anonymous variables to quickly grab the row
            # that was clicked and the team name of that grid. This then is passed to our MainWindow function
            # on_row_submit that takes the row and team name, this will then allow precise parsing on submission.
        parent_layout.addLayout(player_entry_grid)
        return entries


    def on_player_id_enter(self, row_data, team, index):
        # Called when Enter is pressed in a Player ID field.
        # Looks up the codename from the database and fills the Codename field.
        player_id = row_data[0].text().strip()
        if not player_id:
        # Empty field – show error style and clear codename
            row_data[0].setStyleSheet("border: 1px solid yellow; background-color: #ffcccc; color: black;")
            row_data[1].clear()
            return
        # Reset any previous error style
        row_data[0].setStyleSheet("color: black; background-color: #e0e0e0; border: none;")


        # Look up codename by passing player_id to readRecord function to database file,
        # database file returns the readRecord, if player id not found, addRecord


        # MOCK EXAMPLE BELOW


        # codename = get_codename_from_db(player_id)
        # if codename:
        #     row_data[1].setText(codename)
        #     row_data[1].setStyleSheet("color: black")
        #     # Move focus to Equipment ID for faster entry
        #     row_data[2].setFocus()
        # else:
        #     # Player ID not found
        #     row_data[0].setStyleSheet("border: 1px solid red; background-color: #ffcccc; color: black;")
        #     row_data[1].clear()
        #     # Optionally show a message or beep
        #     print(f"[{team}] Player ID {player_id} not found in database.")




    def on_row_submit(self, row_data, team, index):
        # Called when Enter is pressed in Equipment ID field.
        player_id = row_data[0].text().strip()
        equip_id = row_data[2].text().strip()
        if player_id and equip_id:
            # If both fields are found, run this logic.
            print(f"[{team}] SUCCESS - Player: {player_id}, Equipment: {equip_id}, Player Index: {index}")


            # TODO: fix the direct assignment
            self.udp.broadcast_equipment_id(equip_id)


            # Reset style in case ERROR correction by user.
            row_data[0].setStyleSheet("color: black; background-color: #e0e0e0; border: none;")
            row_data[1].setStyleSheet("color: black; background-color: #e0e0e0; border: none;")
        else:
            # If both fields are not found, run error logic and graphically prompt user.
            print(f"[{team}] ERROR: Both fields are required for this row.")
            if not player_id:
                row_data[0].setStyleSheet("border: 1px solid yellow; background-color: #ffcccc; color: black;")
            if not equip_id:
                row_data[2].setStyleSheet("border: 1px solid yellow; background-color: #ffcccc; color: black;")


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
        # Draw a green rectangle that fills this specific widget.
        painter.setBrush(QBrush(QColor(0, 100, 0, 127))) # Dark Green
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
    receive_ip = input("Enter UDP receive IP (default 0.0.0.0): ") or "0.0.0.0"
    broadcast_ip = input("Enter UDP broadcast IP (default 255.255.255.255): ") or "255.255.255.255"


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