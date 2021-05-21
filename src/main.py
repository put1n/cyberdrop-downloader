import sys
import asyncio

from cyberdrop_downloader import CyberDropDownloader


if __name__ == '__main__':
    downloader = CyberDropDownloader(sys.argv[1])

    try:
        asyncio.run(downloader.run())
    except KeyboardInterrupt:
        pass
