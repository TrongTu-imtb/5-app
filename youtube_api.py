from googleapiclient.discovery import build

def search_videos(api_key, query, max_results=5):
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.search().list(
        q=query,
        part='snippet',
        type='video',
        maxResults=max_results
    )
    response = request.execute()
    return [(item['id']['videoId'], item['snippet']['title']) for item in response['items']]

def get_comments(api_key, video_id, max_comments=100):
    youtube = build('youtube', 'v3', developerKey=api_key)
    comments = []
    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=100,
        textFormat='plainText'
    )
    response = request.execute()
    for item in response.get("items", []):
        comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        comments.append(comment)
        if len(comments) >= max_comments:
            break
    return comments