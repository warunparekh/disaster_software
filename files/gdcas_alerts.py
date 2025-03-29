
from concurrent.futures import ThreadPoolExecutor
from files.fetch_gdcas_events import fetch_event,fetch_polygon
import requests
from files.helper import shrink_square

from datetime import datetime
from files.constants  import DISASTERBOXES

def f_gdacs_alerts():

    url = "https://www.gdacs.org/gdacsapi/api/events/geteventlist/EVENTS4APP"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch GDACS alerts: {response.status_code}")
        return []

    data = response.json()
    features = data.get("features", [])

    return features

def fetch_gdacs_alerts():



    alert_items = f_gdacs_alerts()
    alerts = []
    
  

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(fetch_event, alert_items))
        resultsarea = list(executor.map(fetch_polygon, alert_items))



    filtered_data = [
        (item, event, area)
        for item, event, area in zip(alert_items, results, resultsarea)
        if event is not None
    ]

    alert_items_filtered, results_filtered, resultsarea_filtered = zip(*filtered_data)

    for item, event, area in zip(alert_items_filtered, results_filtered, resultsarea_filtered):

        if area == False:
            polygon = list(map(float, event['gdacs:bbox'].split()))
            polygon = shrink_square(polygon, factor=0.05)
            typelabel = 'square'
        else:
            if area == None:
                continue
            elif type(area) == dict:
                area = area['polygon']

            if '(' in area or ')' in area:
                area = area.split('(')[0]  
                area = area.split(')')[0] 
            coordinate_pairs = area.strip().split()
            for q in coordinate_pairs:
                if ',' in q:
                    pass
                else:
                    coordinate_pairs.remove(q)

            polygon = [(float(lat), float(lon)) for lat, lon in (pair.split(',') for pair in coordinate_pairs)]
            typelabel = 'polygon'

        properties = item.get("properties", {})
        
        event_type = properties.get("eventtype")
        label = ""
        color = ""

        if event_type == 'TC':  
            label = "Tropical Cyclone"
            color = "blue"
        elif event_type == 'FL': 
            label = "Flood"
            color = "green"
        elif event_type == 'VO':  
            label = "Volcano"
            color = "red"
        elif event_type == 'DR': 
            label = "Drought"
            color = "orange"
        elif event_type == 'WF':  
            label = "Wildfire"
            color = "darkred"
        elif event_type == 'EQ': 
            label = "EarthQuake"
            color = "brown"

        DISASTERBOXES.append({"id": properties.get("eventid"), 'bbox': polygon, 'color': color, 'label': event['description'], 'type': typelabel})









    for result, ids in zip(results_filtered, alert_items_filtered):
        if result:

            properties = ids.get("properties", {})
            
            event_type = properties.get("eventtype")


            if event_type == 'TC':  
                label = "Tropical Cyclone"
                image = "cyclone.png"
            elif event_type == 'FL': 
                label = "Flood"
                image = "flood.png"
            elif event_type == 'VO':  
                label = "Volcano"
                image = "volcano.png"
            elif event_type == 'DR': 
                label = "Drought"
                image = "drought.png"
            elif event_type == 'WF':  
                label = "Wildfire"
                image = "fire.png"
            elif event_type == 'EQ': 
                label = "EarthQuake"
                image = "earthquake.png"

            if result['gdacs:country'] is None:
                continue


            try:
                pub_date = datetime.strptime(result.get("pubDate", ""), "%a, %d %b %Y %H:%M:%S %Z")
            except (ValueError, AttributeError):

                continue

            alerts.append({
                "id": properties.get("eventid"), 
                "name": f"{label} in {result['gdacs:country']}",
                "type": label,
                "imagefile": image,
                "title": result.get("title", "No Title"),
                "description": result.get("description", "No Description"),
                "location": result.get("geo:Point", {}).get("geo:lat", "Unknown") + ", " + result.get("geo:Point", {}).get("geo:long", "Unknown"),
                "severity": result.get("gdacs:severity", {}).get("#text", "Unknown"),
                "time_ago": pub_date,  
                "image": result.get("enclosure", {}).get("@url", ""),
                "link": result.get("link", ""),
                "details": result,
            })



    alerts.sort(key=lambda x: x["time_ago"], reverse=True)


    unique_alerts = {}
    for alert in alerts:
        name = alert["name"]
        if name not in unique_alerts or alert["time_ago"] > unique_alerts[name]["time_ago"]:
            unique_alerts[name] = alert


    unique_alerts = list(unique_alerts.values())


    for alert in unique_alerts:
        alert["time_ago"] = alert["time_ago"].strftime("%Y-%m-%d %H:%M:%S")

    return unique_alerts






