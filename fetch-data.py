import requests
import json
from datetime import datetime
from textblob import TextBlob  # For sentiment analysis

# Assuming Grok's API endpoint for real-time queries
GROK_API_ENDPOINT = "https://api.grok.ai/v1/realtime_query"

# Headers might include your API key or authentication token
headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}

# Sample request body for querying Nvidia related tweets in real-time
query_data = {
    "query": "Nvidia",
    "use_realtime": True,  # Flag to indicate we want real-time data
    "max_results": 20,  # Fetch more posts initially to sort and select top 5
    "fields": ["user", "time", "message", "link", "likes"]  # Add 'likes' to the fields
}

def fetch_realtime_tweets(query_data):
    try:
        response = requests.post(GROK_API_ENDPOINT, headers=headers, json=query_data)
        response.raise_for_status()  # This will raise an exception for bad status codes
        return response.json()
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def generate_rank(message):
    # Simple sentiment analysis using TextBlob
    blob = TextBlob(message)
    sentiment = blob.sentiment.polarity  # This gives a score from -1 to 1
    
    # Mapping sentiment score to our rank system
    if sentiment < -0.5:
        return "1"  # Very Bad News
    elif -0.5 <= sentiment < -0.1:
        return "2"  # Bad News
    elif -0.1 <= sentiment <= 0.1:
        return "3"  # Neutral
    elif 0.1 < sentiment <= 0.5:
        return "4"  # Good News
    else:
        return "5"  # Very Good News

# Fetch real-time tweets
result = fetch_realtime_tweets(query_data)

if result:
    # Sort tweets by likes in descending order, then take the top 5
    sorted_tweets = sorted(result.get('data', []), key=lambda x: x.get('likes', 0), reverse=True)[:5]
    
    # Convert the result into the desired JSON format with rank generation
    formatted_tweets = []
    
    for tweet in sorted_tweets:  # Use sorted tweets instead of all results
        formatted_tweets.append({
            "User": tweet.get('user', ''),
            "Time": tweet.get('time', ''),
            "Message": tweet.get('message', ''),
            "Rank": generate_rank(tweet.get('message', '')),  # Generate the rank
            "Link": tweet.get('link', ''),
            "Likes": tweet.get('likes', 0)  # Add likes to the output
        })

    # Create the JSON structure
    json_output = json.dumps(formatted_tweets, indent=2)
    print(json_output)
else:
    print("Failed to fetch tweets.")
