from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch
from datetime import datetime, timedelta

# Import from correct module
from meetings.utils import fetch_google_calendar_meetings, fetch_outlook_calendar_meetings
from meetings.serializers import MeetingSerializer

class CalendarMeetingAggregatorTests(TestCase):
    def setUp(self):
        """Set up the test client and required data."""
        self.client = APIClient()
        self.token = "test_valid_token"
        self.invalid_token = "test_invalid_token"
        self.start_date = datetime.utcnow().isoformat()
        self.end_date = (datetime.utcnow() + timedelta(days=14)).isoformat()
        self.api_url = "/api/meetings/"

    @patch("meetings.utils.fetch_google_calendar_meetings")
    @patch("meetings.utils.fetch_outlook_calendar_meetings")
    def test_fetch_meetings_success(self, mock_outlook_meetings, mock_google_meetings):
        """Test successful retrieval of meetings from both Google and Outlook."""
        mock_google_meetings.return_value = [
            {
                "id": "google123",
                "summary": "Google Meeting",
                "description": "Discussion on project scope.",
                "start": {"dateTime": "2025-03-05T10:00:00Z"},
                "end": {"dateTime": "2025-03-05T11:00:00Z"},
                "organizer": {"emailAddress": {"address": "user@yourcompany.com"}},
                "attendees": [
                    {"email": "user@yourcompany.com"},
                    {"email": "client@example.com"},
                ],
                "hangoutLink": "https://meet.google.com/xyz",
            }
        ]

        mock_outlook_meetings.return_value = [
            {
                "id": "outlook456",
                "summary": "Outlook Meeting",
                "description": "Team stand-up meeting.",
                "start": {"dateTime": "2025-03-06T09:00:00Z"},
                "end": {"dateTime": "2025-03-06T09:30:00Z"},
                "organizer": {"emailAddress": {"address": "user@yourcompany.com"}},
                "attendees": [
                    {"email": "user@yourcompany.com"},
                    {"email": "partner@partnercompany.com"},
                ],
                "onlineMeeting": {"joinUrl": "https://teams.microsoft.com/meet/abc"},
            }
        ]

        response = self.client.get(
            self.api_url,
            {"token": self.token, "start_date": self.start_date, "end_date": self.end_date},
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("meetings", response.json())
        self.assertEqual(len(response.json()["meetings"]), 2)

    def test_serializer_output_format(self):
        """Test whether the serializer correctly formats meeting data."""
        sample_meeting = {
            "id": "test123",
            "summary": "Test Meeting",
            "description": "Agenda:\n- Discuss progress\n- Assign tasks",
            "start": {"dateTime": "2025-03-07T12:00:00Z"},
            "end": {"dateTime": "2025-03-07T13:00:00Z"},
            "organizer": {"emailAddress": {"address": "user@yourcompany.com"}},
            "attendees": [
                {"email": "user@yourcompany.com"},
                {"email": "client@example.com"},
            ],
            "hangoutLink": "https://meet.google.com/test",
        }

        serializer = MeetingSerializer(sample_meeting)
        formatted_data = serializer.data

        self.assertEqual(formatted_data["opportunity_name"], "example.com")
        self.assertIn("user@yourcompany.com", formatted_data["our_emails"])
        self.assertIn("client@example.com", formatted_data["others_emails"])
        self.assertTrue(formatted_data["is_multiple_domains"])
        self.assertEqual(formatted_data["title"], "Test Meeting")
        self.assertIn("- Discuss progress", formatted_data["description"])
