
from PyQt5.QtCore import  Qt, pyqtSignal
from PyQt5.QtGui import QFontDatabase, QFont, QPixmap
from PyQt5.QtWidgets import  QWidget,QHBoxLayout, QLabel


from files.constants import filename

class AlertCard(QWidget):
    clicked = pyqtSignal(dict)
    def __init__(self, image_path, disaster_name, location, time_ago, severity):
        super().__init__()
        self.image_path = image_path
        self.disaster_name = disaster_name
        self.location = location
        self.time_ago = time_ago
        self.severity = severity
        self.init_ui(image_path, disaster_name, location, time_ago, severity)

    def init_ui(self, image_path, disaster_name, location, time_ago, severity):

        # layout for the carousel item
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # image label
        image_label = QLabel()
        image_label.setFixedSize(200, 200)
        pixmap = QPixmap(image_path).scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)

        # info label
        info_text = f"""
        <b style="font-size: 30px;">{disaster_name}</b><br>
        <i style="font-size: 18px;">Time Added: {time_ago}</i><br>
        <i style="font-size: 18px;">Location: {location}</i>
        """

        self.info_label = QLabel(info_text)
        self.info_label.setWordWrap(True)



        font_id = QFontDatabase.addApplicationFont(f"{filename}\\Comfortaa-Bold.ttf")
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        custom_font = QFont(font_family, 12)
        
        self.info_label.setFont(custom_font)
        self.info_label.setFixedHeight(200)
        self.info_label.setMinimumWidth(1400)
        self.info_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)


        self.update_stylesheet()

        # widgets to the layout
        layout.addWidget(image_label)
        layout.addWidget(self.info_label)
        layout.addStretch()

        self.setLayout(layout)

        # item clickable
        self.setCursor(Qt.PointingHandCursor)
        self.mousePressEvent = self.on_click
        

    def update_stylesheet(self):
        
        self.info_label.setStyleSheet("""
            background-color: #FFFFFF;
            border-radius: 10px;
            padding: 10px;

        """)
    


    def on_click(self, event):
        alert_data = {
            "image": self.image_path,
            "disaster_name": self.disaster_name,
            "location": self.location,
            "time_ago": self.time_ago,
            "severity": self.severity
        }
        self.clicked.emit(alert_data)
