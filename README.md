# Meeting Aggregator API

This project provides an API to aggregate meetings from Google Calendar and Microsoft Outlook within a given date range. It authenticates using a calendar token and returns structured meeting details.

## Features
- Fetch meetings from Google Calendar and Microsoft Outlook.
- Authenticate using OAuth tokens.
- Filter meetings based on start and end dates.
- Retrieve structured meeting details including title, description, attendees, and meeting links.
- Dockerized for easy deployment.

## Prerequisites
- Python 3.11+
- pip (Python package manager)
- Docker (if running with a container)
- OAuth credentials for Google and Microsoft Calendar API access

## Project Structure
```
meeting_aggregator/
│── meeting_config/       # Django project configuration
│── meeting/         # Django app for calendar integration
│── Dockerfile            # Docker configuration
│── Makefile              # Makefile for building and running the project
│── requirements.txt      # Python dependencies
│── README.md             # Project documentation
```

## Setup Instructions

### 1. Clone the Repository
```sh
git clone https://github.com/your-repo/meeting-aggregator.git
cd meeting-aggregator
```

### 2. Install Dependencies
```sh
pip install -r requirements.txt
```

### 3. Run the Project (Without Docker)
```sh
python meeting_config/manage.py runserver 0.0.0.0:8000
```

### 4. Run with Docker
```sh
docker build -t meeting-aggregator .
docker run -p 8000:8000 meeting-aggregator
```

## API Usage

### Endpoint: Fetch Meetings
**URL:** `/api/meetings/`  
**Method:** `POST`  

### Request Parameters:
| Parameter       | Type    | Required | Description |
|---------------|--------|----------|-------------|
| `outlook_token` | string  | No  | Outlook API token for fetching meetings. |
| `google_token`  | string  | No  | Google API token for fetching meetings. |
| `is_outlook`    | boolean | No  | If `true`, fetch meetings from Outlook Calendar. |
| `is_google`     | boolean | No  | If `true`, fetch meetings from Google Calendar. |
| `start_date`    | string  | No  | (Optional) Fetch meetings from this date (`YYYY-MM-DDTHH:MM:SSZ`). |
| `end_date`      | string  | No  | (Optional) Fetch meetings until this date (`YYYY-MM-DDTHH:MM:SSZ`). |

### Example Requests:

#### Fetch all meetings from both calendars
```json
{
  "outlook_token": "your_outlook_token",
  "google_token": "your_google_token",
  "is_outlook": true,
  "is_google": true
}

#### Fetch only Outlook meetings for a date range

{
  "outlook_token": "your_outlook_token",
  "is_outlook": true,
  "start_date": "2025-03-01T00:00:00Z",
  "end_date": "2025-03-05T23:59:59Z"
}
#### Fetch only Google meetings

{
  "google_token": "your_google_token",
  "is_google": true
}


## Assumptions
- The database setup is already completed.
- OAuth tokens are valid and provide necessary permissions.
- The API endpoints are integrated with external authentication mechanisms.

## Testing the API
You can test the API using `curl`, Postman, or any API testing tool.

```sh
curl -X POST http://127.0.0.1:8000/api/meetings/ -H "Content-Type: application/json" -d '{
    "token": "your-oauth-token",
    "is_google": true,
    "is_outlook": true,
    "start_date": "2024-03-01T00:00:00Z",
    "end_date": "2024-03-10T23:59:59Z"
}'
```

---

Happy Coding! 🚀
