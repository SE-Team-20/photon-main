import socket
import constants
import database
from sound_manager import SoundManager
from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QLineEdit, QLabel, QWidget, QPushButton,
    QFormLayout, QMessageBox, QHBoxLayout, QGridLayout, QGraphicsDropShadowEffect,
    QListWidget, QListWidgetItem
)
from udp_server import UDPServer
from PyQt6.QtGui import QGuiApplication, QPainter, QPen, QBrush, QColor, QFont, QPixmap, QImage
from PyQt6.QtCore import Qt, QTimer, QEvent, pyqtSignal
from util import isDevMode
from constants import *
from model import Model

class UDPConfigWindow(QWidget):
    def __init__(self, window_size):
        super().__init__()
        self.setWindowTitle("Photon - Network Configuration")
        self.resize(window_size)
        self.setObjectName("ConfigWindow")
        self.setStyleSheet(STYLE_CONFIG_WINDOW)
        layout = QVBoxLayout(self)
        layout.addStretch()
        title = QLabel("UDP Network Setup")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(STYLE_CONFIG_TITLE)
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

        if isDevMode():
            self.start_system()
            self.close()
            return

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
            self.model = Model(udp)
            udp.assign_model(self.model)
        except OSError:
            QMessageBox.warning(self, "Network Error", "Unable to bind to the specified IP address.")
            return
        self.main_window = MainWindow(udp, self.model)
        self.main_window.show()
        self.close()

