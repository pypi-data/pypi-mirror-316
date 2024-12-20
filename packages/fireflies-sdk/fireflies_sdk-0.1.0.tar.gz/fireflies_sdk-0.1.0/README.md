# Fireflies SDK

Python SDK for interacting with the Fireflies.ai API. This package provides a simple interface for accessing Fireflies.ai functionality programmatically.

## Installation

```bash
pip install fireflies-sdk
```

## Usage

```python
from fireflies_sdk import FirefliesAPI

# Initialize with your API key
api = FirefliesAPI("your-api-key")

# Join a meeting
result = api.join_meeting(url="https://meet.google.com/xxx-yyyy-zzz")

# Get video URL for a transcript
video_info = api.get_video_url("transcript-id")
print(video_info["title"])
print(video_info["video_url"])
```

## Features

- Join meetings
- Get video URLs
- Download meeting recordings
- List transcripts
- Delete transcripts

## For AWS Lambda

This SDK is designed to be Lambda-friendly. Here's an example Lambda function:

```python
from fireflies_sdk import FirefliesAPI
import os

def lambda_handler(event, context):
    api = FirefliesAPI(os.environ["FIREFLIES_API_KEY"])
    
    transcript_id = event.get("transcript_id")
    try:
        result = api.get_video_url(transcript_id)
        return {
            "statusCode": 200,
            "body": result
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }
```
