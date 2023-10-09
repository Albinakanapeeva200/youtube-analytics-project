from googleapiclient.discovery import build
import os

api_key = os.environ.get('API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Video:

    def __init__(self, video_id):
        """Инициализирует реальными данными атрибуты"""
        self.video_id = video_id
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_id
                                               ).execute()
        self.video_title = video_response['items'][0]['snippet']['title']
        self.video_url = video_response['items'][0]['snippet']['thumbnails']['default']['url']
        self.view_count = video_response['items'][0]['statistics']['viewCount']
        self.like_count = video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return self.video_title


class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        """Инициализирует 'id плейлиста'"""
        super().__init__(video_id)
        self.playlist_id = playlist_id