class MainWindow(QMainWindow):
    def __init__(self, udp_server: UDPServer, model: Model):
        self.udp = udp_server
        self.model = model
        self.db = database
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
        self.red_label.setStyleSheet(STYLE_TEAM_LABEL_ENTRY_RED)
        self.red_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.green_label.setStyleSheet(STYLE_TEAM_LABEL_ENTRY_GREEN)
        self.green_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        red_shadow = QGraphicsDropShadowEffect()
        red_shadow.setBlurRadius(BLUR_RADIUS)
        red_shadow.setOffset(*DROPSHADOW_OFFSET_AMOUNT)
        red_shadow.setColor(QColor(*SHADOW_COLOR))
        self.red_label.setGraphicsEffect(red_shadow)

        green_shadow = QGraphicsDropShadowEffect()
        green_shadow.setBlurRadius(BLUR_RADIUS)
        green_shadow.setOffset(*DROPSHADOW_OFFSET_AMOUNT)
        green_shadow.setColor(QColor(*SHADOW_COLOR))
        self.green_label.setGraphicsEffect(green_shadow)

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

        self.new_game_button = QPushButton("New Game", self.centralWidget())
        self.new_game_button.setFixedSize(ACTION_BUTTON_WIDTH, ACTION_BUTTON_HEIGHT)
        self.new_game_button.move(0, 0)
        self.new_game_button.setStyleSheet(STYLE_ACTION_BUTTON)
        btn_shadow = QGraphicsDropShadowEffect()
        btn_shadow.setBlurRadius(BLUR_RADIUS)
        btn_shadow.setOffset(*DROPSHADOW_OFFSET_AMOUNT)
        btn_shadow.setColor(QColor(*SHADOW_COLOR))
        self.new_game_button.setGraphicsEffect(btn_shadow)
        self.new_game_button.raise_()
        self.new_game_button.clicked.connect(self.clear_all_grids)

        self.play_action_window = PlayActionWindow(self, self.udp, self.model)
        self.start_game_button = QPushButton("Start Game", self.centralWidget())
        self.start_game_button.setFixedSize(ACTION_BUTTON_WIDTH, ACTION_BUTTON_HEIGHT)
        window_height = self.height()
        window_width = self.width()
        self.start_game_button.move(int(window_width/2 - self.start_game_button.width()/2), 0)
        self.start_game_button.setStyleSheet(STYLE_ACTION_BUTTON)
        start_shadow = QGraphicsDropShadowEffect()
        start_shadow.setBlurRadius(BLUR_RADIUS)
        start_shadow.setOffset(*DROPSHADOW_OFFSET_AMOUNT)
        start_shadow.setColor(QColor(*SHADOW_COLOR))
        self.start_game_button.setGraphicsEffect(start_shadow)
        self.start_game_button.raise_()
        self.start_game_button.clicked.connect(self.show_play_action_window)

    def update_panel_sizes(self):
        w = self.width()
        h = self.height()
        panel_width = int(w * PANEL_WIDTH_RATIO)
        panel_height = int(h * PANEL_HEIGHT_RATIO)
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
            lbl.setStyleSheet(STYLE_GRID_HEADER)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        player_entry_grid.addWidget(id_prompt, 0, 1)
        player_entry_grid.addWidget(codename_prompt, 0, 2)
        player_entry_grid.addWidget(eq_prompt, 0, 3)

        background = RED_TEAM_BACKGROUND if team_name == "RED" else GREEN_TEAM_BACKGROUND

        entries = []
        for row in range(1, 16):
            player_index_label = QLabel("")
            player_index_label.setStyleSheet(STYLE_PLAYER_INDEX_LABEL)
            player_index_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            player_index_label.setFixedWidth(PLAYER_INDEX_LABEL_WIDTH)
            player_entry_grid.addWidget(player_index_label, row, 0)
            index_label_list.append(player_index_label)

            id_edit = QLineEdit()
            id_edit.setFixedSize(PLAYER_ID_FIELD_WIDTH, FIELD_HEIGHT)
            id_edit.setStyleSheet(background)

            codename_edit = QLineEdit()
            codename_edit.setFixedSize(CODENAME_FIELD_WIDTH, FIELD_HEIGHT)
            codename_edit.setStyleSheet(background)
            codename_edit.setReadOnly(True)

            equipment_id_edit = QLineEdit()
            equipment_id_edit.setFixedSize(PLAYER_ID_FIELD_WIDTH, FIELD_HEIGHT)
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
            row_data[2].setReadOnly(False)
            row_data[1].setStyleSheet(f"{background}; color: black;")
            row_data[2].setFocus()
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
    def __init__(self, main_window, udp_server:UDPServer, model:Model):
        super().__init__()
        self.main_window = main_window
        self.udp = udp_server
        self.model = model

        self.sound = SoundManager()
        self.start_track_played = False
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowTitle("PHOTON: Play Action")

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

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        team_panel_layout = QHBoxLayout()
        team_panel_layout.setContentsMargins(0, 0, 0, 0)
        team_panel_layout.setSpacing(20)

        # --- Red panel ---
        self.red_panel = RedTeamPanel()
        self.red_panel.setLayout(QVBoxLayout())
        red_layout = self.red_panel.layout()
        red_layout.setContentsMargins(15, 15, 15, 15)
        red_layout.setSpacing(8)

        self.red_label = QLabel("RED TEAM")
        self.red_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.red_label.setStyleSheet(STYLE_TEAM_LABEL_PLAY_RED)
        red_label_shadow = QGraphicsDropShadowEffect()
        red_label_shadow.setBlurRadius(BLUR_RADIUS)
        red_label_shadow.setOffset(*DROPSHADOW_OFFSET_AMOUNT)
        red_label_shadow.setColor(QColor(*SHADOW_COLOR))
        self.red_label.setGraphicsEffect(red_label_shadow)
        red_layout.addWidget(self.red_label)

        self.red_team_score_label = QLabel("Team Score: 0")
        self.red_team_score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.red_team_score_label.setStyleSheet(STYLE_TEAM_SCORE_LABEL_RED)
        red_layout.addWidget(self.red_team_score_label)

        # Red column headers (permanent, above the player rows)
        red_header_grid = QGridLayout()
        red_header_grid.setHorizontalSpacing(10)
        red_header_grid.setVerticalSpacing(0)
        for col, text in enumerate(["", "ID", "Codename", "Equip", "Score"]):
            lbl = QLabel(text)
            lbl.setStyleSheet(STYLE_GRID_HEADER)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            red_header_grid.addWidget(lbl, 0, col)
        red_layout.addLayout(red_header_grid)

        self.red_grid = QGridLayout()
        self.red_grid.setHorizontalSpacing(10)
        self.red_grid.setVerticalSpacing(4)
        red_layout.addLayout(self.red_grid)

        # --- Green panel ---
        self.green_panel = GreenTeamPanel()
        self.green_panel.setLayout(QVBoxLayout())
        green_layout = self.green_panel.layout()
        green_layout.setContentsMargins(15, 15, 15, 15)
        green_layout.setSpacing(8)

        self.green_label = QLabel("GREEN TEAM")
        self.green_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.green_label.setStyleSheet(STYLE_TEAM_LABEL_PLAY_GREEN)
        green_label_shadow = QGraphicsDropShadowEffect()
        green_label_shadow.setBlurRadius(BLUR_RADIUS)
        green_label_shadow.setOffset(*DROPSHADOW_OFFSET_AMOUNT)
        green_label_shadow.setColor(QColor(*SHADOW_COLOR))
        self.green_label.setGraphicsEffect(green_label_shadow)
        green_layout.addWidget(self.green_label)

        self.green_team_score_label = QLabel("Team Score: 0")
        self.green_team_score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.green_team_score_label.setStyleSheet(STYLE_TEAM_SCORE_LABEL_GREEN)
        green_layout.addWidget(self.green_team_score_label)

        # Green column headers (permanent, above the player rows)
        green_header_grid = QGridLayout()
        green_header_grid.setHorizontalSpacing(10)
        green_header_grid.setVerticalSpacing(0)
        for col, text in enumerate(["", "ID", "Codename", "Equip", "Score"]):
            lbl = QLabel(text)
            lbl.setStyleSheet(STYLE_GRID_HEADER)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            green_header_grid.addWidget(lbl, 0, col)
        green_layout.addLayout(green_header_grid)

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
        hit_feed_container.setStyleSheet(f"#HitFeedContainer {{ {STYLE_SEMI_TRANSPARENT_CONTAINER} }}")
        hit_feed_layout = QVBoxLayout(hit_feed_container)
        hit_feed_layout.setContentsMargins(10, 10, 10, 10)

        hit_feed_label = QLabel("Current Game Action")
        hit_feed_label.setStyleSheet(STYLE_SECTION_LABEL)
        hit_feed_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hit_feed_layout.addWidget(hit_feed_label)

        self.hit_list = QListWidget()
        self.hit_list.setStyleSheet(STYLE_HIT_FEED_LIST)
        hit_feed_layout.addWidget(self.hit_list)

        # Timer container
        self.timer_container = QWidget()
        self.timer_container.setObjectName("TimerContainer")
        self.timer_container.setStyleSheet(f"#TimerContainer {{ {STYLE_SEMI_TRANSPARENT_CONTAINER} }}")
        timer_layout = QVBoxLayout(self.timer_container)
        timer_layout.setContentsMargins(10, 10, 10, 12)
        timer_layout.setSpacing(4)

        # Stretch pushes text/timer to the bottom, logo floats at top
        timer_layout.addStretch(1)

        self.phase_label = QLabel("Players get ready!")
        self.phase_label.setStyleSheet(STYLE_SECTION_LABEL)
        self.phase_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        timer_layout.addWidget(self.phase_label)

        self.time_display = QLabel("0:00")
        self.time_display.setStyleSheet(STYLE_TIMER_DISPLAY)
        self.time_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        timer_layout.addWidget(self.time_display)

        self.end_hint_label = QLabel("Press any key to close scoreboard")
        self.end_hint_label.setStyleSheet(STYLE_SECTION_LABEL)
        self.end_hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.end_hint_label.setWordWrap(True)
        self.end_hint_label.setVisible(False)
        timer_layout.addWidget(self.end_hint_label)

        # Floating Photon logo pinned to top of timer container
        self.photon_logo_label = QLabel(self.timer_container)
        self.photon_logo_label.setObjectName("PhotonLogoOverlay")
        self.photon_logo_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.photon_logo_label.setStyleSheet("background: transparent; border: none;")
        self._load_photon_logo()

        bottom_layout.addWidget(hit_feed_container, 2)
        bottom_layout.addWidget(self.timer_container, 1)

        main_layout.addLayout(team_panel_layout, 1)
        main_layout.addLayout(bottom_layout, 1)

        # Data structures for score updates
        self.score_labels = {}
        self.player_scores = {}
        self.icon_labels = {}
        self.red_team_score = 0
        self.green_team_score = 0
        self.flash_visible = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.remaining_seconds = 0
        self.timer_state = "ready"

        self.flash_timer = QTimer()
        self.flash_timer.timeout.connect(self._toggle_flash)

    def _load_photon_logo(self):
        # Try float-logo.png first, fall back to logo.jpg
        logo_path = IMAGES_DIR / "float-logo.png"
        if not logo_path.exists():
            logo_path = IMAGES_DIR / "logo.jpg"
        pixmap = QPixmap(str(logo_path))
        if pixmap.isNull():
            self.photon_logo_label.hide()
            return
        # Crop bottom 28% to remove the "Ultimate Game on Planet Earth" banner
        crop_h = int(pixmap.height() * 0.72)
        pixmap = pixmap.copy(0, 0, pixmap.width(), crop_h)
        # Make white/near-white pixels transparent
        image = pixmap.toImage().convertToFormat(QImage.Format.Format_ARGB32)
        for y in range(image.height()):
            for x in range(image.width()):
                c = image.pixelColor(x, y)
                if c.red() > 215 and c.green() > 215 and c.blue() > 215:
                    c.setAlpha(0)
                    image.setPixelColor(x, y, c)
        self._photon_logo_pixmap = QPixmap.fromImage(image)
        self._reposition_logo()

    def _reposition_logo(self):
        if not hasattr(self, '_photon_logo_pixmap') or self._photon_logo_pixmap.isNull():
            return
        container = self.timer_container
        # 55% width — compact, sits at top without crowding the timer text
        max_w = int(container.width() * 0.55)
        scaled = self._photon_logo_pixmap.scaledToWidth(
            max_w, Qt.TransformationMode.SmoothTransformation
        )
        self.photon_logo_label.setPixmap(scaled)
        self.photon_logo_label.resize(scaled.size())
        # Shift left of center by ~8% of container width
        x = (container.width() - scaled.width()) // 2 - int(container.width() * 0.08)
        # Pin to top with small padding
        y = 6
        self.photon_logo_label.move(x, y)
        self.photon_logo_label.raise_()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._reposition_logo()

    def add_hit(self, text):
        item = QListWidgetItem(text)
        item.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
        self.hit_list.addItem(item)
        self.hit_list.scrollToBottom()

    def start_countdown(self):
        self.timer_state = "ready"
        self.phase_label.setText("Players get ready!")
        self.end_hint_label.setVisible(False)
        self.remaining_seconds = 0 if isDevMode() else COUNTDOWN_READY_SECONDS
        self.start_track_played = False
        self.update_timer_display()
        self.timer.start(TIMER_INTERVAL_MS)
        self.flash_timer.start(FLASH_INTERVAL_MS)

    def start_game(self):
        self.udp.announce_game_start()
        self.udp.start_readloop()

    def update(self):
        self.update_countdown()
        self.update_leaderboard()

    def update_leaderboard(self):
        print("[Window] update_leaderboard called")
        print(f"[Window] messageq size: {len(self.model.messageq)}")
        print(f"[Window] scorediffq size: {len(self.model.scorediffq)}")
        print("updating leaderboard...")

        while(equip_id := self.model.pop_based_equip_id()) is not False:
            self.grant_baseicon(equip_id)

        while(message := self.model.pop_live_message()) is not False:
            self.add_hit(message)

        while(res := self.model.pop_score_diff()) is not False:
            equip_id, diff = res
            self.reflect_score_change(equip_id, diff)

    def update_countdown(self):
        self.remaining_seconds -= 1
        self.update_timer_display()

        if self.timer_state == "ready" and self.remaining_seconds == MUSIC_START_THRESHOLD and not self.start_track_played:
            self.sound.play_random_start_track()
            self.start_track_played = True

        if self.remaining_seconds <= 0:
            if self.timer_state == "ready":
                self.start_game()
                self.timer_state = "game"
                self.phase_label.setText("Game on!")
                self.remaining_seconds = DEV_GAME_DURATION_SECONDS if isDevMode() else GAME_DURATION_SECONDS
                self.update_timer_display()
            elif self.timer_state == "game":
                self.timer.stop()
                self.flash_timer.stop()
                self._reset_flash()
                self.timer_state = "game_over"
                self.phase_label.setText("Game Over")
                self.time_display.setText("0:00")
                self.end_hint_label.setVisible(True)
                self.udp.announce_game_end()
                self.sound.stop()
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

    def keyPressEvent(self, event):
        if self.timer_state == "game_over":
            self.close_play_action_window()
            self.main_window.show()
            self.main_window.raise_()

    def hideEvent(self, event):
        self.sound.stop()
        super().hideEvent(event)

    def close_play_action_window(self):
        self.flash_timer.stop()
        self.hide()

    def refresh_players(self):
        self._clear_grid(self.red_grid)
        self._clear_grid(self.green_grid)
        self.score_labels.clear()
        self.player_scores.clear()
        self.icon_labels.clear()
        self.model.equip_to_team.clear()

        red_data = self.main_window.get_red_team_data()
        for row, (player_id, codename, equip_id) in enumerate(red_data, start=0):
            self._add_player_row(self.red_grid, row, player_id, codename, equip_id, "red")
            self.model.equip_to_codename[int(equip_id)] = codename
            self.model.equip_to_team[int(equip_id)] = Model.RED
            print(f"[Window] equip_to_codename populated: {self.model.equip_to_codename}")

        green_data = self.main_window.get_green_team_data()
        for row, (player_id, codename, equip_id) in enumerate(green_data, start=0):
            self._add_player_row(self.green_grid, row, player_id, codename, equip_id, "green")
            self.model.equip_to_codename[int(equip_id)] = codename
            self.model.equip_to_team[int(equip_id)] = Model.GREEN
            print(f"[Window] equip_to_codename populated: {self.model.equip_to_codename}")

    def _clear_grid(self, grid):
        while grid.count():
            item = grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def _add_player_row(self, grid, row, player_id, codename, equip_id, team):
        alt = row % 2 == 0
        player_style = STYLE_PLAYER_LABEL_ALT if alt else STYLE_PLAYER_LABEL
        equip_style = STYLE_EQUIP_LABEL_ALT if alt else STYLE_EQUIP_LABEL
        score_style = STYLE_SCORE_LABEL_ALT if alt else STYLE_SCORE_LABEL

        icon = QLabel()
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(icon, row, 0)

        id_label = QLabel(str(player_id))
        id_label.setStyleSheet(player_style)
        id_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(id_label, row, 1)

        name_label = QLabel(codename)
        name_label.setStyleSheet(player_style)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(name_label, row, 2)

        equip_label = QLabel(str(equip_id))
        equip_label.setStyleSheet(equip_style)
        equip_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(equip_label, row, 3)

        score_label = QLabel("0")
        score_label.setStyleSheet(score_style)
        score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(score_label, row, 4)

        equip_id_int = int(equip_id)
        self.score_labels[equip_id_int] = (team, score_label)
        self.player_scores[equip_id_int] = 0
        self.icon_labels[equip_id_int] = icon

    def grant_baseicon(self, equip_id):
        if equip_id not in self.icon_labels:
            print(f"Warning: baseicon request received for unknown equipment ID {equip_id}")
            return
        label = self.icon_labels[equip_id]
        pixmap = QPixmap(str(IMAGES_DIR / "baseicon.jpg"))

        if pixmap.isNull():
            label.clear()
            return
        scaled = pixmap.scaled(
            BASEICON_SIZE,
            BASEICON_SIZE,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        label.setPixmap(scaled)
        print(f"baseicon is now reflected to {equip_id}")

    def reflect_score_change(self, equip_id, diff):
        if equip_id not in self.score_labels:
            print(f"Warning: Score received for unknown equipment ID {equip_id}")
            return

        _, label = self.score_labels[equip_id]
        self.player_scores[equip_id] += diff
        label.setText(str(self.player_scores[equip_id]))
        self._update_team_scores()

    def reset_scores(self):
        for equip_id in self.player_scores:
            self.player_scores[equip_id] = 0
            if equip_id in self.score_labels:
                self.score_labels[equip_id][1].setText("0")
        self.red_team_score = 0
        self.green_team_score = 0
        self.red_team_score_label.setText("Team Score: 0")
        self.green_team_score_label.setText("Team Score: 0")

    def _update_team_scores(self):
        red_total = sum(
            score for equip_id, score in self.player_scores.items()
            if self.score_labels.get(equip_id, (None,))[0] == "red"
        )
        green_total = sum(
            score for equip_id, score in self.player_scores.items()
            if self.score_labels.get(equip_id, (None,))[0] == "green"
        )
        self.red_team_score = red_total
        self.green_team_score = green_total
        self.red_team_score_label.setText(f"Team Score: {red_total}")
        self.green_team_score_label.setText(f"Team Score: {green_total}")

    def _reset_flash(self):
        self.red_team_score_label.setStyleSheet(STYLE_TEAM_SCORE_LABEL_RED)
        self.green_team_score_label.setStyleSheet(STYLE_TEAM_SCORE_LABEL_GREEN)

    def _toggle_flash(self):
        if self.timer_state != "game" or self.red_team_score == self.green_team_score:
            self._reset_flash()
            return

        self.flash_visible = not self.flash_visible
        leading_red = self.red_team_score > self.green_team_score

        red_style = STYLE_TEAM_SCORE_LABEL_FLASH_RED if (leading_red and self.flash_visible) else STYLE_TEAM_SCORE_LABEL_RED
        green_style = STYLE_TEAM_SCORE_LABEL_FLASH_GREEN if (not leading_red and self.flash_visible) else STYLE_TEAM_SCORE_LABEL_GREEN

        self.red_team_score_label.setStyleSheet(red_style)
        self.green_team_score_label.setStyleSheet(green_style)

class RedTeamPanel(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = self.rect()

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(*COLOR_PANEL_BG_RED)))
        painter.drawRoundedRect(r, PANEL_BORDER_RADIUS, PANEL_BORDER_RADIUS)

        painter.setBrush(Qt.BrushStyle.NoBrush)
        for pen_width, alpha in PANEL_GLOW_LAYERS:
            pen = QPen(QColor(*COLOR_PANEL_GLOW_RED, alpha))
            pen.setWidth(pen_width)
            painter.setPen(pen)
            inset = pen_width // 2
            painter.drawRoundedRect(
                r.adjusted(inset, inset, -inset, -inset),
                PANEL_BORDER_RADIUS, PANEL_BORDER_RADIUS
            )

        cs = PANEL_CORNER_MARK_SIZE
        cr = PANEL_BORDER_RADIUS
        w, h = r.width() - 1, r.height() - 1
        corner_pen = QPen(QColor(*COLOR_PANEL_GLOW_RED, 255))
        corner_pen.setWidth(2)
        painter.setPen(corner_pen)
        painter.drawLine(cr, 1, cr + cs, 1)
        painter.drawLine(1, cr, 1, cr + cs)
        painter.drawLine(w - cr, 1, w - cr - cs, 1)
        painter.drawLine(w - 1, cr, w - 1, cr + cs)
        painter.drawLine(cr, h - 1, cr + cs, h - 1)
        painter.drawLine(1, h - cr, 1, h - cr - cs)
        painter.drawLine(w - cr, h - 1, w - cr - cs, h - 1)
        painter.drawLine(w - 1, h - cr, w - 1, h - cr - cs)

