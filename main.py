import os
import sys
import platform
from urllib.parse import urlparse

import feedparser
from datetime import datetime, timedelta, date, timezone

import yt_dlp
from dateutil import parser
import requests
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import configparser

system_type = platform.system()

# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the configuration file
config.read('config.ini')

# Get values from the configuration file
download_path = '/media/'+os.getlogin + config.get('Settings', 'DownloadPath')

print(sys.path)

def download_from_rss_feed(feed_url):
    media_urls = extract_urls_from_rss_feed(feed_url)
    print("media Count:{0}".format(len(media_urls)))
    for url in media_urls:
        print(url)
        download_directory = download_path
        download_video_with_subtitles(url, download_directory)


def extract_urls_from_rss_feed(feed_url):
    """extract entries' urls from a feed url published within 24 hours"""
    feed_entries = feedparser.parse(feed_url).entries
    return [entry.link for entry in feed_entries if is_within_7_days(parser.parse(entry.published))]


def is_within_24_hours(dt):
    # Get the current datetime
    current_datetime = datetime.now()

    dt = dt.replace(tzinfo=None)

    # Calculate the difference between the current time and the provided datetime
    time_difference = current_datetime - dt

    # Check if the difference is less than 24 hours
    return time_difference < timedelta(hours=24)


def is_within_7_days(dt):
    # Get the current datetime
    current_datetime = datetime.now()

    dt = dt.replace(tzinfo=None)

    # Calculate the difference between the current time and the provided datetime
    time_difference = current_datetime - dt

    # Check if the difference is less than 7 days
    return time_difference < timedelta(days=7)


def set_download_target_folder():
    if system_type == "Windows":
        print("当前系统是 Windows")
        # os.chdir(r"Z:\TDDOWNLOAD")
        return r"Z:\TDDOWNLOAD"
    elif system_type == "Linux":
        print("当前系统是 Linux")
        # os.chdir(download_path)
        return download_path
    elif system_type == "Darwin":
        print("当前系统是 macOS")
        return download_path
    else:
        print("未知系统")
        return download_path


def extract_domain(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc

def get_available_formats(video_url: str) -> list:
    options = {
        'format': 'mp4',  # You can specify the desired format here
        'quiet': True,      # Suppress output
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(video_url, download=False)
        formats = info.get('formats', [])

        available_formats = []
        audio_only_format = ''
        video_only_format = ''
        for fmt in formats:
            if fmt.get('audio_ext') != 'none' and fmt.get('video_ext') != 'none':
                format_code = fmt.get('format_id')
                available_formats.append(format_code)
            if fmt.get('audio_ext') == 'none' and fmt.get('video_ext') != 'none':
                audio_only_format = fmt.get('format_id')
            if fmt.get('audio_ext') != 'none' and fmt.get('video_ext') == 'none':
                video_only_format = fmt.get('format_id')

        if audio_only_format != '' and video_only_format != '':
            available_formats.append(audio_only_format+'+' + video_only_format)
        return available_formats


def download_video_with_subtitles(video_url, download_directory):
    # youtube-dl 下载视频和字幕
    # os.system("youtube-dl -f mp4 --write-auto-sub --sub-lang zh-Hans --sub-format vtt --convert-subs srt -o " +  download_directory +"/%(title)s.%(ext)s " + video_url)
    # os.system("youtube-dl -f mp4 --write-auto-sub --sub-lang zh-Hant --sub-format vtt --convert-subs srt -o " +  download_directory +"/%(title)s.%(ext)s " + video_url)
    # os.system("youtube-dl -f mp4 --write-auto-sub --sub-lang en --sub-format vtt --convert-subs srt -o " +  download_directory +"/%(title)s.%(ext)s " + video_url)

    # yt-dlp 下载视频和字幕
    # Download the best mp4 video available, or the best video if no mp4 available
    # print(extract_domain(video_url))

    if extract_domain(video_url) == 'www.bilibili.com':
        available_formats = set(get_available_formats(video_url))
        # prefer_formats = set(['30031','30032','30033'])
        # intersection_set = available_formats.intersection(prefer_formats)

        result_list = list(available_formats)
        if len(result_list) > 0:
            print(result_list[0])
            os.system(
            'yt-dlp -f '+ result_list[0] + ' --write-auto-sub --sub-lang "zh.*,en.*" --sub-format vtt --convert-subs srt -o "' + download_directory + '/%(title)s.%(ext)s" ' + video_url)
    else:
        os.system(
            'yt-dlp -f "b[ext=mp4]" --write-auto-sub --sub-lang "zh.*,en.*" --sub-format vtt --convert-subs srt -o "' + download_directory + '/%(title)s.%(ext)s" ' + video_url)

    # yt-dlp module 下载视频和字幕
    # options = {
    #     'format': 'mp4',
    #     'writeautomaticsub': True,  # 下载字幕
    #     'subtitleslangs': ['en.*','zh.*'],  # 字幕语言代码，可以根据需要更改
    # }
    #
    # with yt_dlp.YoutubeDL(options) as ydl:
    #     ydl.download([video_url])


def multi_download_from_file(file):
    # 保存有youtube链接的文件
    with open(file, 'r', encoding="utf8") as f:
        all_urls = f.readlines()
    print(len(all_urls))
    count = 1
    for url in all_urls:
        print('开始下载第{}个'.format(count))

        download_directory = download_path
        download_video_with_subtitles(url, download_directory)

        print('第{}个下载完成,已完成{:.3f}'.format(count, count / len(all_urls)))
        count += 1


def multi_download_from_rss_feed_file(file):
    # 保存有rss feed链接的文件
    with open(file, 'r', encoding="utf8") as f:
        all_feed_lines = f.readlines()
    print(len(all_feed_lines))
    count = 1
    for feed_line in all_feed_lines:
        print('开始下载第{}个'.format(count))
        print(feed_line.strip())
        if feed_line.strip():
            feed_url = feed_line.split("|")[1]
            print(feed_url)
            download_from_rss_feed(feed_url)

        print('第{}个下载完成,已完成{:.3f}'.format(count, count / len(all_feed_lines)))
        count += 1


def clean_directory(directory_path):
    # Get the current date and time
    current_time = datetime.now()

    # Calculate the time threshold (7 days ago)
    threshold_time = current_time - timedelta(days=7)

    # Walk through the directory
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            # Get the file creation time
            creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
            # print("created time "+ creation_time.strftime('%Y-%m-%d'))
            # Compare with the threshold time
            if creation_time < threshold_time:
                # Uncomment the line below to print the files that will be deleted
                encoded_file_path = file_path.encode('utf-8')
                print(f"Deleting: {encoded_file_path}")
                os.remove(encoded_file_path)
                print(f"Deleted: {encoded_file_path}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    download_path = set_download_target_folder()
    # remove files elder than 30 days
    clean_directory(download_path)
    default_urls_list_file_path = "urls_bilibili.txt"
    default_feed_url_list_file_path = "feeds_bilibili.txt"
    print(len(sys.argv))
    if len(sys.argv) > 1:
        default_urls_list_file_path = sys.argv[1]
    if len(sys.argv) > 2:
        default_feed_url_list_file_path = sys.argv[2]
    print(default_urls_list_file_path)
    multi_download_from_file(default_urls_list_file_path)
    multi_download_from_rss_feed_file(default_feed_url_list_file_path)

