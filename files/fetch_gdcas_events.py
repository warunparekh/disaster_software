
import requests
import json
import xmltodict
from gdacs.api import GDACSAPIReader
import urllib.parse
import feedparser
from datetime import datetime, timedelta

client = GDACSAPIReader()

def fetch_event(item):
    properties = item.get("properties", {})
    
    event_type = properties.get("eventtype")
    event_id = properties.get("eventid")
    update = None
    try:
        update = client.get_event(event_type=event_type, event_id=f"{event_id}")
    except Exception:
        pass
    return update



def fetch_polygon(item):
    properties = item.get("properties", {})
    
    event_type = properties.get("eventtype")
    event_id = properties.get("eventid")

    urlnew = f"https://www.gdacs.org/datareport/resources/{event_type}/{event_id}/cap_{event_id}.xml"
    res = requests.get(urlnew)
    
    if res.status_code != 200:
        return None
    
    try:
        xml_parser = xmltodict.parse(res.content)
        content = xml_parser["alert"]['info']
        
        if content.get("area") is None:
            return False
        else:
            content = content['area']
            if type(content) == list:
                content = content[0]
            else:
                content = content['polygon']

        return json.loads(json.dumps(content))

    except Exception as e:
        return None
    



def fetch_google_news_rss(query):

    encoded_query = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}"
    feed = feedparser.parse(url)
    articles = []


    four_weeks_ago = datetime.now() - timedelta(weeks=4)

    for entry in feed.entries:
        try:

            published_date = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %Z")
        except (ValueError, AttributeError):

            continue


        if published_date < four_weeks_ago:
            continue

        articles.append({
            "title": entry.title,
            "link": entry.link,
            "published": published_date,  
            "source": entry.source.title if hasattr(entry, "source") else "Unknown"
        })



    articles.sort(key=lambda x: x["published"], reverse=True)


    articles = articles[:10]


    for article in articles:
        article["published"] = article["published"].strftime("%Y-%m-%d %H:%M:%S")

    return articles