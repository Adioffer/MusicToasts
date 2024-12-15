import asyncio

from consts import (APP_NAME, AI_ENDPOINT_URL, AI_API_KEY, AI_MODEL, COVER_ART_TIMEOUT, LYRICS_TIMEOUT)
from utils.ai_assistant import AiAssistant
from utils.cover_art_manager import CoverArtManager, get_cover_art_manager
from utils.logger import logger
from utils.lyrics_finder import LyricsFinder, get_lyrics_finder
from utils.media_listener import MediaListener
from utils.toast_manager import ToastManager

ai_features_enabled = AI_ENDPOINT_URL and AI_API_KEY and AI_MODEL

if not ai_features_enabled:
    logger.warning("Running without AI features.")


class MainApp:
    def __init__(self):
        self.toast_manager = ToastManager(APP_NAME)
        self.ai_assistant = AiAssistant(AI_ENDPOINT_URL, AI_API_KEY, AI_MODEL)
        self.cover_art_manager: CoverArtManager = get_cover_art_manager()
        self.lyrics_finder: LyricsFinder = get_lyrics_finder()
        self.media_listener = MediaListener()
        self.media_listener.set_on_new_track_callback(self.on_new_track)

    def make_initial_toast(self, artist, track_name):
        toast_id = self.toast_manager.create_new_toast()

        # Add text and buttons
        self.toast_manager.add_text_to_toast(toast_id, [f"Now Playing:", f"{track_name}", f"by {artist}"])

        # Add AI features if available
        self.toast_manager.add_button_to_toast(toast_id, "Fun Fact", "button_FunFact")
        self.toast_manager.add_button_to_toast(toast_id, "Ask a Question", "button_AskQuestion")
        self.toast_manager.add_button_to_toast(toast_id, "Show Lyrics", "button_Lyrics")

        # Add cover art thumbnail
        cover_art_path = self.cover_art_manager.get_song_cover_art(artist, track_name, COVER_ART_TIMEOUT)

        if not cover_art_path:
            # Already logged inside
            pass
        else:
            self.toast_manager.add_image_to_toast(toast_id, cover_art_path)

        # Configure button callbacks
        def on_initial_toast_click(args):
            if args.arguments == "button_Lyrics":
                self.make_lyrics_toast(artist, track_name)
            elif args.arguments == "button_FunFact":
                self.make_ai_fun_fact_toast(artist, track_name)
            elif args.arguments == "button_AskQuestion":
                self.make_ask_ai_toast(artist, track_name)

        self.toast_manager.set_toast_activated_callback(toast_id, on_initial_toast_click)

        self.toast_manager.display_toast(toast_id)
        return toast_id

    def make_error_toast(self, error_message):
        toast_id = self.toast_manager.create_new_toast()

        self.toast_manager.add_text_to_toast(toast_id, ["Error! :( ", error_message])

        self.toast_manager.display_toast(toast_id)
        return toast_id

    def make_lyrics_toast(self, artist, track_name):
        status_code, response = self.lyrics_finder.get_lyrics(artist, track_name, LYRICS_TIMEOUT)

        if status_code != 200 or not response:
            return self.make_error_toast(" ".join(
                ["Could not fetch lyrics.", str(status_code) if status_code else "", response if response else ""]))

        toast_id = self.toast_manager.create_new_toast()

        self.toast_manager.add_text_to_toast(toast_id, [f"Here are the lyrics for {track_name} by {artist}:", response])

        self.toast_manager.display_toast(toast_id)
        return toast_id

    def make_ai_fun_fact_toast(self, artist, track_name):
        if not ai_features_enabled:
            return self.make_error_toast("AI features are not enabled. Please configure the environment variables "
                                         "(MT_AI_ENDPOINT_URL, MT_AI_API_KEY, MT_AI_MODEL) to use AI features.")

        status_code, response = self.ai_assistant.send_prompt(f"Tell me a fun fact about this song - "
                                                              f"'{track_name[:100]}' by '{artist[:100]}'. "  # Avoid long prompts
                                                              f"Make it interesting and surprising!")

        if status_code != 200 or not response:
            return self.make_error_toast(" ".join(
                ["Could not get fun fact from AI assistant.", str(status_code) if status_code else "",
                 response if response else ""]))

        toast_id = self.toast_manager.create_new_toast()

        self.toast_manager.add_text_to_toast(toast_id, ["Fun fact!", response])

        self.toast_manager.display_toast(toast_id)
        return toast_id

    def make_ask_ai_toast(self, artist, track_name):
        if not ai_features_enabled:
            return self.make_error_toast("AI features are not enabled. Please configure the environment variables "
                                         "(MT_AI_ENDPOINT_URL, MT_AI_API_KEY, MT_AI_MODEL) to use AI features.")

        toast_id = self.toast_manager.create_new_toast()

        self.toast_manager.add_text_to_toast(toast_id,
                                             ["Ask a question:", "Type your question below and click 'Send'."])

        self.toast_manager.add_input_to_toast(toast_id, 'question', 'Your question:', '')
        self.toast_manager.add_button_to_toast(toast_id, "Send", "button_Send")

        def on_ask_button_click(args):
            if args.arguments == "button_Send":
                user_question = args.inputs.get('question', '')

                if user_question:
                    status_code, response = self.ai_assistant.send_prompt(
                        f"Regarding the song {track_name} by {artist}. " + user_question)  # Avoid long prompts

                    if status_code != 200 or not response:
                        return self.make_error_toast(" ".join(
                            ["Could not get response from AI assistant.", str(status_code) if status_code else "",
                             response if response else ""]))

                    return self.make_ai_response_toast(response)

        self.toast_manager.set_toast_activated_callback(toast_id, on_ask_button_click)

        self.toast_manager.display_toast(toast_id)
        return toast_id

    def make_ai_response_toast(self, response):
        toast_id = self.toast_manager.create_new_toast()

        self.toast_manager.add_text_to_toast(toast_id, [response])

        self.toast_manager.display_toast(toast_id)
        return toast_id

    def on_new_track(self, artist, track_name):
        self.make_initial_toast(artist, track_name)

    async def run(self):
        while True:
            await self.media_listener.check_new_track()
            await asyncio.sleep(3)


if __name__ == "__main__":
    app = MainApp()
    asyncio.run(app.run())
