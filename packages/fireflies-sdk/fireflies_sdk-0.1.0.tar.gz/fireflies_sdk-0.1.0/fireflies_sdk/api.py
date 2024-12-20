import requests
from datetime import datetime
import json
import os
from dotenv import load_dotenv
from typing import Dict, Optional, Any, Union, List

class FirefliesAPI:
    """SDK for interacting with Fireflies.ai API"""
    
    def __init__(self, api_key: str = None):
        """Initialize the Fireflies API client.
        
        Args:
            api_key (str, optional): Fireflies API key. If not provided, will try to load from environment.
        """
        # Only try to load .env file if it exists (for local development)
        if os.path.exists(".env"):
            load_dotenv()
            
        self.api_key = api_key or os.getenv("FIREFLIES_API_KEY")
        if not self.api_key:
            raise ValueError("API key not provided and not found in environment")
            
        self.api_url = "https://api.fireflies.ai/graphql"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def join_meeting(self, duration: int = 120, name: Optional[str] = None, url: Optional[str] = None) -> Dict[str, Any]:
        """Join a meeting
        
        Args:
            duration: Meeting duration in minutes
            name: Name for the bot
            url: Meeting URL to join
            
        Returns:
            Dict containing meeting info (id, title, date, url, status)
        """
        if url:
            query = """
            mutation AddToLiveMeeting($meetingLink: String!) {
                addToLiveMeeting(meeting_link: $meetingLink) {
                    success
                    message
                }
            }
            """
            variables = {"meetingLink": url}
        else:
            query = """
            mutation JoinBot($duration: Int!, $name: String) {
                joinBot(duration: $duration, name: $name) {
                    success
                    message
                }
            }
            """
            variables = {
                "duration": duration,
                "name": name
            }
        
        response = self._make_request(query, variables)
        data = response.get("data", {})
        result = data.get("addToLiveMeeting" if url else "joinBot", {})
        
        if not result.get("success"):
            raise Exception(result.get("message", "Failed to join meeting"))
            
        return result

    def get_video_url(self, transcript_id: str) -> Dict[str, str]:
        """Get video URL for a transcript
        
        Args:
            transcript_id: ID of the transcript
            
        Returns:
            Dict containing title and video_url
        """
        query = """
        query GetVideoUrl($transcriptId: String!) {
            transcript(id: $transcriptId) {
                id
                title
                video_url
            }
        }
        """
        variables = {"transcriptId": transcript_id}
        
        response = self._make_request(query, variables)
        data = response.get("data", {}).get("transcript", {})
        
        if not data or not data.get("video_url"):
            raise Exception("No video URL available for this transcript")
            
        return {
            "title": data.get("title", "Unknown"),
            "video_url": data["video_url"]
        }

    def list_transcripts(self, limit: int = 10) -> list:
        """List recent transcripts
        
        Args:
            limit: Maximum number of transcripts to return
            
        Returns:
            List of transcript objects
        """
        query = """
        query GetTranscripts($limit: Int!) {
            transcripts(limit: $limit) {
                id
                title
                date
            }
        }
        """
        variables = {"limit": limit}
        
        response = self._make_request(query, variables)
        return response.get("data", {}).get("transcripts", [])

    def delete_transcript(self, transcript_id: str) -> bool:
        """Delete a transcript
        
        Args:
            transcript_id: ID of the transcript to delete
            
        Returns:
            True if successful
        """
        query = """
        mutation DeleteTranscript($transcriptId: String!) {
            deleteTranscript(id: $transcriptId) {
                success
                message
            }
        }
        """
        variables = {"transcriptId": transcript_id}
        
        response = self._make_request(query, variables)
        result = response.get("data", {}).get("deleteTranscript", {})
        
        if not result.get("success"):
            raise Exception(result.get("message", "Failed to delete transcript"))
            
        return True

    def download_video(self, transcript_id: str, output_path: Optional[str] = None) -> str:
        """Download video for a transcript
        
        Args:
            transcript_id: ID of the transcript
            output_path: Path to save the video. If not provided, will use title_id.mp4
            
        Returns:
            Path to the downloaded video file
        """
        video_info = self.get_video_url(transcript_id)
        title = video_info["title"]
        video_url = video_info["video_url"]
        
        if not output_path:
            safe_title = "".join([c if c.isalnum() or c in (' ', '-', '_') else '_' for c in title]).rstrip()
            output_path = f"{safe_title}_{transcript_id}.mp4"
        
        response = requests.get(video_url, stream=True)
        response.raise_for_status()
        
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return output_path

    def get_transcript_text(self, transcript_id: str) -> Dict[str, Any]:
        """Get full transcript text and metadata
        
        Args:
            transcript_id: ID of the transcript
            
        Returns:
            Dict containing transcript info and sentences
        """
        query = """
        query GetTranscript($transcriptId: String!) {
            transcript(id: $transcriptId) {
                id
                title
                sentences {
                    text
                    speaker_name
                    start_time
                    end_time
                }
            }
        }
        """
        variables = {"transcriptId": transcript_id}
        
        response = self._make_request(query, variables)
        data = response.get("data", {}).get("transcript")
        if not data:
            raise Exception("Failed to get transcript")
            
        return data

    def get_participants(self, transcript_id: str) -> List[str]:
        """Get list of participants in a meeting
        
        Args:
            transcript_id: ID of the transcript
            
        Returns:
            List of participant names
        """
        query = """
        query GetMeetingParticipants($transcriptId: String!) {
            transcript(id: $transcriptId) {
                participants
                sentences {
                    speaker_name
                }
            }
        }
        """
        variables = {"transcriptId": transcript_id}
        
        response = self._make_request(query, variables)
        data = response.get("data", {}).get("transcript", {})
        participants = set()
        
        # Get listed participants
        if data.get("participants"):
            # Split any comma-separated lists and add individual emails
            for p in data["participants"]:
                if "," in p:
                    participants.update(email.strip() for email in p.split(","))
                else:
                    participants.add(p)
        
        # Get speakers from transcript
        if data.get("sentences"):
            for sentence in data["sentences"]:
                if sentence.get("speaker_name"):
                    participants.add(sentence["speaker_name"])
        
        # Clean up the names/emails
        cleaned_participants = set()
        for p in participants:
            # Extract name from email if it's an email
            if "@" in p:
                name = p.split("@")[0].replace(".", " ").title()
                cleaned_participants.add(name)
            else:
                cleaned_participants.add(p)
        
        return sorted(cleaned_participants)

    def _make_request(self, query: str, variables: Dict[str, Any]) -> Dict[str, Any]:
        """Make a GraphQL request to the Fireflies API
        
        Args:
            query: GraphQL query string
            variables: Query variables
            
        Returns:
            Response data
        """
        response = requests.post(
            self.api_url,
            json={"query": query, "variables": variables},
            headers=self.headers
        )
        
        result = response.json()
        
        if "errors" in result:
            raise Exception(f"API request failed: {json.dumps(result)}")
            
        return result
