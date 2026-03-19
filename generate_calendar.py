import requests
from datetime import datetime
from icalendar import Calendar, Event

BASE_URL = "https://www.rhodeislandinterscholasticleague.org/public/genie/267/school/886/calendar/json"

cal = Calendar()
cal.add('prodid', '-//Cumberland JV Baseball Calendar//mxm.dk//')
cal.add('version', '2.0')

def fetch_events():
    events = []

    params = {
        "start": "2026-03-01",
        "end": "2026-07-01"
    }

    res = requests.get(BASE_URL, params=params)
    data = res.json()

    for item in data:
        title = item.get("title", "")

        if "Baseball" not in title or "JV" not in title:
            continue

        start = datetime.fromisoformat(item["start"])
        end = datetime.fromisoformat(item["end"])

        events.append({
            "title": title,
            "start": start,
            "end": end,
            "location": item.get("location", ""),
            "description": item.get("description", "")
        })

    return events


for e in fetch_events():
    event = Event()
    event.add('summary', e["title"])
    event.add('dtstart', e["start"])
    event.add('dtend', e["end"])
    event.add('location', e["location"])
    event.add('description', e["description"])
    cal.add_component(event)

with open("cumberland-jv-baseball.ics", "wb") as f:
    f.write(cal.to_ical())
