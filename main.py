from downloader.run import Run
import argparse

class TwitchClipDownloader:
    def __init__(self):
        pass

    def parse_and_run_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-a', '--amount', help='Amount of clips', required=True)
        args = parser.parse_args()

        app = Run()
        app.run(int(args.amount))
    
if __name__ == '__main__':
    main = TwitchClipDownloader()
    main.parse_and_run_args()