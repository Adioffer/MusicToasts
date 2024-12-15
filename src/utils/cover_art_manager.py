import tempfile
from abc import ABC, abstractmethod

import requests

from .logger import logger

__all__ = ['CoverArtManager', 'get_cover_art_manager']


class CoverArtManager(ABC):
    """Abstract class for fetching cover art for songs and albums."""

    @abstractmethod
    def get_song_cover_art(self, artist: str, track_name: str, timeout=None):
        """
        Fetch cover art for a song.

        :param artist: str
        :param track_name: str
        :param timeout: optional[int]
        :return: path to local file with cover art
        """
        pass

    @abstractmethod
    def get_album_cover_art(self, artist: str, album_name: str, timeout=None):
        """
        Fetch cover art for an album.

        :param artist: str
        :param album_name: str
        :param timeout: optional[int]
        :return: path to local file with cover art
        """
        pass


class MusicBrainzManager(CoverArtManager):
    user_agent = "MusicToasts/0.1 ( https://github.com/todo/todo/issues )"
    headers = {"User-Agent": user_agent}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.info("CoverArtManager: Using MusicBrainz API.")

    def get_song_cover_art_url(self, artist: str, track_name: str, timeout=None):
        """
        Fetch the *remote* URL of the cover art for a song.
        """
        try:
            search_url = "https://musicbrainz.org/ws/2/recording/"
            params = {"query": f"artist:{artist} recording:{track_name}", "fmt": "json", "limit": 1}
            response = requests.get(search_url, headers=self.headers, params=params, timeout=timeout)
            response.raise_for_status()
            data = response.json()
            if data['recordings']:
                recording = data['recordings'][0]
                release_id = recording['releases'][0]['id']
                cover_art_url = f"https://coverartarchive.org/release/{release_id}/front-small"
                return cover_art_url
            else:
                logger.info(f"Could not find data for {artist}, {track_name}.")
                return None
        except Exception as e:
            logger.info(f"Error fetching cover art: {e}")

    def get_song_cover_art(self, artist: str, track_name: str, timeout=None):
        cover_art_url = self.get_song_cover_art_url(artist, track_name, timeout)

        if not cover_art_url:
            # Already logged inside
            return None

        try:
            response = requests.get(cover_art_url, timeout=timeout)
            response.raise_for_status()

            # Save the cover art to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                temp_file.write(response.content)
                temp_file_path = temp_file.name

            return temp_file_path
        except Exception as e:
            logger.info(f"Error downloading cover art: {e}.")
            return None

    def get_album_cover_art(self, artist: str, album_name: str, timeout=None):
        raise NotImplementedError("This method is not implemented yet.")


def get_cover_art_manager():
    """ Polymorphism for CoverArtManager. """
    return MusicBrainzManager()
