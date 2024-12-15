from abc import ABC, abstractmethod
from urllib.parse import quote

import requests

from .logger import logger

__all__ = ['LyricsFinder', 'get_lyrics_finder']


class LyricsFinder(ABC):
    """Abstract class for fetching lyrics for songs."""

    @abstractmethod
    def get_lyrics(self, artist: str, track_name: str, timeout=None):
        """
        Fetch lyrics for a song.

        :param artist: str
        :param track_name: str
        :param timeout: optional[int]
        :return: str with lyrics
        """
        pass


class LyricsOvh(LyricsFinder):
    """
    Fetch lyrics using the Lyrics.ovh API.
    """

    api_base_url = "https://api.lyrics.ovh/v1/"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.info("LyricsFinder: Using Lyrics.ovh API.")

    def get_lyrics(self, artist: str, track_name: str, timeout=None):
        try:
            # Decode the artist and track name to be URL-safe

            params = f"{quote(artist)}/{quote(track_name)}"
            response = requests.get(self.api_base_url + params, timeout=timeout)

            if response.status_code == 404:
                logger.info(f"Could not find the lyrics for: {track_name} by {artist}.")
                return None, f"Could not find the lyrics for: {track_name} by {artist}."

            response.raise_for_status()

            data = response.json()
            lyrics = data['lyrics']
            return response.status_code, lyrics
        except KeyError:
            logger.info(f"Could not find the lyrics for: {track_name} by {artist}.")
            return None, f"Could not find the lyrics for: {track_name} by {artist}."
        except Exception as e:
            logger.info(f"Error fetching lyrics: {e}")
            return None, str(e)


def get_lyrics_finder():
    """ Polymorphism for LyricsFinder. """
    return LyricsOvh()
