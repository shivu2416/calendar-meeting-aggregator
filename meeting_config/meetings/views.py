from rest_framework.response import Response
from rest_framework import status, viewsets

from .utils import fetch_meetings

from .serializers import CalendarRequestSerializer


class CalendarMeetingViewSet(viewsets.ViewSet):
    """
    A ViewSet to handle fetching calendar meetings from Google Calendar and Outlook.

    This endpoint accepts a request with an authentication token and optional filters 
    such as `start_date`, `end_date`, `is_google`, and `is_outlook`.

    Workflow:
        - Validate request data using CalendarRequestSerializer.
        - Based on `is_google` and `is_outlook`, fetch meetings from respective calendars.
        - Return a consolidated list of meetings.

    Expected Request Body:
    {
        "token": "your_auth_token",
        "is_google": true,
        "is_outlook": false,
        "start_date": "2025-03-06T00:00:00Z",
        "end_date": "2025-03-07T23:59:59Z"
    }

    Notes:
        - If both `is_google` and `is_outlook` are false/missing, no meetings will be fetched.
        - If `start_date` and `end_date` are omitted, all available meetings will be returned.
    """

    def create(self, request):
        """
            Handle POST request to fetch meetings from Google Calendar and/or Outlook.

            Steps:
            1. Validate request data using the serializer.
            2. Extract `token`, `start_date`, `end_date`, `is_google`, and `is_outlook` from validated data.
            3. Fetch meetings from Google Calendar if `is_google` is True.
            4. Fetch meetings from Outlook if `is_outlook` is True.
            5. Merge and return the meeting data.

            Returns:
                - HTTP 200: Successfully retrieved meetings.
                - HTTP 400: Invalid request data.
        """
        serializer = CalendarRequestSerializer(data=request.data)
        if serializer.is_valid():
            outlook_token = serializer.validated_data.get("outlook_token", None)
            google_token = serializer.validated_data.get("google_token", None)
            start_date = serializer.validated_data.get("start_date")
            end_date = serializer.validated_data.get("end_date")
            is_google = serializer.validated_data.get("is_google", False)
            is_outlook = serializer.validated_data.get("is_outlook", False)
            breakpoint()
            meetings = []
            if is_google and google_token:
                meetings.extend(fetch_meetings(google_token, "google", start_date, end_date))
            if is_outlook and outlook_token:
                meetings.extend(fetch_meetings(outlook_token, "outlook", start_date, end_date))

            return Response(meetings, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
