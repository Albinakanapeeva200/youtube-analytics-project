import os
import json
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id

        self.response = self.get_service().channels().list(
            id=self.channel_id,
            part='snippet,statistics').execute()

        self.title = self.response['items'][0]['snippet']['title']
        self.description = self.response['items'][0]['snippet']['description']
        self.url = self.response['items'][0]['snippet']['thumbnails']['default']['url']
        self.subscriber_count = self.response['items'][0]['statistics']['subscriberCount']
        self.video_count = self.response['items'][0]['statistics']['videoCount']
        self.view_count = self.response['items'][0]['statistics']['viewCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.response, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """Возвращающает объект для работы с YouTube API"""
        api_key = os.environ.get('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def to_json(self, filename):
        """Сохраняет в файл значения атрибутов экземпляра Channel"""
        to_json = {
            'channel_id': self.channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count
        }

        with open(filename, 'w') as file:
            file.write(json.dumps(to_json, indent=2, ensure_ascii=False))
