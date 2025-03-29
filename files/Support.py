from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QHBoxLayout, QTextEdit
from PyQt5.QtGui import QFontDatabase, QFont, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal
from files.gdcas_alerts import fetch_gdacs_alerts
from files.constants import filename
from files.gemini import generate_evacuation_plan_with_gemini
from files.fetch_gdcas_events import fetch_google_news_rss
from playwright.sync_api import sync_playwright
from parsel import Selector
import json
from files.helper import parse_thread
from nested_lookup import nested_lookup

class SupportPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
        self.load_data()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)


        layout.setSpacing(10) 
        layout.setContentsMargins(10, 10, 10, 10) 

        label_style = """
            QLabel {
                font-size: 20px;
                font-weight: bold;
                text-align: center;
                border-radius: 10px;
                padding: 10px;
                background-color: #f0f0f0;
            }
        """
        scroll_area_style = """
            QScrollArea {
                border-radius: 10px;
                background-color: #ffffff;
            }
            QScrollBar:vertical {
                border: none;
                background-color: #f0f0f0;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #c0c0c0;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """


        self.active_alerts_scroll = QScrollArea()
        self.active_alerts_scroll.setStyleSheet(scroll_area_style)
        self.active_alerts_scroll.setFixedSize(1800, 900)
        self.active_alerts_content = QWidget()
        self.active_alerts_layout = QVBoxLayout(self.active_alerts_content)
        self.active_alerts_scroll.setWidget(self.active_alerts_content)
        self.active_alerts_scroll.setWidgetResizable(True)
        layout.addWidget(self.active_alerts_scroll, alignment=Qt.AlignCenter)

        self.text_box = QTextEdit()
        self.text_box.setStyleSheet("""
            QTextEdit {
                font-size: 16px;
                padding: 10px;
                border-radius: 10px;
                background-color: #ffffff;
                border: 1px solid #ccc;
            }
        """)
        self.text_box.setPlaceholderText("Detailed information will appear here...")
        self.text_box.setFixedSize(1800, 900)
        self.text_box.hide()  
        layout.addWidget(self.text_box, alignment=Qt.AlignCenter)

    def load_data(self):
        alerts = fetch_gdacs_alerts()
        for t, alert in enumerate(alerts):
            alert_widget = AlertCardAI(
                image_path=f"{filename}\\{alert['imagefile']}",
                disaster_name=alert["title"],
                location=alert["location"],
                time_ago=alert["time_ago"],
                severity=alert["severity"],
            )
            alert_widget.clicked.connect(lambda _, a=alert: self.show_alert_details(a))
            self.active_alerts_layout.addWidget(alert_widget)

    def show_alert_details(self, alert):

        self.active_alerts_scroll.hide()
        self.text_box.show()


        query = f"{alert['details']['gdacs:country']} {alert['type']}"


        if alert['type'] == None or alert['details']['gdacs:country'] == None:
            articles = []
        else:
            articles = fetch_google_news_rss(query)
        
        posts = self.scrape_threads(query)    
  
        insights = generate_evacuation_plan_with_gemini(alert, articles, posts)

        self.text_box.setPlainText(insights)


    def scrape_threads(self, query):

        url = f"https://www.threads.net/search?q={query}"
        threads = []

        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)  
            context = browser.new_context(viewport={"width": 1920, "height": 1080})
            page = context.new_page()

            page.goto(url)
            page.wait_for_selector("[data-pressable-container=true]")

            selector = Selector(page.content())
            hidden_datasets = selector.css('script[type="application/json"][data-sjs]::text').getall()


            for hidden_dataset in hidden_datasets:

                if '"ScheduledServerJS"' not in hidden_dataset:
                    continue
                if "thread_items" not in hidden_dataset:
                    continue


                data = json.loads(hidden_dataset)
                thread_items = nested_lookup("thread_items", data)
                if not thread_items:
                    continue


                for thread in thread_items:
                    for t in thread:
                        threads.append(parse_thread(t))
                        if len(threads) >= 10: 
                            break
                    if len(threads) >= 10:
                        break
                if len(threads) >= 10:
                    break


            browser.close()

        return threads[:10]


class AlertCardAI(QWidget):
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

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)


        image_label = QLabel()
        image_label.setFixedSize(200, 200)
        pixmap = QPixmap(image_path).scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)


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
        self.info_label.setMinimumWidth(1200)
        self.info_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.update_stylesheet()


        layout.addWidget(image_label)
        layout.addWidget(self.info_label)
        layout.addStretch()

        self.setLayout(layout)


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