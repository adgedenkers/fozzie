# fozzie/sports/fetch.py
import requests
from datetime import date, timedelta

def get_events_for_sport(school_id, sport_id, from_date, to_date):
    url = f"https://www.schedulegalaxy.com/api/v1/schools/{school_id}/activities"
    params = {
        "sport_ids[]": sport_id,
        "from": from_date,
        "to": to_date,
        "per": 100
    }
    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    if isinstance(data, dict) and "activities" in data:
        return data["activities"]
    elif isinstance(data, list):
        return data
    else:
        return []

def get_all_teams(school_id):
    url = f"https://www.schedulegalaxy.com/api/v1/schools/{school_id}/sports"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def get_cached_teams(school_id):
    # No caching — just live fetch
    return get_all_teams(school_id)

def find_sport_id(school_id, level, sport):
    teams = get_all_teams(school_id)
    for t in teams:
        if level.upper() in t["title"].upper() and sport.upper() in t["title"].upper():
            return t["id"]
    return None

def get_next_event(school_id, sport_id):
    today = date.today()
    lookahead_days = 90
    to_date = today + timedelta(days=lookahead_days)

    events = get_events_for_sport(
        school_id, sport_id,
        from_date=today.isoformat(),
        to_date=to_date.isoformat()
    )

    if not events:
        return None

    # Sort events by date and time just to be safe
    def parse_event_datetime(ev):
        return (ev.get("date"), ev.get("start_time") or "00:00")

    events_sorted = sorted(events, key=parse_event_datetime)
    return events_sorted[0] if events_sorted else None



# # fozzie/sports/fetch.py
# import requests

# def get_events_for_sport(school_id, sport_id, from_date, to_date):
#     url = f"https://www.schedulegalaxy.com/api/v1/schools/{school_id}/activities"
#     params = {
#         "sport_ids[]": sport_id,
#         "from": from_date,
#         "to": to_date,
#         "per": 50
#     }
#     response = requests.get(url, params=params)
#     response.raise_for_status()
#     #return response.json()
#     data = response.json()
#     if isinstance(data, dict) and "activities" in data:
#         return data["activities"]
#     elif isinstance(data, list):
#         return data
#     else:
#         return []

# def get_all_teams(school_id):
#     url = f"https://www.schedulegalaxy.com/api/v1/schools/{school_id}/sports"
#     response = requests.get(url)
#     response.raise_for_status()
#     return response.json()

# def get_cached_teams(school_id):
#     # No caching — just live fetch
#     return get_all_teams(school_id)

# def find_sport_id(school_id, level, sport):
#     teams = get_all_teams(school_id)
#     for t in teams:
#         if level.upper() in t["title"].upper() and sport.upper() in t["title"].upper():
#             return t["id"]
#     return None
