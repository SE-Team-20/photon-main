import socket
import constants
import database
from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QLineEdit, QLabel, QWidget, QPushButton,
    QFormLayout, QMessageBox, QHBoxLayout, QGridLayout, QGraphicsDropShadowEffect,
    QListWidget, QListWidgetItem
)
from udp_server import UDPServer
from PyQt6.QtGui import QGuiApplication, QPainter, QBrush, QColor, QFont
from PyQt6.QtCore import Qt, QTimer, QEvent, pyqtSignal
from util import isDevMode
from constants import *

class UDPConfigWindow(QWidget):
    def __init__(self, window_size):
        super().__init__()
        self.setWindowTitle("Photon - Network Configuration")
        self.resize(window_size)
        self.setObjectName("ConfigWindow")
        self.setStyleSheet("""
            #ConfigWindow {
                background-color: black;
            }
            QLabel {
                color: white;
                font-family: Arial;
                font-size: 14px;
            }
            QLineEdit {
                background-color: {SEMI_TRANSPARENT_BLACK};
                border: 1px solid {DARK_GREY};
                padding: 8px;
                border-radius: 6px;
                color: white;
                font-size: 14px;
                min-width: 220px;
            }
            QPushButton {
                background-color: {DEEP_RED};
                padding: 10px 25px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 16px;
                color: white;
            }
            QPushButton:hover {
                background-color: {LIGHT_RED};
            }
        """)
        layout = QVBoxLayout(self)
        layout.addStretch()
        title = QLabel("UDP Network Setup")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(title)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form.setVerticalSpacing(VERTICAL_SPACING)
        form.setHorizontalSpacing(HORIZONTAL_SPACING)
        self.receive_input = QLineEdit(f"{RECIEVE_INPUT}")
        self.broadcast_input = QLineEdit(f"{BROADCAST_INPUT}")
        self.receive_input.setFixedHeight(NETWORK_SECTION_HEIGHT)
        self.broadcast_input.setFixedHeight(NETWORK_SECTION_HEIGHT)
        form.addRow("Receive IP:", self.receive_input)
        form.addRow("Broadcast IP:", self.broadcast_input)
        layout.addLayout(form)
        layout.addSpacing(NETWORK_SECTION_SPACING)

        self.start_button = QPushButton("Start System")
        self.start_button.clicked.connect(self.start_system)
        layout.addWidget(self.start_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        self.main_window = None

    def validate_ip(self, ip):
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            return False

    def start_system(self):
        receive_ip = self.receive_input.text().strip()
        broadcast_ip = self.broadcast_input.text().strip()
        if not receive_ip or not broadcast_ip:
            QMessageBox.warning(self, "Missing Input", "Please enter both Receive IP and Broadcast IP.")
            return
        if not self.validate_ip(receive_ip):
            QMessageBox.warning(self, "Invalid IP", "Receive IP is not valid.")
            return
        if not self.validate_ip(broadcast_ip):
            QMessageBox.warning(self, "Invalid IP", "Broadcast IP is not valid.")
            return
        try:
            udp = UDPServer(receive_ip=receive_ip, broadcast_ip=broadcast_ip)
        except OSError:
            QMessageBox.warning(self, "Network Error", "Unable to bind to the specified IP address.")
            return
        self.main_window = MainWindow(udp, database)
        self.main_window.show()
        self.close()

class MainWindow(QMainWindow):
    def __init__(self, udp_server, db):
        self.udp = udp_server
        self.db = db
        super().__init__()
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowTitle("PHOTON")
        screen = QGuiApplication.primaryScreen().availableGeometry()
        window_width = screen.width() * ASPECT_RATIO
        window_height = screen.height() * ASPECT_RATIO
        x = (screen.width() - window_width) // 2
        y = (screen.height() - window_height) // 2
        self.setGeometry(int(x), int(y), int(window_width), int(window_height))
        self.setFixedSize(int(window_width), int(window_height))

        central_widget = QWidget()
        central_widget.setObjectName("MainWindowWidget")
        central_widget.setStyleSheet(f"""
            #MainWindowWidget {{
                border-image: url('{BLURRED_LOGO}');
                background-position: center;
            }}
        """)
        self.setCentralWidget(central_widget)

        team_layout = QHBoxLayout(central_widget)
        team_layout.setContentsMargins(0, 0, 0, 0)
        team_layout.setSpacing(0)

        self.left_container = QWidget()
        left_layout = QVBoxLayout(self.left_container)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)

        self.red_panel = RedTeamPanel()
        self.red_panel.setLayout(QVBoxLayout())

        self.right_container = QWidget()
        right_layout = QVBoxLayout(self.right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        self.green_panel = GreenTeamPanel()
        self.green_panel.setLayout(QVBoxLayout())

        self.red_label = QLabel("RED TEAM")
        self.green_label = QLabel("GREEN TEAM")
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
        green_label_style = red_label_style.replace("rgba(100, 0, 0, 150)", "rgba(0, 100, 0, 150)")
        self.green_label.setStyleSheet(green_label_style)
        self.green_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(0, 5)
        shadow.setColor(QColor(0, 0, 0, 160))
        self.red_label.setGraphicsEffect(shadow)
        self.green_label.setGraphicsEffect(shadow)

        left_layout.addStretch(2)
        left_layout.addWidget(self.red_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        left_layout.addStretch(1)
        left_layout.addWidget(self.red_panel, alignment=Qt.AlignmentFlag.AlignHCenter)

        right_layout.addStretch(2)
        right_layout.addWidget(self.green_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        right_layout.addStretch(1)
        right_layout.addWidget(self.green_panel, alignment=Qt.AlignmentFlag.AlignHCenter)

        team_layout.addWidget(self.left_container, 1)
        team_layout.addWidget(self.right_container, 1)

        self.red_index_labels = []
        self.green_index_labels = []
        self.red_entries = self.create_player_grid(self.red_panel.layout(), "RED", self.red_index_labels)
        self.green_entries = self.create_player_grid(self.green_panel.layout(), "GREEN", self.green_index_labels)

        self.update_panel_sizes()

        # New Game button
        self.new_game_button = QPushButton("New Game", self.centralWidget())
        self.new_game_button.setFixedSize(120, 60)
        self.new_game_button.move(0, 0)
        button_style = """
            background-color: rgba(40, 110, 230, 150);
            border-radius: 20px;
            padding: 5px;
            font-weight: bold;
            font-size: 13px;
            font-family: 'Orbitron', 'Courier New', sans-serif;
            color: white;
        """
        self.new_game_button.setStyleSheet(button_style)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(0, 5)
        shadow.setColor(QColor(0, 0, 0, 160))
        self.new_game_button.setGraphicsEffect(shadow)
        self.new_game_button.raise_()
        self.new_game_button.clicked.connect(self.clear_all_grids)

        # Start play action window
        self.play_action_window = PlayActionWindow(self, self.udp)
        self.start_game_button = QPushButton("Start Game", self.centralWidget())
        self.start_game_button.setFixedSize(120, 60)
        window_height = self.height()
        window_width = self.width()
        self.start_game_button.move(window_width/2 - self.start_game_button.width()/2, 0)
        button_style = """
            background-color: rgba(40, 110, 230, 150);
            border-radius: 20px;
            padding: 5px;
            font-weight: bold;
            font-size: 13px;
            font-family: 'Orbitron', 'Courier New', sans-serif;
            color: white;
        """
        self.start_game_button.setStyleSheet(button_style)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(0, 5)
        shadow.setColor(QColor(0, 0, 0, 160))
        self.start_game_button.setGraphicsEffect(shadow)
        self.start_game_button.raise_()
        self.start_game_button.clicked.connect(self.show_play_action_window)

    def update_panel_sizes(self):
        w = self.width()
        h = self.height()
        panel_width = int(w * 0.48)
        panel_height = int(h * 0.6)
        self.red_panel.setFixedSize(panel_width, panel_height)
        self.green_panel.setFixedSize(panel_width, panel_height)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_panel_sizes()

    def create_player_grid(self, parent_layout, team_name, index_label_list):
        player_entry_grid = QGridLayout()
        player_entry_grid.setHorizontalSpacing(15)
        player_entry_grid.setVerticalSpacing(8)

        id_prompt = QLabel("Player ID")
        eq_prompt = QLabel("Equipment ID")
        codename_prompt = QLabel("Codename")
        for lbl in (id_prompt, codename_prompt, eq_prompt):
            lbl.setStyleSheet("color: white; font-weight: bold; font-size: 12px;")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        player_entry_grid.addWidget(id_prompt, 0, 1)
        player_entry_grid.addWidget(codename_prompt, 0, 2)
        player_entry_grid.addWidget(eq_prompt, 0, 3)

        background = RED_TEAM_BACKGROUND if team_name == "RED" else GREEN_TEAM_BACKGROUND

        entries = []
        for row in range(1, 16):
            player_index_label = QLabel("")
            player_index_label.setStyleSheet("color: black; font-weight: bold;")
            player_index_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            player_index_label.setFixedWidth(70)
            player_entry_grid.addWidget(player_index_label, row, 0)
            index_label_list.append(player_index_label)

            id_edit = QLineEdit()
            id_edit.setFixedSize(35, 28)
            id_edit.setStyleSheet(background)

            codename_edit = QLineEdit()
            codename_edit.setFixedSize(140, 28)
            codename_edit.setStyleSheet(background)
            codename_edit.setReadOnly(True)

            equipment_id_edit = QLineEdit()
            equipment_id_edit.setFixedSize(35, 28)
            equipment_id_edit.setStyleSheet(background)
            equipment_id_edit.setReadOnly(True)

            player_entry_grid.addWidget(id_edit, row, 1)
            player_entry_grid.addWidget(codename_edit, row, 2)
            player_entry_grid.addWidget(equipment_id_edit, row, 3)

            row_data = [id_edit, codename_edit, equipment_id_edit]
            entries.append(row_data)

            id_edit.returnPressed.connect(lambda r=row_data, t=team_name, idx=row-1: self.on_id_enter(r, t, idx))
            id_edit.keyPressEvent = lambda event, r=row_data, t=team_name, idx=row-1: self.on_id_keypress(event, r, t, idx)
            codename_edit.returnPressed.connect(lambda r=row_data, t=team_name, idx=row-1: self.on_codename_enter(r, t, idx))
            equipment_id_edit.returnPressed.connect(lambda r=row_data, t=team_name, idx=row-1: self.on_row_submit(r, t, idx))

        parent_layout.setContentsMargins(15, 15, 15, 15)
        parent_layout.addLayout(player_entry_grid)
        return entries

    def get_red_team_data(self):
        red_team_data = []
        for row in self.red_entries:
            id_text = row[0].text().strip()
            codename_text = row[1].text().strip()
            equip_text = row[2].text().strip()
            if id_text and codename_text and equip_text:
                red_team_data.append((id_text, codename_text, equip_text))
        return red_team_data

    def get_green_team_data(self):
        green_team_data = []
        for row in self.green_entries:
            id_text = row[0].text().strip()
            codename_text = row[1].text().strip()
            equip_text = row[2].text().strip()
            if id_text and codename_text and equip_text:
                green_team_data.append((id_text, codename_text, equip_text))
        return green_team_data

    def on_id_enter(self, row_data, team, index):
        id_text = row_data[0].text().strip()
        index_labels = self.red_index_labels if team == "RED" else self.green_index_labels
        background = RED_TEAM_BACKGROUND if team == "RED" else GREEN_TEAM_BACKGROUND

        if not id_text:
            index_labels[index].setText("")
            row_data[1].clear()
            row_data[1].setReadOnly(True)
            row_data[1].setPlaceholderText("")
            row_data[1].setStyleSheet(background)
            return

        try:
            id_val = int(id_text)
        except ValueError:
            print(f"Error: id must be integer: {id_text}")
            return

        index_labels[index].setText(f"Player #{index+1}")
        codename = False if isDevMode() else self.db._query_codename(id_val)

        if codename:
            row_data[1].setText(codename)
            row_data[1].setReadOnly(False)
            row_data[1].setStyleSheet(f"{background}; color: black;")
            row_data[1].setPlaceholderText("")
            row_data[2].setReadOnly(False)
            row_data[2].setFocus()
        else:
            row_data[1].clear()
            row_data[1].setReadOnly(False)
            row_data[1].setPlaceholderText("Enter codename for new player")
            row_data[1].setStyleSheet(f"{background}; color: gray;")
            row_data[1].setFocus()

    def on_id_keypress(self, event, row_data, team, index):
        if event.key() == Qt.Key.Key_Delete:
            id_text = row_data[0].text().strip()
            if not id_text:
                return
            is_registered = self.db._is_registered()
            success = self.db._delete_player(id_text)
            if success:
                row_data[0].clear()
                row_data[1].clear()
                row_data[1].setReadOnly(False)
                row_data[1].setPlaceholderText("Successfully deleted player")
                index_labels = self.red_index_labels if team=="RED" else self.green_index_labels
                index_labels[index].setText("")
            else:
                print("Failed deleting the player from database")

        QLineEdit.keyPressEvent(row_data[0], event)

    def on_codename_enter(self, row_data, team, index):
        if row_data[1].isReadOnly():
            return

        id_text = row_data[0].text().strip()
        codename = row_data[1].text().strip()
        if not id_text or not codename:
            row_data[2].setReadOnly(True)
            return

        try:
            id_val = int(id_text)
        except ValueError:
            return

        background = RED_TEAM_BACKGROUND if team == "RED" else GREEN_TEAM_BACKGROUND

        if isDevMode():
            print("Error: we cannot proceed with database connection when isDevMode is active.")
            row_data[2].setReadOnly(False)
            return

        result = self.db._update_codename(id_val, codename)

        if result == NEW_CODENAME_ADDED:
            row_data[2].setReadOnly(False)
            row_data[1].setStyleSheet(f"{background}; color: black;")
            row_data[1].setPlaceholderText("")
            msg = QMessageBox(self)
            msg.setStyleSheet(COOL_FONT)
            msg.setWindowTitle(f"{COOL_GUY_EMOJI}")
            msg.setText("New player added to the vault!")
            msg.setIconPixmap(constants.logo_icon())
            msg.exec()
        elif result == EXISTING_CODENAME_UPDATED:
            row_data[2].setReadOnly(False)
            row_data[1].setStyleSheet(f"{background}; color: black;")
            row_data[1].setPlaceholderText("")
            msg = QMessageBox(self)
            msg.setStyleSheet(COOL_FONT)
            msg.setWindowTitle(f"{COOL_GUY_EMOJI}")
            msg.setText("Codename updated successfully!")
            msg.setIconPixmap(constants.logo_icon())
            msg.exec()
        elif result == CODENAME_ALREADY_EXISTS:
            msg = QMessageBox(self)
            msg.setStyleSheet(COOL_FONT)
            msg.setWindowTitle("Uh oh...")
            msg.setText("Codename already exists for a different player. Please ask player for a different codename.")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.exec()
            row_data[1].setStyleSheet(f"{background}; border: 1px solid red;")
            row_data[1].setFocus()
        elif result == ERROR_OCCURRED:
            msg = QMessageBox(self)
            msg.setStyleSheet(COOL_FONT)
            msg.setWindowTitle("Error")
            msg.setText("An unexpected error occurred while saving the codename. Try restarting application.")
            msg.setIcon(QMessageBox.Icon.Critical)
        elif result == CODENAME_CHANGE_ATTEMPT_MATCHES_EXISTING:
            msg = QMessageBox(self)
            msg.setStyleSheet(COOL_FONT)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Doh!")
            msg.setText("No codename change detected.")
            msg.exec()
        else:
            msg = QMessageBox(self)
            msg.setStyleSheet(COOL_FONT)
            msg.setWindowTitle("Error")
            msg.setText("A really unexpected error occurred. Try calling IT.")
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.exec()

        if index < MAX_NUM_PLAYER_MINUSONE:
            this_row = self.red_entries[index] if team == "RED" else self.green_entries[index]
            this_row[2].setFocus()

    def on_row_submit(self, row_data, team, index):
        id_text = row_data[0].text().strip()
        equip_text = row_data[2].text().strip()
        background = RED_TEAM_BACKGROUND if team == "RED" else GREEN_TEAM_BACKGROUND

        try:
            equip_id = int(equip_text)
        except ValueError:
            row_data[2].setStyleSheet(f"{background}; border: 1px solid red;")
            return

        # Parity check
        if (team == "RED" and equip_id % 2 == 0) or (team == "GREEN" and equip_id % 2 == 1):
            print("Error: wrong equipment ID parity for the team color")
            row_data[2].setStyleSheet(f"{background}; border: 1px solid red;")
            return

        if not id_text or not equip_text:
            print(f"[{team}] ERROR: Both fields are required for this row.")
            if not id_text:
                row_data[0].setStyleSheet(f"{background}; border: 1px solid red;")
            if not equip_text:
                row_data[2].setStyleSheet(f"{background}; border: 1px solid red;")
            return

        if not isDevMode() and self.db._queue_player(id_text, 0 if team == "RED" else 1, equip_id):
            print(f"[{team}] SUCCESS - Player: {id_text}, Equipment: {equip_id}, Player Index: {index}")

        row_data[2].setStyleSheet(f"{background}; color: black; font-weight: bold; font-size: 12px;")
        self.udp.broadcast_equipment_id(equip_id)
        if index < MAX_NUM_PLAYER_MINUSONE:
            next_row = self.red_entries[index+1] if team == "RED" else self.green_entries[index+1]
            next_row[0].setFocus()

    def clear_all_grids(self):
        confirmation_message = QMessageBox(self)
        confirmation_message.setWindowTitle("Confirm Reset")
        confirmation_message.setText("Are you ready for a New Game?")
        confirmation_message.setIcon(QMessageBox.Icon.Question)
        confirmation_message.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        confirmation_result = confirmation_message.exec()
        if confirmation_result == QMessageBox.StandardButton.No:
            return
        else:
            for i in range(MAX_NUM_PLAYER):
                self.red_index_labels[i].setText("")
                self.green_index_labels[i].setText("")
                for entry in self.red_entries[i]:
                    entry.clear()
                    entry.setReadOnly(entry != self.red_entries[i][0])
                    entry.setStyleSheet(RED_TEAM_BACKGROUND)
                    entry.setPlaceholderText("")
                for entry in self.green_entries[i]:
                    entry.clear()
                    entry.setReadOnly(entry != self.green_entries[i][0])
                    entry.setStyleSheet(GREEN_TEAM_BACKGROUND)
                    entry.setPlaceholderText("")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_F12:
            self.clear_all_grids()
        elif event.key() == Qt.Key.Key_F5:
            self.play_action_window.show()
        else:
            super().keyPressEvent(event)

    def show_play_action_window(self):
        self.play_action_window.refresh_players()
        self.play_action_window.show()

class PlayActionWindow(QMainWindow):
    def __init__(self, main_window, udp_server):
        super().__init__()
        self.main_window = main_window
        self.udp = udp_server

        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowTitle("PHOTON: Play Action")

        # Same size as main window
        screen = QGuiApplication.primaryScreen().availableGeometry()
        window_width = screen.width() * ASPECT_RATIO
        window_height = screen.height() * ASPECT_RATIO
        x = (screen.width() - window_width) // 2
        y = (screen.height() - window_height) // 2
        self.setGeometry(int(x), int(y), int(window_width), int(window_height))
        self.setFixedSize(int(window_width), int(window_height))

        central_widget = QWidget()
        central_widget.setObjectName("PlayActionCentralWidget")
        central_widget.setStyleSheet(f"""
            #PlayActionCentralWidget {{
                border-image: url('{BLURRED_LOGO}');
                background-position: center;
            }}
        """)
        self.setCentralWidget(central_widget)

        # Main vertical layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        team_panel_layout = QHBoxLayout()
        team_panel_layout.setContentsMargins(0, 0, 0, 0)
        team_panel_layout.setSpacing(20)

        self.red_panel = RedTeamPanel()
        self.red_panel.setLayout(QVBoxLayout())
        red_layout = self.red_panel.layout()
        red_layout.setContentsMargins(15, 15, 15, 15)
        red_layout.setSpacing(8)

        self.red_label = QLabel("RED TEAM")
        self.red_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        red_label_style = """
            color: white;
            font-weight: bold;
            font-size: 24px;
            font-family: 'Audiowide', 'Orbitron', 'Courier New', sans-serif;
            background-color: rgba(100, 0, 0, 150);
            border-radius: 15px;
            padding: 5px 15px;
            margin: 5px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
        """
        self.red_label.setStyleSheet(red_label_style)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(0, 5)
        shadow.setColor(QColor(0, 0, 0, 160))
        self.red_label.setGraphicsEffect(shadow)
        red_layout.addWidget(self.red_label)

        self.red_grid = QGridLayout()
        self.red_grid.setHorizontalSpacing(10)
        self.red_grid.setVerticalSpacing(4)
        red_layout.addLayout(self.red_grid)

        self.green_panel = GreenTeamPanel()
        self.green_panel.setLayout(QVBoxLayout())
        green_layout = self.green_panel.layout()
        green_layout.setContentsMargins(15, 15, 15, 15)
        green_layout.setSpacing(8)

        self.green_label = QLabel("GREEN TEAM")
        self.green_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        green_label_style = """
            color: white;
            font-weight: bold;
            font-size: 24px;
            font-family: 'Audiowide', 'Orbitron', 'Courier New', sans-serif;
            background-color: rgba(0, 100, 0, 150);
            border-radius: 15px;
            padding: 5px 15px;
            margin: 5px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
        """
        self.green_label.setStyleSheet(green_label_style)
        self.green_label.setGraphicsEffect(shadow)  # reuse shadow
        green_layout.addWidget(self.green_label)

        self.green_grid = QGridLayout()
        self.green_grid.setHorizontalSpacing(10)
        self.green_grid.setVerticalSpacing(4)
        green_layout.addLayout(self.green_grid)

        team_panel_layout.addWidget(self.red_panel, 1)
        team_panel_layout.addWidget(self.green_panel, 1)

        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(20)

        # Hit feed container
        hit_feed_container = QWidget()
        hit_feed_container.setObjectName("HitFeedContainer")
        hit_feed_container.setStyleSheet("""
            #HitFeedContainer {
                background-color: rgba(0, 0, 0, 127);
                border-radius: 15px;
            }
        """)
        hit_feed_layout = QVBoxLayout(hit_feed_container)
        hit_feed_layout.setContentsMargins(10, 10, 10, 10)

        hit_feed_label = QLabel("Current Game Action")
        hit_feed_label.setStyleSheet("color: white; font-weight: bold; font-size: 18px; font-family: 'Orbitron';")
        hit_feed_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hit_feed_layout.addWidget(hit_feed_label)

        self.hit_list = QListWidget()
        self.hit_list.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                color: white;
                font-size: 14px;
                font-family: 'Courier New';
                border: none;
            }
            QListWidget::item {
                padding: 2px;
            }
        """)
        hit_feed_layout.addWidget(self.hit_list)

        # Timer container
        timer_container = QWidget()
        timer_container.setObjectName("TimerContainer")
        timer_container.setStyleSheet("""
            #TimerContainer {
                background-color: rgba(0, 0, 0, 127);
                border-radius: 15px;
            }
        """)
        timer_layout = QVBoxLayout(timer_container)
        timer_layout.setContentsMargins(10, 10, 10, 10)

        self.phase_label = QLabel("Players get ready!")
        self.phase_label.setStyleSheet("color: white; font-weight: bold; font-size: 18px; font-family: 'Orbitron';")
        self.phase_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        timer_layout.addWidget(self.phase_label)

        self.time_display = QLabel("0:00")
        self.time_display.setStyleSheet("color: #ffffaa; font-size: 36px; font-weight: bold; font-family: 'Orbitron';")
        self.time_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        timer_layout.addWidget(self.time_display)

        bottom_layout.addWidget(hit_feed_container, 2)
        bottom_layout.addWidget(timer_container, 1)

        # Add top and bottom halves to main layout with equal stretch
        main_layout.addLayout(team_panel_layout, 1)
        main_layout.addLayout(bottom_layout, 1)

        # Data structures for score updates
        self.score_labels = {}
        self.player_scores = {}

        # Timer for countdown
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_countdown)
        self.remaining_seconds = 0
        self.timer_state = "ready"

        # Connect UDP score signal
        if hasattr(self.udp, 'score_received'):
            self.udp.score_received.connect(self.on_score_received)

        # Example initial feed entries
        self.add_hit("Scooby Doo hit Opus")
        self.add_hit("Scooby Doo hit Opus")
        self.add_hit("Scooby Doo hit Opus")
        self.add_hit("Opus hit Scooby Doo")
        self.add_hit("Opus hit the Base")
        self.add_hit("Opus hit Scooby Doo")
        self.add_hit("Opus hit Scooby Doo")

    def add_hit(self, text):
        item = QListWidgetItem(text)
        item.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
        self.hit_list.addItem(item)
        self.hit_list.scrollToBottom()

    def start_countdown(self):
        self.timer_state = "ready"
        self.phase_label.setText("Players get ready!")
        self.remaining_seconds = 30
        self.update_timer_display()
        self.timer.start(1000)

    def update_countdown(self):
        self.remaining_seconds -= 1
        self.update_timer_display()

        if self.remaining_seconds <= 0:
            if self.timer_state == "ready":
                self.timer_state = "game"
                self.phase_label.setText("Game on!")
                self.remaining_seconds = 2
                self.update_timer_display()
            elif self.timer_state == "game":
                self.timer.stop()
                self.phase_label.setText("Game Over")
                self.time_display.setText("0:00")
                self.udp.broadcast_equipment_id(221)
            else:
                self.timer.stop()

    def update_timer_display(self):
        minutes = self.remaining_seconds // 60
        seconds = self.remaining_seconds % 60
        self.time_display.setText(f"{minutes}:{seconds:02d}")

    def showEvent(self, event):
        self.refresh_players()
        self.start_countdown()
        super().showEvent(event)

    def refresh_players(self):
        self._clear_grid(self.red_grid)
        self._clear_grid(self.green_grid)
        self.score_labels.clear()
        self.player_scores.clear()

        headers = ["ID", "Codename", "Equip", "Score"]
        header_style = "color: white; font-weight: bold; font-size: 12px;"
        for col, text in enumerate(headers):
            header_red = QLabel(text)
            header_red.setStyleSheet(header_style)
            header_red.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.red_grid.addWidget(header_red, 0, col)

            header_green = QLabel(text)
            header_green.setStyleSheet(header_style)
            header_green.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.green_grid.addWidget(header_green, 0, col)

        red_data = self.main_window.get_red_team_data()
        for row, (player_id, codename, equip_id) in enumerate(red_data, start=1):
            self._add_player_row(self.red_grid, row, player_id, codename, equip_id, "red")

        green_data = self.main_window.get_green_team_data()
        for row, (player_id, codename, equip_id) in enumerate(green_data, start=1):
            self._add_player_row(self.green_grid, row, player_id, codename, equip_id, "green")

    def _clear_grid(self, grid):
        while grid.count():
            item = grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def _add_player_row(self, grid, row, player_id, codename, equip_id, team):
        id_label = QLabel(str(player_id))
        id_label.setStyleSheet("color: white; font-size: 12px;")
        id_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(id_label, row, 0)

        name_label = QLabel(codename)
        name_label.setStyleSheet("color: white; font-size: 12px;")
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(name_label, row, 1)

        equip_label = QLabel(str(equip_id))
        equip_label.setStyleSheet("color: #cccccc; font-size: 12px; font-weight: bold;")
        equip_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(equip_label, row, 2)

        score_label = QLabel("0")
        score_label.setStyleSheet("color: #ffffaa; font-size: 14px; font-weight: bold;")
        score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(score_label, row, 3)

        equip_id_int = int(equip_id)
        self.score_labels[equip_id_int] = (team, score_label)
        self.player_scores[equip_id_int] = 0

    def on_score_received(self, equip_id, points):
        if equip_id in self.score_labels:
            team, label = self.score_labels[equip_id]
            self.player_scores[equip_id] += points
            label.setText(str(self.player_scores[equip_id]))
        else:
            print(f"Warning: Score received for unknown equipment ID {equip_id}")

    def reset_scores(self):
        for equip_id in self.player_scores:
            self.player_scores[equip_id] = 0
            if equip_id in self.score_labels:
                self.score_labels[equip_id][1].setText("0")

class RedTeamPanel(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QBrush(QColor(100, 0, 0, 127)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 20, 20)

class GreenTeamPanel(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QBrush(QColor(0, 100, 0, 127)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 20, 20)