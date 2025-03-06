from rest_framework import serializers


class CalendarRequestSerializer(serializers.Serializer):

    """
    Serializer to validate and parse request data for fetching calendar meetings.

    Fields:
        - token (str): Required. The authentication token for accessing the calendar API.
        - is_google (bool): Optional. If True, fetch meetings from Google Calendar.
        - is_outlook (bool): Optional. If True, fetch meetings from Microsoft Outlook Calendar.
        - start_date (datetime): Optional. The start date/time filter for fetching meetings.
        - end_date (datetime): Optional. The end date/time filter for fetching meetings.
    
    Notes:
        - `start_date` and `end_date` follow the format: YYYY-MM-DDTHH:MM:SSZ (ISO 8601).
        - If `start_date` and `end_date` are not provided, all available meetings are fetched.
        - At least one of `is_google` or `is_outlook` should be True; otherwise, the API should return an error.
    """

    outlook_token = serializers.CharField(required=False)
    google_token = serializers.CharField(required=False)
    is_google = serializers.BooleanField(required=False, default=False)
    is_outlook = serializers.BooleanField(required=False, default=False)
    start_date = serializers.DateTimeField(required=False, format="%Y-%m-%dT%H:%M:%SZ", allow_null=True)
    end_date = serializers.DateTimeField(required=False, format="%Y-%m-%dT%H:%M:%SZ", allow_null=True)