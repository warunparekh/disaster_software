
from files.gdcas_alerts import fetch_gdacs_alerts
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel
from files.Alertdetails import AlertCard
from files.constants import filename

class DashboardPage(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
        self.load_data()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        

        active_alerts_label = QLabel("🚨 Active Alerts")
        active_alerts_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(active_alerts_label)

        self.active_alerts_scroll = QScrollArea()
        self.active_alerts_content = QWidget()
        self.active_alerts_layout = QVBoxLayout(self.active_alerts_content)
        self.active_alerts_scroll.setWidget(self.active_alerts_content)
        self.active_alerts_scroll.setWidgetResizable(True)
        layout.addWidget(self.active_alerts_scroll)



        


    def load_data(self):

        alerts = fetch_gdacs_alerts()


        for t,alert in enumerate(alerts):
            alert_widget = AlertCard(
                image_path=f"{filename}\\{alert['imagefile']}", 
                disaster_name=alert["title"],
                location=alert["location"],
                time_ago=alert["time_ago"],
                severity=alert["severity"],
            )
            alert_widget.clicked.connect(lambda _, a=alert: self.show_alert_details(a))
            self.active_alerts_layout.addWidget(alert_widget)


    def show_alert_details(self, alert):

        self.parent.alert_details_page.set_alert_details(alert)
        self.parent.stacked_widget.setCurrentWidget(self.parent.alert_details_page)