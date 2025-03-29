from email.mime.text import MIMEText
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QComboBox, QHBoxLayout, QSizePolicy
from PyQt5.QtGui import QFont
import json

from files.constants import filename

class EmergencyPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_emergency_data()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        h_layout = QHBoxLayout()

        self.contacts = QTextEdit()
        self.contacts.setReadOnly(True)
        
        font = QFont()
        font.setPointSize(12) 
        self.contacts.setFont(font)

        self.contacts.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        first_html = f"""
            <h3 style='color: #d9534f; font-size: 48px;'>Emergency Contacts for the United States of America</h3>
            <ul style='font-size: 36px;'>
                <li>🚑 Ambulance: 911</li>
                <li>🚒 Fire Department: 911</li>
                <li>👮 Police: 911</li>
            </ </ul>
        """

        self.contacts.setHtml(first_html)


        h_layout.addWidget(self.contacts)

        self.country_selector = QComboBox()
        self.country_selector.addItem("Select Country")
        self.country_selector.currentIndexChanged.connect(self.update_contacts)
        
        self.country_selector.setFixedWidth(400)  
        self.country_selector.setMinimumHeight(80)  

        self.country_selector.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #f9f9f9;
                font-size: 12pt;  /* Font size for the dropdown */
            }
            QComboBox:hover {
                border: 1px solid #888;  /* Change border color on hover */
            }
            QComboBox::drop-down {
                border-left: 1px solid #ccc;  /* Border for the dropdown arrow */
            }
            QComboBox::down-arrow {
                image: url('path_to_your_arrow_image.png');  /* Optional: Custom arrow image */
            }
        """)

        h_layout.addWidget(self.country_selector)

        layout.addLayout(h_layout)

        layout.addSpacing(10)

    def load_emergency_data(self):
        with open(f'{filename}\\emergency_contacts.json', 'r') as file:
            self.emergency_data = json.load(file)

        for entry in self.emergency_data:
            country_name = entry["Country"]["Name"]
            self.country_selector.addItem(country_name)

    def update_contacts(self):
        country_index = self.country_selector.currentIndex()
        if country_index == 0: 
            self.contacts.setHtml("<h3>Please select a country to see emergency contacts.</h3>")
            return

        selected_country = self.emergency_data[country_index - 1]  
        contacts_html = self.get_emergency_contacts(selected_country)
        self.contacts.setHtml(contacts_html)

    def get_emergency_contacts(self, country_data):
        country_name = country_data["Country"]["Name"]
        
        ambulance_numbers = ", ".join(filter(None, country_data["Ambulance"]["All"])) if country_data["Ambulance"]["All"] else "N/A"
        fire_numbers = ", ".join(filter(None, country_data["Fire"]["All"])) if country_data["Fire"]["All"] else "N/A"
        police_numbers = ", ".join(filter(None, country_data["Police"]["All"])) if country_data["Police"]["All"] else "N/A"

        return f"""
            <h3 style='color: #d9534f; font-size: 48px;'>Emergency Contacts for {country_name}</h3>
            <ul style='font-size: 36px;'>
                <li>🚑 Ambulance: {ambulance_numbers}</li>
                <li>🚒 Fire Department: {fire_numbers}</li>
                <li>👮 Police: {police_numbers}</li>
            </ </ul>
        """