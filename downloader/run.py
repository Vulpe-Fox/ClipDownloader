from downloader.clips import Collector, Downloader

class Run:
    def __init__(self):
        self.collector = Collector()
        self.downloader = Downloader()

    def run(self, amount):
        # get clips
        self.collector.get_clips(quantity = amount)
        clips = self.collector.clips_content

        # download clips
        self.downloader.download_top_clips(clips)