import os
import json
import datetime
import isodate
from googleapiclient.discovery import build


class PlayList:
    api_key = os.environ.get('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.playlist = self.youtube.playlists().list(id=self.playlist_id, part='snippet', ).execute()
        self.title = self.playlist['items'][0]['snippet']['title']
        self.playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                                 part='snippet,contentDetails',
                                                                 maxResults=50,
                                                                 ).execute()
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                         id=','.join(self.video_ids)
                                                         ).execute()

    def print_info(self):
        print(json.dumps(self.playlist, indent=2, ensure_ascii=False))
        print(json.dumps(self.playlist_videos, indent=2, ensure_ascii=False))
        print(json.dumps(self.video_response, indent=2, ensure_ascii=False))

    @property
    def total_duration(self):
        """Возвращает объект класса с суммарной длительность плейлиста"""
        duration = datetime.timedelta()
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration += isodate.parse_duration(iso_8601_duration)
        return duration

    def show_best_video(self):
        """Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)"""
        likes = 0
        best_video = ''
        for video in self.video_response['items']:
            like_count = int(video['statistics']['likeCount'])
            if like_count > likes:
                best_video = video['id']
        return f'https://youtu.be/{best_video}'
