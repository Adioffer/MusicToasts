import winsdk.windows.media.control as control


class MediaListener:
    """
    Listens for changes in the currently playing media and calls a callback when a new track is detected.
    """

    def __init__(self):
        self.current_track = None
        self.on_new_track_callback = None

    def set_on_new_track_callback(self, callback):
        self.on_new_track_callback = callback

    async def get_current_media_info(self):
        sessions = await control.GlobalSystemMediaTransportControlsSessionManager.request_async()
        current_session = sessions.get_current_session()
        if current_session:
            media_properties = await current_session.try_get_media_properties_async()
            artist = media_properties.artist
            track_name = media_properties.title
            return artist, track_name
        return None

    async def check_new_track(self):
        new_track = await self.get_current_media_info()
        if new_track and new_track[0] and new_track[1] and new_track != self.current_track:
            self.current_track = new_track
            if self.on_new_track_callback:
                self.on_new_track_callback(*self.current_track)
