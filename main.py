import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QSizePolicy
from files.Dashboard import DashboardPage
from files.emergency import EmergencyPage
from files.Mappage import MapPage
from files.Alertpage import AlertDetailsPage
from  files.constants import DISASTERBOXES
from  files.Support import SupportPage


class MainAPP(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Disaster Response System")
        self.setGeometry(100, 100, 1920, 1080)
        

        self.current_stylesheet = ""
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        

        self.create_sidebar()
        self.create_main_content()
        self.showMaximized()
        self.update_stylesheet()

    def create_sidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setFixedWidth(200)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        sidebar_layout.setSpacing(15)

        buttons = [
            ("🌐 Dashboard", self.show_dashboard),
            ("🗺 Map", self.show_map),
            ("🚨 Emergency", self.show_emergency),
            ("❓ AI Support", self.show_support),
        ]

        for text, handler in buttons:
            btn = AccessibleButton(text)
            btn.clicked.connect(handler)
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()


        self.main_layout.addWidget(self.sidebar)

    def create_main_content(self):
        self.stacked_widget = QStackedWidget()
        

        self.dashboard_page = DashboardPage(self)
        self.map_page = MapPage(DISASTERBOXES)
        self.emergency_page = EmergencyPage()
        self.alert_details_page = AlertDetailsPage(self)
        self.support_page = SupportPage(self)


        self.stacked_widget.addWidget(self.dashboard_page)
        self.stacked_widget.addWidget(self.map_page)
        self.stacked_widget.addWidget(self.emergency_page)
        self.stacked_widget.addWidget(self.alert_details_page)
        self.stacked_widget.addWidget(self.support_page)

        self.main_layout.addWidget(self.stacked_widget, 1)




    def update_stylesheet(self):
        style = """
            QWidget {
                background-color: #f0f4f8;
                color: #2d3748;
            }
            QPushButton {
                background-color: #ffffff;
                color: #2d3748;
                border: 1px solid #cbd5e0;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #ebf8ff;
            }
            QTextEdit, QLineEdit {
                background-color: #ffffff;
                border: 1px solid #cbd5e0;
                border-radius: 6px;
                padding: 8px;
            }
        """
    
        self.setStyleSheet(style)

    def show_dashboard(self): self.stacked_widget.setCurrentWidget(self.dashboard_page)
    def show_map(self): self.stacked_widget.setCurrentWidget(self.map_page)
    def show_emergency(self): self.stacked_widget.setCurrentWidget(self.emergency_page)
    def show_support(self): self.stacked_widget.setCurrentWidget(self.support_page)





class AccessibleButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                padding: 15px;
                font-size: 16px;
                border-radius: 8px;
            }
        """)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainAPP()
    window.show()
    sys.exit(app.exec_())