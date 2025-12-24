from datetime import datetime, timezone
import json
import boto3
import requests
import time
import os
import logging 
from botocore.exceptions import BotoCoreError, NoCredentialsError, PartialCredentialsError

#setting logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


GITHUB_EVENTS_URL = "https://api.github.com/events" # the GitHub API endpoint for public events
STREAM_NAME = "job-analytics-stream" # the name of the Kinesis stream
REGION = "eu-north-1" # AWS region
POLL_INTERVAL = 10 # seconds between polling GitHub API

#POLLING -- cheking the source repeatedly to check if something has changed or an event has occured

#setting up kinesis client
def create_kinesis_client():
    try:
        kinesis_client = boto3.client('kinesis', region_name = REGION) # Initialize Kinesis client to push records into kinesis securely
        return kinesis_client
    except (BotoCoreError, NoCredentialsError, PartialCredentialsError) as e:
        logging.error(f"Failed to create Kinesis client: {e}")
        raise

#Describing the stream like Shards, status, ShardId, SequesnceNumber etc
def Describe_stream(kinesis_client):
    try:
        response = kinesis_client.describe_stream(StreamName=STREAM_NAME)
        logging.info(f"Stream Description: {response}")
    except BotoCoreError as e:
        logging.error(f"Failed to describe Kinesis stream: {e}")
        raise


#fecth github details
def fetch_github_events():
    response = requests.get(GITHUB_EVENTS_URL, headers={"Accept": "application/vnd.github.v3+json"}) # Make a GET request to GitHub API to fetch public events
    response.raise_for_status() # Raise an error for bad responses
    return response.json() # Return the JSON response


def send_to_kinesis(event):
    response = kinesis_client.put_record(
        StreamName = STREAM_NAME,
        Data = json.dumps(event),
        PartitionKey = event.get("event_type", "UNKNOWN") # it will help to distribute the data across multiple shards based on event type example PushEvent, PullRequestEvent etc
    )
    return response

if __name__ == "__main__":
    print("Starting GitHub Event Producer...")
    kinesis_client = create_kinesis_client()
    Describe_stream(kinesis_client)
    while True:
        try:
            events = fetch_github_events()
            for event in events:
                enriched_event = {
                "event_id": event.get("id"),
                "event_type": event.get("type"),
                "repo_name": event.get("repo", {}).get("name"),
                "actor": event.get("actor", {}).get("login"),
                "created_at": event.get("created_at"),
                "ingestion_time": datetime.now(timezone.utc).isoformat()
            }
            event_id  = enriched_event["event_id"]
            response = send_to_kinesis(enriched_event)
            Shard_id = response['ShardId']
            sequesnce_number = response['SequenceNumber']
            logging.info(f"Event_id : {event_id} sent to Kinesis - ShardId: {Shard_id}, SequenceNumber: {sequesnce_number}")
    
        except Exception as e:
            print("Error:", e)

        time.sleep(POLL_INTERVAL)