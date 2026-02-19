import socket
from database import DB
import testdb
from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QLineEdit,
    QLabel,
    QWidget,
    QPushButton,
    QFormLayout,
    QMessageBox,
    QHBoxLayout,
    QGridLayout,
    QGraphicsDropShadowEffect,
)
from udp_server import UDPServer

from PyQt6.QtGui import QGuiApplication, QPainter, QBrush, QColor
from PyQt6.QtCore import Qt

from util import isDevMode

from constants import (
    BLURRED_LOGO
)

class UDPConfigWindow(QWidget):
    def __init__(self, window_size):
        super().__init__()

        self.setWindowTitle("Photon - Network Configuration")
        self.resize(window_size)
        self.setObjectName("ConfigWindow")

        # ---------- Style ----------
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
                background-color: rgba(0, 0, 0, 180);
                border: 1px solid #555;
                padding: 8px;
                border-radius: 6px;
                color: white;
                font-size: 14px;
                min-width: 220px;
            }

            QPushButton {
                background-color: #b30000;
                padding: 10px 25px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 16px;
                color: white;
            }

            QPushButton:hover {
                background-color: #e60000;
            }
        """)

        # ---------- Layout ----------
        layout = QVBoxLayout(self)
        layout.addStretch()

        title = QLabel("UDP Network Setup")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(title)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        # Only 2 inputs (as required)
        self.receive_input = QLineEdit("0.0.0.0")
        self.broadcast_input = QLineEdit("127.0.0.1")

        form.addRow("Receive IP:", self.receive_input)
        form.addRow("Broadcast IP:", self.broadcast_input)

        layout.addLayout(form)
        layout.addSpacing(20)

        self.start_button = QPushButton("Start System")
        self.start_button.clicked.connect(self.start_system)
        layout.addWidget(self.start_button, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()

        self.main_window = None

    # ---------- Validate IPv4 ----------
    def validate_ip(self, ip):
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            return False

    # ---------- Start System ----------
    def start_system(self):
        receive_ip = self.receive_input.text().strip()
        broadcast_ip = self.broadcast_input.text().strip()

        # Check empty first
        if not receive_ip or not broadcast_ip:
            QMessageBox.warning(
                self, "Missing Input", "Please enter both Receive IP and Broadcast IP."
            )
            return

        # Validate IP format
        if not self.validate_ip(receive_ip):
            QMessageBox.warning(self, "Invalid IP", "Receive IP is not valid.")
            return

        if not self.validate_ip(broadcast_ip):
            QMessageBox.warning(self, "Invalid IP", "Broadcast IP is not valid.")
            return

        try:
            udp = UDPServer(receive_ip=receive_ip, broadcast_ip=broadcast_ip)
        except OSError:
            QMessageBox.warning(
                self, "Network Error", "Unable to bind to the specified IP address."
            )
            return

        self.main_window = MainWindow(udp, DB())
        self.main_window.show()
        self.close()

class MainWindow(QMainWindow):
    # UDP server, database instance
    def __init__(self, udp_server, db):
        self.udp = udp_server
        self.db = db

        super().__init__()

        # Display the file in front of other apps
        self.setWindowFlags(
            self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint
        )

        # header
        self.setWindowTitle("PHOTON")

        # screen size and coordinates
        screen=QGuiApplication.primaryScreen().availableGeometry()
        window_width = screen.width()//2
        window_height = screen.height()//2
        x=(screen.width() - window_width)//2
        y=(screen.height() - window_height)//2
        self.setGeometry(x, y, window_width, window_height)

        # central widget with background image
        central_widget = QWidget()
        central_widget.setObjectName("MainWindowWidget")
        central_widget.setStyleSheet(f"""
            #MainWindowWidget {{
                border-image: url('{BLURRED_LOGO}');
                background-position: center;
            }}
        """)
        self.setCentralWidget(central_widget)

        # main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # left side container
        self.left_container = QWidget()
        left_layout = QVBoxLayout(self.left_container)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)

        # red team panel
        self.red_panel = RedTeamPanel()
        self.red_panel.setLayout(QVBoxLayout())

        # right side container
        self.right_container = QWidget()
        right_layout = QVBoxLayout(self.right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        # green team panel
        self.green_panel = GreenTeamPanel()
        self.green_panel.setLayout(QVBoxLayout())

        self.red_label = QLabel("RED TEAM")
        self.green_label = QLabel("GREEN TEAM")

        # style for red label
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

        # style for green label
        green_label_style = red_label_style.replace("rgba(100, 0, 0, 150)", "rgba(0, 100, 0, 150)")
        self.green_label.setStyleSheet(green_label_style)
        self.green_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # stylesheets for labels
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

        # data binding to the grid

        self.red_index_labels = []
        self.green_index_labels = []

        self.create_player_grid(self.red_panel.layout(), "RED", self.red_index_labels)
        self.create_player_grid(self.green_panel.layout(), "GREEN", self.green_index_labels)

        # apply initial dimension ruling
        self.update_panel_sizes()

    # Automatically called on the change in window size
    def update_panel_sizes(self):
        w = self.width()
        h = self.height()
        panel_width = int(w * 0.48)
        panel_height = int(h * 0.5)
        self.red_panel.setFixedSize(panel_width, panel_height)
        self.green_panel.setFixedSize(panel_width, panel_height)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_panel_sizes()


    def create_player_grid(self, parent_layout, team_name, index_label_list):
        player_entry_grid = QGridLayout()

        # basic visual
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
        entries = []
        for row in range(1, 16):
            # visual
            player_index_label = QLabel("")
            player_index_label.setStyleSheet("color: black; font-weight: bold;")
            player_index_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            player_entry_grid.addWidget(player_index_label, row, 0)

            # push to reference list
            index_label_list.append(player_index_label)

            # UI input fields
            player_id_edit = QLineEdit()
            codename_edit = QLineEdit()
            equipment_id_edit = QLineEdit()

            for entry in (player_id_edit, codename_edit, equipment_id_edit):
                entry.setFixedSize(80, 20)
                entry.setStyleSheet(cool_font)

            # enable the input field iff the player ID is entered and the database does not have it
            codename_edit.setReadOnly(True)
            equipment_id_edit.setReadOnly(True)
            
            player_entry_grid.addWidget(player_id_edit, row, 1)
            player_entry_grid.addWidget(codename_edit, row, 2)
            player_entry_grid.addWidget(equipment_id_edit, row, 3)

            row_data = [player_id_edit, codename_edit, equipment_id_edit]
            entries.append(row_data)

            # OnKeyPressed(return) -> enable event
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
        
        parent_layout.addLayout(player_entry_grid)
        return entries

    # Affects the codename section after making the query to the database
    def on_player_id_enter(self, row_data, team, index):
        player_id = row_data[0].text().strip()

        index_labels = self.red_index_labels if team=="RED" else self.green_index_labels

        # clear the label
        if not player_id:
            index_labels[index].setText("")
            row_data[1].clear()
            row_data[1].setReadOnly(True)
            row_data[1].setPlaceholderText("")
            return
        
        # Convert to integer
        try:
            player_id = int(player_id)
        except ValueError:
            print(f"Error: player_id must be integer: {player_id}")
            return
        
        # Visual update
        index_labels[index].setText(f"Player #{index+1}")

        # Query if the player ID is registered already
        codename = False if isDevMode() else self.db.isRegistered(player_id)

        if codename:
            # fill the codename and move to equipment
            row_data[1].setText(codename)
            row_data[1].setReadOnly(False)
            row_data[1].setStyleSheet("color: black;")
            row_data[1].setPlaceholderText("")
            row_data[2].setReadOnly(False)
            row_data[2].setFocus()
        else:
            # open up the availability to edit
            row_data[1].clear()
            row_data[1].setReadOnly(False)
            row_data[1].setPlaceholderText("Enter codename for new player")
            row_data[1].setStyleSheet("color: gray;")
            row_data[1].setFocus()

    # Change the codename corresponding to the player ID if registered
    def on_codename_enter(self, row_data, team, index):
        if row_data[1].isReadOnly():
            return

        player_id_text = row_data[0].text().strip()
        codename = row_data[1].text().strip()

        # ignore if blank
        if not player_id_text or not codename:
            row_data[2].setReadOnly(True)
            return

        # Ignore when invalid ID
        try:
            player_id = int(player_id_text)
        except ValueError:
            return 

        # Attempt to add the new player
        if isDevMode():
            print("Error: we cannot proceed with database connection when isDevMode is active.")
            row_data[2].setReadOnly(False)
            return
        
        isRegistered = self.db.isRegistered()

        # different methods (update if existing / add new if new)
        success = self.db.updateCodename(player_id, codename) if isRegistered else self.db.usePlayerID(player_id, codename)

        if success:
            # Player added – update style and move to equipment
            row_data[2].setReadOnly(False)
            row_data[1].setStyleSheet("color: black;")
            row_data[1].setPlaceholderText("")
            row_data[2].setFocus()
        else:
            print("Failed registering the new codename to the player ID on database")
            row_data[1].setStyleSheet("border: 1px solid red; background-color: #ffcccc;")

    # broadcast the equipment ID if successful
    def on_row_submit(self, row_data, team, index):
        player_id = row_data[0].text().strip()
        equip_id = row_data[2].text().strip()

        # ignore if invalid data type for equip ID
        try:
            equip_id = int(equip_id)
        except ValueError:
            row_data[2].setStyleSheet("border: 1px solid red; background-color: #ffcccc; color: black;")
            return
        

        # check parity for team ID (red odd, green even)
        if team=="RED" and equip_id%2==0 or team=="GREEN" and equip_id%2==1:
            print("Error: wrong equipment ID parity for the team color")
            row_data[2].setStyleSheet("border: 1px solid red; background-color: #ffcccc; color: black;")
            return
        
        # if the previous input field remains blank
        if not player_id or not equip_id:
            print(f"[{team}] ERROR: Both fields are required for this row.")
            if not player_id:
                row_data[0].setStyleSheet("border: 1px solid red; background-color: #ffcccc; color: black;")
            if not equip_id:
                row_data[2].setStyleSheet("border: 1px solid red; background-color: #ffcccc; color: black;")
            return
        
        # Connects to database and register the in-game info
        if not isDevMode() and self.db.addPlayerNextGame(player_id, 0 if team=="RED" else 1, equip_id):
            print(f"[{team}] SUCCESS - Player: {player_id}, Equipment: {equip_id}, Player Index: {index}")

        row_data[2].setStyleSheet("color: black; font-weight: bold; font-size: 12px;")
        self.udp.broadcast_equipment_id(equip_id)
            

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
