import os
#import time
import requests
#from selenium.webdriver.chrome.options import Options
from datetime import date
from downloader.api import Api
from downloader.utils import client_id, client_secret

api = Api()
api.auth(client_id, client_secret)

class Content:
    def __init__(self, url, broadcaster_id, broadcaster_name, game_id, title, thumbnail_url, duration, path):
        self.url = url
        self.broadcaster_id = broadcaster_id
        self.broadcaster_name = broadcaster_name
        self.game_id = game_id
        self.title = title
        self.thumbnail_url = thumbnail_url
        self.duration = duration
        self.path = path
    
    def __str__(self):
        return f'''url: {self.url}\n
        broadcaster_id: {self.broadcaster_id}\n
        broadcaster_name: {self.broadcaster_name}\n
        game_id: {self.game_id}\n
        title: {self.title}\n
        thumbnail_url: {self.thumbnail_url}'''

class Collector:
    def __init__(self):
        self.clips_content = []
        self.by_game = None

    # 293 is from reference
    def get_clips(self, quantity = 293, broadcaster_id = None, game_id = None, languages = []):
        self.by_game = True if game_id else False
        self.languages = languages
        params = {
            'broadcaster_id' : broadcaster_id,
            'game_id' : game_id,
            'first' : quantity,
            'started_at' : date.fromisoformat(2015-12-31),
            'ended_at' : date.fromisoformat(2024-12-31),
            'after' : None
        }

        while len(self.clips_content) < quantity:
            response = requests.get('https://api.twitch.tv/helix/clips', params=params, headers=api.headers).json()
            for clip in response['data']:
                self.clips_content.append(Content(
                    clip['url'],
                    clip['broadcaster_id'],
                    clip['broadcaster_name'],
                    clip['game_id'],
                    clip['title'],
                    clip['thumbnail_url'],
                    clip['duration'],
                    f'files/clips/{clip["title"].replace(" ", "_").replace("/","_").lower()}.mp4'
                ))
                if len(self.clips_content) == quantity: break
            params['after'] = response['pagination']['cursor']

class Downloader():
    def __init__(self):
        pass

    '''
    def download_clip_driver(self, clip):
        option = Options()
        option.headless = True
        driver = webdriver.Chrome(options=option)
        driver.get(clip.url)

        time.sleep(1)

        clip_url = driver.find_element("xpath", "//div[@class='Layout-sc-1xcs6mc-0 video-ref']//video").get_property("src")
        driver.quit()

        r = requests.get(clip_url)

        if r.headers['Content-Type'] == 'binary/octet-stream' or r.headers['Content-Type'] == 'video/mp4':
            if not os.path.exists('files/clips'):
                os.makedirs('files/clips')

            with open(clip.path, 'wb') as f:
                f.write(r.content)
        else:
            print(f'failure while downloading clip: {clip.thumbnail_url}')
    '''
    def download_clip_thumbnail(clip):
        index = clip.thumbnail_url.find('-preview')
        clip_url = clip.thumbnail_url[:index] + '.mp4'

        r = requests.get(clip_url)

        if r.headers['Content-Type'] == 'binary/octet-stream':
            if not os.path.exists('files/clips'): os.makedirs('files/clips')
            with open(clip.path, 'wb') as f:
                f.write(r.content)

        else:
            print(f'failure while downloading clip: {clip.thumbnail_url}')

    def download_thumbnail(self, clip):
        r = requests.get(clip.thumbnail_url)
        if not os.path.exists('files/thumbnails'): os.makedirs('files/thumbnails')
        try:
            with open(f'files/thumbnails/{clip.title.replace(" ", "_").replace("/","_").lower()}.jpg', 'wb') as f:
                f.write(r.content)
        except:
            print(f'Failed to download thumbnail: {clip.thumbnail_url}')

    def download_top_clips(self, clips):
        for i in range(len(clips)):
            print(f'Downloading clip {i+1}/{len(clips)}')
            clip = clips[i]
            if clip.thumbnail_url.find('clips-media-assets2.twitch.tv') != -1:
                self.download_clip_thumbnail(clip)
                self.download_thumbnail(clip)
            