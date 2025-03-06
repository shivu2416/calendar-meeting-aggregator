import requests
import jwt
from datetime import datetime

def fetch_meetings(token, provider, start_date=None, end_date=None):
    """
    Fetches meetings from Google Calendar or Outlook Calendar based on the provider.
    
    :param token: OAuth access token for authentication.
    :param provider: "google" for Google Calendar, "outlook" for Outlook Calendar.
    :param start_date: (Optional) Start date to filter meetings.
    :param end_date: (Optional) End date to filter meetings.
    :return: List of meeting details.
    """

    # Define API URLs based on provider
    PROVIDERS = {
        "google": {
            "base_url": "https://www.googleapis.com/calendar/v3",
            "calendars_endpoint": "/users/me/calendarList",
            "events_endpoint": "/calendars/{}/events",
            "auth_header": "Bearer",
            "meeting_link_field": "hangoutLink",
            "email_field": "email",
            "organizer_field": "organizer.email",
            "attendee_field": "email",
            "event_title": "summary",
            "event_desc": "description",
        },
        "outlook": {
            "base_url": "https://graph.microsoft.com/v1.0/me",
            "calendars_endpoint": "/calendars",
            "events_endpoint": "/calendars/{}/events",
            "auth_header": "Bearer",
            "meeting_link_field": "onlineMeeting.joinUrl",
            "email_field": "emailAddress.address",
            "organizer_field": "organizer.emailAddress.address",
            "attendee_field": "emailAddress.address",
            "event_title": "subject",
            "event_desc": "bodyPreview",
        }
    }

    if provider not in PROVIDERS:
        raise ValueError("Invalid provider. Choose 'google' or 'outlook'.")

    API = PROVIDERS[provider]
    BASE_URL = API["base_url"]
    HEADERS = {"Authorization": f"{API['auth_header']} {token}"}

    try:
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        user_email = decoded_token.get("email", "") or decoded_token.get("unique_name", "") or decoded_token.get("upn", "")
        SYNCED_DOMAIN = user_email.split("@")[1] if "@" in user_email else None
    except Exception as e:
        print("Error decoding token:", e)
        SYNCED_DOMAIN = None

    def get_calendars():
        """Fetch the list of calendars accessible by the user."""
        url = f"{BASE_URL}{API['calendars_endpoint']}"
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            key = "items" if provider == "google" else "value"
            return [cal["id"] for cal in response.json().get(key, [])]
        return []

    def parse_datetime(dt_str):
        """Safely parse datetime string."""
        try:
            return datetime.fromisoformat(dt_str.replace("Z", "+00:00")) if dt_str else None
        except ValueError:
            return None

    def get_meetings(calendar_id, start_date=None, end_date=None):
        """Fetch meetings for a specific calendar."""
        url = f"{BASE_URL}{API['events_endpoint'].format(calendar_id)}"
        params = {
            "timeMin": start_date.isoformat() if start_date else None,
            "timeMax": end_date.isoformat() if end_date else None,
            "singleEvents": True,
            "orderBy": "startTime",
        } if provider == "google" else {}

        response = requests.get(url, headers=HEADERS, params=params)
        meetings = []

        if response.status_code == 200:
            key = "items" if provider == "google" else "value"
            events = response.json().get(key, [])
            for event in events:
                event_start_str = event.get("start", {}).get("dateTime", event.get("start", {}).get("date", ""))
                event_end_str = event.get("end", {}).get("dateTime", event.get("end", {}).get("date", ""))

                event_start = parse_datetime(event_start_str)
                event_end = parse_datetime(event_end_str)

                # Apply date filtering
                if start_date and event_start and event_start < start_date:
                    continue
                if end_date and event_start and event_start > end_date:
                    continue

                attendees = event.get("attendees", [])
                our_emails = []
                others_emails = set()

                for attendee in attendees:
                    email = attendee.get(API["attendee_field"], "")
                    domain = email.split("@")[1] if "@" in email else ""
                    if domain == SYNCED_DOMAIN:
                        our_emails.append(email)
                    else:
                        others_emails.add(email)

                meeting_data = {
                    "opportunity_name": event.get(API["organizer_field"], ""),
                    "our_emails": our_emails,
                    "others_emails": list(others_emails),
                    "is_multiple_domains": len(set(email.split("@")[1] for email in others_emails if "@" in email)) > 1,
                    "start_time": event_start_str,
                    "end_time": event_end_str,
                    "meeting_link": event.get(API["meeting_link_field"], ""),
                    "calendar_meeting_id": event.get("id", ""),
                    "title": event.get(API["event_title"], ""),
                    "desc": event.get(API["event_desc"], ""),
                }
                meetings.append(meeting_data)
        return meetings

    all_meetings = []
    calendar_ids = get_calendars()
    for calendar_id in calendar_ids:
        all_meetings.extend(get_meetings(calendar_id, start_date, end_date))

    return all_meetings
