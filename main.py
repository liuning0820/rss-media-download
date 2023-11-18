# This is a sample Python script.
import feedparser

import requests
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import youtube_dl
import os
import webbrowser

import configparser

import platform

system_type = platform.system()


# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the configuration file
config.read('config.ini')

# Get values from the configuration file
download_path = config.get('Settings', 'DownloadPath')




def download_from_rss_feed(feed_url):
    media_urls = extract_urls_from_rss_feed(feed_url)
    for url in media_urls[1:3]:
        print(url)
        download_from_url(url)


def extract_urls_from_rss_feed(feed_url):
    """extract entries' urls from a feed url"""
    feed_entries = feedparser.parse(feed_url).entries
    return [entry.link for entry in feed_entries]


def download_from_url(url):
    if system_type == "Windows":
        print("当前系统是 Windows")
        os.chdir(r"Z:\TDDOWNLOAD")
    elif system_type == "Linux":
        print("当前系统是 Linux")
        os.chdir(download_path)
    elif system_type == "Darwin":
        print("当前系统是 macOS")
    else:
        print("未知系统")    

    # 下载视频和字幕
    os.system("youtube-dl -f mp4 --write-auto-sub --sub-lang zh-Hans --sub-format vtt --convert-subs srt " + url)
    os.system("youtube-dl -f mp4 --write-auto-sub --sub-lang zh-Hant --sub-format vtt --convert-subs srt " + url)
    os.system("youtube-dl -f mp4 --write-auto-sub --sub-lang en --sub-format vtt --convert-subs srt " + url)

    os.system("youtube-dl -f mp4 --write-auto-sub --sub-lang zh-Hans --sub-format vtt " + url)
    os.system("youtube-dl -f mp4 --write-auto-sub --sub-lang zh-Hant --sub-format vtt " + url)
    os.system("youtube-dl -f mp4 --write-auto-sub --sub-lang en --sub-format vtt " + url)


def multi_download_from_file(file):
    # 保存有youtube链接的文件
    with open(file, 'r', encoding="utf8") as f:
        all_urls = f.readlines()
    print(len(all_urls))
    count = 1
    for url in all_urls:
        print('开始下载第{}个'.format(count))

        # os.system("youtube-dl --write-auto-sub \
        # --sub-lang es --write-auto-sub  -f m4a " + url)

        download_from_url(url)

        print('第{}个下载完成,已完成{:.3f}'.format(count, count / len(all_urls)))
        count += 1


def multi_download_from_rss_feed_file(file):
    # 保存有rss feed链接的文件
    with open(file, 'r', encoding="utf8") as f:
        all_feed_urls = f.readlines()
    print(len(all_feed_urls))
    count = 1
    for feed_url in all_feed_urls:
        print('开始下载第{}个'.format(count))
        print(feed_url)
        download_from_rss_feed(feed_url)

        print('第{}个下载完成,已完成{:.3f}'.format(count, count / len(all_feed_urls)))
        count += 1


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # download_from_rss_feed("https://www.youtube.com/feeds/videos.xml?channel_id=UCs_tLP3AiwYKwdUHpltJPuA")
    # multi_download_from_file("url.txt")
    multi_download_from_rss_feed_file("feeds.txt")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
