
import folium
from PyQt5.QtWebEngineWidgets import QWebEngineView



class MapPage(QWebEngineView):
    def __init__(self, disaster_boxes=None):
        super().__init__()
        self.disaster_boxes = disaster_boxes if disaster_boxes else []
        self.load_map()

    def load_map(self):
        m = folium.Map(location=[0, 0], zoom_start=4)



        for box in self.disaster_boxes:
            if box['type'] == 'polygon':
                folium.Polygon(
                    locations=box['bbox'],
                    color=box['color'],
                    fill=True,
                    fill_color=box['color'],
                    fill_opacity=0.4,
                    popup=folium.Popup(box['label'], max_width=300)
                    
                ).add_to(m)
            elif box['type'] == 'square':
                folium.Rectangle(
                    bounds=[(box['bbox'][2], box['bbox'][0]), (box['bbox'][3], box['bbox'][1])],
                    color=box['color'],
                    fill=True,
                    fill_color=box['color'],
                    fill_opacity=0.4,
                    popup=folium.Popup(box['label'], max_width=300)
                ).add_to(m)

        l_html = '''
        <div style="
            position: fixed; 
            bottom: 40px; left: 40px; width: 200px; height: 180px; 
            background-color: white; z-index:9999; font-size:14px;
            border:2px solid grey; padding: 10px;
            ">
            <b>Disaster Type</b><br>
            <i style="background:blue; width: 10px; height: 10px; display: inline-block;"></i> Tropical Cyclone <br>
            <i style="background:green; width: 10px; height: 10px; display: inline-block;"></i> Flood <br>
            <i style="background:red; width: 10px; height: 10px; display: inline-block;"></i> Volcano <br>
            <i style="background:orange; width: 10px; height: 10px; display: inline-block;"></i> Drought <br>
            <i style="background:darkred; width: 10px; height: 10px; display: inline-block;"></i> Wildfire <br>
            <i style="background:brown; width: 10px; height: 10px; display: inline-block;"></i> Earthquake <br>
        </div>
        '''
        m.get_root().html.add_child(folium.Element(l_html))

        self.setHtml(m._repr_html_())

    def set_theme(self):
        self.load_map()