class GreenTeamPanel(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = self.rect()

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(*COLOR_PANEL_BG_GREEN)))
        painter.drawRoundedRect(r, PANEL_BORDER_RADIUS, PANEL_BORDER_RADIUS)

        painter.setBrush(Qt.BrushStyle.NoBrush)
        for pen_width, alpha in PANEL_GLOW_LAYERS:
            pen = QPen(QColor(*COLOR_PANEL_GLOW_GREEN, alpha))
            pen.setWidth(pen_width)
            painter.setPen(pen)
            inset = pen_width // 2
            painter.drawRoundedRect(
                r.adjusted(inset, inset, -inset, -inset),
                PANEL_BORDER_RADIUS, PANEL_BORDER_RADIUS
            )

        cs = PANEL_CORNER_MARK_SIZE
        cr = PANEL_BORDER_RADIUS
        w, h = r.width() - 1, r.height() - 1
        corner_pen = QPen(QColor(*COLOR_PANEL_GLOW_GREEN, 255))
        corner_pen.setWidth(2)
        painter.setPen(corner_pen)
        painter.drawLine(cr, 1, cr + cs, 1)
        painter.drawLine(1, cr, 1, cr + cs)
        painter.drawLine(w - cr, 1, w - cr - cs, 1)
        painter.drawLine(w - 1, cr, w - 1, cr + cs)
        painter.drawLine(cr, h - 1, cr + cs, h - 1)
        painter.drawLine(1, h - cr, 1, h - cr - cs)
        painter.drawLine(w - cr, h - 1, w - cr - cs, h - 1)
        painter.drawLine(w - 1, h - cr, w - 1, h - cr - cs)