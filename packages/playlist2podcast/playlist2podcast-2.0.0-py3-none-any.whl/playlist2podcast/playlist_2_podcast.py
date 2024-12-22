"""Main / Overall logic for downloading videos of a Youtube playlist,
converting to MP3 and creating a podcast ATOM feed.

playlist2podcast - create podcast feed from a playlist URL
Copyright (C) 2021 - 2022  Mark S Burgunder

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import json
import re
import sys
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import msgspec
import requests
import typer
from feedgen.feed import FeedEntry
from feedgen.feed import FeedGenerator
from loguru import logger as log
from PIL import Image
from typing_extensions import Annotated
from yt_dlp import YoutubeDL

from playlist2podcast import __display_name__
from playlist2podcast import __version__

log.catch()


class IgnoringLogger:
    """Logger class that ignores all logging silently."""

    def debug(self, msg):
        """Process debug log messages."""
        # For compatibility with youtube-dl, both debug and info are passed into debug
        # You can distinguish them by the prefix '[debug] '
        if msg.startswith("[debug] "):
            pass
        else:
            self.info(msg)

    def info(self, msg):
        """Process info log messages."""
        pass

    def warning(self, msg):
        """Process warning log messages."""
        pass

    def error(self, msg):
        """Process error log messages."""
        pass


YDL_DL_OPTS = {
    "quiet": "true",
    "ignoreerrors": "true",
    "logger": IgnoringLogger(),
    "format": "bestaudio/best",
    "outtmpl": "publish/media/%(id)s.%(ext)s",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "opus",
        }
    ],
}


class PlayList(msgspec.Struct):
    """Definition of a playlist."""

    url: str
    include: List[str] = msgspec.field(default_factory=list)
    exclude: List[str] = msgspec.field(default_factory=list)


class Config(msgspec.Struct):
    """Attributes that make up the Configuration."""

    version: str
    podcast_host: str
    publish_dir: str = "publish"
    media_dir: str = "media"
    number_of_episodes: int = 5
    log_level: str = "INFO"
    youtube_cookie_file: Optional[str] = None
    play_lists: list[PlayList] = msgspec.field(default_factory=list)


def start_main() -> None:
    """Start main processing."""
    typer.run(main)


def main(  # nocl
    config_file: Annotated[
        Path,
        typer.Option(
            "--config-file",
            "-c",
            help="Path of configuration file",
            file_okay=True,
            dir_okay=False,
            readable=True,
            resolve_path=True,
        ),
    ] = Path("config.toml"),
    logging_config: Annotated[
        Optional[Path],
        typer.Option(
            "--logging-config",
            "-l",
            help="Path of filename that defines logging",
            file_okay=True,
            dir_okay=False,
            readable=True,
            resolve_path=True,
        ),
    ] = None,
    publish_dir: Annotated[
        Optional[Path],
        typer.Option(
            "--publish-dir",
            "-p",
            help="Directory to save feed.rss and media to. Overrides setting config file",
            file_okay=False,
            dir_okay=True,
            writable=True,
            resolve_path=True,
        ),
    ] = None,
) -> None:
    """Create Podcast feed from Youtube Playlist."""
    with config_file.open(mode="rb") as file:
        config = msgspec.toml.decode(file.read(), type=Config)
    setup_logging(logging_config)
    log.opt(colors=True).info(
        f"<cyan>Welcome to</cyan> <green><bold>{__display_name__}</bold></green> "
        f"<cyan>version</cyan> <yellow>{__version__}</yellow>"
    )

    if publish_dir:
        config.publish_dir = str(publish_dir)

    if not (Path(config.publish_dir) / Path(config.media_dir)).exists():
        (Path(config.publish_dir) / Path(config.media_dir)).mkdir(parents=True)

    downloader = setup_downloader(config)
    feed = create_feed(config)

    for current_play_list in config.play_lists:
        log.opt(colors=True).info(
            f"<cyan>Downloading info for videos on playlist:</cyan> <bold><red>{current_play_list.url}</red></bold>"
        )
        download_info = downloader.extract_info(url=current_play_list.url, download=False)
        log.debug(f"main() - download_info = {json.dumps(download_info, indent=4)}")
        videos_list = download_info["entries"]

        videos_to_download = determine_videos_to_download(current_play_list, videos_list)

        add_episodes(config, downloader, feed, videos_to_download)

    feed.rss_file(filename=f"{config.publish_dir}/feed.rss", extensions=True, pretty=True, xml_declaration=True)


def determine_videos_to_download(current_play_list, videos_list) -> List[Any]:
    """Determine list of videos to download."""
    videos_to_download = []
    for video in videos_list:
        if video and is_video_included(
            video_title=video["title"],
            video_original_url=video["original_url"],
            include_filters=current_play_list.include,
            exclude_filters=current_play_list.exclude,
        ):
            videos_to_download.append(video)
    return videos_to_download


def setup_downloader(config) -> YoutubeDL:
    """Set up downloader."""
    download_options = YDL_DL_OPTS
    download_options["outtmpl"] = f"{config.publish_dir}/{config.media_dir}/%(id)s.%(ext)s"
    download_options["playlistend"] = config.number_of_episodes * 3
    if config.youtube_cookie_file:
        download_options["cookiefile"] = config.youtube_cookie_file
    downloader = YoutubeDL(download_options)
    return downloader


def create_feed(config) -> FeedGenerator:
    """Create feed."""
    feed = FeedGenerator()
    feed.load_extension("podcast")
    feed.author(name="Marvin", email="marvin@example.com")
    feed.link(href=f"{config.podcast_host}/feed.rss", rel="alternate")
    feed.title("Marvin's Youtube Playlist Podcast")
    feed.description("Marvin's Youtube Playlist Podcast")
    return feed


def setup_logging(logging_config_file: Optional[Path]) -> None:
    """Set up logging."""
    if logging_config_file and logging_config_file.is_file():
        with logging_config_file.open(mode="rb") as log_config_file:
            logging_config = msgspec.toml.decode(log_config_file.read())

        for handler in logging_config.get("handlers"):
            if handler.get("sink") == "sys.stdout":
                handler["sink"] = sys.stdout

        log.configure(**logging_config)


def is_video_included(
    video_title: str,
    video_original_url: str,
    include_filters: List[str],
    exclude_filters: List[str],
) -> bool:
    """Check video title against include and exclude filters to determine if
    video should be considered for adding to podcast or not.

    :param video_title: Title of video to check filters against.
    :param video_original_url: Original URL of video to check filters against.
    :param include_filters: List of regex patterns acting as include filters.
        If one include filter matches, video will be considered for adding.
    :param exclude_filters: List of regex patterns acting as exclude filters.
        If one exclude filter matches, video will be skipped, even if there is a
        matching include filter. I.e. exclude > include
    :return: True if video should be considered for adding and False if video should
        be skipped based on filters.
    """
    log.debug(f"Filtering: Checking video: {video_title} at {video_original_url}")

    should_include_video = False

    title_len = len(video_title)
    url_len = len(video_original_url)

    if title_len == 0 and url_len == 0:
        return should_include_video

    if len(include_filters) == 0:
        should_include_video = True

    else:
        for include_filter in include_filters:
            regex = re.compile(include_filter)
            if title_len and regex.match(video_title):
                log.debug(f"Filtering: Include filter '{include_filter}' matches")
                should_include_video = True
                break
            if url_len and regex.match(video_original_url):
                log.debug(f"Filtering: Include filter '{include_filter}' matches")
                should_include_video = True
                break

    if len(exclude_filters) > 0:
        for exclude_filter in exclude_filters:
            regex = re.compile(exclude_filter)
            if title_len and regex.match(video_title):
                log.debug(f"Filtering: Exclude filter '{exclude_filter}' matches", exclude_filter)
                should_include_video = False
                break
            if url_len and regex.match(video_original_url):
                log.debug(f"Filtering: Exclude filter '{exclude_filter}' matches", exclude_filter)
                should_include_video = False
                break

    log.debug(f"Filtering: Video '{video_title}' included? {should_include_video}")

    return should_include_video


def add_episodes(
    config: Config,
    downloader: YoutubeDL,
    feed: FeedGenerator,
    play_list_info: List[Dict[str, str]],
) -> None:
    """Iterate through play list info and decides which videos to process and
    add to feed and then does so.

    :param config: Contains program configuration
    :param downloader: Youtube-dl object to download and process videos
    :param feed: RSS feed to add episodes to
    :param play_list_info: List of info dicts for each video in the playlist
    :return: None
    """
    ids_in_feed = {entry.id() for entry in feed.entry()}
    number_episodes_added = 0
    for video in play_list_info:
        video_id = video["id"]
        if number_episodes_added < config.number_of_episodes:
            local_audio_file = Path(config.publish_dir) / Path(config.media_dir) / Path(f"{video_id}.opus")
            host_audio_file = f"{config.podcast_host}/{config.media_dir}/{video_id}.opus"
            thumbnail = get_thumbnail(config=config, video_id=video_id, video=video)

            feed_entry = create_feed_entry(
                video=video,
                thumbnail=thumbnail,
                host_audio_file=host_audio_file,
                config=config,
            )
            feed.add_entry(feedEntry=feed_entry)

            # Download video if needed
            if not local_audio_file.is_file():
                log.opt(colors=True).info(
                    f"Downloading episode with id <green>{feed_entry.id()}</green> "
                    f"and length <yellow>{timedelta(seconds=int(video['duration']))}</yellow> "
                    f"uploaded on <yellow>{feed_entry.published():%Y-%m-%d}</yellow> with "
                    f"title <green>{feed_entry.title()}</green>"
                )
                downloader.download(url_list=[video["webpage_url"]])

            number_episodes_added += 1
            ids_in_feed.add(feed_entry.id())

            log.debug(
                f"Added episode with id {feed_entry.id()} "
                f"from {feed_entry.published():%Y-%m-%d} "
                f"with title {feed_entry.title()}"
            )

        else:
            # Nothing to be done if episode / video has already been added to the feed
            if video_id in ids_in_feed:
                continue

            remove_unneeded_files(config, video)


def create_feed_entry(
    video: Dict[str, str],
    thumbnail: Path,
    host_audio_file: str,
    config: Config,
) -> FeedEntry:
    """Create feed entry to add to rss feed."""
    published_on = datetime.strptime(video.get("upload_date", "19700101"), "%Y%m%d").replace(tzinfo=timezone.utc)
    feed_entry = FeedEntry()
    feed_entry.load_extension("podcast")
    feed_entry.author(name=video["uploader"])
    feed_entry.id(id=video["id"])
    feed_entry.link(href=video["webpage_url"])
    feed_entry.title(title=video["title"])
    feed_entry.description(description=video["description"])
    feed_entry.published(published=published_on)
    feed_entry.podcast.itunes_image(f"{config.podcast_host}/{config.media_dir}/{thumbnail}")
    feed_entry.podcast.itunes_duration(int(video["duration"]))
    feed_entry.enclosure(url=host_audio_file, type="audio/ogg")

    return feed_entry


def remove_unneeded_files(config: Config, video) -> None:
    """Remove files not needed for published feed."""
    try:
        (Path(config.publish_dir) / Path(config.media_dir) / Path(f"{video['id']}.*")).unlink()
        log.debug(
            f"Removed old files for episode with id {video['id']} "
            f"from {video['upload_date']} with title {video['title']}"
        )
    except FileNotFoundError:
        log.debug(f"Skipping episode with id {video['id']} from {video['upload_date']} with title {video['title']}")


def get_thumbnail(config: Config, video_id: str, video: Dict[str, Any]) -> Path:
    """Get the highest quality thumbnail out of the video dict, converts it to
    JPG and returns the filename of the converted file.

    :param config: Configuration class instance
    :param video_id: YouTube video id
    :param video: youtube-dl information dict about one particular video

    :return:  Filename of the converted Thumbnail
    """
    image_url = video["thumbnails"][-1]["url"]
    image_type = image_url.split(".")[-1]
    local_image = Path(config.publish_dir) / Path(f"{video_id}.{image_type}")
    publish_image = Path(f"{video_id}.jpg")
    publish_image_path = Path(config.publish_dir) / config.media_dir / publish_image
    if not publish_image_path.is_file():
        remote_image = requests.get(url=image_url, timeout=5)
        with local_image.open("wb") as file:
            file.write(remote_image.content)
        thumbnail_wip = Image.open(local_image)
        thumbnail_wip.save(publish_image_path)
        local_image.unlink()
    return publish_image


if __name__ == "__main__":
    typer.run(main)
